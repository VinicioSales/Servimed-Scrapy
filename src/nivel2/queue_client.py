"""
Cliente para Enfileiramento de Tarefas
======================================

Cliente para adicionar tarefas de scraping na fila do Celery.
"""

import json
from typing import Dict, Optional
from src.nivel2.celery_app import app


class TaskQueueClient:
    """Cliente para gerenciar filas de tarefas"""
    
    def __init__(self):
        self.celery_app = app
    
    def enqueue_scraping_task(
        self, 
        usuario: str, 
        senha: str, 
        callback_url: str = "https://desafio.cotefacil.net",
        filtro: str = "",
        max_pages: Optional[int] = 1,
        framework: str = "original"
    ) -> str:
        """
        Enfileira uma tarefa de scraping
        
        Args:
            usuario: Usuário para autenticação na API de callback
            senha: Senha para autenticação na API de callback
            callback_url: URL da API de callback (sempre do .env)
            filtro: Filtro para produtos (opcional)
            max_pages: Número máximo de páginas (opcional)
            framework: Framework para scraping (original ou scrapy)
            
        Returns:
            str: ID da tarefa
        """
        task_data = {
            "usuario": usuario,
            "senha": senha,
            "callback_url": callback_url,
            "filtro": filtro,
            "max_pages": max_pages,
            "framework": framework
        }
        
        print(f"Enfileirando tarefa ({framework}): {json.dumps(task_data, indent=2)}")
        
        # Envia tarefa para fila (usando fila padrão)
        result = self.celery_app.send_task(
            'src.nivel2.tasks.processar_scraping_simple',
            args=[task_data]
        )
        
        print(f"Tarefa enfileirada com ID: {result.id}")
        return result.id
    
    def get_task_status(self, task_id: str) -> Dict:
        """
        Obtém status de uma tarefa
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            Dict: Status da tarefa
        """
        result = self.celery_app.AsyncResult(task_id)
        
        status_info = {
            'task_id': task_id,
            'status': result.status,
            'ready': result.ready(),
            'successful': result.successful() if result.ready() else None,
            'failed': result.failed() if result.ready() else None,
        }
        
        if result.ready():
            if result.successful():
                status_info['result'] = result.result
            elif result.failed():
                status_info['error'] = str(result.info)
        
        return status_info
    
    def test_queue_connection(self) -> bool:
        """Testa conexão com a fila"""
        try:
            result = self.celery_app.send_task(
                'src.nivel2.tasks.test_connection_task'
            )
            return True
        except Exception as e:
            print(f"Erro ao conectar com fila: {e}")
            return False
    
    def get_worker_status(self) -> Dict:
        """Obtém status dos workers"""
        try:
            inspect = self.celery_app.control.inspect()
            active = inspect.active()
            registered = inspect.registered()
            
            return {
                'workers_active': len(active) if active else 0,
                'active_tasks': active,
                'registered_tasks': registered
            }
        except Exception as e:
            return {'error': str(e)}


# Exemplo de uso
if __name__ == "__main__":
    client = TaskQueueClient()
    
    # Exemplo de tarefa
    task_id = client.enqueue_scraping_task(
        usuario="juliano@farmaprevonline.com.br",
        senha="a007299A",
        callback_url="https://desafio.cotefacil.net",
        filtro="teste",
        max_pages=1
    )
    
    print(f"Tarefa criada: {task_id}")
    
    # Verificar status
    import time
    time.sleep(2)
    status = client.get_task_status(task_id)
    print(f"Status: {json.dumps(status, indent=2)}")
