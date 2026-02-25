## Importante por enquanto: ##

pyinstaller --noconfirm --onedir --windowed  "C:/2rgiScan/main.py"

## Comando para gerar GUI a partir do arquivo .ui do QtDesigner ##

pyside6-uic c:\2rgiScan\gui\main.ui -o c:\2rgiScan\gui\ui_main.py
pyside6-uic c:\2rgiScan\gui\LoginUI.ui -o c:\2rgiScan\gui\ui_LoginUI.py

copiar pasta db/banco.db
copiar arquivo config.ini

## Importante para sempre: ##
Colocar ambos na raiz do programa

Sempre ao usar o programa em uma nova maquina este IP precisa estar na regra do firewall senão, não vai conseguir acessar o postgre na vmauto

IP VMAuto = 192.168.1.206
Porta = 5432