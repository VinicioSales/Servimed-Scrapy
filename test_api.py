#!/usr/bin/env python3
"""
Teste OAuth2 da API Cotefacil
=============================
"""

import requests
import json
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

def test_oauth2_auth():
    """Teste da autenticação OAuth2 password flow"""
    
    # Dados do .env
    username = os.getenv('PORTAL_EMAIL')
    password = os.getenv('PORTAL_PASSWORD')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    base_url = os.getenv('COTEFACIL_API_URL', 'https://desafio.cotefacil.net')
    
    print("=== TESTE OAUTH2 COTEFACIL ===")
    print(f"Username: {username}")
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")
    print(f"Base URL: {base_url}")
    print()
    
    # Dados para OAuth2 token
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
    
    try:
        # 1. Obter token
        print("1. Obtendo access token...")
        token_response = requests.post(
            f"{base_url}/oauth/token",
            data=token_data,
            headers=token_headers,
            timeout=30
        )
        
        print(f"Status: {token_response.status_code}")
        print(f"Response: {token_response.text}")
        
        if token_response.status_code != 200:
            print("❌ Falha na autenticação")
            return False
        
        token_info = token_response.json()
        access_token = token_info.get("access_token")
        
        if not access_token:
            print("❌ Access token não encontrado")
            return False
        
        print(f"✅ Access token obtido: {access_token[:50]}...")
        
        # 2. Testar envio de produto
        print("\n2. Testando envio de produto...")
        
        api_headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        test_products = [
            {
                "gtin": "7898636193493",
                "codigo": "444212", 
                "descricao": "BEBIDA HIDRATANTE SOROX LIMAO 550ML - TESTE OAUTH2",
                "preco_fabrica": 8.18,
                "estoque": 4102
            }
        ]
        
        produto_response = requests.post(
            f"{base_url}/produto",
            json=test_products,
            headers=api_headers,
            timeout=30
        )
        
        print(f"Status: {produto_response.status_code}")
        print(f"Response: {produto_response.text}")
        
        if produto_response.status_code == 201:
            print("✅ SUCCESS - Produto enviado via OAuth2!")
            return True
        else:
            print("❌ ERRO - Falha no envio do produto")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    test_oauth2_auth()
