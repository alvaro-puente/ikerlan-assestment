#!/usr/bin/env python3

from CustomLogger import CustomLogger
import paho.mqtt.client as mqtt
from Processor import Processor
import json

subscribersLogger = CustomLogger('/edge_server/logs/subscribers.log', "subscribers")

"""
This class provides all the methods to generate a MQTT subscriber that listens to a certain topic
and process it in the way is defined in the processMessage() method from Processor class. 
"""
class MQTTSubscriber():
    
    def __init__(self, brokerAddress, brokerPort, user, password, clientID):
        # MQTT Broker information
        self.client = mqtt.Client()
        self.client.username_pw_set(user, password)
        self.brokerAddress = brokerAddress
        self.brokerPort = brokerPort
        self.clientID = clientID
        # Processing functions
        self.processor = Processor()
        # Callbacks
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage

    # Connect to broker
    def connect(self):
        try:
            self.client.connect(self.brokerAddress, self.brokerPort)
            self.client.loop_start()
        except Exception as e:
            subscribersLogger.logger.error(self.clientID + ": Error connecting to broker: " + str(e))

    # Subscribe to topic (QoS 0 by default)
    def subscribe(self, topic, qos=0):
        try:
            subscribersLogger.logger.info("Subscriber " + self.clientID + " subscribed to " + topic)
            self.client.subscribe(topic, qos=qos)
        except Exception as e:
            subscribersLogger.logger.error(self.clientID + ": Error subscribing to topic " + topic + ": " + str(e))

    # Connect callback
    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            subscribersLogger.logger.info(self.clientID + " connected to broker successfully")
        else:
            subscribersLogger.logger.error(self.clientID + " failed to connect to broker with result code " + str(rc))

    # Message callback
    def onMessage(self, client, userdata, msg):
        try:
            subscribersLogger.logger.debug(self.clientID + " received a message " + str(msg.payload))
            message = json.loads(msg.payload)
            self.processor.processMessage(message)
        except Exception as e:
            subscribersLogger.logger.error(self.clientID + ": Error processing message: " + str(e))