import json
import time
from threading import Lock

from loguru import logger
from lights import (
    Light,
    get_light_state,
    toggle_light,
    turn_on,
    turn_off,
    get_many_lights_state,
)
import paho.mqtt.client as mqtt


class LightsManager:

    class _ActionableLight:

        def __init__(self, light: Light):
            self.light = light

        @property
        def state(self):
            return get_light_state(self.light)

        def toggle(self):
            return toggle_light(self.light)

        def turn_on(self):
            return turn_on(self.light)

        def turn_off(self):
            return turn_off(self.light)

    def __init__(self, lights: list[Light]):
        self.lights: list[Light] = lights
        self._lights_mapping = {light.id: light for light in self.lights}

    def __getitem__(self, name):
        if name not in self._lights_mapping:
            raise KeyError(f"No light called {name}")

        return self._ActionableLight(self._lights_mapping[name])

    def list(self):
        return list(self._lights_mapping.keys())


class HassMqttLighstManager(LightsManager):

    LIGHT_OFF = "off"
    LIGHT_ON = "on"
    MQTT_PREFIX = "panel"
    LIGHTS_AVAILABLE = "true"
    LIGHTS_UNAVAILABLE = "false"
    # Use the same topic as availability for all lights. This makes us able
    # to use last will as offline
    AVAILABILITY_TOPIC = f"{MQTT_PREFIX}/_all/avail"

    def __init__(self, lights, mqtt_client: mqtt.Client):
        """
        The mqtt client is a configured but not started client, i.e. loop_start
        was not called; .connect was called.
        """
        super().__init__(lights)
        self.mqtt_client = mqtt_client
        self.input_states: dict[int, bool] = {}
        self._relay_states_lock = Lock()
        self._initialized = False
        self.setup_mqtt_client()

    def setup_mqtt_client(self):
        self.mqtt_client.on_message = self.handle_mqtt_msg
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.loop_start()
        logger.debug("Setup mqtt client complete")

    def handle_mqtt_msg(self, client, userdata, msg):
        logger.debug(f"Got message: {msg}")
        light_id = msg.topic.split("/")[1]
        light = self[light_id]

        payload = msg.payload.decode()
        state = None
        if payload == self.LIGHT_ON:
            logger.debug(f"Turn on light {light_id}")
            if light.light.input_no is None:
                light.toggle()
            else:
                state = light.turn_on()
        elif payload == self.LIGHT_OFF:
            logger.debug(f"Turn off {light_id}")
            if light.light.input_no is None:
                light.toggle()
            else:
                state = light.turn_off()
        else:
            logger.error(f"Invalid payload from mqtt: {payload}")

        # if not input number
        if state is not None:
            self.mqtt_client.publish(
                self.make_state_topic(light_id),
                self.LIGHT_ON if state else self.LIGHT_OFF,
                retain=True,
            )

    def _make_device_description(self):
        return {
            "device": {
                "name": "Electrical Panel Controls",
                "identifiers": 20223235422,
                "model": "Raspberry Pi Electrical Panel",
                "manufacturer": "The Candale",
                "sw_version": "0.5",
                "hw_version": "1.0",
            }
        }

    def make_state_topic(self, light_id):
        return f"{self.MQTT_PREFIX}/{light_id}/state"

    def make_cmd_topic(self, light_id):
        return f"{self.MQTT_PREFIX}/{light_id}/cmd"

    def make_availability_topic(self, light_id):
        return f"{self.MQTT_PREFIX}/{light_id}/avail"

    def set_last_will(self, mqtt_client):
        mqtt_client.will_set(
            self.AVAILABILITY_TOPIC, payload=self.LIGHTS_UNAVAILABLE, retain=True
        )

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to mqtt")
        logger.debug("Publishing availability")
        self.advertise_to_hass()
        self._initialized = True

        self.mqtt_client.publish(
            self.AVAILABILITY_TOPIC, payload=self.LIGHTS_AVAILABLE, retain=True
        )

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning("Disconnected from Broker. Reconnecting...")

    def advertise_to_hass(self):
        for light in self.lights:
            payload = self._make_device_description()
            cmd_topic = self.make_cmd_topic(light.id)

            payload.update(
                {
                    "name": light.verbose_name,
                    "object_id": f"{light.id}_light",
                    "unique_id": f"{light.id}_light",
                    "command_topic": cmd_topic,
                    "payload_on": self.LIGHT_ON,
                    "payload_off": self.LIGHT_OFF,
                    "optimistic": light.input_no is None,
                    "device_class": "light",
                    "availability_topic": self.AVAILABILITY_TOPIC,
                    "payload_available": self.LIGHTS_AVAILABLE,
                    "payload_not_available": self.LIGHTS_UNAVAILABLE,
                }
            )

            if light.input_no is not None:
                payload["state_topic"] = self.make_state_topic(light.id)

            self.mqtt_client.publish(
                f"homeassistant/light/panel/{light.id}/config",
                payload=json.dumps(payload),
                retain=True,
            )
            if light.input_no is not None:
                state = get_light_state(light)
                self.input_states[light.id] = state
                self.mqtt_client.publish(
                    self.make_state_topic(light.id),
                    self.LIGHT_ON if state else self.LIGHT_OFF,
                    retain=True,
                )
                logger.debug(f"Published light's {light.id} state as {state}")

            self.mqtt_client.subscribe(cmd_topic)

            logger.debug(f"Published light {light.id}_light. Subscribed to {cmd_topic}")
        self.mqtt_client.publish(
            self.AVAILABILITY_TOPIC, payload=self.LIGHTS_AVAILABLE, retain=True
        )

    def run_forever():
        pass

    def observe_forever(self):
        while self._initialized is False:
            logger.debug("Waiting for completed initialization")
            time.sleep(1)

        logger.info("Observing lights forever")
        # TODO: make sure you report the state of the direct lights as well
        indirect_lights = [
            light
            for light in self.lights
            if light.indirect and light.input_no is not None
        ]
        while True:
            lights_states = get_many_lights_state(indirect_lights)
            for light in indirect_lights:
                state = lights_states[light.input_no]
                if state != self.input_states[light.id]:
                    logger.debug(
                        f"Light {light.id} changed from {self.input_states[light.id]} to {state}"
                    )
                    self.mqtt_client.publish(
                        self.make_state_topic(light.id),
                        self.LIGHT_ON if state else self.LIGHT_OFF,
                        retain=True,
                    )
                    self.input_states[light.id] = state

            time.sleep(0.1)
