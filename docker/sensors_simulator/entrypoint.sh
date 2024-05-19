#!/bin/bash

# Get hostname 
CONTAINER_HOSTNAME=$(cat /etc/hostname) 

# Add authentication entry to the hosts display inside of the container xauth configuration
xauth add "$CONTAINER_HOSTNAME/unix$DISPLAY" MIT-MAGIC-COOKIE-1 "$AUTH_COOKIE"

# Wait until database is up
until mysql -h 10.5.0.8 -u root -prootpassword -e "SELECT 1"; do
    >&2 echo "Database still not available. Waiting ..."
    sleep 1
done

# Launch nodes
if [ "$DEV" = true ]; then
    # Debug terminal
    xterm -hold -T sensor_simulator:Debug -e bash &
    xterm -hold -T sensor_simulator:publisher -e bash -c 'python3 /sensors_simulator/scripts/sensorsSimulator.py' &
else
    # Launch nodes
    python3 /sensors_simulator/scripts/sensorsSimulator.py &
fi

eval "bash"