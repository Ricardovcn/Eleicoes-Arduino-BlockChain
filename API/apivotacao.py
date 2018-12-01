#coding: utf-8

import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = './imagens'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def inicio():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return json.dumps({'erro': 'Utilize o metodo GET para acessar essa páginas.'})


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

# A partir do cadastro de um formulário, a API obtém os valores
# escolhidos pelo usuário, e a imagem do candidato.
# Retorna um json no formato abaixo
# {
#  'nome': 'Bulbassauro',
#  'numeroCandidato': 17,
#  'partido': 'PJL',
#  'imagem': 'Bulbassauro.png'
# }
@app.route('/cadastrar', methods=['GET','POST'])
def cadastrarCandidato():
    if request.method == 'POST':
        # Obtem o nome do candidato para salvar a imagem
        nomeCandidato = request.form['nomeCandidato']

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Transforma o nome da imagem obtida para o nome do candidato
            nomeImagem = nomeCandidato + '.' + filename.split('.')[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeImagem))

        candidato = {}
        candidato['nome'] = nomeCandidato
        candidato['numeroCandidato'] = int(request.form['numCandidato'])
        candidato['partido'] = request.form['partido']
        candidato['imagem'] = nomeImagem
        return json.dumps(candidato)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
