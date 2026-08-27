import socket

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP
s.connect((HOST, PORT))                        # CONECTA no servidor
print("Conectado. Digite mensagens (ou 'sair'):")
while True:
    msg = input("> ")
    if msg == "sair":
        break
    s.sendall(msg.encode())                    # ENVIA bytes
    eco = s.recv(1024)                         # RECEBE o eco
    print("eco:", eco.decode())
s.close()