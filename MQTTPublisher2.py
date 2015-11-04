import paho.mqtt.client as mqtt
import json
import datetime
import logging
import traceback
import sys
from random import randint
from time import sleep 

USERID="TESTNODE"
CLIENTID="1234567899"
BROKERIP="CONCEPTIOTTESTHUB.azure-devices.net"
#BROKERIP="localhost"
BROKERPORT=1883
KEEPALIVE=15
QOS=0
LOGFILE  = 'MQTTPublisher2.log'
LOGLEVEL = 'DEBUG'
 
class PayLoad(object):
	def __init__(self):
		self.TimeStamp__c=''
		self.Measurement__c=''
	def setTimeStamp(self):
		self.TimeStamp__c=str(datetime.datetime.now())
	def setMeasurement(self, data):
		self.Measurement__c=data
	def tojson(self):
		return json.dumps(self.__dict__)
 
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code "+str(rc))

def on_publish(client, userdata, flags, rc):
	logging.debug("Published message to topic" +topic)
	print("Published message to topic" +topic)


# set up logging
loglevel=LOGLEVEL
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(filename=LOGFILE, filemode='w', level=numeric_level,format='%(asctime)s : %(filename)s - %(message)s')
	
	
mqttc = mqtt.Client()
#mqttc.connect(BROKERIP, port=BROKERPORT, keepalive=KEEPALIVE, bind_address="")
try:
	mqttc.connect(BROKERIP, port=BROKERPORT)
	mqttc.loop_start()
	topic = USERID + "/" + CLIENTID + "/act"
	payload = PayLoad()

	while True:
		payload.setTimeStamp()
		payload.setMeasurement(randint(0,100))
		data=str(payload.tojson())
		logging.debug("payload: %s", data)
		mqttc.publish(topic, data)
		logging.debug("published on topic: %s", topic)
		sleep(3)
except:
	logging.debug("Unexpected error:  %s", traceback.format_exc())


