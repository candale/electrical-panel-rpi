import paho.mqtt.client as mqtt
from managers import HassMqttLighstManager
from config import load_lights



client = mqtt.Client()
client.username_pw_set('test', 'password')
client.connect('localhost', 1883, 60)
client.loop_start()

lights = load_lights()
manager = HassMqttLighstManager(lights, client)
manager.observe_forever()
