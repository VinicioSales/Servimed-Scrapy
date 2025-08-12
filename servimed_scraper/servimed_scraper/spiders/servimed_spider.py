import json
import scrapy


class ServimedSpider(scrapy.Spider):
    name = 'servimed'
    
    def __init__(self, username=None, password=None, client_id=None):
        self.username = username
        self.password = password
        self.client_id = client_id
        
        # Headers base para todas as requisições
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://pedidoeletronico.servimed.com.br',
            'Referer': 'https://pedidoeletronico.servimed.com.br/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        
        # Headers específicos para login (serão atualizados após autenticação)
        self.login_headers = self.base_headers.copy()
        
        # Headers de sessão (serão preenchidos após login)
        self.session_headers = self.base_headers.copy()
        
    def start_requests(self):
        yield scrapy.Request(
            url="https://pedidoeletronico.servimed.com.br/",
            callback=self.parse_login_page,
            headers=self.base_headers
        )
        
    def parse_login_page(self, response):
        # Dados de login baseados na investigação do DevTools
        login_data = {
            'usuario': self.username,  # O site usa 'usuario', não 'username'
            'senha': self.password     # O site usa 'senha', não 'password'
        }

        # URL encontrada na investigação
        yield scrapy.Request(
            url="https://peapi.servimed.com.br/api/usuario/login",
            method="POST",
            body=json.dumps(login_data),
            headers=self.login_headers,
            callback=self.handle_login_response
        )
        
    def handle_login_response(self, response):
        if response.status == 200:
            # Extrair dados do usuário da resposta JSON
            data = json.loads(response.text)
            usuario_data = data.get('usuario', {})
            
            # Extrair tokens dos cookies da resposta
            cookies = response.headers.getlist('Set-Cookie')
            session_token = None
            access_token = None
            
            for cookie in cookies:
                cookie_str = cookie.decode('utf-8')
                if cookie_str.startswith('sessiontoken='):
                    session_token = cookie_str.split('sessiontoken=')[1].split(';')[0]
                elif cookie_str.startswith('accesstoken='):
                    access_token = cookie_str.split('accesstoken=')[1].split(';')[0]
            
            # Atualizar headers de sessão com os dados obtidos
            if access_token and session_token:
                self.session_headers.update({
                    'accesstoken': access_token,
                    'loggedUser': str(usuario_data.get('codigoUsuario', '')),
                    'Cookie': f'sessiontoken={session_token}; accesstoken={access_token}',
                    'contenttype': 'application/json'
                })
                
                self.logger.info(f"Login realizado com sucesso! Usuário: {usuario_data.get('codigoUsuario')}")
                
                # Prosseguir para busca de produtos
                yield from self.fetch_products(response)
            else:
                self.logger.error("Não foi possível extrair os tokens de autenticação")
        else:
            self.logger.error(f"Erro no login: Status {response.status}")
            self.logger.error(f"Resposta: {response.text}")
        
    def fetch_products(self, response):
        # TODO: Investigar endpoint correto de produtos
        # Por enquanto, simular dados para continuar o desenvolvimento
        
        self.logger.info("SIMULANDO dados de produtos - endpoint real precisa ser investigado")
        
        # Produtos simulados baseados na estrutura esperada
        produtos_simulados = [
            {
                'gtin': '7891234567890',
                'codigo': 'DIP001',
                'descricao': 'Dipirona Sódica 500mg c/ 20 comprimidos',
                'preco_fabrica': 15.90,
                'estoque': 100
            },
            {
                'gtin': '7891234567891',
                'codigo': 'PAR002',
                'descricao': 'Paracetamol 750mg c/ 20 comprimidos',
                'preco_fabrica': 12.50,
                'estoque': 50
            },
            {
                'gtin': '7891234567892',
                'codigo': 'IBU003',
                'descricao': 'Ibuprofeno 600mg c/ 20 comprimidos',
                'preco_fabrica': 18.75,
                'estoque': 75
            }
        ]
        
        self.logger.info(f"Produtos simulados encontrados: {len(produtos_simulados)}")
        
        # Retornar os dados simulados
        for produto in produtos_simulados:
            yield produto
    
    def parse_products(self, response):
        # Processar resposta dos produtos
        if response.status == 200:
            data = json.loads(response.text)
            # Aqui você processará os produtos retornados
            self.logger.info(f"Produtos encontrados: {len(data.get('produtos', []))}")
            
            # Retornar os dados dos produtos
            for produto in data.get('produtos', []):
                yield {
                    'gtin': produto.get('gtin'),
                    'codigo': produto.get('codigo'),
                    'descricao': produto.get('descricao'),
                    'preco_fabrica': produto.get('precoFabrica'),
                    'estoque': produto.get('estoque')
                }