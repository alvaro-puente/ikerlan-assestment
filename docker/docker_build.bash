#!/bin/bash

# Depending on the flags activated some images are built or not
for arg in "$@"
do
    case $arg in
    "--all")
        docker build -t $SENSORS_SIMULATOR_IMAGE -f docker/sensors_simulator/dockerfile .
        docker build -t $MOSQUITTO_BROKER_IMAGE -f docker/mosquitto_broker/dockerfile .
        docker build -t $EDGE_SERVER_IMAGE -f docker/edge_server/dockerfile .
        ;;
    "--sensor-sim")
        docker build -t $SENSORS_SIMULATOR_IMAGE -f docker/sensors_simulator/dockerfile .
        ;;
    "--mosquitto")
        docker build -t $MOSQUITTO_BROKER_IMAGE -f docker/mosquitto_broker/dockerfile .
        ;;
    "--edge-server")
        docker build -t $EDGE_SERVER_IMAGE -f docker/edge_server/dockerfile .
        ;;
    esac
done