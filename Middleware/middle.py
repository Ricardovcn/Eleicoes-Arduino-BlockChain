import modulo_bluetooth as bluez
import requests, json, random, string
from Crypto.Cipher import AES

passwd_criptografar = "webservices-2018"
passwd_blockchain = "webservices-2018"

cripto = AES.new(passwd_criptografar)
endereco = '10.3.1.21:5000'

def _criptografar(data):
    # Adiciona o caractere para separar o git dos dados.
    data = json.dumps(data) + '#'
    resto = len(data) % 16

    # Verifica se o tamanho é multiplo de 16,
    # se não adiciona caracteres para que seja.
    if resto > 0:
        data = data + ''.join([random.choice(string.ascii_letters) for n in range(16 - resto)])

    return cripto.encrypt(data)

bluez.connect()

while True:
    msg = bluez.receive(";")
    msg_sp = msg.split(":")
    op = msg_sp[0]
    cand_num = msg_sp[1]
    if(op=="C"):
        uri = "http://{servidor}/candidato/{numero}".format(servidor=endereco, numero=cand_num)
        print(uri)
        response = requests.get(uri)
        print(response.text)
        candidato = json.loads(response.text)
        bluez.send(candidato["nome"])
    else:
        uri = "http://{servidor}/voto/".format(servidor=endereco)

        data = {
            'voto': cand_num, 
            'passwd_blockchain': passwd_blockchain
        }

        response = requests.get(uri, data=_criptografar(data))
        candidato = json.loads(response.text)
        bluez.send(candidato["mensagem"])

      
