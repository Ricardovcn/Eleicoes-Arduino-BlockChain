from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from requests.exceptions import ConnectionError
import json


ABI = None
CONTRACT_ADDRESS = None
w3 = None
contract_eleicao = None

def cadastrar_candidato(numero, nome, partido):
    try:
        tx_hash = contract_eleicao.functions.adicionarCandidato(
            numero, nome, partido
        ).transact()
        
        # Espera a transação ser minerada
        w3.eth.waitForTransactionReceipt(tx_hash)
    except ConnectionError:
        raise "Não foi possível conectar com a rede de blockchain"
    except BadFunctionCallOutput:
        raise "Você deve fazer o deploy do contrato novamente."

    return True


def votar_candidato(numero):
    try:
        tx_hash = contract_eleicao.functions.votarCandidato(
            numero
        ).transact()

        # Espera a transação ser minerada
        w3.eth.waitForTransactionReceipt(tx_hash)
    except ValueError:
        return False
    except ConnectionError:
        raise Exception("Não foi possível conectar com a rede de blockchain")
    except BadFunctionCallOutput:
        raise Exception("Você deve fazer o deploy do contrato novamente.")

    return True


def checar_candidato(numero):
    try:
        c = contract_eleicao.functions.getCandidato(numero).call()

    except ValueError:
        return None
    except ConnectionError:
        raise Exception("Não foi possível conectar com a rede de blockchain")
    except BadFunctionCallOutput:
        raise Exception("Você deve fazer o deploy do contrato novamente.")
    
    return {'nome':c[1], 'partido': c[2]}


def apurar_votacao():
    try:    
        numeros = contract_eleicao.functions.getNumerosDosCandidatos().call()

        candidatos = []
        for n in numeros:
            c = contract_eleicao.functions.getCandidato( n ).call()
            candidato = {
                'numero': c[0],
                'nome': c[1],
                'partido': c[2],
                'votos': c[3]
            }

            candidatos.append(candidato)

    except ConnectionError:
        raise Exception("Não foi possível conectar com a rede de blockchain")
    except BadFunctionCallOutput:
        raise Exception("Você deve fazer o deploy do contrato novamente.")

    return candidatos


def _inicializar():
    global w3, ABI, CONTRACT_ADDRESS, contract_eleicao

    try:
        # Obtém as instancia do Web3 e define a conta default
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        w3.eth.defaultAccount = w3.eth.accounts[1]

        # Obtém o ABI e CONTRACT_ADDRESS do contrato eleicao
        with open("data.json", 'r') as f:
            datastore = json.load(f)
            ABI = datastore["abi"]
            CONTRACT_ADDRESS = datastore["contract_address"]

        # Obtém a instancia do contrato
        contract_eleicao = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

    except ConnectionError:
        raise Exception("Não foi possível conectar com a rede de blockchain")


_inicializar()