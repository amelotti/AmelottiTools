import json
import boto3
import CloudFlare
import os

def lambda_handler(event, context):
    msgjson = json.loads(event["Records"][0]["Sns"]["Message"])
    ret = ''
    
    if msgjson['Event'] == 'autoscaling:EC2_INSTANCE_LAUNCH':
        print("autoscaling:EC2_INSTANCE_LAUNCH")
        ret = cadastrainstancia(msgjson)
    elif msgjson['Event'] == 'autoscaling:EC2_INSTANCE_TERMINATE':
        print("autoscaling:EC2_INSTANCE_TERMINATE")
        ret = removeinstancia(msgjson)
    else:
        print("Ação inválida")
        print(msgjson)
    
    
def cadastrainstancia(msgjson):
    zone_id = os.getenv('ZONEID')
    token = os.getenv('TOKEN')
    comment = os.getenv('COMMENT')

    ec2 = boto3.resource('ec2')
    cf = CloudFlare.CloudFlare(token=token)
    
    # Obtem o IP da nova instância
    try:
        instance = ec2.Instance(msgjson['EC2InstanceId'])
        instance_ip = instance.public_ip_address
    except:
        print("Não foi possível obter o IP da instância. Verifique o status da instância " + msgjson['EC2InstanceId'])
    
    # Adiciona um IP nas whitelists dp CF
    try:
        data = {"configuration": {"target": "ip", "value": instance_ip}, "mode": "whitelist", "notes": comment + " - " + msgjson['EC2InstanceId']}
        resp = cf.zones.firewall.access_rules.rules.post(zone_id, data=data)
    except:
        print("Não foi possível adicionar o IP à whitelist no cloudflare. Verifique o retorno da chamada: " + resp)

    
def removeinstancia(msgjson):
    zone_id = os.getenv('ZONEID')
    token = os.getenv('TOKEN')
    comment = os.getenv('COMMENT')

    cf = CloudFlare.CloudFlare(token=token)
    
    # Remove a regra da whitelist do CF
    try:
        # Lista as entradas nas regras do CF filtradas por instance id
        data = {'per_page': 1, 'notes': comment + " - " + msgjson['EC2InstanceId']}
        resp = cf.zones.firewall.access_rules.rules.get(zone_id, params=data)
        # Obtém o ID da regra a ser deletada
        cfrid = resp[0]['id']
        # Deleta a regra
        resp = cf.zones.firewall.access_rules.rules.delete(zone_id, cfrid)
    except:
        print("Não foi possível remover o IP das whitelists do CF. Verifique o retorno da chamada: " + resp)
    
