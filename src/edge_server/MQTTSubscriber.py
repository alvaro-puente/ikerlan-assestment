#!/usr/bin/env python3

from ProcessedDataDatabase import ProcessedDataDatabase
from SensorsDataDatabase import SensorsDataDatabase
from concurrent.futures import ThreadPoolExecutor
from CustomLogger import CustomLogger
import paho.mqtt.client as mqtt
from Processor import Processor
import json
import uuid

subscribersLogger = CustomLogger('/edge_server/logs/subscribers.log', "subscribers")

class MQTTSubscriber():
    
    def __init__(self, brokerAddress, brokerPort, user, password, clientID):
        # MQTT Broker information
        self.client = mqtt.Client()
        self.client.username_pw_set(user, password)
        self.brokerAddress = brokerAddress
        self.brokerPort = brokerPort
        self.clientID = clientID
        # Connect to databases
        self.sensorsDataDatabase = SensorsDataDatabase()
        self.sensorsDataDatabase.connect()
        self.processedDataDatabase = ProcessedDataDatabase()
        self.processedDataDatabase.connect()
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
            self.processMessage(message)
        except Exception as e:
            subscribersLogger.logger.error(self.clientID + ": Error processing message: " + str(e))

    # Store message in database
    def processMessage(self, message):
        # Store message
        self.storeMessage(message)
        # Check if database reaches more than numberOfEntries
        numberOfEntries = 50
        hasNumberEntries = self.sensorsDataDatabase.hasNumberOfEntries(numberOfEntries)
        # If reaches...
        if hasNumberEntries:
            # Process data entries
            self.applyProcessing(numberOfEntries)

    # Store message in database
    def storeMessage(self, message):
        id = str(uuid.uuid4())
        name = message["sensor_id"]
        type = message["sensor_type"]
        value = message["value"]
        timestamp = message["timestamp"]
        self.sensorsDataDatabase.addEntry(id, name, type, value, timestamp)
        
    # Process the message
    def applyProcessing(self, numberOfEntries):
        # Get numberOfentries number of values to be processed
        idValuePairs = self.sensorsDataDatabase.obtainNumberOfEntriesValues(numberOfEntries)
        ids = [row[0] for row in idValuePairs]
        values = [row[1] for row in idValuePairs]
        # Process values and store them in a new database
        processedValues = self.processor.applyOutliersFilter(values)
        for value in processedValues:
            id = str(uuid.uuid4())
            self.processedDataDatabase.addEntry(id, value)
        # Delete processed values from database
        self.sensorsDataDatabase.deleteEntriesById(ids)



