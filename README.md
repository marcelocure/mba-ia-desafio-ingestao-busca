# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de ingestão e busca semântica com LangChain, PostgreSQL e pgVector.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Chave de API da OpenAI **ou** Google (Gemini)
- Arquivo `document.pdf` na raiz do projeto

## Configuração

1. Copie o template de variáveis de ambiente:

```bash
cp .env.example .env
```

1. Edite o `.env` e configure sua chave de API:

```bash
# OpenAI (prioridade se ambas estiverem definidas)
OPENAI_API_KEY=sua-chave-aqui

# ou Gemini
GOOGLE_API_KEY=sua-chave-aqui
```

1. Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

1. Suba o banco de dados:

```bash
docker compose up -d
```

## Execução

### 1. Ingestão do PDF

```bash
python src/ingest.py
```

O script lê o PDF, divide em chunks de 1000 caracteres (overlap de 150), gera embeddings e armazena no PostgreSQL.

### 2. Chat via CLI

```bash
python src/chat.py
```

Exemplo de interação:

```
Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Pressione Enter em uma pergunta vazia ou use `Ctrl+C` para encerrar.

## Modelos utilizados


| Provedor | Embeddings             | LLM                   |
| -------- | ---------------------- | --------------------- |
| OpenAI   | text-embedding-3-small | gpt-5-nano            |
| Gemini   | models/embedding-001   | gemini-2.5-flash-lite |


