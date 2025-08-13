"""
Tarefas Celery Simplificadas - Versão Windows
==============================================

Versão otimizada para funcionamento no Windows com pool=solo
"""

import os
import sys
import json
import time
from pathlib import Path

# Configurar path de forma mais robusta
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent
src_dir = project_root / "src"

# Adicionar ao path se não estiver
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.nivel2.celery_app import app


@app.task(bind=True)
def test_connection_task_simple(self):
    """Tarefa de teste simples"""
    try:
        return {
            'status': 'success',
            'message': 'Worker funcionando',
            'task_id': self.request.id,
            'timestamp': time.time()
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'task_id': self.request.id
        }


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'countdown': 30})
def processar_scraping_simple(self, task_data):
    """
    Versão simplificada da tarefa de scraping com suporte a Scrapy
    """
    try:
        task_id = self.request.id
        print(f"[{task_id}] Iniciando processamento...")
        
        # Extrair dados da tarefa
        framework = "scrapy"  # Sempre usar Scrapy
        usuario = task_data.get('usuario')
        senha = task_data.get('senha')
        callback_url = task_data.get('callback_url', 'https://desafio.cotefacil.net')
        filtro = task_data.get('filtro', '')
        max_pages = task_data.get('max_pages', 1)
        
        print(f"[{task_id}] Configurações: framework='scrapy', filtro='{filtro}', max_pages={max_pages}")
        
        # 1. Executar scraping sempre com Scrapy
        print(f"[{task_id}] Iniciando scraping via Scrapy...")
        
        # Importar Scrapy wrapper
        try:
            from scrapy_wrapper import ScrapyServimedWrapper
            
            wrapper = ScrapyServimedWrapper()
            resultado_scrapy = wrapper.run_spider(filtro=filtro, max_pages=max_pages)
            
            if resultado_scrapy:
                results = wrapper.get_results()
                if results['success']:
                    produtos_coletados = results['total']
                    arquivo_produtos = 'data/servimed_produtos_scrapy.json'
                    print(f"[{task_id}] Scrapy concluído: {produtos_coletados} produtos")
                    framework = 'scrapy'
                else:
                    raise Exception(f"Erro no Scrapy: {results.get('error')}")
            else:
                raise Exception("Falha na execução do Scrapy")
                
        except Exception as e_scrapy:
            print(f"[{task_id}] ERRO no Scrapy: {e_scrapy}")
            print(f"[{task_id}] Fallback para sistema original...")
            
            # Fallback para sistema original
            from servimed_scraper.scraper import ServimedScraperCompleto
            
            scraper = ServimedScraperCompleto()
            resultado_scraping = scraper.run(filtro=filtro, max_pages=max_pages)
            
            produtos_coletados = resultado_scraping['total_produtos']
            arquivo_produtos = resultado_scraping['arquivo_salvo']
            framework = 'original'
            print(f"[{task_id}] Sistema original concluído: {produtos_coletados} produtos")
        
        # 2. Enviar para API de callback
        print(f"[{task_id}] Enviando para API de callback...")
        
        from api_client.callback_client import CallbackAPIClient
        api_client = CallbackAPIClient(base_url=callback_url)
        
        # Autenticar usando OAuth2 password flow
        print(f"[{task_id}] Realizando autenticação OAuth2...")
        auth_success = api_client.authenticate()
        
        if not auth_success:
            print(f"[{task_id}] ERRO: Falha na autenticação OAuth2!")
            return {
                'status': 'error',
                'task_id': task_id,
                'error': 'Falha na autenticação OAuth2 com a API',
                'framework': framework,
                'timestamp': time.time()
            }
        
        # Enviar produtos
        print(f"[{task_id}] Enviando produtos para API...")
        
        # Ler arquivo de produtos gerado
        arquivo_produtos = resultado_scraping['arquivo_salvo']
        with open(arquivo_produtos, 'r', encoding='utf-8') as f:
            dados_completos = json.load(f)
        
        # Extrair apenas a lista de produtos
        produtos = dados_completos.get('produtos', [])
        print(f"[{task_id}] Produtos extraídos para envio: {len(produtos)}")
        
        api_response = api_client.send_products(produtos)
        print(f"[{task_id}] Resposta da API: {api_response}")
        
        resultado_final = {
            'status': 'success',
            'task_id': task_id,
            'produtos_coletados': produtos_coletados,
            'tempo_scraping': resultado_scraping['tempo_execucao'],
            'arquivo_local': arquivo_produtos,
            'api_response': api_response,
            'callback_url': callback_url,
            'filtro_usado': filtro,
            'timestamp': time.time()
        }
        
        print(f"[{task_id}] Tarefa concluída com sucesso!")
        return resultado_final
        
    except Exception as e:
        error_msg = f"Erro na tarefa {self.request.id}: {str(e)}"
        print(f"[ERROR] {error_msg}")
        
        # Log do erro para debug
        import traceback
        traceback.print_exc()
        
        return {
            'status': 'error',
            'task_id': self.request.id,
            'error': error_msg,
            'timestamp': time.time()
        }


@app.task(bind=True)
def status_task_simple(self, message="Status check"):
    """Tarefa simples de status"""
    return {
        'status': 'active',
        'message': message,
        'task_id': self.request.id,
        'worker_info': {
            'pid': os.getpid(),
            'cwd': str(Path.cwd()),
            'python_path': sys.path[:3]  # Primeiros 3 itens do path
        }
    }


# Registrar tarefas no app
app.tasks.register(test_connection_task_simple)
app.tasks.register(processar_scraping_simple)
app.tasks.register(status_task_simple)

print("Tarefas simplificadas registradas com sucesso!")
