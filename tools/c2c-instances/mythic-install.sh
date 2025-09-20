#!/usr/bin/bash
# Coded by violentr
#
# This script will install Mythic C2C
# Minimal configuration will be set

echo -e "[+] Installing OS dependencies \n"
sudo apt install make -y

echo -e "[+] Downloading Mythic"

mkdir -p tools
git clone https://github.com/its-a-feature/Mythic --depth 1 --single-branch

echo -e "[+] Install dependencies for Mythic"

cd Mythic && sudo ./install_docker_ubuntu
sudo make

echo -e "[+] Configuring Mythic \n"
sudo -E ./mythic-cli install github https://github.com/MythicAgents/Apollo.git
sudo -E ./mythic-cli install github https://github.com/MythicC2Profiles/http

echo -e "[+] Starting Mythic project \n"
sudo ./mythic-cli start
sudo ./mythic-cli status

# Port forwarding, accessible via ssh on localhost
# ssh -L 7443:127.0.0.1:7443 -i key.pem ubuntu@aws_ec2_ip
# ./mythic-cli config get MYTHIC_ADMIN_PASSWORD
# cat .env
