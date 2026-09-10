from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Tarefas")
tarefas = []                # "banco" em memória (só para aula)

class Tarefa(BaseModel):    # o TIPO da entrada -> vira validação + /docs
    titulo: str


@app.get("/tarefas")            # LER a coleção
def listar():
    return tarefas


@app.post("/tarefas", status_code=201)  # CRIAR (201 = Created)
def criar(tarefa: Tarefa):
    nova = {"id": len(tarefas) + 1, "titulo": tarefa.titulo}
    tarefas.append(nova)
    return nova

@app.get("/tarefas/{tid}")        # LER um item
def obter(tid: int):
    for t in tarefas:
        if t['id'] == tid:
            return t
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


## Comando para executar:
# uvicorn app:app --reload --port 8000
# abra no navegador:  http://localhost:8000/docs