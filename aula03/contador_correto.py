import threading, time
total = 0
lock = threading.Lock()          # a trava

def soma_muitas():
    global total
    for _ in range(2000):
        with lock:               # SEÇÃO CRÍTICA: uma thread por vez
            atual = total
            time.sleep(0)
            total = atual + 1

ts = [threading.Thread(target=soma_muitas) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print("total:", total)           # agora SEMPRE 4000