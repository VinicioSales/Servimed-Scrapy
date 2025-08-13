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
        """Gera requisições iniciais - vai direto para produtos (pula ObterVencimentos que dá 500)"""
        
        # Ir direto para requisição de produtos
        url = f"{self.base_url}{self.api_endpoint}"
        full_url = f"{url}?siteVersion=4.0.27"
        
        # Payload POST exato conforme capturado do DevTools
        payload = {
            "filtro": self.filtro,
            "pagina": 1,
            "registrosPorPagina": 25,
            "ordenarDecrescente": False,
            "colunaOrdenacao": "nenhuma",
            "clienteId": 267511,
            "tipoVendaId": 1,
            "fabricanteIdFiltro": 0,
            "pIIdFiltro": 0,
            "cestaPPFiltro": False,
            "codigoExterno": 0,
            "codigoUsuario": 22850,
            "promocaoSelecionada": "",
            "indicadorTipoUsuario": "CLI",
            "kindUser": 0,
            "xlsx": [],
            "principioAtivo": "",
            "master": False,
            "kindSeller": 0,
            "grupoEconomico": "",
            "users": [
                518565,
                267511
            ],
            "list": True
        }
        
        self.logger.info(f'Iniciando scraping direto: {full_url}')
        self.logger.info(f'Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}')
        
        yield scrapy.Request(
            url=full_url,
            method='POST',
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            callback=self.parse_products,
            errback=self.handle_error,
            meta={'handle_httpstatus_list': [403, 500], 'page': 1}
        )
    
    def after_vencimentos(self, response):
        """Callback após ObterVencimentos - agora faz requisição de produtos"""
        
        self.logger.info(f'ObterVencimentos concluído, status: {response.status}')
        
        # Agora faz a requisição de produtos
        url = f"{self.base_url}{self.api_endpoint}"
        full_url = f"{url}?siteVersion=4.0.27"
        
        # Payload POST exato conforme capturado do DevTools
        payload = {
            "filtro": self.filtro,
            "pagina": 1,
            "registrosPorPagina": 25,
            "ordenarDecrescente": False,
            "colunaOrdenacao": "nenhuma",
            "clienteId": 267511,
            "tipoVendaId": 1,
            "fabricanteIdFiltro": 0,
            "pIIdFiltro": 0,
            "cestaPPFiltro": False,
            "codigoExterno": 0,
            "codigoUsuario": 22850,
            "promocaoSelecionada": "",
            "indicadorTipoUsuario": "CLI",
            "kindUser": 0,
            "xlsx": [],
            "principioAtivo": "",
            "master": False,
            "kindSeller": 0,
            "grupoEconomico": "",
            "users": [
                518565,
                267511
            ],
            "list": True
        }
        
        self.logger.info(f'Iniciando scraping POST: {full_url}')
        self.logger.info(f'Payload: {json.dumps(payload, indent=2)}')
        
        yield scrapy.Request(
            url=full_url,
            method='POST',
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            callback=self.parse_products,
            errback=self.handle_error,
            meta={'page': 1, 'handle_httpstatus_list': [403]}
        )
    
    def parse_products(self, response):
        """Parse da resposta de produtos"""
        
        page = response.meta['page']
        self.logger.info(f'Processando página {page}, status: {response.status}')
        
        # Handle 403 responses
        if response.status == 403:
            self.logger.error(f'HTTP 403 Forbidden na página {page}')
            self.logger.error(f'Response headers: {dict(response.headers)}')
            self.logger.error(f'Response body: {response.text[:500]}...')
            return
        
        try:
            # Parse do JSON
            data = json.loads(response.text)
            
            # Extrair produtos - estrutura correta conforme DevTools
            produtos = data.get('lista', [])
            total_registros = data.get('totalRegistros', 0)
            registros_por_pagina = data.get('registrosPorPagina', 25)
            
            self.logger.info(f'Página {page}: {len(produtos)} produtos encontrados de {total_registros} total')
            
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
            if page < self.max_pages and len(produtos) == registros_por_pagina and self.total_products < total_registros:
                next_page = page + 1
                
                # URL da próxima página - POST conforme DevTools
                next_url = f"{self.base_url}{self.api_endpoint}?siteVersion=4.0.27"
                
                # Payload POST exato conforme capturado do DevTools - próxima página
                payload = {
                    "filtro": self.filtro,
                    "pagina": next_page,
                    "registrosPorPagina": 25,
                    "ordenarDecrescente": False,
                    "colunaOrdenacao": "nenhuma",
                    "clienteId": 267511,
                    "tipoVendaId": 1,
                    "fabricanteIdFiltro": 0,
                    "pIIdFiltro": 0,
                    "cestaPPFiltro": False,
                    "codigoExterno": 0,
                    "codigoUsuario": 22850,
                    "promocaoSelecionada": "",
                    "indicadorTipoUsuario": "CLI",
                    "kindUser": 0,
                    "xlsx": [],
                    "principioAtivo": "",
                    "master": False,
                    "kindSeller": 0,
                    "grupoEconomico": "",
                    "users": [
                        518565,
                        267511
                    ],
                    "list": True
                }
                
                self.logger.info(f'Requisitando página {next_page}')
                
                yield scrapy.Request(
                    url=next_url,
                    method='POST',
                    body=json.dumps(payload),
                    headers={'Content-Type': 'application/json'},
                    callback=self.parse_products,
                    errback=self.handle_error,
                    meta={'page': next_page, 'handle_httpstatus_list': [403]}
                )
        
        except json.JSONDecodeError as e:
            self.logger.error(f'Erro ao decodificar JSON da página {page}: {e}')
        except Exception as e:
            self.logger.error(f'Erro no parse da página {page}: {e}')
    
    def handle_error(self, failure):
        """Handle request errors"""
        self.logger.error(f'Request failed: {failure.value}')
        if hasattr(failure.value, 'response'):
            response = failure.value.response
            self.logger.error(f'Response status: {response.status}')
            self.logger.error(f'Response headers: {dict(response.headers)}')
            self.logger.error(f'Response body: {response.text[:500]}...')
    
    def extract_product_data(self, produto_data):
        """Extrai dados do produto do JSON"""
        
        try:
            # Criar item
            item = ProdutoItem()
            
            # Mapear campos conforme estrutura real da API
            item['gtin'] = str(produto_data.get('codigoBarras', ''))
            item['codigo'] = str(produto_data.get('codigoExterno', produto_data.get('id', '')))
            item['descricao'] = produto_data.get('descricao', '')
            
            # Preço (pode ser string ou float)
            preco_raw = produto_data.get('precoVenda', 0)
            try:
                item['preco_fabrica'] = float(preco_raw) if preco_raw else 0.0
            except (ValueError, TypeError):
                item['preco_fabrica'] = 0.0
            
            # Estoque (pode ser string ou int)
            estoque_raw = produto_data.get('quantidadeEstoque', 0)
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
