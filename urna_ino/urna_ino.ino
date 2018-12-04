#include <LiquidCrystal.h>
#include <Keypad.h>
 
//Define os pinos que serão utilizados para ligação ao display
LiquidCrystal lcd(47, 45, 48, 46, 42, 40);

const byte qtdLinhas = 4; //QUANTIDADE DE LINHAS DO TECLADO
const byte qtdColunas = 4; //QUANTIDADE DE COLUNAS DO TECLADO
 
//CONSTRUÇÃO DA MATRIZ DE CARACTERES
char matriz_teclas[qtdLinhas][qtdColunas] = {
  {'1','2','3','A'},
  {'4','5','6','A'},
  {'7','8','9','C'},
  {'A','0','A','D'}
};

byte PinosqtdLinhas[qtdLinhas] = {22, 24, 26, 28}; //PINOS UTILIZADOS PELAS LINHAS
byte PinosqtdColunas[qtdColunas] = {50, 51, 52,53}; //PINOS UTILIZADOS PELAS COLUNAS

//INICIALIZAÇÃO DO TECLADO
Keypad teclado = Keypad( makeKeymap(matriz_teclas), PinosqtdLinhas, PinosqtdColunas, qtdLinhas, qtdColunas);

String cand_numero = "";
String cand_nome = "";
String op ="";
bool first = true;

char teclado_ler(){
  char tecla_pressionada = teclado.getKey(); //VERIFICA SE ALGUMA DAS TECLAS FOI PRESSIONADA
 
  return tecla_pressionada;
}

void lcd_limpar(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Numero:");
  //Posiciona o cursor na coluna 7, linha 0;
}

void cand_limpar(){
  cand_numero = "";
  cand_nome = "";
}

void lcd_cat_numero(String num){
  lcd.setCursor(7, 0);
  lcd.print(num);
}

void lcd_cat_nome(String nome){
  lcd.setCursor(0, 1);
  lcd.print("Nome:");
  lcd.setCursor(5, 1);
  lcd.print(nome);
}

void lcd_confirmar(){
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Confirmado");
  delay(2000);
  lcd_limpar();
  cand_limpar();
}

void lcd_erro(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Erro ao votar!");
  delay(2000);
  lcd_limpar();
  cand_limpar();
}

void lcd_nao_existe(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Nao existe!");
  delay(2000);
  lcd_limpar();
  cand_limpar();
}

String bluez_ler(){
  String command = "";
  if(first){
    first = false;
    delay(5000);
  }else
    delay(2000);
  if (Serial3.available()) {
    while(Serial3.available()){
     delay(10);
     char c = Serial3.read();
     if(c == ';') break;
     command += c;
    }
  }
  return command;
}

void bluez_escrever(String mensagem){
  Serial3.print(mensagem + ";");
}

void func_C(){
  op = "V:";
  if(cand_nome == "")
     op = "C:";
  bluez_escrever(op+cand_numero);
  cand_nome = bluez_ler();
  if(cand_nome == "Confirmado")
     lcd_confirmar();
  else if(cand_nome == "Erro")
     lcd_erro();
  else if(cand_nome == "Não existe")
      lcd_nao_existe();
  else
     lcd_cat_nome(cand_nome);
}

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  Serial3.begin(9600);//BLUTOOTH
  lcd_limpar();
}

void loop() {
  char tecla = teclado_ler();
  if(tecla){
    switch(tecla){
      case 'D':
        lcd_limpar();
        cand_limpar();
        break;
      case 'C':
        if(cand_numero.length() > 0)
          func_C();
        break;
      case 'A':
        break;
      default:
        cand_numero += tecla;
    }
    delay(10);
    lcd_cat_numero(cand_numero);
  }
}
