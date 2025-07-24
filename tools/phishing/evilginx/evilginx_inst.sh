#!/bin/env bash
# Copyright by violentr
# Install and configure Evilginx for Linux

install_dependencies() {
    echo "Installing dependencies..."
    sudo apt update
    sudo apt install -y git make gcc libpcap-dev libnetfilter-queue-dev
    echo "Dependencies installed."
}

install_evilginx() {
    echo -e "[+] Downlod Evilginx from github\n"
    mkdir -p ~/mytools/Evilginx
    wget "https://github.com/kgretzky/evilginx2/releases/download/v3.3.0/evilginx-v3.3.0-linux-64bit.zip"
    unzip "evilginx-v3.3.0-linux-64bit.zip"
    chmod +x evilginx
}

configure_evilginx() {
    if [ ! -e "$FILE_PATH" ]; then
    echo -e "[+] Create symlink for evilginx\n"
        ln -s "$(pwd)/evilginx" "/usr/local/bin/evilginx"
    fi
    echo -e "[+] Configuring Evilginx...\n"

    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "[!] Configuration file $CONFIG_FILE not found!\n"
        exit 1
    fi

    jq --arg domain "$DOMAIN" --arg ipv4 "$EXTERNAL_IP" \
       '.general.domain = $domain | .general.ipv4 = $ipv4' \
       "$CONFIG_FILE" > tmp.$$.json && mv tmp.$$.json "$CONFIG_FILE"
    mkdir -p ~/.evilginx
    cp config.json ~/.evilginx/

echo -e "[+] Configuration updated successfully.\n"
    echo -e "[+] Evilginx configured with domain: $domain and IP: $ip.\n"
}

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <domain> <external_ip>"
    exit 1
fi

DOMAIN=$1
EXTERNAL_IP=$2
CONFIG_FILE="config.json"
FILE_PATH="/usr/local/bin/evilginx"
#
# install_dependencies
install_evilginx
configure_evilginx $DOMAIN $EXTERNAL_IP

echo "Evilginx installation and configuration complete."
