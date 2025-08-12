import os
import sys
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

from celery_app import app
from servimed_scraper.clients.cotefacil_client import CotefacilApiClient


@app.task(bind=True)
def simple_scrape_task(self, username=None, password=None):
    """
    Tarefa simplificada para testar o sistema
    """
    try:
        print(f"🚀 Iniciando tarefa de scraping...")
        print(f"📧 Username: {username or 'usando .env'}")
        
        # Simular execução do spider (versão simplificada)
        from servimed_scraper.clients.cotefacil_client import CotefacilApiClient
        
        # Testar conexão com API
        print("🔌 Testando conexão com API Cotefácil...")
        client = CotefacilApiClient()
        
        if client.authenticate():
            print("✅ Autenticação bem-sucedida!")
            products = client.get_products()
            print(f"📦 Produtos encontrados: {len(products)}")
        else:
            print("❌ Falha na autenticação")
            products = []
        
        # Simular processamento
        result = {
            'status': 'success',
            'task_id': str(self.request.id),
            'products_found': len(products),
            'timestamp': datetime.now().isoformat(),
            'message': f'Scraping concluído! {len(products)} produtos encontrados.'
        }
        
        print(f"✅ Tarefa concluída: {result}")
        return result
        
    except Exception as e:
        error_msg = f"❌ Erro na tarefa: {str(e)}"
        print(error_msg)
        return {
            'status': 'error',
            'task_id': str(self.request.id),
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


@app.task
def health_check():
    """
    Verificação de saúde do sistema
    """
    try:
        print("🏥 Executando verificação de saúde...")
        
        # Testar API
        client = CotefacilApiClient()
        api_status = client.authenticate()
        
        result = {
            'status': 'healthy',
            'cotefacil_api': 'connected' if api_status else 'disconnected',
            'celery': 'working',
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Sistema saudável: {result}")
        return result
        
    except Exception as e:
        error_result = {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        print(f"❌ Sistema com problemas: {error_result}")
        return error_result
