import paho.mqtt.client as mqtt
import json
import datetime
from time import sleep 

USERID="TESTNODE"
CLIENTID="1234567890"
BROKER="CONCEPTIOTTESTHUB.azure-devices.net"
#BROKER="localhost"
BROKERPORT=1883
KEEPALIVE=15
QOS=0

#topic = "a/b/c"
topic = USERID + "/#" 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, BROKERPORT, 60)

client.loop_start()

while True:
		sleep(1)