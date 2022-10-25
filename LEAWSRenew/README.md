# LEAWSRenew
Renova certificados LetsEncrypt em um ambiente AWS sem portas públicas (80 e 443)

Esse script vai renovar certificados Lets Encrypt usados em um proxy docker, dentro de um ambiente AWS onde não temos portas 80 e 443 abertas publicamente.

*Variáveis*
- DAYS: tempo, em segundos, para expiração do certificado. Determina em que momento executar o processo de renovação
- DOMAIN: domínio do certificado a ser renovado (o certificado já deve ter sido emitido. Nesse caso, será apenas renovado pelo parâmetro renew do certbot)
- PEM: caminho para o arquivo do certificado (geralmente não é preciso alterar essa variável)
- DCOMPOSE: caminho para o arquivo docker-compose.yml que controla do container proxy
- DPROXY: nome do container proxy (conforme indicado dentro do arquivo compose). Esse é um container rodando nginx ou apache e que irá importar o certificado (pode ser um container com qualquer outra aplicação que vá usar/importar o certificado Lets Encrypt)
- SGID: para que o certificado seja renovado, é necessário abrir, temporariamente a porta 80. Isso é feito no Security Group indicado nessa variável


