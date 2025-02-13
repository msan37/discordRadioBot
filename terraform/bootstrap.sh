#!/bin/bash
# Update package lists and install Docker
apt-get update -y
apt-get install -y docker.io

# Start Docker and configure it to start on boot
systemctl start docker
systemctl enable docker

# (Optional) Private image; you'll need to login.
# docker login -u username -p password

# Run Discord bot container
docker run -d --restart always --name discord_bot discordradiobot:latest