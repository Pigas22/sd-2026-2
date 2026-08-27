import socket, threading
HOST, PORT = "127.0.0.1", 5000


def atender(conexao, endereco): # roda em uma THREAD por cliente
    print(f"[servidor] {endereco} conectou", flush=True)
    while True:
        dado = conexao.recv(1024)
        if not dado: break
        conexao.sendall(dado) # eco
    conexao.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)); s.listen()
print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)
while True:
    conexao, endereco = s.accept() # aceita um cliente...
    threading.Thread(
        target=atender,
        args=(conexao, endereco),
        daemon=True
    ).start() # entrega à Thread e VOLTA já
