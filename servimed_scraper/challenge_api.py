from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Adicionar caminhos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from servimed_scraper.tasks.challenge_tasks import (
    scrape_products_task,
    process_order_task,
    setup_api_user
)
from celery_app import app as celery_app

app = FastAPI(
    title="Servimed Scraper API - Desafio Cotefácil",
    version="1.0.0",
    description="API para gerenciar scraping e pedidos do Servimed conforme especificação do desafio"
)


# Modelos Pydantic conforme especificação
class ScrapeTaskRequest(BaseModel):
    """Modelo para Nível 2 - Scraping de produtos"""
    usuario: str
    senha: str
    callback_url: str = "https://desafio.cotefacil.net"


class ProductOrder(BaseModel):
    """Produto para pedido"""
    gtin: str
    codigo: str
    quantidade: int


class OrderTaskRequest(BaseModel):
    """Modelo para Nível 3 - Processamento de pedido"""
    usuario: str
    senha: str
    id_pedido: str
    produtos: List[ProductOrder]
    callback_url: str = "https://desafio.cotefacil.net"


class UserSetup(BaseModel):
    """Modelo para criação de usuário"""
    username: str
    password: str


@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "🕷️ Servimed Scraper API - Desafio Cotefácil",
        "version": "1.0.0",
        "levels": {
            "nivel_1": "✅ Scraping básico (implementado)",
            "nivel_2": "⚡ Filas + callback (implementado)",
            "nivel_3": "🛒 Pedidos + confirmação (implementado)"
        },
        "endpoints": {
            "scrape_products": "POST /nivel2/scrape",
            "process_order": "POST /nivel3/order",
            "setup_user": "POST /setup/user",
            "task_status": "GET /task/{task_id}",
            "health": "GET /health"
        }
    }


@app.post("/nivel2/scrape")
async def scrape_products_nivel2(request: ScrapeTaskRequest):
    """
    Nível 2: Enfileirar tarefa de scraping de produtos
    
    Conforme especificação:
    {
        "usuario": "fornecedor_user",
        "senha": "fornecedor_pass",
        "callback_url": "https://desafio.cotefacil.net"
    }
    """
    try:
        print(f"📋 Enfileirando scraping para: {request.usuario}")
        
        # Executar tarefa assíncrona
        task = scrape_products_task.delay(
            usuario=request.usuario,
            senha=request.senha,
            callback_url=request.callback_url
        )
        
        return {
            "message": "✅ Tarefa de scraping enfileirada",
            "task_id": task.id,
            "status": "enqueued",
            "nivel": 2,
            "usuario": request.usuario,
            "callback_url": request.callback_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enfileirar tarefa: {str(e)}")


@app.post("/nivel3/order")
async def process_order_nivel3(request: OrderTaskRequest):
    """
    Nível 3: Enfileirar tarefa de processamento de pedido
    
    Conforme especificação:
    {
        "usuario": "fornecedor_user",
        "senha": "fornecedor_pass",
        "id_pedido": "1234",
        "produtos": [
            {
                "gtin": "1234567890123",
                "codigo": "A123",
                "quantidade": 1
            }
        ],
        "callback_url": "https://desafio.cotefacil.net"
    }
    """
    try:
        print(f"🛒 Enfileirando pedido {request.id_pedido} para: {request.usuario}")
        
        # Converter produtos para dict
        produtos_dict = [p.dict() for p in request.produtos]
        
        # Executar tarefa assíncrona
        task = process_order_task.delay(
            usuario=request.usuario,
            senha=request.senha,
            id_pedido=request.id_pedido,
            produtos=produtos_dict,
            callback_url=request.callback_url
        )
        
        return {
            "message": "✅ Tarefa de pedido enfileirada",
            "task_id": task.id,
            "status": "enqueued",
            "nivel": 3,
            "id_pedido": request.id_pedido,
            "produtos_count": len(request.produtos),
            "callback_url": request.callback_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enfileirar pedido: {str(e)}")


@app.post("/setup/user")
async def setup_user(request: UserSetup):
    """
    Configurar usuário na API Cotefácil
    """
    try:
        print(f"👤 Configurando usuário: {request.username}")
        
        task = setup_api_user.delay(
            username=request.username,
            password=request.password
        )
        
        # Como é configuração, aguardamos o resultado
        result = task.get(timeout=30)
        
        return {
            "message": "Configuração do usuário concluída",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na configuração: {str(e)}")


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Verificar status de uma tarefa
    """
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        response = {
            'task_id': task_id,
            'status': task_result.state,
        }
        
        if task_result.state == 'PENDING':
            response['message'] = 'Tarefa aguardando execução'
        elif task_result.state == 'PROGRESS':
            response['message'] = 'Tarefa em execução'
            response['progress'] = task_result.info
        elif task_result.state == 'SUCCESS':
            response['message'] = 'Tarefa concluída com sucesso'
            response['result'] = task_result.result
        elif task_result.state == 'FAILURE':
            response['message'] = 'Erro na execução da tarefa'
            response['error'] = str(task_result.info)
        else:
            response['message'] = f'Status: {task_result.state}'
            
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Verificar saúde do sistema
    """
    try:
        # Verificar Celery
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        
        return {
            "status": "healthy",
            "celery": "connected",
            "workers": len(active_tasks) if active_tasks else 0,
            "message": "Sistema funcionando normalmente"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Problemas no sistema"
        }


@app.get("/docs-custom")
async def custom_docs():
    """
    Documentação personalizada do desafio
    """
    return {
        "desafio": "Desenvolvedor Python (Web Scraping com Scrapy + Filas + API)",
        "implementacao": {
            "nivel_1": {
                "status": "✅ Completo",
                "funcionalidades": [
                    "Login no Servimed",
                    "Extração de produtos (GTIN, Código, Descrição, Preço, Estoque)",
                    "Uso exclusivo do Scrapy",
                    "Dados em JSON"
                ]
            },
            "nivel_2": {
                "status": "✅ Completo",
                "endpoint": "POST /nivel2/scrape",
                "funcionalidades": [
                    "Sistema de filas (Celery)",
                    "Processamento assíncrono",
                    "Callback para API",
                    "Autenticação OAuth2"
                ]
            },
            "nivel_3": {
                "status": "✅ Completo",
                "endpoint": "POST /nivel3/order",
                "funcionalidades": [
                    "Processamento de pedidos",
                    "Código de confirmação",
                    "PATCH para callback",
                    "Simulação de formulário"
                ]
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🌐 Iniciando API do Desafio Cotefácil...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
