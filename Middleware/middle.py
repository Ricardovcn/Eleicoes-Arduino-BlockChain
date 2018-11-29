import modulo_bluetooth as bluez
import requests, json

bluez.connect()

while True:
    msg = bluez.receive(";")
    msg_sp = msg.split(":")
    op = msg_sp[0]
    cand_num = msg_sp[1]

    uri = "http://192.168.1.142:5000/candidato/" if(op=="C") else "http://192.168.1.142:5000/voto/"

    response = requests.get(uri+str(cand_num))
    candidato = json.loads(response.text)

    if(op=="C"):
        bluez.send(candidato["nome"])
    else:
        bluez.send(candidato["mensagem"])