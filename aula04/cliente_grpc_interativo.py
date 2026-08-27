import grpc
import servico_pb2, servico_pb2_grpc


print("====== Calculadora =======")
print("- Operação: [Soma]")
item_A = int(input("| Digite o 1° número: ").strip())
item_B = int(input("| Digite o 2° número: ").strip())

with grpc.insecure_channel("127.0.0.1:50051") as canal:
    stub = servico_pb2_grpc.CalculadoraStub(canal)
    resposta = stub.Somar(servico_pb2.Operandos(a=item_A, b=item_B))   # parece local!

    print("-------------------------")
    print(f"Conta: {item_A} + {item_B} =", resposta.valor)