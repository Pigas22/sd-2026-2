# cliente_eco.py — demonstração da Aula 1 (falha parcial)
# Rode em OUTRO terminal:  python cliente_eco.py
# Enquanto ele aguarda a resposta, derrube o servidor (Ctrl+C no terminal do servidor).
import socket, time

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)                       # tempo-limite do cliente (segundos)
t0 = time.time()
try:
    s.connect((HOST, PORT))
    s.sendall(b"oi")
    print("[cliente] enviei 'oi', aguardando resposta...", flush=True)
    resposta = s.recv(1024)
    print("[cliente] resposta:", resposta or "(conexão encerrada sem resposta)")
except socket.timeout:
    print(f"[cliente] ERRO: tempo-limite estourou após {time.time()-t0:.1f}s sem resposta")
except ConnectionResetError:
    print(f"[cliente] ERRO: conexão resetada após {time.time()-t0:.1f}s (o servidor sumiu)")
finally:
    s.close()