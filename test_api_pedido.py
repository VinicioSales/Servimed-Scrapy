#!/usr/bin/env python3
"""
Teste de Diagnóstico - Nível 3
===============================

Teste direto para identificar problemas na API de pedidos.
"""

import sys
import os
import requests
import json
import time
import urllib3
from dotenv import load_dotenv

# Desabilitar avisos SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar .env
load_dotenv()

def test_api_pedido_direto():
    """Teste direto da API de pedido com dados reais"""
    
    print("=== DIAGNÓSTICO API DE PEDIDOS ===")
    
    # 1. Teste de conectividade
    print("\n1. Testando conectividade...")
    base_url = os.getenv('BASE_URL', 'https://peapi.servimed.com.br')
    
    try:
        response = requests.get(base_url, timeout=10, verify=False)
        print(f"✅ Conectividade OK: {response.status_code}")
    except Exception as e:
        print(f"❌ Falha na conectividade: {e}")
        return False
    
    # 2. Teste de autenticação
    print("\n2. Testando headers de autenticação...")
    
    access_token = os.getenv('ACCESS_TOKEN')
    session_token = os.getenv('SESSION_TOKEN')
    logged_user = os.getenv('LOGGED_USER')
    client_id = os.getenv('CLIENT_ID')
    x_cart = os.getenv('X_CART')
    
    print(f"Access Token: {access_token[:20] if access_token else 'MISSING'}...")
    print(f"Session Token: {session_token[:20] if session_token else 'MISSING'}...")
    print(f"Logged User: {logged_user}")
    print(f"Client ID: {client_id}")
    print(f"X-Cart: {x_cart[:20] if x_cart else 'MISSING'}...")
    
    if not all([access_token, session_token, logged_user, client_id, x_cart]):
        print("❌ Headers de autenticação incompletos!")
        return False
    
    # 3. Teste da estrutura do payload
    print("\n3. Testando estrutura do payload...")
    
    # Payload baseado no DevTools - usando dados mínimos
    payload_teste = {
        "customerId": int(client_id),
        "userCode": int(logged_user),
        "daysOfPlots": 28,
        "pieces": ["21", "28", "35"],
        "quantityPlots": 1,
        "sellId": 1,
        "itens": [
            {
                "id": 444212,  # Produto que sabemos que existe
                "selectedPromotionID": -1,
                "taxValue": 11.95,
                "quantityRequested": 1,
                "baseValue": 8.18,
                "totalStIvaValue": 11.95,
                "totalValue": 11.95,
                "discount": 0,
                "descontos": [],
                "discountValue": 8.18,
                "stIVA": 3.77
            }
        ]
    }
    
    print(f"Payload preparado: {json.dumps(payload_teste, indent=2)}")
    
    # 4. Teste da requisição
    print("\n4. Fazendo requisição para API...")
    
    # Headers completos baseados no DevTools
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://pedidoeletronico.servimed.com.br',
        'Referer': 'https://pedidoeletronico.servimed.com.br/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'accesstoken': access_token,
        'loggeduser': logged_user,
        'x-cart': x_cart,
        'x-peperone': str(int(time.time() * 1000)),  # Timestamp em ms
        'contenttype': 'application/json'
    }
    
    # Cookies
    cookies = {
        'accesstoken': access_token,
        'sessiontoken': session_token
    }
    
    endpoint = f"{base_url}/api/Pedido/TrasmitirPedido"
    print(f"Endpoint: {endpoint}")
    
    try:
        response = requests.post(
            endpoint,
            json=payload_teste,
            headers=headers,
            cookies=cookies,
            timeout=30,
            verify=False
        )
        
        print(f"\n📊 RESULTADO:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('executado') == 'Ok':
                    print("✅ SUCCESS: Pedido realizado com sucesso!")
                    return True
                else:
                    print(f"❌ Pedido rejeitado: {result}")
                    return False
            except:
                print("❌ Resposta não é JSON válido")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

if __name__ == "__main__":
    test_api_pedido_direto()
