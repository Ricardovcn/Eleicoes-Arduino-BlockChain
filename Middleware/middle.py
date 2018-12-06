import modulo_bluetooth as bluez
import requests, json, random, string
from base64 import b64encode
from Crypto.Cipher import AES

passwd_criptografar = "webservices-2018"
passwd_blockchain = "webservices-2018"

cripto = AES.new(passwd_criptografar.encode(), AES.MODE_EAX)
endereco = '10.3.1.21:5000'

def _criptografar(data):
    data_send = {}

    data_cript = cripto.encrypt(data.encode())
    data_send['data'] = b64encode(data_cript).decode()
    data_send['nonce'] = b64encode(cripto.nonce).decode()

    return data_send

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

        voto = {
            'voto': cand_num, 
            'passwd_blockchain': passwd_blockchain
        }

        response = requests.get(uri, data=_criptografar(voto))
        candidato = json.loads(response.text)
        bluez.send(candidato["mensagem"])

      
