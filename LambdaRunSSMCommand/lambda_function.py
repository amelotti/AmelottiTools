import json
import boto3
import time


class EntradaMaliciosa(Exception):
    pass


# Handler lambda. Recebe parâmetros da request GET e chama o método para rodar o comando SSM pré-definido
def lambda_handler(event, context):
    parametro01 = event['queryStringParameters']['param01']
    
    response = executaComandoSSM(parametro01=parametro01)
    
    return {
        'statusCode': 200,
        'body': response,
        'headers': {
            'Content-Type': 'text/html'
        }
    }


# Verifica se há caracteres especiais na entrada do parâmetro
def checaCaracterEspecial(parametro01):
    special_characters = " !\"#$%&'()*+,-/:;<=>?@[\]^_`{|}~"
    return (any(c in special_characters for c in dominio))


# Executa o documento do tipo comando no AWS Systems Manager
def executaComandoSSM(parametro01):
    ssm_client = boto3.client('ssm')
    
    response = '<!DOCTYPE html><html lang="pt-BR"><head><title>AWS SSM</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script></head>'
    response = response + '<body><div class="container"><h2>Execução de comando via AWS SSM</h2><br/><div class="panel-group"><div class="panel panel-default"><div class="panel-heading">Retorno da execução de comando SSM</div><div class="panel-body">'
    
    # Verifica se há caracteres especiais na entrada do usuário e aborta em caso positivo
    try:
        if checaCaracterEspecial(parametro01=parametro01):
            #print ("ERRO NO CARACTER ESPECIAL")
            raise EntradaMaliciosa(parametro01)
    except EntradaMaliciosa:
        response = response + "A entrada " + parametro01 + " é inválida. Favor verificar<br/>"
        response = response + '</div></div></div></div></body> </html>'
        return (response)
   
    ssm_waiter = ssm_client.get_waiter('command_executed')
    
    # Chama o comando SSM definido em NOME_DO_DOCUMENTO_SSM. Aqui, está direcionado a uma única instancia mas pode ser executado em uma lista.
    # Passa como parâmetro para o comando SSM o argumento definido no request
    r = ssm_client.send_command(InstanceIds=['ID_DA_INSTANCIA'],DocumentName="NOME_DO_DOCUMENTO_SSM",Parameters={'parametro01':[parametro01]},)
    cmdid = r['Command']['CommandId']
    
    # Configuração do waiter do comando, aguarda a execução concluir antes de seguir
    ssm_waiter.wait(
        CommandId=cmdid,
        InstanceId='ID_DA_INSTANCIA',
        WaiterConfig={
          'Delay': 10,
          'MaxAttempts': 5
        }
    )
    
    # Recebe o retorno do processamento do comando e retorna para o response - essa etapa não é obrigatória
    output = ssm_client.get_command_invocation(CommandId=cmdid,InstanceId='ID_DA_INSTANCIA',)
    response = response + output['StandardOutputContent']
    response = response + '</div></div></div></div></body> </html>'
    
    return (response)
