#!/bin/bash
# Purpose: Renew LE certificate and reload docker proxy
# Author: Luiz Amelotti <luiz@amelotti.com>
# -----------------------------------------------------


# Time, in seconds, before renew - Default 7 days
DAYS="604800"
# Domain to check/renew
DOMAIN="teste.com"
# LE certificate path
PEM="/etc/letsencrypt/live/$DOMAIN/cert.pem"
# Path to docker-compose.yml
DCOMPOSE="/opt/app/docker-compose.yml"
# Docker proxy container name
DPROXY=app-proxy
# AWS Security Group IP
SGID="sg-0e877a70ceEXAMPLE"

_openssl="/usr/bin/openssl"

$_openssl x509 -enddate -noout -in "$PEM"  -checkend "$DAYS" | grep -q 'Certificate will expire'

if [ $? -eq 0 ]
then
  docker compose -f $DCOMPOSE stop $DPROXY

  aws ec2 authorize-security-group-ingress --group-id "$SGID" --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "IpRanges": [{"CidrIp": "'"0.0.0.0/0"'", "Description": "LE80"}]}]'
  aws ec2 authorize-security-group-ingress --group-id "$SGID" --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443, "IpRanges": [{"CidrIp": "'"0.0.0.0/0"'", "Description": "LE443"}]}]'

  certbot renew

  aws ec2 revoke-security-group-ingress --group-id "$SGID" --protocol tcp --port 80 --cidr "0.0.0.0/0"
  aws ec2 revoke-security-group-ingress --group-id "$SGID" --protocol tcp --port 443 --cidr "0.0.0.0/0"

  docker compose -f $DCOMPOSE up -d $DPROXY
fi

