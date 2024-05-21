#!/bin/bash

# Image naming and current version
export SENSORS_SIMULATOR_IMAGE=sensors_simulator:1.0
export MOSQUITTO_BROKER_IMAGE=mosquitto_server:1.0
export EDGE_SERVER_IMAGE=edge_server:1.0

# Broker configuration
export BROKER_ADDRESS="10.5.0.7"
export BROKER_PORT="8883"
# Autentication
export EDGE_SERVER_USER="edge_server"
export EDGE_SERVER_PWD="edge_server"
export SIMULATOR_USER="sensors_simulator"
export SIMULATOR_PWD="sensors_simulator"

# Initialization variables
export AUTH_COOKIE=$(xauth list | awk '/MIT-MAGIC-COOKIE-1/ {print $NF; exit}')
export DEV=false

# Stop images if they were up
bash ./docker/docker_stop.bash

# If no --dev flag is written
file="./docker/docker-compose.yaml"

# Check which flags have been set
for arg in "$@"
do
  case $arg in
   "--build-dev")
      DEV=true
      # Docker compose for developemt environment
      file="./docker/docker-compose-dev.yaml"
      # Build all images
      bash ./docker/docker_build.bash --all
     ;;
   "--dev")
      DEV=true
      # Docker compose for developemt environment
      file="./docker/docker-compose-dev.yaml"
     ;; 
   "--build")
      # Build all images
      bash ./docker/docker_build.bash --all
     ;; 
  esac
done

# Start kokatbot containers
docker-compose -f $file up