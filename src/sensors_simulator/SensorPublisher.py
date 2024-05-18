#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import threading
import logging
import random
import json
import time
import sys

# Configure log file
logging.basicConfig(filename='/sensors_simulator/logs/sensor_publishers.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Print logs 
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

class SensorPublisher():

    def __init__(self, clientID, brokerAddress, brokerPort, user, password, topic):
        self.client = mqtt.Client()
        self.clientID = clientID
        self.client.username_pw_set(user, password)
        self.brokerAddress = brokerAddress
        self.brokerPort = brokerPort
        self.topic = topic
        # Callbacks
        self.client.on_connect = self.onConnect
        self.client.on_disconnect = self.onDisconnect
        self.client.on_publish = self.onPublish

    # Generate message to send
    def generateData(self):
        sensor_id = "sensor_" + str(random.randint(1, 10))
        sensor_type = "type_" + str(random.randint(1, 3))
        value = random.uniform(0, 100)
        data = {
            "sensor_id": sensor_id, 
            "sensor_type": sensor_type, 
            "value": value
        }
        return json.dumps(data)

    # Function that sends data to topic
    def publishData(self):
        try:
            while True:
                data = self.generateData()
                logging.info(self.clientID + ": publishing data: " + str(data))
                self.client.publish(self.topic, data)
                time.sleep(10)
        except Exception as e:
            logging.error(self.clientID + ": Error publishing data to topic " + self.topic + ": " + str(e))

    # Connect to broker and start the loop
    def start(self):
        try:
            self.client.connect(self.brokerAddress, self.brokerPort)
            self.client.loop_start()
        except Exception as e:
            logging.error(self.clientID + ": Error connecting to broker: " + str(e))

    # Close MQTT connection
    def stop(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            logging.error(self.clientID + ": Error disconnecting from broker: " + str(e))

    # Connect callback
    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(self.clientID + ": connected to broker successfully")
            # Start publishing data in a separate thread
            publishThread = threading.Thread(target=self.publishData)
            publishThread.start()
        else:
            logging.error(self.clientID + ": failed to connect to broker with result code " + str(rc))

    # Disconnect callback
    def onDisconnect(self, client, userdata, rc):
        logging.info(self.clientID + ": disconnected from broker with result code " + str(rc))

    # Publish callback
    def onPublish(self, client, userdata, mid):
        logging.info(self.clientID + ": published message with mid " + str(mid))
