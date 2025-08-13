#!/usr/bin/env python3
"""Teste isolado do callback API"""

import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Carregar produtos do arquivo
with open('data/servimed_produtos_scrapy.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

produtos = dados.get('produtos', [])
print(f"Produtos carregados: {len(produtos)}")

# Converter para o formato correto do callback
produtos_callback = []
for produto in produtos[:3]:  # Testar apenas 3 produtos
    produto_callback = {
        "gtin": str(produto.get('gtin', '')),
        "codigo": str(produto.get('codigo', '')),
        "descricao": str(produto.get('descricao', '')),
        "preco_fabrica": float(produto.get('preco_fabrica', 0.0)),
        "estoque": int(produto.get('estoque', 0))
    }
    produtos_callback.append(produto_callback)

print(f"\n=== PRODUTOS CONVERTIDOS PARA CALLBACK ===")
print(json.dumps(produtos_callback, indent=2, ensure_ascii=False))

# Testar autenticação OAuth2
print(f"\n=== TESTANDO AUTENTICAÇÃO ===")
auth_data = {
    "username": os.getenv('PORTAL_EMAIL'),
    "password": os.getenv('PORTAL_PASSWORD'),
    "client_id": os.getenv('CLIENT_ID'),
    "client_secret": os.getenv('CLIENT_SECRET'),
    "grant_type": "password"
}

print(f"Username: {auth_data['username']}")
print(f"Client ID: {auth_data['client_id']}")

try:
    # Autenticar
    auth_response = requests.post(
        "https://desafio.cotefacil.net/oauth/token",
        data=auth_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        timeout=30
    )
    
    print(f"Status da autenticação: {auth_response.status_code}")
    print(f"Resposta: {auth_response.text}")
    
    if auth_response.status_code == 200:
        token_info = auth_response.json()
        access_token = token_info.get("access_token")
        
        if access_token:
            print(f"✅ Token obtido: {access_token[:50]}...")
            
            # Testar envio de produtos
            print(f"\n=== TESTANDO ENVIO DE PRODUTOS ===")
            
            produto_response = requests.post(
                "https://desafio.cotefacil.net/produto",
                json=produtos_callback,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=60
            )
            
            print(f"Status do envio: {produto_response.status_code}")
            print(f"Headers da resposta: {dict(produto_response.headers)}")
            print(f"Resposta: {produto_response.text}")
            
            if produto_response.status_code == 201:
                print("✅ PRODUTOS ENVIADOS COM SUCESSO!")
            else:
                print("❌ ERRO NO ENVIO DOS PRODUTOS")
        else:
            print("❌ Token não encontrado na resposta")
    else:
        print("❌ FALHA NA AUTENTICAÇÃO")
        
except Exception as e:
    print(f"❌ ERRO: {e}")
