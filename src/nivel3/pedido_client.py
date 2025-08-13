"""
Cliente de Pedidos - Nível 3
=============================

Cliente para realizar pedidos no portal Servimed e enviar confirmação para API.
"""

import requests
import json
import os
import time
import uuid
import urllib3
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Desabilitar warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar .env
load_dotenv()


class PedidoClient:
    """Cliente para realizar pedidos no portal Servimed"""
    
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'https://peapi.servimed.com.br')
        self.portal_url = os.getenv('PORTAL_URL', 'https://pedidoeletronico.servimed.com.br')
        self.session = requests.Session()
        
        # Headers padrão baseados na análise do DevTools
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': self.portal_url,
            'Referer': f'{self.portal_url}/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        })
        
        # Autenticação
        self.access_token = None
        self.session_token = None
        self.logged_user = None
        self.client_id = None
        self.x_cart = None
        
    def authenticate(self) -> bool:
        """
        Autentica no portal usando tokens do .env
        
        Returns:
            bool: True se autenticado com sucesso
        """
        try:
            # Carregar tokens do .env
            self.access_token = os.getenv('ACCESS_TOKEN')
            self.session_token = os.getenv('SESSION_TOKEN')
            self.logged_user = os.getenv('LOGGED_USER')
            self.client_id = os.getenv('CLIENT_ID')
            self.x_cart = os.getenv('X_CART')
            
            if not all([self.access_token, self.session_token, self.logged_user, self.client_id]):
                print("Tokens de autenticação incompletos no .env")
                return False
            
            self.session.headers.update({
                'accesstoken': self.access_token,
                'loggeduser': self.logged_user,
                'x-cart': self.x_cart,
                'x-peperone': str(int(time.time() * 1000))  # Timestamp em milliseconds
            })
            
            # Configurar cookies
            self.session.cookies.update({
                'accesstoken': self.access_token,
                'sessiontoken': self.session_token
            })
            
            print(f"Autenticação configurada para usuário: {self.logged_user}")
            return True
            
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return False
    
    def buscar_produto_por_codigo(self, codigo: str) -> Optional[Dict]:
        """
        Busca produto pelo código no portal
        
        Args:
            codigo: Código do produto
            
        Returns:
            Dict: Dados do produto ou None se não encontrado
        """
        try:
            # Usar a mesma lógica do scraper para buscar produto
            from ..servimed_scraper.scraper import ServimedScraperCompleto
            
            scraper = ServimedScraperCompleto()
            # Fazer busca com filtro do código
            resultado = scraper.run(filtro=codigo, max_pages=1)
            
            # Verificar se retornou dados válidos
            if not resultado or 'arquivo_salvo' not in resultado:
                print(f"Falha na busca do produto {codigo}")
                return None
            
            # Ler arquivo de produtos gerado
            arquivo_produtos = resultado['arquivo_salvo']
            with open(arquivo_produtos, 'r', encoding='utf-8') as f:
                dados_completos = json.load(f)
            
            # Extrair apenas a lista de produtos
            produtos = dados_completos.get('produtos', [])
            
            # Procurar produto com código exato
            for produto in produtos:
                if str(produto.get('codigo', '')) == str(codigo):
                    print(f"Produto encontrado: {produto.get('descricao', '')}")
                    return produto
            
            print(f"Produto com código {codigo} não encontrado")
            return None
            
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
            return None
    
    def realizar_pedido(self, produtos_pedido: List[Dict]) -> Optional[str]:
        """
        Realiza pedido no portal Servimed e retorna o código do pedido
        
        Args:
            produtos_pedido: Lista de produtos com {gtin, codigo, quantidade}
            
        Returns:
            str: Código do pedido retornado pelo Servimed ou None se falhou
        """
        try:
            if not self.access_token:
                print("Não autenticado. Execute authenticate() primeiro.")
                return None
            
            # Buscar dados dos produtos
            itens_pedido = []
            
            for item in produtos_pedido:
                codigo = item.get('codigo')
                quantidade = item.get('quantidade', 1)
                
                # Buscar dados do produto
                produto = self.buscar_produto_por_codigo(codigo)
                if not produto:
                    print(f"Produto {codigo} não encontrado, ignorando...")
                    continue
                
                # Montar item do pedido baseado no DevTools
                item_pedido = {
                    "id": int(produto.get('codigo')),
                    "selectedPromotionID": -1,
                    "taxValue": float(produto.get('preco_fabrica', 0)) * 1.46,  # Aproximação do imposto
                    "quantityRequested": int(quantidade),
                    "baseValue": float(produto.get('preco_fabrica', 0)),
                    "totalStIvaValue": float(produto.get('preco_fabrica', 0)) * 1.46,
                    "totalValue": float(produto.get('preco_fabrica', 0)) * 1.46 * quantidade,
                    "discount": 0,
                    "descontos": [],
                    "discountValue": float(produto.get('preco_fabrica', 0)),
                    "stIVA": 3.77  # Valor padrão observado
                }
                
                itens_pedido.append(item_pedido)
                print(f"Item adicionado: {produto.get('descricao', '')} (Qtd: {quantidade})")
            
            if not itens_pedido:
                print("Nenhum produto válido para o pedido")
                return None
            
            # Montar payload do pedido baseado no DevTools
            payload_pedido = {
                "customerId": int(self.client_id),
                "userCode": int(self.logged_user),
                "daysOfPlots": 28,
                "pieces": ["21", "28", "35"],  # Valores padrão observados
                "quantityPlots": 1,
                "sellId": 1,
                "itens": itens_pedido
            }
            
            print(f"Enviando pedido com {len(itens_pedido)} itens...")
            print(f"Payload: {json.dumps(payload_pedido, indent=2)}")
            
            # Enviar pedido
            response = self.session.post(
                f"{self.base_url}/api/Pedido/TrasmitirPedido",
                json=payload_pedido,
                timeout=30,
                verify=False
            )
            
            print(f"Status da resposta: {response.status_code}")
            print(f"Resposta: {response.text}")
            
            if response.status_code == 200:
                resposta = response.json()
                print(f"Resposta do Servimed: {resposta}")
                
                if resposta.get('executado') == 'Ok':
                    # Servimed retorna apenas {'executado': 'Ok'} sem código do pedido
                    # Gerar código único e intuitivo baseado nas características do pedido
                    
                    from datetime import datetime
                    
                    # Data e hora atual para criar código legível
                    agora = datetime.now()
                    data_str = agora.strftime("%d%m%Y")  # DDMMAAAA
                    hora_str = agora.strftime("%H%M")    # HHMM
                    
                    # Informações do pedido
                    primeiro_produto = str(itens_pedido[0].get('id', '000000')) if itens_pedido else '000000'
                    quantidade_total = sum(item.get('quantityRequested', 0) for item in itens_pedido)
                    cliente_sufixo = str(self.client_id)[-4:]  # Últimos 4 dígitos do cliente
                    
                    # Formato legível: SERVIMED_DDMMAAAA_HHMM_PRODUTO1_QTD_CLIENTE
                    # Exemplo: SERVIMED_13082025_1245_444212_01_7511
                    codigo_pedido = f"SERVIMED_{data_str}_{hora_str}_{primeiro_produto}_{quantidade_total:02d}_{cliente_sufixo}"
                    
                    print(f"Pedido realizado com sucesso no Servimed!")
                    print(f"Código gerado para rastreamento: {codigo_pedido}")
                    print(f"  - Data: {agora.strftime('%d/%m/%Y %H:%M')}")
                    print(f"  - Primeiro produto: {primeiro_produto}")
                    print(f"  - Quantidade total: {quantidade_total}")
                    print(f"  - Cliente: {self.client_id} (sufixo: {cliente_sufixo})")
                    
                    return codigo_pedido
                else:
                    print(f"Pedido rejeitado pelo Servimed: {resposta}")
                    return None
            else:
                print(f"Erro HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"Erro ao realizar pedido: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Testa conexão com o portal"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10, verify=False)
            return response.status_code < 500
        except:
            return False

