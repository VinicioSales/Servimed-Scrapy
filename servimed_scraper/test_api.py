from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Adicionar caminhos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from test_tasks import simple_scrape_task, health_check
from celery_app import app as celery_app

app = FastAPI(title="Servimed Scraper API - Teste", version="1.0.0")


class ScrapeRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "🕷️ Servimed Scraper API - Modo Teste",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "scrape": "POST /scrape",
            "health": "GET /health",
            "test": "GET /test"
        }
    }


@app.post("/scrape")
async def start_scraping(request: ScrapeRequest):
    """
    Iniciar tarefa de scraping
    """
    try:
        print(f"🚀 Recebida solicitação de scraping...")
        
        # Executar tarefa
        task = simple_scrape_task.delay(
            username=request.username,
            password=request.password
        )
        
        # Como está em modo eager, já temos o resultado
        result = task.get()
        
        return {
            "task_id": task.id,
            "status": "completed",
            "result": result,
            "message": "Tarefa executada com sucesso!"
        }
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


@app.get("/health")
async def health_check_endpoint():
    """
    Verificar saúde do sistema
    """
    try:
        print("🏥 Verificando saúde do sistema...")
        
        # Executar verificação
        task = health_check.delay()
        result = task.get()
        
        return result
        
    except Exception as e:
        print(f"❌ Erro na verificação: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
async def test_endpoint():
    """
    Endpoint de teste simples
    """
    return {
        "message": "🧪 Sistema funcionando!",
        "celery_configured": True,
        "api_working": True
    }


if __name__ == "__main__":
    import uvicorn
    print("🌐 Iniciando API de teste...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
