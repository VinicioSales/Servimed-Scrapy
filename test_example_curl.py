#!/usr/bin/env python3
"""
Teste com os EXATOS tokens do exemplo cURL funcionando
"""

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_example_curl():
    """Testa exatamente os dados do exemplo cURL que funciona"""
    
    url = "https://peapi.servimed.com.br/api/carrinho/oculto?siteVersion=4.0.27"
    
    # Headers EXATOS do exemplo cURL
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'x-cart': '61f3a5133570647a8f31df0db83cbc648a075760a82064b14dcb8b039c6c1251',
        'x-peperone': '1753806772560',
        'Content-Type': 'application/json',
        'contentType': 'application/json',
        'loggedUser': '22850',
        'accesstoken': '9de56ce0-6c99-11f0-97a1-f768a574e337',
        'Origin': 'https://pedidoeletronico.servimed.com.br',
        'Connection': 'keep-alive',
        'Referer': 'https://pedidoeletronico.servimed.com.br/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }
    
    # Cookies EXATOS do exemplo cURL
    cookies = {
        'sessiontoken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RpZ29Vc3VhcmlvIjoyMjg1MCwidG9rZW4iOiI5ZGU1NmNlMC02Yzk5LTExZjAtOTdhMS1mNzY4YTU3NGUzMzciLCJpYXQiOjE3NTM4MDY3NzIsImV4cCI6MTc1Mzg0OTk3MiwiYXVkIjoiaHR0cDovL3NlcnZpbWVkLmNvbS5iciIsImlzcyI6IlNlcnZpbWVkIiwic3ViIjoic2VydmltZWRAU2VydmltZWQuY29tLmJyIn0.L1A0mnETOb-JZFixvyak6xf9Cq6dw_thUnL-RlWjvvqOOzcBta4ygzxtWmr49zT_WSML40jJ_dlRqVMfgIOdyg',
        'accesstoken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RpZ29Vc3VhcmlvIjoyMjg1MCwidG9rZW4iOiI5ZGU1NmNlMC02Yzk5LTExZjAtOTdhMS1mNzY4YTU3NGUzMzciLCJpYXQiOjE3NTM4MDY3NzIsImV4cCI6MTc1Mzg0OTk3MiwiYXVkIjoiaHR0cDovL3NlcnZpbWVkLmNvbS5iciIsImlzcyI6IlNlcnZpbWVkIiwic3ViIjoic2VydmltZWRAU2VydmltZWQuY29tLmJyIn0.L1A0mnETOb-JZFixvyak6xf9Cq6dw_thUnL-RlWjvvqOOzcBta4ygzxtWmr49zT_WSML40jJ_dlRqVMfgIOdyg'
    }
    
    # Payload EXATO do exemplo cURL
    payload = {
        "filtro": "dipirona",
        "pagina": 1,
        "registrosPorPagina": 20,
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
    
    print(f"🧪 Testando exemplo cURL exato...")
    print(f"URL: {url}")
    print(f"Access Token: {headers['accesstoken'][:20]}...")
    print(f"X-Cart: {headers['x-cart'][:20]}...")
    
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
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS! API funcionando com exemplo cURL!")
            print(f"📄 Total produtos: {len(data.get('products', []))}")
            print(f"📄 Total registros: {data.get('totalRecords', 0)}")
            
            if 'products' in data and len(data['products']) > 0:
                print(f"\n🛍️ Primeiro produto:")
                print(json.dumps(data['products'][0], indent=2, ensure_ascii=False))
                
            return data
            
        else:
            print(f"❌ FAILED!")
            print(f"Response: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return None

if __name__ == "__main__":
    test_example_curl()
