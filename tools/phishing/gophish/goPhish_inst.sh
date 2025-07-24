#!/bin/bash
# Copyright by @violentr
# Install and configure gophish kit for Linux Ubuntu (64 bit)

install_gophish() {
    echo "Installing GoPhish..."
    wget https://github.com/gophish/gophish/releases/download/v0.11.0/gophish-v0.11.0-linux-64bit.zip
    unzip gophish-v0.11.0-linux-64bit.zip
    rm gophish-v0.11.0-linux-64bit.zip
    echo "GoPhish installed."
}

install_certbot() {
    echo "Installing Certbot..."
    sudo apt update
    sudo apt install -y certbot
    echo "Certbot installed."
}

generate_certificates() {
    echo "Generating certificates..."
    read -p "Enter your domain name (e.g., example.com): " domain
    echo -e "Configure certbot \n"
    sudo certbot certonly -d $domain --manual --preferred-challenges dns --register-unsafely-without-email
    echo "Certificates generated."
}

configure_gophish() {
    echo "Configuring GoPhish..."
    config_file="config.json"
    listen_url="0.0.0.0:3333"
    cert_path="/etc/letsencrypt/live/$domain/fullchain.pem"
    key_path="/etc/letsencrypt/live/$domain/privkey.pem"

    # Update config.json
    jq --arg listen_url "$listen_url" --arg cert_path "$cert_path" --arg key_path "$key_path" \
    '.admin_server.listen_url = $listen_url | .admin_server.use_tls = true | .admin_server.cert_path = $cert_path | .admin_server.key_path = $key_path' \
    $config_file > tmp.$$.json && mv tmp.$$.json $config_file

    echo "GoPhish configured."
}

install_gophish
install_certbot
generate_certificates
configure_gophish

echo "GoPhish installation and configuration complete."
