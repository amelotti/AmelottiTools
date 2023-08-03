Código para função lambda cadastrar e remover IPs de whitelist do CloudFlare via ASG

Em algumas situações podemos querer adicionar IPs a whitelists no Cloudflare de máquinas que vão precisar bypassar os controles definidos (por exemplo, comunicação entre servidores confiáveis). Esse código permite cadastrar uma função lambda que irá receber eventos (Launch e Terminate) de um AutoScaling Group, via tópico SNS, e irá cadastrar ou remover o IP da instância nas whitelists do CF. _Este código não é recomendado caso você defina uma política zero trust. Neste caso estamos confiando em um servidor remoto e permitindo que o mesmo bypasse as regras, políticas e controles do CF._

Variáveis: 
- ZONEID: id da zona DNS no CloudFlare
- TOKE: api token do CloudFlare (este token deve ter permissão 'Edit' no item zone.firewall services)
- COMMENT: texto que será inserido no campo 'notes' da regra de whitelist nas IP Access Rules do CF
