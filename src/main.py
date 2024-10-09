import paho.mqtt.client as mqtt
from loguru import logger
from managers import HassMqttLighstManager
from config import load_lights


def on_connect(client, userdata, flags, rc):
    logger.info('Connected to mqtt')


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning('Disconnected from Broker. Reconnecting...')


client = mqtt.Client()
client.username_pw_set('test', 'password')
client.connect('localhost', 1883, 60)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.loop_start()

lights = load_lights()
manager = HassMqttLighstManager(lights, client)
manager.observe_forever()
