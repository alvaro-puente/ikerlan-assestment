#!/bin/bash

set -euxo pipefail

apt-get update && apt-get install -y --no-install-recommends \
    gnome-terminal \
    iputils-ping \
    dbus-x11 \
    xterm \
    xauth

apt-get clean && rm -rf /var/lib/apt/lists/*