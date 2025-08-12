import os
import sys
import json
from celery import current_app
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ..spiders.servimed_spider import ServimedSpider
from ..clients.cotefacil_client import CotefacilApiClient

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Importar a aplicação Celery
from celery_app import app


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def scrape_servimed_task(self, username=None, password=None):
    """
    Tarefa Celery para executar o spider do Servimed
    """
    try:
        # Configurar o processo do Scrapy
        settings = get_project_settings()
        settings.set('LOG_LEVEL', 'INFO')
        
        # Criar processo do crawler
        process = CrawlerProcess(settings)
        
        # Lista para armazenar os produtos coletados
        collected_items = []
        
        def collect_item(item, response, spider):
            collected_items.append(dict(item))
        
        # Conectar o sinal para coletar itens
        from scrapy import signals
        from pydispatch import dispatcher
        dispatcher.connect(collect_item, signal=signals.item_scraped)
        
        # Executar o spider
        process.crawl(ServimedSpider, username=username, password=password)
        process.start()
        
        # Processar produtos coletados em outra tarefa
        if collected_items:
            process_products_task.delay(collected_items)
        
        return {
            'status': 'success',
            'products_found': len(collected_items),
            'message': f'Scraping concluído. {len(collected_items)} produtos encontrados.'
        }
        
    except Exception as e:
        # Log do erro
        print(f"Erro na tarefa de scraping: {str(e)}")
        
        # Re-raise para trigger do retry automático
        raise self.retry(exc=e)


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'countdown': 30})
def process_products_task(self, products):
    """
    Tarefa para processar produtos coletados
    """
    try:
        processed_products = []
        
        for product in products:
            # Validar e enriquecer dados do produto
            processed_product = {
                'gtin': product.get('gtin'),
                'codigo': product.get('codigo'),
                'descricao': product.get('descricao'),
                'preco_fabrica': product.get('preco_fabrica'),
                'estoque': product.get('estoque'),
                'processed_at': self.request.id,
                'status': 'processed'
            }
            
            # Adicionar validações específicas
            if processed_product['gtin'] and processed_product['codigo']:
                processed_products.append(processed_product)
        
        # Enviar produtos processados para API (se necessário)
        if processed_products:
            send_to_api_task.delay(processed_products)
        
        return {
            'status': 'success',
            'processed_count': len(processed_products),
            'message': f'{len(processed_products)} produtos processados com sucesso.'
        }
        
    except Exception as e:
        print(f"Erro no processamento de produtos: {str(e)}")
        raise self.retry(exc=e)


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 120})
def send_to_api_task(self, products):
    """
    Tarefa para enviar produtos para API externa
    """
    try:
        # Aqui você implementaria o envio para API externa
        # Por exemplo, callback para o sistema que solicitou o scraping
        
        api_response = {
            'products_sent': len(products),
            'timestamp': self.request.id,
            'status': 'sent'
        }
        
        # Simulação de envio para API
        print(f"Enviando {len(products)} produtos para API externa...")
        
        return {
            'status': 'success',
            'products_sent': len(products),
            'message': f'{len(products)} produtos enviados para API externa.'
        }
        
    except Exception as e:
        print(f"Erro no envio para API: {str(e)}")
        raise self.retry(exc=e)


@app.task
def health_check():
    """
    Tarefa para verificar saúde do sistema
    """
    from datetime import datetime
    
    try:
        # Verificar conectividade com APIs
        client = CotefacilApiClient()
        api_status = client.authenticate()
        
        return {
            'status': 'healthy',
            'cotefacil_api': 'connected' if api_status else 'disconnected',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
