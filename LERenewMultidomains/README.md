# LERenewMultidomains
Renova multiplos certificados LetsEncrypt em um ambiente com nginx

Esse script vai renovar uma lista de certificados Lets Encrypt usados em um nginx, usando validação DNS baseado no Cloudflare.

*Variáveis*
- DOMAINS: lista de domínios que serão renovados - já devem existir no Cloudflare
- VALIDFOR: quantos dias antes do certificado vencer para serem renovados
- LELIVEPATH: Path da pasta live do Lets Encrypt
- CFCREDS: caminho e arquivo com credenciais para autenticação na API do Cloudflare

