import os

import paho.mqtt.client as mqtt
from loguru import logger
from managers import HassMqttLighstManager
from config import load_lights
from in_out.i2c import configure
from in_out.core import install_safeguard_for_relays


USERNAME = os.environ["MQTT_USERNAME"]
PASSWORD = os.environ["MQTT_PASSWORD"]
HOSTNAME = os.environ["MQTT_HOSTNAME"]

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(HOSTNAME, 1883, 60)

configure(1)
lights = load_lights()
manager = HassMqttLighstManager(lights, client)
install_safeguard_for_relays(list(range(0, 32)))
manager.observe_forever()
