import json
import urllib.parse
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class CotefacilApiClient:
    """Cliente para API do Cotefácil"""
    
    def __init__(self):
        self.username = os.getenv('COTEFACIL_USERNAME')
        self.password = os.getenv('COTEFACIL_PASSWORD')
        self.client_id = os.getenv('COTEFACIL_CLIENT_ID')
        self.client_secret = os.getenv('COTEFACIL_CLIENT_SECRET')
        self.base_url = os.getenv('COTEFACIL_BASE_URL', 'https://desafio.cotefacil.net')
        self.access_token = None
        
    def authenticate(self):
        """Autentica na API e obtém token de acesso"""
        auth_url = f"{self.base_url}/oauth/token"
        
        auth_data = {
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password"
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0'
        }
        
        try:
            response = requests.post(
                auth_url,
                data=auth_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                self.access_token = auth_data.get('access_token')
                return True
            else:
                print(f"Erro na autenticação: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"Erro na requisição de autenticação: {e}")
            return False
    
    def get_products(self):
        """Busca produtos da API"""
        if not self.access_token:
            if not self.authenticate():
                return []
        
        products_url = f"{self.base_url}/produto"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0'
        }
        
        try:
            response = requests.get(
                products_url,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro ao buscar produtos: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            print(f"Erro na requisição de produtos: {e}")
            return []

    def signup(self, username, password):
        """Criar usuário na API Cotefácil"""
        signup_url = f"{self.base_url}/oauth/signup"
        
        signup_data = {
            "username": username,
            "password": password
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0'
        }
        
        try:
            response = requests.post(
                signup_url,
                json=signup_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Usuário criado com sucesso: {username}")
                return True
            else:
                print(f"⚠️ Erro no signup: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Erro na requisição de signup: {e}")
            return False

    def send_products_to_callback(self, products, callback_url=None):
        """Enviar produtos para API de callback"""
        if not self.access_token:
            if not self.authenticate():
                return False
        
        callback_url = callback_url or f"{self.base_url}/produto"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0'
        }
        
        # Formatar produtos conforme especificação
        formatted_products = []
        for product in products:
            formatted_products.append({
                "gtin": product.get('gtin'),
                "codigo": product.get('codigo'),
                "descricao": product.get('descricao'),
                "preco_fabrica": product.get('preco_fabrica'),
                "estoque": product.get('estoque')
            })
        
        try:
            response = requests.post(
                callback_url,
                json=formatted_products,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ {len(formatted_products)} produtos enviados para callback")
                return True
            else:
                print(f"⚠️ Erro no callback: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Erro na requisição de callback: {e}")
            return False

    def send_order_confirmation(self, order_id, confirmation_data, callback_url=None):
        """Enviar confirmação de pedido para API"""
        if not self.access_token:
            if not self.authenticate():
                return False
        
        callback_url = callback_url or f"{self.base_url}/pedido/{order_id}"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0'
        }
        
        try:
            response = requests.patch(
                callback_url,
                json=confirmation_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Confirmação do pedido {order_id} enviada")
                return True
            else:
                print(f"⚠️ Erro no envio de confirmação: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Erro na requisição de confirmação: {e}")
            return False
