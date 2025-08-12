from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from servimed_scraper.tasks.scraping_tasks import (
    scrape_servimed_task,
    process_products_task,
    health_check
)
from celery_app import app as celery_app

app = FastAPI(title="Servimed Scraper API", version="1.0.0")


class ScrapeRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Servimed Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "scrape": "/scrape",
            "task_status": "/task/{task_id}",
            "health": "/health"
        }
    }


@app.post("/scrape", response_model=TaskResponse)
async def start_scraping(request: ScrapeRequest):
    """
    Iniciar tarefa de scraping do Servimed
    """
    try:
        # Executar tarefa assíncrona
        task = scrape_servimed_task.delay(
            username=request.username,
            password=request.password
        )
        
        return TaskResponse(
            task_id=task.id,
            status="started",
            message="Tarefa de scraping iniciada com sucesso"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar scraping: {str(e)}")


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Verificar status de uma tarefa
    """
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            response = {
                'task_id': task_id,
                'status': 'PENDING',
                'message': 'Tarefa aguardando execução'
            }
        elif task_result.state == 'PROGRESS':
            response = {
                'task_id': task_id,
                'status': 'PROGRESS',
                'message': 'Tarefa em execução',
                'progress': task_result.info
            }
        elif task_result.state == 'SUCCESS':
            response = {
                'task_id': task_id,
                'status': 'SUCCESS',
                'message': 'Tarefa concluída com sucesso',
                'result': task_result.result
            }
        else:
            response = {
                'task_id': task_id,
                'status': task_result.state,
                'message': 'Erro na execução da tarefa',
                'error': str(task_result.info)
            }
            
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status: {str(e)}")


@app.get("/health")
async def health_check_endpoint():
    """
    Verificar saúde do sistema
    """
    try:
        # Executar verificação de saúde
        task = health_check.delay()
        result = task.get(timeout=10)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na verificação de saúde: {str(e)}")


@app.get("/tasks/active")
async def get_active_tasks():
    """
    Listar tarefas ativas
    """
    try:
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        
        return {
            'active_tasks': active_tasks,
            'total_workers': len(active_tasks) if active_tasks else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar tarefas: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
