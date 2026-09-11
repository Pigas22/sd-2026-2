"""Cliente gRPC de exemplo.

  python -m app.servidor_grpc        # um terminal
  python -m exemplos.cliente_grpc    # outro
"""
import sys

import grpc

import inferencia_pb2
import inferencia_pb2_grpc

TEXTOS = sys.argv[1:] or [
    "o atendimento foi excelente",
    "produto quebrou no primeiro dia",
    "entrega pontual e embalagem perfeita",
]

with grpc.insecure_channel("localhost:50051") as canal:
    stub = inferencia_pb2_grpc.InferenciaStub(canal)

    r = stub.Prever(inferencia_pb2.PedidoPrever(texto=TEXTOS[0]))
    print("Prever:", r.sentimento, r.confianca, "|", r.texto)

    lote = stub.PreverLote(inferencia_pb2.PedidoLote(textos=TEXTOS))
    for r in lote.resultados:
        print("PreverLote:", r.sentimento, r.confianca, "|", r.texto)

    try:
        stub.PreverLote(inferencia_pb2.PedidoLote(textos=[]))
    except grpc.RpcError as e:
        print("lote vazio:", e.code().name, "-", e.details())
