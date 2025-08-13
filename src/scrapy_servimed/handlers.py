"""
CUSTOM DOWNLOAD HANDLER - ANTI-BOT BYPASS
=========================================

Handler customizado que usa Python requests ao invés do engine do Scrapy
para contornar sistemas de detecção anti-bot.
"""

import os
import time
import requests
import urllib3
from scrapy.http import HtmlResponse, TextResponse
from scrapy.core.downloader.handlers.http import HTTPDownloadHandler
from scrapy.exceptions import NotSupported
from dotenv import load_dotenv

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()


class AntiDetectionDownloadHandler(HTTPDownloadHandler):
    """Handler que usa requests para contornar detecção anti-bot"""
    
    def __init__(self, settings, crawler=None):
        super().__init__(settings, crawler)
        
        # Configurações de autenticação
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_jwt = os.getenv('ACCESS_TOKEN_JWT')
        self.session_token = os.getenv('SESSION_TOKEN')
        self.logged_user = os.getenv('LOGGED_USER')
        self.client_id = os.getenv('CLIENT_ID')
        self.x_cart = os.getenv('X_CART')
        
        # Sessão requests reutilizável
        self.session = requests.Session()
        self.session.verify = False
        
        # Headers padrão que funcionam
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Origin': 'https://pedidoeletronico.servimed.com.br',
            'Referer': 'https://pedidoeletronico.servimed.com.br/',
            'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }
        
        # Cookies padrão que funcionam
        self.default_cookies = {
            'accesstoken': self.access_token_jwt,
            'sessiontoken': self.session_token,
            '_ga': 'GA1.1.1496905904.1755017918',
            '_ga_0684EZD6WN': 'GS2.1.s1755087487$o8$g1$t1755089675$j38$l0$h0',
            '_ga_TGSHLZ7V8G': 'GS2.3.s1755018324$o1$g1$t1755018332$j52$l0$h0',
            '_gat': '1',
            '_gid': 'GA1.3.808374586.1755017918'
        }
    
    def download_request(self, request, spider):
        """Substitui requisições Scrapy por requests Python"""
        
        try:
            # Preparar headers
            headers = self.default_headers.copy()
            
            # Adicionar headers específicos da requisição
            for key, value in request.headers.items():
                if isinstance(value, list) and len(value) > 0:
                    headers[key.decode()] = value[0].decode()
                elif isinstance(value, bytes):
                    headers[key.decode()] = value.decode()
                elif isinstance(value, str):
                    headers[key] = value
            
            # Headers específicos de autenticação
            if self.access_token:
                headers['accesstoken'] = self.access_token
            if self.logged_user:
                headers['loggeduser'] = self.logged_user
            if self.x_cart:
                headers['x-cart'] = self.x_cart
            
            headers['x-peperone'] = str(int(time.time() * 1000))
            
            # Preparar cookies
            cookies = self.default_cookies.copy()
            
            # Adicionar cookies da requisição se houver
            if hasattr(request, 'cookies') and request.cookies:
                cookies.update(request.cookies)
            
            # Fazer requisição com requests
            if request.method == 'POST':
                # Para POST, usar JSON body se disponível
                json_data = None
                data = None
                
                if hasattr(request, 'body') and request.body:
                    try:
                        import json
                        json_data = json.loads(request.body.decode('utf-8'))
                        headers['Content-Type'] = 'application/json'
                    except:
                        data = request.body
                
                response = self.session.post(
                    request.url,
                    headers=headers,
                    cookies=cookies,
                    json=json_data,
                    data=data,
                    timeout=10,  # Reduced timeout
                    verify=False
                )
            else:
                # GET request
                response = self.session.get(
                    request.url,
                    headers=headers,
                    cookies=cookies,
                    timeout=10,  # Reduced timeout
                    verify=False
                )
            
            # Converter resposta requests para Response do Scrapy
            scrapy_response = self._convert_response(response, request)
            
            # Log do resultado
            spider.logger.info(f"Anti-detection request: {request.method} {request.url} -> {response.status_code}")
            
            return scrapy_response
            
        except Exception as e:
            spider.logger.error(f"Anti-detection download failed: {e}")
            # Fallback para handler padrão
            return super().download_request(request, spider)
    
    def _convert_response(self, requests_response, scrapy_request):
        """Converte resposta requests para Response do Scrapy"""
        
        # Preparar headers para Scrapy
        scrapy_headers = {}
        for key, value in requests_response.headers.items():
            scrapy_headers[key] = [value.encode()]
        
        # Determinar tipo de resposta
        content_type = requests_response.headers.get('content-type', '').lower()
        
        if 'json' in content_type or 'application/json' in content_type:
            # Response JSON
            response_class = TextResponse
        else:
            # Response HTML
            response_class = HtmlResponse
        
        # Criar response do Scrapy
        return response_class(
            url=scrapy_request.url,
            status=requests_response.status_code,
            headers=scrapy_headers,
            body=requests_response.content,
            encoding=requests_response.encoding or 'utf-8',
            request=scrapy_request
        )
