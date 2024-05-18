#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import paho.mqtt.client as mqtt
import logging
import sys

# Configure log file
logging.basicConfig(filename='/edge_server/logs/subscribers.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Print logs 
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

class MQTTSubscriber():
    
    def __init__(self, brokerAddress, brokerPort, user, password, clientID):
        # Paralelization of tasks (2 workers per subscriber)
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.client = mqtt.Client()
        self.client.username_pw_set(user, password)
        self.brokerAddress = brokerAddress
        self.brokerPort = brokerPort
        self.clientID = clientID
        # Callbacks
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage

    # Connect to broker
    def connect(self):
        try:
            self.client.connect(self.brokerAddress, self.brokerPort)
            self.client.loop_start()
        except Exception as e:
            logging.error("Error connecting to broker: " + str(e))

    # Subscribe to topic (QoS 0 by default)
    def subscribe(self, topic, qos=0):
        try:
            logging.info("Subscriber " + str(self.clientID) + " subscribed to " + topic)
            self.client.subscribe(topic, qos=qos)
        except Exception as e:
            logging.error("Error subscribing to topic " + topic + ": " + str(e))

    # Connect callback
    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(str(self.clientID) + " connected to broker successfully")
        else:
            logging.error(str(self.clientID) + " failed to connect to broker with result code " + str(rc))

    # Message callback
    def onMessage(self, client, userdata, msg):
        try:
            logging.debug(str(self.clientID) + " received a message " + str(msg.payload))
            self.processMessage(msg.payload)
        except Exception as e:
            logging.error("Error processing message: " + str(e))

    def processMessage(self, payload):
        # Store message
        print("Process message: " + str(payload))



