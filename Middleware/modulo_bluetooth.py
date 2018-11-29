import bluetooth, time, json

bluez = ('20:16:10:25:30:24', 'HC-06')

sock = None
char_end = "!"

def connect():
    global sock
    try:
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        while bluez not in nearby_devices:
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print('Founded HC-06')
        addr = bluez[0]
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((addr, port))
        time.sleep(1)
        print("Connected HC-06")
        return True
    except:
        print("Not connected HC-06")
        return False

def send(msg):
    global sock
    try:
        sock.send(msg+';')
        return True
    except:
        return False

def receive(end_c):
    global sock
    try:
        data = sock.recv(1024).decode('utf-8')
        while(end_c not in data):
            data = data+sock.recv(1024).decode('utf-8')
        return data.replace(';','')
    except:
        return ""


"""
bluez = ('20:16:10:25:34:22', 'HC-06')

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))
while bluez not in nearby_devices:
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))

addr = bluez[0]
name = bluez[1]

print ("Conectando em %s - %s" %(name, addr))

port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((addr, port))
time.sleep(1)

try:
    while True:
        tempo = int(input("Informe o tempo de alimentação: "))
        tanque = int(input("Informe o tanque a alimentar: "))
        dados = {
            "tanque":tanque,
            "tempo":tempo
        }
        sock.send(json.dumps(dados))
        data = sock.recv(1024).decode('utf-8')
        while("!" not in data):
            data = data+sock.recv(1024).decode('utf-8')
        print(data)
except Exception as e:
    print("Comando nao reconhecido... Finalizando conexao...")
    sock.close()
    print("ALL DONE!!!", e)
"""