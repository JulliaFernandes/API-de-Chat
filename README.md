# API de Chat com IA - Agente de Cálculo Matemático

Uma API simples de chat que conecta a um Agente de IA local com suporte a cálculos matemáticos.

## Pré-requisitos

- Python 3.12 ou superior
- [Ollama](https://ollama.ai) instalado e rodando localmente
- pip ou similar para gerenciar pacotes Python

## Instalação

### 1. Clonar o repositório

```bash
git clone <seu-repo>
cd ProjetoChat
```

### 2. Criar e ativar o ambiente virtual

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

### 3. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Ollama

**Instalar Ollama:**
- Acesse [https://ollama.ai](https://ollama.ai) e siga as instruções para seu sistema operacional.

**Baixar um modelo** (exemplo com `llama2`):
```bash
ollama pull llama2
```

**Iniciar o servidor Ollama:**
```bash
ollama serve
```

Por padrão, Ollama escuta em `http://localhost:11434`. Se usar outra porta/host, atualize no `.env`.

### 5. Configurar variáveis de ambiente

Edite o arquivo `.env` na raiz do projeto:

```dotenv
# Configurações do Ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

```

Se estiver usando um modelo diferente, substitua `llama2` pelo nome do seu modelo.

## Execução

### Iniciar o servidor FastAPI

Com o Ollama rodando em outro terminal, execute:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Ou, para recarregar automaticamente ao editar código (sem --reload se estiver no Windows e tiver problemas):

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Você verá algo como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Acessar a API

**Documentação interativa (Swagger UI):**
```
http://localhost:8000/docs
```

**ReDoc (documentação alternativa):**
```
http://localhost:8000/redoc
```

**Health check:**
```bash
curl http://localhost:8000/
```

Resposta esperada:
```json
{
  "status": "online",
  "message": "API de Chat com IA funcionando!"
```

## Endpoints

### POST `/chat`

Envia uma mensagem e recebe a resposta do agente.

**Request:**
```json
{
  "message": "Quanto é 1234 * 5678?"
}
```

**Response:**
```json
{
  "response": "1234 * 5678 = 7006652. Este é o resultado da multiplicação de 1234 por 5678."
}
```

### Exemplos de uso

**Com curl:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual é a raiz quadrada de 144?"}'
```

**Com Python (requests):**
```python
import requests

url = "http://localhost:8000/chat"
payload = {"message": "Quanto é 2 elevado a 10?"}

response = requests.post(url, json=payload)
print(response.json())
```

## Teste de Funcionalidades

### 1. Cálculos Matemáticos

O agente deve reconhecer e resolver:

```
- "Quanto é 1234 * 5678?"
- "Qual a raiz quadrada de 144?"
- "Quanto é 2 elevado a 10?"
- "Calcule: 3.14 * 100"
- "16 / 4 + 3"
```

### 2. Conversação Geral

O agente deve responder:

```
- "Qual é a capital do Brasil?"
- "Explique o conceito de programação"
- "Qual é a data de hoje?" (responderá com conhecimento geral do modelo)
```

## Estrutura do Projeto

```
ProjetoChat/
├── main.py              # API FastAPI principal
├── agent.py             # Lógica do agente (chamadas a Ollama + cálculos)
├── .env                 # Configurações (não versionar em produção)
├── .gitignore           # Arquivos ignorados por git
├── requirements.txt     # Dependências Python
└── README.md            # Este arquivo
```

### Arquivos Principais

**`main.py`**
- Define os endpoints FastAPI
- Inicializa o agente
- Manipula requisições de chat

**`agent.py`**
- Lógica do agente de IA
- Função `calculator()` para operações matemáticas
- Detecção de perguntas que requerem cálculo
- Integração com Ollama via API HTTP

**`requirements.txt`**
- Dependências do projeto (FastAPI, Uvicorn, etc.)

**`.env`**
- Configurações (URL do Ollama, modelo, etc.)


## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
