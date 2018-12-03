import json
from flask import Flask, Response, request, jsonify
import eleicao

app = Flask(__name__)


@app.route("/cand/<int:numero>/<nome>/<partido>", methods=['GET'])
def user(numero, nome, partido):
    status = eleicao.cadastrar_candidato(numero, nome, partido)
    return jsonify({"data": status}), 200


@app.route("/check/<int:numero>", methods=['GET'])
def user2(numero):
    data = eleicao.checar_candidato(numero)
    return jsonify({"data": data}), 200


@app.route("/votar/<int:numero>", methods=['GET'])
def user3(numero):
    data = eleicao.votar_candidato(numero)
    return jsonify({"data": data}), 200


@app.route("/apurar", methods=['GET'])
def user4():
    data = eleicao.apurar_votacao()
    return jsonify({"data": data}), 200

if __name__ == '__main__':
    app.run(debug=True)