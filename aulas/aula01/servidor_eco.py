# servidor_eco.py — demonstração da Aula 1 (falha parcial)
# Rode em um terminal:  python servidor_eco.py
# Enquanto o cliente espera, aperte Ctrl+C aqui para "derrubar" o servidor.
import socket, time

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
print(f"[servidor] ouvindo em {HOST}:{PORT} (Ctrl+C para derrubar)", flush=True)

while True:
    conexao, endereco = s.accept()
    dado = conexao.recv(1024)
    print(f"[servidor] recebi {dado!r} de {endereco} — processando (15s)...", flush=True)
    time.sleep(15)                     # simula processamento lento
    conexao.sendall(b"ECO: " + dado)   # (só chega aqui se NAO for derrubado)
    conexao.close()