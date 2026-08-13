import socket, threading

def atender_cliente(conexao, endereco):
    print(f"[servidor] cliente conectado: {endereco}", flush=True)
    while True:
        dado = conexao.recv(1024)                 # RECEBE bytes
        if not dado:                              # cliente fechou → sai
            break
        print(f"[servidor] recebi: {dado.decode()}", flush=True)
        conexao.sendall(dado)                     # ECO: devolve o mesmo
    conexao.close()

HOST, PORT = "127.0.0.1", 5000               # localhost + porta escolhida

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reusar a porta
s.bind((HOST, PORT))                          # reserva o endereço
s.listen(2)                                    # passa a ESCUTAR
print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

while True:
    conexao, endereco = s.accept()                # ACEITA um cliente (bloqueia)
    threading.Thread(target=atender_cliente, args=(conexao,endereco,)).start()
