#!/bin/bash

###
# Renova uma lista de certificados com lets encrypt, usando validação baseada em DNS no CloudFlare. Certificados instalados e configurados no nginx
###

# lista de dominios
domains="domain01.com.br domain02.com.br domain03.com.br"

# prazo para vencimento do certificado
validfor=10

# path da pasta live do Lets Encrypt
lelivepath='/etc/letsencrypt/live'

# arquivo com as credenciais para a API do Cloudflare
cfcreds='~/.cf.creds'

for d in $domains
do
        if [ `ssl-cert-check -c $lelivepath/$d/fullchain.pem | awk '{print $6}' | tail -n 1` -lt 10 ]
        then
                echo "certbot certonly --force-renewal --dns-cloudflare --dns-cloudflare-credentials $cfcreds -d $d"
                echo "service nginx reload"
        fi
done

