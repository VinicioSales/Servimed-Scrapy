"""
SPIDER PRINCIPAL - SERVIMED
===========================

Spider Scrapy para coleta de produtos do portal Servimed.
"""

import scrapy
import json
import os
import time
from urllib.parse import urlencode
from ..items import ProdutoItem
from dotenv import load_dotenv

load_dotenv()


class ServimedProductsSpider(scrapy.Spider):
    name = 'servimed_products'
    allowed_domains = ['peapi.servimed.com.br']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }
    
    def __init__(self, filtro='', max_pages=1, callback_url='', *args, **kwargs):
        super(ServimedProductsSpider, self).__init__(*args, **kwargs)
        
        # Parâmetros
        self.filtro = filtro
        self.max_pages = int(max_pages)
        self.callback_url = callback_url
        
        # Configurações da API
        self.base_url = os.getenv('BASE_URL', 'https://peapi.servimed.com.br')
        self.api_endpoint = '/api/carrinho/oculto'
        
        # Contadores
        self.current_page = 1
        self.total_products = 0
        
        self.logger.info(f'Spider inicializado: filtro="{filtro}", max_pages={max_pages}')
    
    def start_requests(self):
        """Gera requisições iniciais"""
        
        # URL da API de produtos
        url = f"{self.base_url}{self.api_endpoint}"
        
        # Parâmetros da primeira página
        params = {
            'page': 1,
            'search': self.filtro,
            'limit': 50  # Produtos por página
        }
        
        # URL completa
        full_url = f"{url}?{urlencode(params)}"
        
        self.logger.info(f'Iniciando scraping: {full_url}')
        
        yield scrapy.Request(
            url=full_url,
            callback=self.parse_products,
            meta={'page': 1}
        )
    
    def parse_products(self, response):
        """Parse da resposta de produtos"""
        
        page = response.meta['page']
        self.logger.info(f'Processando página {page}, status: {response.status}')
        
        try:
            # Parse do JSON
            data = json.loads(response.text)
            
            # Extrair produtos
            produtos = data.get('data', [])
            total_found = len(produtos)
            
            self.logger.info(f'Página {page}: {total_found} produtos encontrados')
            
            if not produtos:
                self.logger.info('Nenhum produto encontrado, finalizando')
                return
            
            # Processar cada produto
            for produto in produtos:
                item = self.extract_product_data(produto)
                if item:
                    yield item
                    self.total_products += 1
            
            # Verificar se deve continuar para próxima página
            if page < self.max_pages and total_found > 0:
                next_page = page + 1
                
                # Parâmetros da próxima página
                params = {
                    'page': next_page,
                    'search': self.filtro,
                    'limit': 50
                }
                
                next_url = f"{self.base_url}{self.api_endpoint}?{urlencode(params)}"
                
                self.logger.info(f'Requisitando página {next_page}')
                
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_products,
                    meta={'page': next_page}
                )
        
        except json.JSONDecodeError as e:
            self.logger.error(f'Erro ao decodificar JSON da página {page}: {e}')
        except Exception as e:
            self.logger.error(f'Erro no parse da página {page}: {e}')
    
    def extract_product_data(self, produto_data):
        """Extrai dados do produto do JSON"""
        
        try:
            # Criar item
            item = ProdutoItem()
            
            # Mapear campos
            item['gtin'] = produto_data.get('gtin', '')
            item['codigo'] = produto_data.get('codigo', '')
            item['descricao'] = produto_data.get('descricao', '')
            
            # Preço (pode ser string ou float)
            preco_raw = produto_data.get('preco_fabrica', 0)
            try:
                item['preco_fabrica'] = float(preco_raw) if preco_raw else 0.0
            except (ValueError, TypeError):
                item['preco_fabrica'] = 0.0
            
            # Estoque (pode ser string ou int)
            estoque_raw = produto_data.get('estoque', 0)
            try:
                item['estoque'] = int(estoque_raw) if estoque_raw else 0
            except (ValueError, TypeError):
                item['estoque'] = 0
            
            # Metadados
            item['url'] = self.base_url
            item['timestamp'] = time.time()
            item['usuario'] = os.getenv('LOGGED_USER', '')
            
            # Log do produto extraído
            self.logger.debug(f'Produto extraído: {item["codigo"]} - {item["descricao"][:50]}...')
            
            return item
            
        except Exception as e:
            self.logger.error(f'Erro ao extrair produto: {e}')
            return None
    
    def closed(self, reason):
        """Callback quando spider fecha"""
        self.logger.info(f'Spider finalizado: {reason}')
        self.logger.info(f'Total de produtos coletados: {self.total_products}')
        
        # Estatísticas finais
        stats = {
            'total_products': self.total_products,
            'pages_processed': self.current_page,
            'filter_used': self.filtro,
            'reason': reason
        }
        
        self.logger.info(f'Estatísticas finais: {stats}')
