import json
import scrapy
import os
from dotenv import load_dotenv
from ..clients.cotefacil_client import CotefacilApiClient

load_dotenv()


class ServimedSpider(scrapy.Spider):
    name = 'servimed'
    
    handle_httpstatus_list = [401, 403]
    
    def __init__(self, username=None, password=None, client_id=None):
        self.username = username or os.getenv('SERVIMED_USERNAME')
        self.password = password or os.getenv('SERVIMED_PASSWORD')
        self.client_id = client_id or os.getenv('SERVIMED_CLIENT_ID')
        
        self.servimed_base_url = os.getenv('SERVIMED_BASE_URL', 'https://pedidoeletronico.servimed.com.br')
        self.servimed_api_url = os.getenv('SERVIMED_API_URL', 'https://peapi.servimed.com.br')
        
        self.cotefacil_client = CotefacilApiClient()
        
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': self.servimed_base_url,
            'Referer': f'{self.servimed_base_url}/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        
        self.login_headers = self.base_headers.copy()
        
        self.session_headers = self.base_headers.copy()
        
    def start_requests(self):
        yield scrapy.Request(
            url=f"{self.servimed_base_url}/",
            callback=self.parse_login_page,
            headers=self.base_headers
        )
        
    def parse_login_page(self, response):
        login_data = {
            'usuario': self.username,
            'senha': self.password
        }

        yield scrapy.Request(
            url=f"{self.servimed_api_url}/api/usuario/login",
            method="POST",
            body=json.dumps(login_data),
            headers=self.login_headers,
            callback=self.handle_login_response
        )
        
    def handle_login_response(self, response):
        if response.status == 200:
            data = json.loads(response.text)
            usuario_data = data.get('usuario', {})
            
            cookies = response.headers.getlist('Set-Cookie')
            session_token = None
            access_token = None
            
            for cookie in cookies:
                cookie_str = cookie.decode('utf-8')
                if cookie_str.startswith('sessiontoken='):
                    session_token = cookie_str.split('sessiontoken=')[1].split(';')[0]
                elif cookie_str.startswith('accesstoken='):
                    access_token = cookie_str.split('accesstoken=')[1].split(';')[0]
            
            if access_token and session_token:
                self.session_headers.update({
                    'accesstoken': access_token,
                    'loggedUser': str(usuario_data.get('codigoUsuario', '')),
                    'Cookie': f'sessiontoken={session_token}; accesstoken={access_token}',
                    'contenttype': 'application/json'
                })
                
                self.logger.info(f"Login realizado com sucesso! Usuário: {usuario_data.get('codigoUsuario')}")
                
                yield from self.fetch_products(response)
            else:
                self.logger.error("Não foi possível extrair os tokens de autenticação")
        else:
            self.logger.error(f"Erro no login: Status {response.status}")
            self.logger.error(f"Resposta: {response.text}")
        
    def fetch_products(self, response):
        self.logger.info("Buscando produtos da API Cotefácil...")
        
        products = self.cotefacil_client.get_products()
        self.logger.info(f"Produtos encontrados na API: {len(products)}")
        
        for produto in products:
            yield {
                'gtin': produto.get('gtin'),
                'codigo': produto.get('codigo'),
                'descricao': produto.get('descricao'),
                'preco_fabrica': produto.get('preco_fabrica'),
                'estoque': produto.get('estoque')
            }
    
    def parse_products(self, response):
        if response.status == 200:
            data = json.loads(response.text)
            self.logger.info(f"Produtos encontrados: {len(data.get('produtos', []))}")
            
            for produto in data.get('produtos', []):
                yield {
                    'gtin': produto.get('gtin'),
                    'codigo': produto.get('codigo'),
                    'descricao': produto.get('descricao'),
                    'preco_fabrica': produto.get('precoFabrica'),
                    'estoque': produto.get('estoque')
                }