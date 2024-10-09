import os

import paho.mqtt.client as mqtt
from loguru import logger
from managers import HassMqttLighstManager
from config import load_lights


USERNAME = os.environ['MQTT_USERNAME']
PASSWORD = os.environ['MQTT_PASSWORD']
HOSTNAME = os.environ['MQTT_HOSTNAME']

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(HOSTNAME, 1883, 60)

lights = load_lights()
manager = HassMqttLighstManager(lights, client)
manager.observe_forever()
