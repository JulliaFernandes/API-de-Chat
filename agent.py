from strands import Agent
from strands.tools import tool
from strands.models.ollama import OllamaModel
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@tool
def calculator(expression: str) -> str:
    """
    Calcula expressões matemáticas.
    
    Args:
        expression: Expressão matemática em formato Python
        
    Returns:
        Resultado do cálculo
    """
    try:
        logger.info(f"Calculator chamado com: {expression}")
        import math
        
        # Dicionário com funções matemáticas seguras
        safe_dict = {
            "sqrt": math.sqrt,
            "pow": math.pow,
            "abs": abs,
            "round": round,
            "max": max,
            "min": min,
        }
        
        # Calcula a expressão de forma segura
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        
        # Formatar resultado
        if isinstance(result, float):
            result_str = f"{result:.10f}".rstrip('0').rstrip('.')
        else:
            result_str = str(result)
        
        logger.info(f"Resultado calculado: {result_str}")
        return f"O resultado é {result_str}"
        
    except Exception as e:
        logger.error(f"Erro no calculator: {str(e)}")
        return f"Erro ao calcular: {str(e)}"


def create_agent():
    """Cria e configura o agente de IA"""
    
    model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    logger.info(f"Criando agente com modelo: {model_name}")
    logger.info(f"Ollama host: {ollama_host}")
    
    # Criar modelo Ollama
    ollama_model = OllamaModel(
        host=ollama_host,
        model_id=model_name
    )
    
    logger.info("Modelo Ollama criado")
    
    # Criar agente
    agent = Agent(
        model=ollama_model,
        system_prompt="""Você é um assistente útil que pode responder perguntas gerais e realizar cálculos matemáticos.

IMPORTANTE: Use a ferramenta calculator SOMENTE quando houver uma operação matemática para calcular.

QUANDO USAR A FERRAMENTA:
- "Quanto é 5 + 3?" → USE calculator
- "Qual a raiz quadrada de 144?" → USE calculator
- "Quanto é 1234 * 5678?" → USE calculator
- "Calcule 2 elevado a 10" → USE calculator

QUANDO NÃO USAR A FERRAMENTA:
- "Quais são as cores do arco-íris?" → NÃO USE calculator, responda diretamente
- "O que é inteligência artificial?" → NÃO USE calculator, responda diretamente
- "Olá, como você está?" → NÃO USE calculator, responda diretamente
- "Quem foi Albert Einstein?" → NÃO USE calculator, responda diretamente

Para perguntas que NÃO envolvem cálculos matemáticos, responda normalmente usando seu conhecimento.""",
        tools=[calculator],
    )
    
    logger.info("Agente criado com sucesso!")
    return agent