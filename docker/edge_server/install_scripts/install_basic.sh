#!/bin/bash

set -euxo pipefail

apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    gnome-terminal \
    iputils-ping \
    dbus-x11 \
    xterm \
    xauth

apt-get clean && rm -rf /var/lib/apt/lists/*