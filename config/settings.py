"""
Configurações do Servimed Scraper
=================================

Carrega variáveis de ambiente do arquivo .env e define configurações
"""

import os
from pathlib import Path

def load_env():
    """Carrega variáveis do arquivo .env"""
    env_path = Path(__file__).parent.parent / '.env'
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    else:
        print("AVISO: Arquivo .env nao encontrado!")
        print("Crie o arquivo .env com as variaveis necessarias.")
        raise FileNotFoundError("Arquivo .env e obrigatorio")
    
    return env_vars

# Carrega variáveis do .env
env_vars = load_env()

# TOKENS DE AUTENTICAÇÃO (do arquivo .env)
ACCESS_TOKEN = env_vars.get('ACCESS_TOKEN')
SESSION_TOKEN = env_vars.get('SESSION_TOKEN')

# CONFIGURAÇÕES DO USUÁRIO (do arquivo .env)
LOGGED_USER = env_vars.get('LOGGED_USER')
CLIENT_ID = int(env_vars.get('CLIENT_ID', 0))
X_CART = env_vars.get('X_CART')

# USUÁRIOS (converte string para lista)
users_str = env_vars.get('USERS', '')
USERS = [int(x.strip()) for x in users_str.split(',') if x.strip().isdigit()]

# CREDENCIAIS DO PORTAL (do arquivo .env)
PORTAL_EMAIL = env_vars.get('PORTAL_EMAIL')
PORTAL_PASSWORD = env_vars.get('PORTAL_PASSWORD')

# URLs (do arquivo .env)
PORTAL_URL = env_vars.get('PORTAL_URL', 'https://pedidoeletronico.servimed.com.br')
BASE_URL = env_vars.get('BASE_URL', 'https://peapi.servimed.com.br')
API_ENDPOINT = env_vars.get('API_ENDPOINT', '/api/carrinho/oculto')
SITE_VERSION = env_vars.get('SITE_VERSION', '4.0.27')

# CONFIGURAÇÕES DE SCRAPING (não sensíveis)
RECORDS_PER_PAGE = 25  # Produtos por página (máximo 25)
DELAY_BETWEEN_REQUESTS = 2  # Segundos entre requisições
TIMEOUT_SECONDS = 30  # Timeout para requisições HTTP

# CONFIGURAÇÕES AVANÇADAS (não sensíveis)
VERIFY_SSL = False  # Verificar certificados SSL
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"

def validate_config():
    """Valida se todas as variáveis obrigatórias estão definidas"""
    required_vars = {
        'ACCESS_TOKEN': ACCESS_TOKEN,
        'SESSION_TOKEN': SESSION_TOKEN,
        'LOGGED_USER': LOGGED_USER,
        'CLIENT_ID': CLIENT_ID,
        'X_CART': X_CART,
        'PORTAL_EMAIL': PORTAL_EMAIL,
        'PORTAL_PASSWORD': PORTAL_PASSWORD
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    
    if missing_vars:
        print("ERRO: Variaveis obrigatorias nao encontradas no .env:")
        for var in missing_vars:
            print(f"   - {var}")
        raise ValueError("Configuracao incompleta")
    
    print("Configuracao carregada com sucesso!")
    print(f"Usuario: {PORTAL_EMAIL}")
    print(f"Token valido ate: Wed Aug 13 09:48:17 2025")

# Executa validação ao importar
if __name__ != "__main__":
    validate_config()
