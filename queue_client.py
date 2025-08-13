"""
Cliente Simplificado para Testes do Nível 2
"""

import os
import sys
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from celery import Celery

# Configuração Redis
import os
import json
import time
from celery import Celery
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configurações
REDIS_URL = "redis://localhost:6379/0"

# Criar app Celery
app = Celery(
    'servimed_scraper_simple',
    broker=REDIS_URL,
    backend=REDIS_URL
)


def enqueue_scraping(filtro="", max_pages=1):
    """Enfileira tarefa de scraping"""
    
    # Obter credenciais do .env
    usuario = os.getenv('CALLBACK_API_USER')
    senha = os.getenv('CALLBACK_API_PASSWORD')
    callback_url = os.getenv('CALLBACK_URL', 'https://desafio.cotefacil.net')
    
    if not usuario or not senha:
        print("Credenciais não encontradas no .env")
        print("Configure CALLBACK_API_USER e CALLBACK_API_PASSWORD")
        return None
    
    task_data = {
        "usuario": usuario,
        "senha": senha, 
        "callback_url": callback_url,
        "filtro": filtro,
        "max_pages": max_pages
    }
    
    result = app.send_task('src.nivel2.tasks.processar_scraping_simple', args=[task_data])
    return result.id


def get_status(task_id):
    """Verifica status de uma tarefa"""
    result = app.AsyncResult(task_id)
    return {
        'task_id': task_id,
        'status': result.status,
        'ready': result.ready(),
        'result': result.result if result.ready() and result.successful() else None,
        'error': str(result.info) if result.ready() and result.failed() else None
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python queue_client.py enqueue <filtro> [max_pages]")
        print("  python queue_client.py status <task_id>")
        print()
        print("Exemplos:")
        print("  python queue_client.py enqueue hidratante 1")
        print("  python queue_client.py status abc123-def456")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "enqueue":
        filtro = sys.argv[2] if len(sys.argv) > 2 else ""
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        
        task_id = enqueue_scraping(filtro, max_pages)
        print(f"Task criada: {task_id}")
        
    elif command == "status":
        if len(sys.argv) < 3:
            print("Erro: Task ID necessario")
            sys.exit(1)
        
        task_id = sys.argv[2]
        status = get_status(task_id)
        
        import json
        print(json.dumps(status, indent=2))
    
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)
