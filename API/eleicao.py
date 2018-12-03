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