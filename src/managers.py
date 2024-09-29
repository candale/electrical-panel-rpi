import json
from loguru import logger
from lights import Light, get_light_state, toggle_light, turn_on, turn_off


class LightsManager:

    class _ActionableLight:

        def __init__(self, light):
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
        self.lights = lights
        self._lights_mapping = {
            light.id: light for light in self.lights
        }

    def __getitem__(self, name):
        if name not in self._lights_mapping:
            raise KeyError(f'No light called {name}')

        return self._ActionableLight(self._lights_mapping[name])

    def list(self):
        return list(self._lights_mapping.keys())


class HassMqttLighstManager(LightsManager):

    LIGHT_OFF = 'off'
    LIGHT_ON = 'on'
    MQTT_PREFIX = 'panel'

    def __init__(self, lights, mqtt_client):
        super().__init__(lights)
        self.mqtt_client = mqtt_client
        self.setup_mqtt_client()
        self.advertise_to_hass()

    def setup_mqtt_client(self):
        self.mqtt_client.on_message = self.handle_mqtt_msg
        logger.debug('Setup mqtt client')

    def handle_mqtt_msg(self, client, userdata, msg):
        light_id = msg.topic.split('/')[1]
        light = self[light_id]

        payload = msg.payload.decode()
        state = None
        if payload == self.LIGHT_ON:
            logger.debug(f'Turn on light {light_id}')
            if light.light.input_no is None:
                light.toggle()
            else:
                state = light.turn_on()
        elif payload == self.LIGHT_OFF:
            logger.debug(f'Turn off {light_id}')
            if light.light.input_no is None:
                light.toggle()
            else:
                state = light.turn_off()
        else:
            logger.error(f'Invalid payload from mqtt: {payload}')

        # if not input number
        if state is not None:
            self.mqtt_client.publish(
                self.make_state_topic(light_id),
                self.LIGHT_ON if state else self.LIGHT_OFF
            )

    def _make_device_description(self):
        return {
            "device": {
                "name": "Electrical Panel Controls",
                "identifiers": 2022323542,
                "model": "Raspberry Pi Electrical Panel",
                "manufacturer": "The Candale",
                'sw_version': '0.4',
                'hw_version': '1.0'
            }
        }

    def make_state_topic(self, light_id):
        return f'{self.MQTT_PREFIX}/{light_id}/state'

    def advertise_to_hass(self):
        for light in self.lights:
            payload = self._make_device_description()
            cmd_topic = f'{self.MQTT_PREFIX}/{light.id}/cmd'

            payload.update(
                {
                    'name': light.verbose_name,
                    'object_id': f'{light.id}_light',
                    'unique_id': f'{light.id}_light',
                    'command_topic': cmd_topic,
                    'payload_on': self.LIGHT_ON,
                    'payload_off': self.LIGHT_OFF,
                    'optimistic': light.input_no is None,
                    'device_class': 'light',
                }
            )

            if light.input_no is not None:
                payload['state_topic'] = self.make_state_topic(light.id)

            self.mqtt_client.publish(
                f'homeassistant/light/panel/{light.id}/config',
                payload=json.dumps(payload)
            )
            self.mqtt_client.subscribe(cmd_topic)
            logger.debug(f'Published light {light.id}. Subscribed to {cmd_topic}')
