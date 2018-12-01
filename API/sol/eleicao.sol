pragma solidity ^0.4.25;

contract eleicao{
    
    struct Candidato {
        uint numero;
        string nome;
        string partido;
        uint votos;
    }
    
    mapping (uint => Candidato) private candidatos;
    uint[] private numerosCandidatos;
    
    constructor() public{
        
    }

    function adicionarCandidato(uint _numero, string _nome, string _partido) public{
        candidatos[_numero] = Candidato(_numero, _nome, _partido, 1);
        numerosCandidatos.push(_numero);
    }
    
    function votarCandidato(uint _numero) candidatoExiste(_numero) public returns (bool){
        candidatos[_numero].votos += 1;
        return true;
    }

    function getNumerosDosCandidatos() public constant returns (uint[]){
        return numerosCandidatos;
    }
    
    
    function getCandidato(uint _numero) candidatoExiste(_numero) public constant returns (uint, string, string, uint){
        return (_numero, candidatos[_numero].nome, candidatos[_numero].partido, candidatos[_numero].votos-1);
    }

    /*Modifiers permitem gastar menos ether para o caso da transação não ser efetivada.*/
    modifier candidatoExiste(uint _numero){
        require(candidatos[_numero].numero > 0);
        _;
    }
    
}
