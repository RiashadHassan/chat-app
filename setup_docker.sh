#!/bin/bash

# Exit on error
set -e

USER_TO_FIX=${1:-$USER}

# Check if docker group exists
if ! getent group docker >/dev/null; then
    echo "Creating 'docker' group..."
    sudo groupadd docker
fi

# Check if user is already in docker group
if id -nG "$USER_TO_FIX" | grep -qw docker; then
    echo "✅ User '$USER_TO_FIX' already has Docker permissions."
else
    echo "🔧 Adding user '$USER_TO_FIX' to the 'docker' group..."
    sudo usermod -aG docker "$USER_TO_FIX"
    echo "✅ Done. Please log out and log back in, or run: newgrp docker"
fi
