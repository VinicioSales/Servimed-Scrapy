"""
MIDDLEWARES - SCRAPY SERVIMED
=====================        # Cookies - incluindo todos os cookies capturados do DevTools
        # Cookies devem conter os JWTs completos conforme DevTools
        request.cookies.update({
            'accesstoken': self.access_token_jwt,  # JWT completo do accesstoken
            'sessiontoken': self.session_token,   # JWT completo do sessiontoken
            '_ga': 'GA1.1.1496905904.1755017918',
            '_ga_0684EZD6WN': 'GS2.1.s1755087487$o8$g1$t1755089675$j38$l0$h0',
            '_ga_TGSHLZ7V8G': 'GS2.3.s1755018324$o1$g1$t1755018332$j52$l0$h0',
            '_gat': '1',
            '_gid': 'GA1.3.808374586.1755017918'
        })Middlewares para autenticação e sessão.
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
        self.access_token_jwt = os.getenv('ACCESS_TOKEN_JWT')
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
        
        # Headers EXATAMENTE como no exemplo cURL funcionando
        request.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',  # Firefox do exemplo!
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'x-cart': self.x_cart,
            'x-peperone': str(int(time.time() * 1000)),
            'Content-Type': 'application/json',
            'contentType': 'application/json',  # Lowercase 'T' como no exemplo!
            'loggedUser': self.logged_user,
            'accesstoken': self.access_token,  # UUID nos headers
            'Origin': 'https://pedidoeletronico.servimed.com.br',
            'Connection': 'keep-alive',
            'Referer': 'https://pedidoeletronico.servimed.com.br/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        })
        
        # Cookies - JWTs completos como no exemplo
        request.cookies.update({
            'sessiontoken': self.session_token,   # JWT completo nos cookies
            'accesstoken': self.access_token_jwt, # JWT completo nos cookies
            '_ga': 'GA1.1.1496905904.1755017918',
            '_ga_0684EZD6WN': 'GS2.1.s1755087487$o8$g1$t1755089675$j38$l0$h0',
            '_ga_TGSHLZ7V8G': 'GS2.3.s1755018324$o1$g1$t1755018332$j52$l0$h0',
            '_gat': '1',
            '_gid': 'GA1.3.808374586.1755017918'
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
