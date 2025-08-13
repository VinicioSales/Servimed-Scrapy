#!/usr/bin/env python3
"""
Teste com diferentes estratégias para contornar bloqueios
"""

import requests
import json
import os
import time
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

def test_with_different_strategies():
    """Testa diferentes estratégias para acessar o servidor"""
    
    # URLs para testar
    urls = [
        "https://pedidoeletronico.servimed.com.br/",  # Portal principal
        "https://peapi.servimed.com.br/api/carrinho/oculto?siteVersion=4.0.27"  # API
    ]
    
    # Diferentes User-Agents
    user_agents = [
        # Chrome Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        # Firefox Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        # Edge Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        # Mobile Chrome
        'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
    ]
    
    for i, url in enumerate(urls):
        print(f"\n🌐 TESTANDO URL {i+1}: {url}")
        
        for j, ua in enumerate(user_agents):
            print(f"\n  🔍 User-Agent {j+1}: {ua[:50]}...")
            
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
            
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=15,
                    verify=False,
                    allow_redirects=True
                )
                
                print(f"    ✅ Status: {response.status_code}")
                print(f"    📏 Size: {len(response.content)} bytes")
                
                if response.status_code == 200:
                    print(f"    🎉 SUCESSO! URL acessível com este User-Agent")
                    if 'login' in response.text.lower() or 'servimed' in response.text.lower():
                        print(f"    🔑 Página contém elementos de login/servimed")
                    return True
                    
            except requests.exceptions.Timeout:
                print(f"    ⏱️ Timeout")
            except requests.exceptions.ConnectionError:
                print(f"    🚫 Connection Error")
            except Exception as e:
                print(f"    💥 Error: {e}")
    
    return False

def test_simple_browser_request():
    """Teste simples simulando navegador"""
    
    print(f"\n🌍 TESTE SIMPLES - SIMULANDO NAVEGADOR")
    
    session = requests.Session()
    session.verify = False
    
    # Headers que imitam navegador real
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'no-cache'
    })
    
    try:
        print(f"📍 Acessando portal principal...")
        response = session.get('https://pedidoeletronico.servimed.com.br/', timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Size: {len(response.content)} bytes")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"✅ PORTAL ACESSÍVEL!")
            
            # Extrair informações úteis
            content = response.text.lower()
            if 'login' in content:
                print(f"🔑 Página de login detectada")
            if 'api' in content:
                print(f"📡 Referências à API encontradas")
            if 'token' in content:
                print(f"🎫 Referências a tokens encontradas")
                
            return True
        else:
            print(f"❌ Falha no acesso")
            return False
            
    except Exception as e:
        print(f"💥 Erro: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTANDO CONECTIVIDADE COM SERVIMED")
    print("=" * 50)
    
    # Teste 1: Diferentes estratégias
    success1 = test_with_different_strategies()
    
    # Teste 2: Simulação simples de navegador
    success2 = test_simple_browser_request()
    
    print(f"\n📊 RESULTADOS:")
    print(f"Teste estratégias: {'✅' if success1 else '❌'}")
    print(f"Teste navegador: {'✅' if success2 else '❌'}")
    
    if success1 or success2:
        print(f"\n🎉 SERVIDOR ACESSÍVEL! Podemos continuar com o scraping.")
    else:
        print(f"\n🚫 Servidor inacessível via requests. Necessário capturar tokens do navegador.")
