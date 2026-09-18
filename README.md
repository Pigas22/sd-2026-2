# Serviço de Inferência Distribuído — C1.A2

Sistemas Distribuídos e Computação em Nuvem · FAESA · 2026/2

Serviço que recebe um texto e diz se o sentimento é positivo ou negativo.
O sistema disponibiliza interfaces REST e gRPC e utiliza Redis como fila de tarefas e armazenamento temporário de resultados.

## Arquitetura

```text
Cliente REST ──▶ API REST ──┐
                            ├──▶ Redis ──▶ Worker ──▶ Modelo
Cliente gRPC ──▶ API gRPC ──┘
```

- **REST:** recebe tarefas síncronas e assíncronas.
- **gRPC:** realiza inferência individual ou em lote.
- **Redis:** armazena a fila, resultados e tarefas descartadas.
- **Worker:** processa tarefas assíncronas.
- **Modelo:** classificador de sentimento positivo/negativo.
- **Logs:** cada processo cria um arquivo novo em `logs/` e registra continuamente o id,
  o tamanho da entrada e o tempo de resposta das requisições.

## Requisitos

- Python 3.11+
- Docker e Docker Compose
- Redis
- Dependências listadas em `requirements.txt`

## Instalação

```bash
git clone https://github.com/Pigas22/sd-2026-2-kit-c1a2.git
cd sd-2026-2-kit-c1a2
```

### Criar e Ativar Ambiente Vitural Python

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

## Executando o Redis

```bash
docker compose up -d
```

## Gerando os stubs gRPC

Windows:

```powershell
.\scripts\gerar_stubs.ps1
```

Linux/macOS:

```bash
./scripts/gerar_stubs.sh
```

## Executando os serviços

Abra terminais separados.

### API REST

```bash
uvicorn app.api_rest:app --reload --port 8000
```

### Worker

```bash
python -m app.worker
```

É possível executar vários workers simultaneamente:

```bash
python -m app.worker
```

As tarefas serão distribuídas pela fila Redis.

### Servidor gRPC

```bash
python -m app.servidor_grpc
```

- REST: `http://localhost:8000`
- Documentação: `http://localhost:8000/docs`
- gRPC: porta `50051`

## API REST

### Verificar saúde

```http
GET /saude
```

Resposta:

```json
{
  "status": "ok",
  "modelo_carregado": true
}
```

### Inferência síncrona

```http
POST /predict-sync
Content-Type: application/json
```

Corpo:

```json
{
  "texto": "o atendimento foi excelente"
}
```

### Submeter tarefa assíncrona

```http
POST /predict
Content-Type: application/json
```

Resposta `202 Accepted`:

```json
{
  "id": " identificador-da-tarefa "
}
```

### Consultar resultado

```http
GET /resultado/{id}
```

Enquanto aguarda:

```json
{
  "status": "na_fila"
}
```

Quando concluído:

```json
{
  "texto": "o atendimento foi excelente",
  "sentimento": "positivo",
  "confianca": 0.8123,
  "status": "pronto",
  "tempo_ms": 3.42
}
```

Em caso de falha após três tentativas:

```json
{
  "status": "falhou",
  "erro": "mensagem do erro",
  "tentativas": 3
}
```

## API gRPC

O contrato está em:

```text
proto/inferencia.proto
```

Métodos disponíveis:

- `Prever`: classifica um texto.
- `PreverLote`: classifica vários textos em uma chamada.

Cliente de exemplo:

```bash
python -m exemplos.cliente_grpc
```

## Tratamento de erros

- Texto vazio no REST: HTTP `400`.
- Texto vazio no gRPC: `INVALID_ARGUMENT`.
- Tarefas assíncronas são tentadas até três vezes.
- Após três falhas, a tarefa é enviada para `tarefas:descarte`.
- Resultados são armazenados no Redis.

## Estrutura principal

```text
app/
├── api_rest.py
├── fila.py
├── modelo.py
├── servidor_grpc.py
└── worker.py

proto/
└── inferencia.proto

exemplos/
├── cliente_rest.py
└── cliente_grpc.py
```

## Teste rápido

```bash
python exemplos/cliente_rest.py "o atendimento foi ótimo"
python -m exemplos.cliente_grpc
```

## Autores

- Davi Tâmbara Rodrigues
- Thiago Holz
- Samuel Eduardo Rocha de Souza
