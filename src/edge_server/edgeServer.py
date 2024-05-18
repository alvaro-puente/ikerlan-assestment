#!/usr/bin/env python3

from MQTTSubscriber import MQTTSubscriber
import os

# Execute edge server logic
if __name__ == "__main__":
    # Get broker address and port
    BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
    BROKER_PORT= int(os.getenv("BROKER_PORT"))
    USER = os.getenv("EDGE_SERVER_USER")
    PWD = os.getenv("EDGE_SERVER_PWD")
    # Define subscribers
    subs1 = MQTTSubscriber(BROKER_ADDRESS, BROKER_PORT, USER, PWD, "subs1")
    subs1.connect()
    subs1.subscribe("sensor_data/temperature")
    print("Subscriber 1 listening...")
    subs2 = MQTTSubscriber(BROKER_ADDRESS, BROKER_PORT, USER, PWD, "subs2")
    subs2.connect()
    subs2.subscribe("sensor_data/humidity")
    print("Subscriber 2 listening...")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        subs1.client.disconnect()
        subs1.client.loop_stop()
        subs2.client.disconnect()
        subs2.client.loop_stop()