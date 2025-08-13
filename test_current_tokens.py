#!/usr/bin/env python3
"""
Teste rápido dos nossos tokens atuais
"""

import requests
import json
import os
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

def test_current_tokens():
    """Testa se nossos tokens atuais ainda funcionam"""
    
    url = "https://peapi.servimed.com.br/api/carrinho/oculto?siteVersion=4.0.27"
    
    # Usar nossos tokens do .env
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_jwt = os.getenv('ACCESS_TOKEN_JWT')
    session_token = os.getenv('SESSION_TOKEN')
    logged_user = os.getenv('LOGGED_USER')
    x_cart = os.getenv('X_CART')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'accesstoken': access_token,
        'loggeduser': logged_user,
        'x-cart': x_cart,
        'x-peperone': '1755090891000',
        'Origin': 'https://pedidoeletronico.servimed.com.br',
        'Referer': 'https://pedidoeletronico.servimed.com.br/',
        'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    
    cookies = {
        'accesstoken': access_token_jwt,
        'sessiontoken': session_token,
        '_ga': 'GA1.1.1496905904.1755017918',
        '_ga_0684EZD6WN': 'GS2.1.s1755087487$o8$g1$t1755089675$j38$l0$h0',
        '_ga_TGSHLZ7V8G': 'GS2.3.s1755018324$o1$g1$t1755018332$j52$l0$h0',
        '_gat': '1',
        '_gid': 'GA1.3.808374586.1755017918'
    }
    
    payload = {
        "filtro": "",
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
    
    print(f"🧪 Testando nossos tokens atuais...")
    print(f"Access Token: {access_token[:20]}...")
    print(f"Session Token: {session_token[:50]}...")
    
    try:
        response = requests.post(
            url,
            headers=headers,
            cookies=cookies,
            json=payload,
            timeout=10,
            verify=False
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Tokens ainda válidos!")
            print(f"📄 Total produtos: {len(data.get('products', []))}")
            print(f"📄 Total registros: {data.get('totalRecords', 0)}")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    test_current_tokens()
