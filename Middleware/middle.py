import modulo_bluetooth as bluez
import requests, json
from Crypto.Cipher import AES

cripto = AES.new("EmboraCaraPertoE")

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
        uri = "http://192.168.1.142:5000/candidato/"
        response = requests.get(uri+str(cand_num))
        candidato = json.loads(response.text)
        bluez.send(candidato["nome"])
    else:
        uri = "http://192.168.1.142:5000/voto/"
        response = requests.get(uri, data=_criptografar({'Voto':cand_num}))
        candidato = json.loads(response.text)
        bluez.send(candidato["mensagem"])

      