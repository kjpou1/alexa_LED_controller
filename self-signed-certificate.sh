#!/bin/bash

# Create necessary directories
sudo mkdir -p ./ssl/private
sudo mkdir -p ./ssl/certs

# Create a self signed SSL certificate.
sudo openssl req -new -newkey rsa:4096 -x509 -days 3650 -nodes \
             -subj /C=LU/ST=LU/L=LU/O=NA/CN=localhost \
             -keyout ./ssl/private/insecure.key -out ./ssl/certs/insecure.pem

# Create a DHParam file. Use 4096 bits instead of 2048 bits in production.
sudo openssl dhparam -out ./ssl/dhparam2048.pem 2048
