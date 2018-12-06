pragma solidity ^0.4.25;

contract eleicao{
    
    string password;

    struct Candidato {
        uint numero;
        string path_foto;
        string nome;
        string partido;
        uint votos;
    }
    
    mapping (uint => Candidato) private candidatos;
    uint[] private numerosCandidatos;
    
    constructor() public{
        password = "c37f3340567e333f06ae409fb9faa353";
    }

    function adicionarCandidato(uint _numero, string _path_foto, string _nome, string _partido) public{
        candidatos[_numero] = Candidato(_numero, _path_foto, _nome, _partido, 1);
        numerosCandidatos.push(_numero);
    }
    
    function votarCandidato(uint _numero) candidatoExiste(_numero) public returns (bool){
        candidatos[_numero].votos += 1;
        return true;
    }

    function getNumerosDosCandidatos() public constant returns (uint[]){
        return numerosCandidatos;
    }

    function getCandidato(uint _numero) candidatoExiste(_numero) public constant returns (uint, string, string, string, uint){
        return (
            _numero, 
            candidatos[_numero].path_foto, 
            candidatos[_numero].nome, 
            candidatos[_numero].partido, 
            candidatos[_numero].votos-1
        );
    }

    function getPassword() public constant returns (string){
        return password;
    }

    function setPassword(string _password) public{
        password = _password;
    }

    /*Modifiers permitem gastar menos ether para o caso da transação não ser efetivada.*/
    modifier candidatoExiste(uint _numero){
        require(candidatos[_numero].numero > 0);
        _;
    }
    
}
