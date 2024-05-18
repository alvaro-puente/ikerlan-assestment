#!/usr/bin/env python3

from SensorPublisher import SensorPublisher
import os

if __name__ == "__main__":
    # Get broker address and port
    BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
    BROKER_PORT= os.getenv("BROKER_PORT")
    # Start publishing
    pub1 = SensorPublisher("pub1", BROKER_ADDRESS, BROKER_PORT)
    pub1.start("sensor_data/temperature")
    pub2 = SensorPublisher("pub2", BROKER_ADDRESS, BROKER_PORT)
    pub2.start("sensor_data/humidity")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pub1.stop()
        pub2.stop()