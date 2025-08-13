#!/usr/bin/env python3
"""
SPIDER SCRAPY SIMPLIFICADO - SERVIMED
======================================

Spider Scrapy que coleta dados via requests (nível 1) e processa via Scrapy.
"""

import scrapy
import requests
import json
import os
import warnings
from dotenv import load_dotenv
from urllib.parse import urlencode

# Suprimir avisos SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
try:
    import urllib3
    urllib3.disable_warnings()
except:
    pass

load_dotenv()


class ServimedSimpleSpider(scrapy.Spider):
    """Spider simplificado que usa requests para coletar e Scrapy para processar"""
    
    name = 'servimed_simple'
    
    def __init__(self, filtro='', max_pages=1, callback_url='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filtro = filtro
        self.max_pages = int(max_pages)
        self.callback_url = callback_url
        self.produtos_coletados = []
        
        self.logger.info(f"Spider inicializado: filtro=\"{filtro}\", max_pages={max_pages}")
    
    def start_requests(self):
        """Inicia com uma única requisição dummy"""
        return [scrapy.Request('http://httpbin.org/get', callback=self.collect_via_requests)]
    
    def collect_via_requests(self, response):
        """Coleta dados via requests (como no nível 1)"""
        
        try:
            self.logger.info("🔄 Coletando dados via requests...")
            
            # Headers para autenticação
            headers = {
                'accesstoken': os.getenv('ACCESS_TOKEN'),
                'loggeduser': os.getenv('LOGGED_USER'),
                'x-cart': os.getenv('X_CART'),
                'x-peperone': str(int(__import__('time').time() * 1000)),
                'contenttype': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://pedidoeletronico.servimed.com.br',
                'Referer': 'https://pedidoeletronico.servimed.com.br/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Coleta por página
            for page in range(1, self.max_pages + 1):
                params = {
                    'page': page,
                    'limit': 50
                }
                
                if self.filtro:
                    params['search'] = self.filtro
                
                url = f"https://peapi.servimed.com.br/api/carrinho/oculto?{urlencode(params)}"
                
                self.logger.info(f"📄 Página {page}: {url}")
                
                # Requisição via requests
                resp = requests.get(url, headers=headers, timeout=30, verify=False)
                
                if resp.status_code == 200:
                    data = resp.json()
                    products = data.get('data', {}).get('products', [])
                    
                    self.logger.info(f"✅ Página {page}: {len(products)} produtos")
                    
                    # Processa cada produto via Scrapy
                    for product in products:
                        yield self.create_scrapy_item(product)
                        
                else:
                    self.logger.error(f"❌ Erro na página {page}: {resp.status_code}")
                    break
            
        except Exception as e:
            self.logger.error(f"❌ Erro na coleta: {e}")
    
    def create_scrapy_item(self, product_data):
        """Cria item Scrapy a partir dos dados do produto"""
        
        # Retorna dicionário simples (será convertido para item no pipeline)
        item = {
            'codigo': product_data.get('codigo', ''),
            'descricao': product_data.get('descricao', ''),
            'preco_fabrica': float(product_data.get('preco_fabrica', 0)),
            'estoque': int(product_data.get('estoque', 0)),
            'gtin': product_data.get('gtin', ''),
            'disponivel': product_data.get('disponivel', True),
            'fonte': 'scrapy_simple',
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        
        return item
    
    def closed(self, reason):
        """Executado quando spider finaliza"""
        self.logger.info(f"Spider finalizado: {reason}")
        
        # Estatísticas básicas
        try:
            stats = getattr(self.crawler, 'stats', None)
            if stats:
                total_items = stats.get_value('item_scraped_count', 0)
            else:
                total_items = 0
        except:
            total_items = 0
        
        self.logger.info(f"Total de produtos coletados: {total_items}")
        self.logger.info(f"Estatísticas finais: {{'total_products': {total_items}, 'pages_processed': {self.max_pages}, 'filter_used': '{self.filtro}', 'reason': '{reason}'}}")
