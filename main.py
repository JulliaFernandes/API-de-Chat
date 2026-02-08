from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import create_agent
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis do arquivo .env
load_dotenv()

# Criar a aplicação FastAPI
app = FastAPI(
    title="API de Chat com IA",
    description="API que conecta a um Agente de IA com ferramentas de cálculo",
    version="1.0.0"
)

# Definir os modelos de dados
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Inicializar o agente quando o servidor inicia
logger.info("Inicializando agente...")
agent = create_agent()
logger.info("Agente inicializado com sucesso!")

@app.get("/")
async def root():
    """Endpoint para verificar se a API está funcionando"""
    return {
        "status": "online",
        "message": "API de Chat com IA funcionando!"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de chat
    Recebe uma mensagem e retorna a resposta do agente
    """
    try:
        logger.info(f"Recebida mensagem: {request.message}")
        
        # Envia a mensagem para o agente processar
        logger.info("Chamando agente...")
        result = agent(request.message)
        
        # Converter AgentResult para string
        response_text = str(result)
        
        logger.info(f"Resposta recebida: {response_text[:100] if len(response_text) > 100 else response_text}")
        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Erro ao processar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))