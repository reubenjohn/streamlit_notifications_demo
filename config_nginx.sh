#!/bin/bash

# This script configures nginx using the port provided as an argument

# Get the port from command line argument
PORT=${1:-80}

# Replace __PORT__ in the nginx.conf with the actual port
sed "s/__PORT__/$PORT/g" nginx.conf > /etc/nginx/sites-available/default

# Enable the site configuration
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

echo "Nginx configured to use port $PORT"