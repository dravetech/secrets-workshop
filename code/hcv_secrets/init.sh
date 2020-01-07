#!/bin/sh
VAULT="docker-compose exec vault-dev-server"

$VAULT vault login
$VAULT vault kv put secret/bma password=this-is-the-password-for-bma
$VAULT vault kv put secret/bma/rtr00 password=this-is-rtr00-password
$VAULT vault kv put secret/defaults password=this-is-the-default-password
