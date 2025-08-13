"""
MIDDLEWARES - SCRAPY SERVIMED
============================

Middlewares para autenticação e sessão.
"""

import os
import time
import json
import logging
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.exceptions import NotConfigured
from itemadapter import is_item, ItemAdapter
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

logger = logging.getLogger(__name__)


class OAuth2AuthMiddleware:
    """Middleware para autenticação OAuth2"""
    
    def __init__(self):
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.session_token = os.getenv('SESSION_TOKEN')
        self.logged_user = os.getenv('LOGGED_USER')
        self.client_id = os.getenv('CLIENT_ID')
        self.x_cart = os.getenv('X_CART')
        
        if not all([self.access_token, self.session_token, self.logged_user]):
            raise NotConfigured("Tokens OAuth2 não encontrados no .env")
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls()
    
    def process_request(self, request, spider):
        """Adiciona headers de autenticação em todas as requisições"""
        
        # Headers OAuth2
        request.headers.update({
            'accesstoken': self.access_token,
            'loggeduser': self.logged_user,
            'x-cart': self.x_cart,
            'x-peperone': str(int(time.time() * 1000)),
            'contenttype': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://pedidoeletronico.servimed.com.br',
            'Referer': 'https://pedidoeletronico.servimed.com.br/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Cookies
        request.cookies.update({
            'accesstoken': self.access_token,
            'sessiontoken': self.session_token
        })
        
        return None


class ServimedSessionMiddleware:
    """Middleware para manter sessão ativa"""
    
    def __init__(self):
        self.session_data = {}
    
    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o
    
    def spider_opened(self, spider):
        logger.info(f'Spider {spider.name} aberto com autenticação OAuth2')
        
        # Log das configurações (sem expor tokens)
        access_token = os.getenv('ACCESS_TOKEN', '')
        if access_token:
            logger.info(f'Token válido: {access_token[:20]}...')
    
    def process_request(self, request, spider):
        """Processa requisições mantendo sessão"""
        
        # Adicionar timeout
        request.meta['download_timeout'] = 30
        
        # SSL bypass se necessário
        request.meta['dont_filter'] = True
        
        return None
    
    def process_response(self, request, response, spider):
        """Processa respostas e atualiza sessão se necessário"""
        
        # Log de resposta
        logger.debug(f'Response {response.status} for {request.url}')
        
        # Verificar se precisa atualizar tokens
        if response.status == 401:
            logger.warning('Token expirado - necessário atualizar')
        
        return response
