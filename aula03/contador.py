import threading, time
total = 0
def soma_muitas():
    global total
    for _ in range(2000):
        atual = total         # LER
        time.sleep(0)         # força a troca de thread aqui
        total = atual + 1     # GRAVAR

ts = [threading.Thread(target=soma_muitas) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print("total:", total)        # deveria ser 4000 — mas sai bem MENOS
