"""
Scraper para o Portal Servimed
==============================

Coleta produtos da API do Servimed com opções de filtro personalizáveis.
"""

import requests
import json
import time
import urllib3
from pathlib import Path
import sys

# Adiciona o diretório config ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import *
from config.paths import OUTPUT_FILES

# Desabilita avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ServimedScraperCompleto:
    """
    Scraper para coletar produtos disponíveis no Servimed
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = VERIFY_SSL
        
        # Tokens
        self.access_token = ACCESS_TOKEN
        self.session_token = SESSION_TOKEN
        
        # Configurações
        self.logged_user = LOGGED_USER
        self.x_cart = X_CART
        self.client_id = CLIENT_ID
        self.users = USERS
        
        # Lista para armazenar todos os produtos
        self.todos_produtos = []
        
        # Configura sessão
        self._setup_session()
    
    def _setup_session(self):
        """Configura a sessão HTTP com cookies e headers"""
        # Cookies
        self.session.cookies.set('sessiontoken', self.session_token, domain='.servimed.com.br')
        self.session.cookies.set('accesstoken', self.access_token, domain='.servimed.com.br')
        
        # Headers base
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
            'accesstoken': self.access_token,
            'content-type': 'application/json',
            'contenttype': 'application/json',
            'loggeduser': str(self.logged_user),
            'origin': PORTAL_URL,
            'referer': f'{PORTAL_URL}/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': USER_AGENT,
            'x-cart': self.x_cart
        }
    
    def search_products(self, filtro="", page=1):
        """
        Busca produtos na API do Servimed
        
        Args:
            filtro (str): Termo de busca (vazio = todos os produtos)
            page (int): Número da página (inicia em 1)
            
        Returns:
            dict: Dados da resposta da API ou None em caso de erro
        """
        url = f'{BASE_URL}{API_ENDPOINT}?siteVersion={SITE_VERSION}'
        
        payload = {
            "filtro": filtro,  # Filtro personalizável
            "pagina": page,
            "registrosPorPagina": RECORDS_PER_PAGE,
            "ordenarDecrescente": False,
            "colunaOrdenacao": "nenhuma",
            "clienteId": self.client_id,
            "tipoVendaId": 1,
            "fabricanteIdFiltro": 0,
            "pIIdFiltro": 0,
            "cestaPPFiltro": False,
            "codigoExterno": 0,
            "codigoUsuario": int(self.logged_user),
            "promocaoSelecionada": "",
            "indicadorTipoUsuario": "CLI",
            "kindUser": 0,
            "xlsx": [],
            "principioAtivo": "",
            "master": False,
            "kindSeller": 0,
            "grupoEconomico": "",
            "users": self.users,
            "list": True
        }
        
        # Atualiza timestamp
        headers = self.headers.copy()
        headers['x-peperone'] = str(int(time.time() * 1000))
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=TIMEOUT_SECONDS)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro HTTP {response.status_code}: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def processar_produto(self, produto):
        """
        Extrai apenas os campos específicos solicitados
        """
        produto_processado = {
            'gtin_ean': produto.get('codigoBarras'),
            'codigo': produto.get('codigoExterno'),
            'descricao': produto.get('descricao'),
            'preco_fabrica': produto.get('valorBase'),
            'estoque': produto.get('quantidadeEstoque'),
            'data_coleta': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return produto_processado
    
    def get_all_products(self, filtro="", max_pages=None):
        """
        Coleta produtos com filtro específico
        
        Args:
            filtro (str): Termo para buscar (vazio = todos os produtos)
            max_pages (int, optional): Máximo de páginas para coletar
            
        Returns:
            list: Lista com todos os produtos encontrados
        """
        page = 1
        
        tipo_busca = "TODOS OS PRODUTOS" if not filtro else f"FILTRO: '{filtro}'"
        print(f"Coletando produtos - {tipo_busca}")
        print("=" * 60)
        
        while True:
            print(f"Pagina {page:>4}...", end=" ")
            
            data = self.search_products(filtro, page)
            
            if not data or 'lista' not in data:
                print("Erro ou fim dos dados")
                break
            
            products = data['lista']
            
            if not products:  # Lista vazia = fim dos produtos
                print("Fim dos produtos")
                break
            
            # Processa cada produto
            for produto in products:
                produto_processado = self.processar_produto(produto)
                self.todos_produtos.append(produto_processado)
            
            # Info de paginação
            total_records = data.get('totalRegistros', 0)
            records_per_page = data.get('registrosPorPagina', RECORDS_PER_PAGE)
            total_pages = (total_records + records_per_page - 1) // records_per_page
            
            print(f"OK {len(products)} produtos (Total: {len(self.todos_produtos)}/{total_records})")
            
            # Verifica se deve parar
            if page >= total_pages or (max_pages and page >= max_pages):
                break
            
            # A cada 50 páginas, salva backup
            if page % 50 == 0:
                self.salvar_backup(page, filtro)
            
            page += 1
            
            # Pausa entre requisições
            if DELAY_BETWEEN_REQUESTS > 0:
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        print(f"\nCOLETA FINALIZADA: {len(self.todos_produtos)} produtos coletados")
        return self.todos_produtos
    
    def salvar_backup(self, page, filtro=""):
        """Salva backup a cada X páginas"""
        dados_backup = {
            "metadados": {
                "total_produtos_ate_agora": len(self.todos_produtos),
                "pagina_atual": page,
                "filtro_usado": filtro if filtro else "TODOS OS PRODUTOS",
                "data_backup": time.strftime('%Y-%m-%d %H:%M:%S'),
                "fonte": "Portal Servimed - Backup Automático"
            },
            "produtos": self.todos_produtos
        }
        
        backup_file = OUTPUT_FILES['backup']
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(dados_backup, f, ensure_ascii=False, indent=2)
        
        print(f"Backup salvo: {backup_file}")
    
    def salvar_todos_produtos(self, filtro=""):
        """
        Salva todos os produtos coletados em arquivo final com nome fixo
        """
        if not self.todos_produtos:
            print("Nenhum produto para salvar")
            return None
        
        # Define qual arquivo usar baseado no filtro
        if filtro:
            filename = OUTPUT_FILES['filtered_products']
            tipo_busca = f"FILTRO: '{filtro}'"
        else:
            filename = OUTPUT_FILES['all_products']
            tipo_busca = "TODOS OS PRODUTOS (sem filtro)"
        
        # Adiciona metadados
        dados_finais = {
            "metadados": {
                "total_produtos": len(self.todos_produtos),
                "data_coleta": time.strftime('%Y-%m-%d %H:%M:%S'),
                "filtro_usado": filtro if filtro else None,
                "tipo_busca": tipo_busca,
                "fonte": "Portal Servimed - API Completa",
                "usuario": PORTAL_EMAIL,
                "campos_extraidos": [
                    "gtin_ean (Código de Barras)",
                    "codigo (Código Externo)",
                    "descricao",
                    "preco_fabrica (Valor Base)",
                    "estoque (Quantidade)"
                ]
            },
            "produtos": self.todos_produtos
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=2)
        
        print(f"Arquivo final salvo: {filename}")
        print(f"Total de produtos salvos: {len(self.todos_produtos)}")
        
        return str(filename)
    
    def run(self, filtro="", max_pages=None):
        """
        Executa a coleta completa de produtos
        
        Args:
            filtro (str): Termo para filtrar produtos (padrão: vazio = todos)
            max_pages (int): Número máximo de páginas (padrão: None = sem limite)
        """
        print("=" * 60)
        print("SERVIMED SCRAPER - COLETA DE PRODUTOS")
        print("=" * 60)
        
        if filtro:
            print(f"Objetivo: Coletar produtos com filtro '{filtro}'")
        else:
            print(f"Objetivo: Coletar TODOS os produtos disponiveis")
            
        print(f"Token valido ate: {time.ctime(1755089297)}")
        
        if not filtro:
            print(f"Estimativa: ~12.935 produtos (518 paginas)")
        
        print()
        
        start_time = time.time()
        
        # Coleta produtos com ou sem filtro
        produtos = self.get_all_products(filtro=filtro, max_pages=max_pages)
        
        # Salva arquivo final
        arquivo_salvo = self.salvar_todos_produtos(filtro=filtro)
        
        end_time = time.time()
        duracao = end_time - start_time
        
        print("=" * 60)
        print("RESUMO FINAL")
        print("=" * 60)
        print(f"Produtos coletados: {len(self.todos_produtos)}")
        print(f"Arquivo salvo: {arquivo_salvo}")
        print(f"Tempo total: {duracao/60:.1f} minutos")
        print(f"Velocidade: {len(self.todos_produtos)/(duracao/60):.0f} produtos/minuto")
        print("=" * 60)
        
        # Mostra amostra dos dados
        if self.todos_produtos:
            print("\nAMOSTRA DOS DADOS:")
            for i, produto in enumerate(self.todos_produtos[:5]):
                print(f"{i+1}. GTIN: {produto['gtin_ean']}")
                print(f"   Código: {produto['codigo']}")
                print(f"   Descrição: {produto['descricao'][:60]}...")
                print(f"   Preço Fábrica: R$ {produto['preco_fabrica']}")
                print(f"   Estoque: {produto['estoque']}")
                print()
        
        return {
            'arquivo_salvo': arquivo_salvo,
            'total_produtos': len(self.todos_produtos),
            'tempo_execucao': duracao
        }
