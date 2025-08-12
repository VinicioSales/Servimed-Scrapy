import requests
import json

def test_api():
    """Testar API local"""
    base_url = "http://localhost:8000"
    
    print("🧪 TESTANDO API SERVIMED SCRAPER")
    print("=" * 50)
    
    try:
        # Teste 1: Endpoint raiz
        print("📍 1. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        print()
        
        # Teste 2: Health check
        print("🏥 2. Testando health check...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        print()
        
        # Teste 3: Endpoint de teste
        print("🧪 3. Testando endpoint de teste...")
        response = requests.get(f"{base_url}/test")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        print()
        
        # Teste 4: Scraping
        print("🕷️ 4. Testando scraping...")
        scrape_data = {"username": None, "password": None}
        response = requests.post(f"{base_url}/scrape", json=scrape_data)
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        print()
        
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando em http://localhost:8000")
        print("   Certifique-se de que a API foi iniciada com: python test_api.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_api()
