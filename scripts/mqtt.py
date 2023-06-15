import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe('#')

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)

client = mqtt.Client()
client.username_pw_set('test', 'password')
client.on_connect = on_connect
client.on_message = on_message

client.connect('localhost', 1883, 60)
client.loop_start()
