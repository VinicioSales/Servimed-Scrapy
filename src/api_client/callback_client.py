"""
Cliente para API de Callback
============================

Cliente para autenticação e envio de produtos para a API de callback.
"""

import requests
import json
from typing import List, Dict, Optional


class CallbackAPIClient:
    """Cliente para interagir com a API de callback"""
    
    def __init__(self, base_url: str = "https://desafio.cotefacil.net"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.session = requests.Session()
    
    def authenticate(self, username: str, password: str, client_id: str, client_secret: str) -> bool:
        """
        Autentica na API e obtém o token de acesso
        
        Args:
            username: Email do usuário
            password: Senha do usuário  
            client_id: ID do cliente
            client_secret: Secret do cliente
            
        Returns:
            bool: True se autenticado com sucesso
        """
        try:
            # Primeiro, criar usuário se não existir
            self._create_user_if_not_exists(username, password)
            
            # Dados para autenticação OAuth2
            auth_data = {
                "username": username,
                "password": password,
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "password"
            }
            
            # Headers para OAuth2
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            response = self.session.post(
                f"{self.base_url}/oauth/token",
                data=auth_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get("access_token")
                
                # Adiciona token aos headers da sessão
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                
                print(f"Autenticacao realizada com sucesso!")
                print(f"Token obtido: {self.token[:50]}...")
                return True
            else:
                print(f"Erro na autenticacao: {response.status_code}")
                print(f"Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"Erro durante autenticacao: {e}")
            return False
    
    def _create_user_if_not_exists(self, username: str, password: str):
        """Tenta criar usuário se não existir"""
        try:
            signup_data = {
                "username": username,
                "password": password,
                "email": username  # Usando email como username
            }
            
            response = self.session.post(
                f"{self.base_url}/oauth/signup",
                json=signup_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"Usuario criado/verificado: {username}")
            elif response.status_code == 409:
                print(f"Usuario ja existe: {username}")
            else:
                print(f"Aviso ao criar usuario: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Aviso ao criar usuario: {e}")
    
    def send_products(self, products: List[Dict]) -> bool:
        """
        Envia lista de produtos para a API
        
        Args:
            products: Lista de produtos no formato esperado pela API
            
        Returns:
            bool: True se enviado com sucesso
        """
        if not self.token:
            print("Erro: Nao autenticado. Execute authenticate() primeiro.")
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
            
            if response.status_code == 201:
                result = response.json()
                print(f"Produtos enviados com sucesso! {len(result)} produtos processados.")
                return True
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
