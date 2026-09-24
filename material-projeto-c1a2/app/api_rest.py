"""
Interface REST do servico de inferencia.

O QUE JA ESTA PRONTO:
  - carregamento do modelo UMA vez, na subida (nao a cada requisicao)
  - rota sincrona /predict-sync, usada no laboratorio da Aula 6

O QUE VOCE PRECISA FAZER (TAREFAS.md, itens 1 e 2):
  - POST /predict  -> colocar na fila e devolver o id
  - GET  /resultado/{id} -> devolver o resultado quando estiver pronto

Rodar:  uvicorn app.api_rest:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""
import time
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app import fila
from app.log import registrar_requisicao

from app.modelo import carregar_modelo

app = FastAPI(title="Servico de Inferencia - C1.A2", version="0.1.0")

modelo = None


class Entrada(BaseModel):
    texto: str


@app.on_event("startup")
def _subir():
    """Carrega o modelo UMA vez. Este e o ponto-chave da Aula 6."""
    global modelo
    inicio = time.time()
    modelo = carregar_modelo()
    print(f"[startup] modelo carregado em {time.time() - inicio:.3f}s")


@app.get("/saude")
def saude():
    return {"status": "ok", "modelo_carregado": modelo is not None}


@app.post("/predict-sync")
def predict_sync(entrada: Entrada):
    """Inferencia SINCRONA: o cliente espera a resposta. Lab da Aula 6."""
    inicio = time.perf_counter()
    identificador = str(uuid.uuid4())
    try:
        if not entrada.texto.strip():
            raise HTTPException(status_code=400, detail="texto vazio")
        resultado = modelo.prever(entrada.texto)
        resultado["tempo_ms"] = round((time.time() - inicio) * 1000, 2)
        return resultado
    finally:
        registrar_requisicao(identificador, len(entrada.texto), inicio, "rest")


# ------------------------------------------------------------------
# TAREFA 1 - submissao assincrona
# ------------------------------------------------------------------
@app.post("/predict", status_code=202)
def predict(entrada: Entrada):
    """Deve enfileirar a tarefa e devolver {"id": ...} SEM esperar."""
    # DICA: use app.fila.enfileirar(entrada.texto)
    # raise NotImplementedError("implemente a submissao assincrona")

    inicio = time.perf_counter()
    identificador = str(uuid.uuid4())
    try:
        if not entrada.texto.strip():
            raise HTTPException(status_code=400, detail="texto vazio")
        id_tarefa = fila.enfileirar(entrada.texto)
        identificador = id_tarefa
        return {"id": id_tarefa}
    finally:
        registrar_requisicao(identificador, len(entrada.texto), inicio, "rest")

# ------------------------------------------------------------------
# TAREFA 2 - consulta do resultado
# ------------------------------------------------------------------
@app.get("/resultado/{tarefa_id}")
def resultado(tarefa_id: str):
    """Deve devolver o resultado; 404 se o id nao existir."""
    # DICA: use app.fila.buscar_resultado(tarefa_id)
    # raise NotImplementedError("implemente a consulta de resultado")

    inicio = time.perf_counter()
    try:
        retorno = fila.buscar_resultado(tarefa_id)
        if retorno:
            return retorno
        raise HTTPException(status_code=404, detail="tarefa não encontrada")
    finally:
        registrar_requisicao(tarefa_id, 0, inicio, "rest")
