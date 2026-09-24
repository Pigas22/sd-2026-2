"""Registro das requisicoes recebidas pelos servicos."""
from datetime import datetime
from pathlib import Path
import threading
import time
import uuid


PASTA_LOG = Path(__file__).resolve().parent.parent / "logs"
PASTA_LOG.mkdir(exist_ok=True)
ARQUIVO_LOG = PASTA_LOG / (
    f"requisicoes-{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:8]}.log"
)
_lock = threading.Lock()


def registrar_requisicao(identificador: str, tamanho_entrada: int,
                         inicio: float, servico: str) -> None:
    """Adiciona uma linha com os dados da requisicao no log do processo."""
    tempo_ms = round((time.perf_counter() - inicio) * 1000, 2)
    linha = (
        f"id={identificador} servico={servico} "
        f"tamanho_entrada={tamanho_entrada} tempo_resposta_ms={tempo_ms}\n"
    )
    with _lock:
        with ARQUIVO_LOG.open("a", encoding="utf-8") as arquivo:
            arquivo.write(linha)