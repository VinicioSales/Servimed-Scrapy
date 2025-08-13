"""
Cliente para API de Callback
============================

Cliente para autenticação e envio de produtos para a API de callback.
"""

import requests
import json
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class CallbackAPIClient:
    """Cliente para interagir com a API de callback"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or os.getenv('COTEFACIL_API_URL', 'https://desafio.cotefacil.net')).rstrip('/')
        self.access_token = None
        self.session = requests.Session()
        
        # Configurar headers padrão
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def authenticate(self, username: Optional[str] = None, password: Optional[str] = None, 
                    client_id: Optional[str] = None, client_secret: Optional[str] = None) -> bool:
        """
        Autentica via OAuth2PasswordBearer usando dados do .env
        
        Returns:
            bool: True se autenticado com sucesso
        """
        # Usar dados do .env se não fornecidos
        username = username or os.getenv('PORTAL_EMAIL')
        password = password or os.getenv('PORTAL_PASSWORD')
        client_id = client_id or os.getenv('CLIENT_ID')
        client_secret = client_secret or os.getenv('CLIENT_SECRET')
        
        if not all([username, password, client_id, client_secret]):
            print("ERRO: Credenciais OAuth2 incompletas no .env")
            return False
        
        try:
            # Dados para OAuth2 password flow
            token_data = {
                "username": username,
                "password": password,
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "password"
            }
            
            # Headers para OAuth2 token request
            token_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            print(f"Autenticando com username: {username}")
            print(f"Client ID: {client_id}")
            
            response = self.session.post(
                f"{self.base_url}/oauth/token",
                data=token_data,
                headers=token_headers,
                timeout=30
            )
            
            print(f"Status da autenticação: {response.status_code}")
            print(f"Resposta: {response.text}")
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get("access_token")
                
                if self.access_token:
                    # Atualizar headers da sessão com o token
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.access_token}"
                    })
                    
                    print(f"Autenticação bem-sucedida!")
                    print(f"Access token obtido: {self.access_token[:50]}...")
                    return True
                else:
                    print("Token de acesso não encontrado na resposta")
                    return False
            else:
                print(f"Falha na autenticação: {response.status_code}")
                print(f"Erro: {response.text}")
                return False
                
        except Exception as e:
            print(f"Erro durante autenticação OAuth2: {e}")
            return False
    
    def send_products(self, products: List[Dict]) -> bool:
        """
        Envia lista de produtos para a API
        
        Args:
            products: Lista de produtos no formato esperado pela API
            
        Returns:
            bool: True se enviado com sucesso
        """
        if not self.access_token:
            print("Erro: Não autenticado. Execute authenticate() primeiro.")
            return False
        
        try:
            # Converte produtos para o formato da API
            api_products = []
            for produto in products:
                api_product = {
                    "gtin": str(produto.get('gtin_ean', '')),
                    "codigo": str(produto.get('codigo', '')),
                    "descricao": str(produto.get('descricao', '')),
                    "preco_fabrica": float(produto.get('preco_fabrica', 0.0)),
                    "estoque": int(produto.get('estoque', 0))
                }
                api_products.append(api_product)
            
            response = self.session.post(
                f"{self.base_url}/produto",
                json=api_products,
                timeout=60
            )
            
            print(f"Status da requisição: {response.status_code}")
            print(f"Headers da resposta: {dict(response.headers)}")
            print(f"Conteúdo da resposta: {response.text}")
            
            if response.status_code == 201:
                result = response.json()
                print(f"Produtos enviados com sucesso! {len(result)} produtos processados.")
                return True
            elif response.status_code == 401:
                print(f"ERRO DE AUTENTICAÇÃO: Token inválido ou expirado!")
                print(f"Resposta: {response.text}")
                return False
            else:
                print(f"Erro ao enviar produtos: {response.status_code}")
                print(f"Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"Erro ao enviar produtos: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Testa conexão com a API"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            return response.status_code < 500
        except:
            return False
