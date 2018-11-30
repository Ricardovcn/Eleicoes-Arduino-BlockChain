#coding: utf-8

import json
from flask import Flask


app = Flask(__name__)

@app.route('/candidato/<voto>', methods=['GET'])
def candidato(voto):
    if(int(voto)==17):
        return json.dumps({'nome': "Bulbassauro"})
    elif(int(voto)==13):
        return json.dumps({'nome': "Andrade"})
    elif(int(voto)==12):
        return json.dumps({'nome': "Cangaciro"})
    else:
        return json.dumps({'nome': "Voto Nulo"})

@app.route('/voto/<voto>', methods=['GET'])
def vota(voto):
        return json.dumps({'mensagem': 'Confirmado'})


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.142")