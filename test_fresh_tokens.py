#!/usr/bin/env python3
"""Teste direto com requests usando tokens frescos"""

import requests
import json
import os
from dotenv import load_dotenv

# Carregar tokens do .env
load_dotenv()

url = "https://peapi.servimed.com.br/api/carrinho/oculto"
params = {"siteVersion": "4.0.27"}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8",
    "access-control-allow-credentials": "true",
    "access-control-allow-headers": "Origin,X-Requested-With,Content-Type,Accept,Authorization,cache-control,x-cart",
    "access-control-allow-methods": "GET, POST, OPTIONS, PUT, PATCH, DELETE",
    "access-control-allow-origin": "*",
    "accesstoken": os.getenv("ACCESS_TOKEN"),
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://pedidoeletronico.servimed.com.br",
    "referer": "https://pedidoeletronico.servimed.com.br/",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sessiontoken": os.getenv("SESSION_TOKEN"),
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-cart": os.getenv("X_CART")
}

cookies = {
    "accesstoken": os.getenv("ACCESS_TOKEN"),
    "sessiontoken": os.getenv("SESSION_TOKEN"),
    "user": "22850",
    "_ga": "GA1.3.1433953037.1755090889",
    "_gid": "GA1.3.1013264097.1755090889",
    "_ga_JBRP3MHFXT": "GS1.3.1755090889.1.1.1755092008.0.0.0"
}

payload = {
    "filtro": "",  # Sem filtro para testar
    "pagina": 1,
    "registrosPorPagina": 25,
    "ordenarDecrescente": False,
    "colunaOrdenacao": "nenhuma",
    "clienteId": 267511,
    "tipoVendaId": 1,
    "fabricanteIdFiltro": 0,
    "pIIdFiltro": 0,
    "cestaPPFiltro": False,
    "codigoExterno": 0,
    "codigoUsuario": 22850,
    "promocaoSelecionada": "",
    "indicadorTipoUsuario": "CLI",
    "kindUser": 0,
    "xlsx": [],
    "principioAtivo": "",
    "master": False,
    "kindSeller": 0,
    "grupoEconomico": "",
    "users": [518565, 267511],
    "list": True
}

print("=== TESTE COM REQUESTS E TOKENS FRESCOS ===")
print(f"URL: {url}")
print(f"Payload filtro: {payload['filtro']}")
print(f"Access Token: {os.getenv('ACCESS_TOKEN')[:20]}...")
print()

try:
    response = requests.post(
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        json=payload,
        timeout=15,
        verify=False  # Desabilita verificação SSL
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Size: {len(response.content)} bytes")
    print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
    
    if response.status_code == 200:
        data = response.json()
        produtos = data.get('produtos', [])
        print(f"✅ SUCESSO! {len(produtos)} produtos encontrados")
        
        if produtos:
            print("\n=== EXEMPLO DE PRODUTO ===")
            produto = produtos[0]
            print(f"Código: {produto.get('codigo', 'N/A')}")
            print(f"Nome: {produto.get('nome', 'N/A')}")
            print(f"Preço: R$ {produto.get('preco', 'N/A')}")
            print(f"Fabricante: {produto.get('fabricante', 'N/A')}")
    else:
        print(f"❌ ERRO: HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ ERRO DE REQUISIÇÃO: {e}")
