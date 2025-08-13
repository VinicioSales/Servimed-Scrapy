#!/usr/bin/env python3
"""
Teste de login com as credenciais do desafio
Email: juliano@farmaprevonline.com.br  
Senha: a007299A
"""

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_login():
    """Testa login com as credenciais do desafio"""
    
    # Credenciais do desafio
    email = "juliano@farmaprevonline.com.br"
    password = "a007299A"
    
    login_url = "https://peapi.servimed.com.br/api/Usuario/Login"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://pedidoeletronico.servimed.com.br',
        'Referer': 'https://pedidoeletronico.servimed.com.br/',
        'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    
    payload = {
        "login": email,
        "senha": password
    }
    
    print(f"🔐 Testando login com credenciais do desafio...")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"URL: {login_url}")
    
    try:
        response = requests.post(
            login_url,
            headers=headers,
            json=payload,
            timeout=10,
            verify=False
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ LOGIN SUCCESSFUL!")
            print(f"📄 Response Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Extrair tokens se disponíveis
            if 'accesstoken' in data:
                print(f"\n🔑 ACCESS_TOKEN: {data['accesstoken']}")
                
            if 'sessiontoken' in data:
                print(f"🔑 SESSION_TOKEN: {data['sessiontoken']}")
                
            # Verificar cookies de resposta
            if response.cookies:
                print(f"\n🍪 Response Cookies:")
                for cookie in response.cookies:
                    print(f"  {cookie.name} = {cookie.value}")
                    
            return data
            
        else:
            print(f"❌ LOGIN FAILED!")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return None

if __name__ == "__main__":
    test_login()
