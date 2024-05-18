#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import logging
import random
import json
import time

# Configure log file
logging.basicConfig(filename='/sensors_simulator/logs/sensor_publishers.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SensorPublisher():

    def __init__(self, clientID, brokerAddress, brokerPort, user, password):
        self.client = mqtt.Client()
        self.client.username_pw_set(user, password)
        self.brokerAddress = brokerAddress
        self.brokerPort = brokerPort
        self.clientID = clientID
        
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
    def publishData(self, topic):
        try:
            while True:
                data = self.generateData()
                self.client.publish(topic, data)
                time.sleep(0.1)
        except Exception as e:
            logging.error(self.clientID + ": Error publishing data to topic " + topic + ":" + str(e))

    # Connect to broker and start sending data
    def start(self, topic):
        try:
            self.client.connect(self.brokerAddress, self.brokerPort)
            logging.info(self.clientID + " connected succesfully!")
            self.publishData(topic)
        except Exception as e:
            logging.error(self.clientID + ": Error connecting to broker or publishing data to topic " + topic + ":" + str(e))

    # Close MQTT connection
    def stop(self):
        try:
            self.client.disconnect()
        except Exception as e:
            logging.error(self.clientID + ": Error disconnecting from broker: " + str(e))


