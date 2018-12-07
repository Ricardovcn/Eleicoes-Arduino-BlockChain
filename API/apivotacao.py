#coding: utf-8

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from base64 import b64decode
import json
import eleicao
from Crypto.Cipher import AES

NAME_APP = 'Eleições TSI'
passwd_criptografia = 'webservices-2018'

UPLOAD_FOLDER = './static/imagens'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

HOST = '192.168.1.136'
PORT = 5000
ADDRESS = HOST + ':' + str(PORT)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

candidatos = {'candidatos': []}



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def paginaErros(mensagemErro):
    return render_template('index.html', nome=NAME_APP, erro=True, mensagem=mensagemErro, address=ADDRESS)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.html', nome=NAME_APP, paginaInicial=True, address=ADDRESS)


@app.route('/cadastro', methods=['GET'])
def paginaCadastro():
    return render_template('index.html', cadastrarCandidato=True, nome=NAME_APP, address=ADDRESS)


def verificarNumero(numeroCandidato):
    if numeroCandidato == 0:
        return False
    else:
        candidatos = eleicao.apurar_votacao()

        for cand in candidatos:
            nCand = int(cand['numero'])

            if(nCand == numeroCandidato):
                return False

    return True

@app.route('/listaCandidatos', methods=['GET'])
def lista():
    candidatos = eleicao.apurar_votacao()
    if len(candidatos) == 0:
        return render_template('index.html', nome=NAME_APP, listar=True, listaVazia=True, address=ADDRESS)    


    return render_template('index.html', nome=NAME_APP, listar=True, listaCandidatos=candidatos, address=ADDRESS)


def calcularPorcentagem(votosCandidato, totalDeVotos):
    if totalDeVotos == 0:
        return 0

    return round(float((votosCandidato / totalDeVotos) * 100), 2)

@app.route('/apurarVotacao', methods=['GET'])
def apurarVotacao():
    candidatos = eleicao.apurar_votacao()

    totalDeVotos = 0

    candidatos.sort(key=lambda c: c['votos'], reverse=True)

    for cand in candidatos:
        totalDeVotos +=  int(cand['votos'])

    for cand in candidatos:
        cand['porcentagem'] = calcularPorcentagem(int(cand['votos']), totalDeVotos)


    if len(candidatos) == 0:
        return render_template('index.html', nome=NAME_APP, apurar=True, listaVazia=True, address=ADDRESS)

    

    return render_template('index.html', nome=NAME_APP, apurar=True, listaCandidatos=candidatos, address=ADDRESS)


@app.route('/candidato/<int:numero>', methods=['GET'])
def candidato(numero):
    dados = None
    try:
        dados = eleicao.checar_candidato(numero)
    except Exception as e:
        print(e)

    if not dados:
        return json.dumps({'nome': 'Não existe'})

    return json.dumps(dados)



def descriptografar(data):
    #print('data dict ', data, type(data))    

    data_cript = b64decode(data['data'].encode())
    nonce = b64decode(data['nonce'].encode())
    
    #print('data cript', data_cript, type(data_cript))
    #print('nonce', nonce, type(nonce))

    cripto = AES.new(passwd_criptografia.encode(), AES.MODE_EAX, nonce=nonce)
    data = cripto.decrypt(data_cript)
    #print('data ', data, type(data))

    return data
    
    

@app.route('/voto/', methods=['GET'])
def vota():
    try:
        #print(request.form)
        data = descriptografar(request.form)
        data = data.decode('utf-8')

        data = json.loads(data)

        print(data)

        if not eleicao.autenticar(data['passwd_blockchain']):
            raise Exception('Acesso a blockchain: Permissão negada!')

        #print(data['voto'])

        eleicao.votar_candidato(int(data['voto']))
    except Exception as e:
        print(e)
        return json.dumps({'mensagem': 'erro'})
        

    return json.dumps({'mensagem': 'Confirmado'})



# A partir do cadastro de um formulário, a API obtém os valores
# escolhidos pelo usuário, e a imagem do candidato.
# Retorna um json no formato abaixo
# {
#  'nome': 'Bulbassauro',
#  'numeroCandidato': 17,
#  'partido': 'PSL',
#  'imagem': 'Bulbassauro.png'
# }
@app.route('/cadastrar', methods=['POST'])
def cadastrarCandidato():
    chave = request.form['chave']

    if eleicao.autenticar(chave):
        nomeCandidato = request.form['nomeCandidato']
        nCandidato = request.form['numCandidato']
        partido = request.form['partido']

        if (nomeCandidato != "") & (nCandidato != "") & (partido != ""):
            # Obtem o nome do candidato para salvar a imagem
            numeroCandidato = int(nCandidato)

            if verificarNumero(numeroCandidato):
                # check if the post request has the file part
                nomeImagem = ''
                if 'file' not in request.files:
                    nomeImagem = 'candidato-sem-foto.png'
                else:
                    file = request.files['file']
                    # if user does not select file, browser also
                    # submit a empty part without filename
                    if file.filename == '':
                        nomeImagem = 'candidato-sem-foto.png'
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        # Transforma o nome da imagem obtida para o nome do candidato
                        nomeImagem = str(nCandidato) + '.' + filename.split('.')[1]
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeImagem))

                candidato = {}
                candidato['nome'] = nomeCandidato
                candidato['numeroCandidato'] = numeroCandidato
                candidato['partido'] = partido
                candidato['nome_imagem'] = nomeImagem

                candidatos['candidatos'].append(candidato)
                eleicao.cadastrar_candidato(numeroCandidato, nomeCandidato, partido, nomeImagem)
                return render_template('index.html', nome=NAME_APP, candidatoCadastrado = candidato, address=ADDRESS)
            else:
                return paginaErros('O número fornecido não é válido ou já está registrado para outro candidato!')
        else:
            return paginaErros('Os campos Nome, Número e Partido não podem estar vazios!')
    else:
        return paginaErros('A chave de segurança fornecida não é válida! Apenas usuários com a chave de segurança podem realizar o cadastro de candidatos.')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
