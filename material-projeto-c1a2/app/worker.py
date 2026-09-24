"""
Worker: consome a fila e executa a inferencia.

O QUE JA ESTA PRONTO: o laco principal e o carregamento do modelo.
Em caso de falha a tarefa volta para a fila; apos 3 tentativas vai para a
fila de descarte (dead-letter) e o cliente passa a ver status "falhou".

Rodar:  python -m app.worker
Suba mais de um worker em terminais diferentes e veja a carga se dividir.
"""
import time

from app import fila
from app.log import registrar_requisicao
from app.modelo import carregar_modelo

MAX_TENTATIVAS = 3


def main():
    print("[worker] carregando modelo...")
    modelo = carregar_modelo()
    print("[worker] pronto. aguardando tarefas (Ctrl+C para sair)")

    while True:
        tarefa = fila.proxima_tarefa(timeout=5)
        if tarefa is None:
            continue

        print(f"[worker] processando {tarefa['id']}")
        inicio = time.perf_counter()
        try:
            resultado = modelo.prever(tarefa["texto"])
            resultado["status"] = "pronto"
            resultado["tempo_ms"] = round((time.time() - inicio) * 1000, 2)

            # TAREFA 3: guarde o resultado para o cliente consultar depois.
            # DICA: fila.guardar_resultado(tarefa["id"], resultado)
            # raise NotImplementedError("guarde o resultado na TAREFA 3")

            fila.guardar_resultado(tarefa["id"], resultado)

        except NotImplementedError:
            raise
        # ------------------------------------------------------------------
        # TAREFA 5 - retentativa e fila de descarte (dead-letter)
        # ------------------------------------------------------------------
        except Exception as erro:  # noqa: BLE001
            # TAREFA 5: retentativa + dead-letter em vez de so registrar.
            # print(f"[worker] ERRO em {tarefa['id']}: {erro}")

            tarefa["tentativas"] = tarefa.get("tentativas", 0) + 1

            if tarefa["tentativas"] < MAX_TENTATIVAS:
                print(f"[worker] ERRO em {tarefa['id']}: {erro} "
                      f"(tentativa {tarefa['tentativas']} de {MAX_TENTATIVAS}, "
                      f"voltando para a fila)")
                fila.reenfileirar(tarefa)
            else:
                print(f"[worker] DESCARTE de {tarefa['id']} apos "
                      f"{tarefa['tentativas']} tentativas: {erro}")
                fila.descartar(tarefa, str(erro))
                fila.guardar_resultado(tarefa["id"], {
                    "status": "falhou",
                    "erro": str(erro),
                    "tentativas": tarefa["tentativas"],
                })
        finally:
            registrar_requisicao(
                tarefa["id"], len(tarefa["texto"]), inicio, "worker"
            )


if __name__ == "__main__":
    main()
