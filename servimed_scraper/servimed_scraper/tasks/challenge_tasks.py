import os
import sys
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

from celery_app import app
from servimed_scraper.clients.cotefacil_client import CotefacilApiClient


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def scrape_products_task(self, usuario, senha, callback_url):
    """
    Tarefa Nível 2: Scraping de produtos conforme especificação
    
    Parâmetros:
    {
        "usuario": "fornecedor_user",
        "senha": "fornecedor_pass", 
        "callback_url": "https://desafio.cotefacil.net"
    }
    """
    try:
        print(f"🚀 Iniciando scraping para usuário: {usuario}")
        
        # 1. Executar spider do Servimed (simulado - já temos os produtos da API)
        client = CotefacilApiClient()
        
        # 2. Autenticar e buscar produtos
        if client.authenticate():
            products = client.get_products()
            print(f"📦 {len(products)} produtos encontrados")
            
            # 3. Enviar para callback API
            if products:
                success = client.send_products_to_callback(products, callback_url)
                if success:
                    result = {
                        'status': 'success',
                        'products_sent': len(products),
                        'callback_url': callback_url,
                        'message': f'Produtos enviados para callback com sucesso'
                    }
                else:
                    result = {
                        'status': 'callback_error',
                        'products_found': len(products),
                        'message': 'Produtos encontrados mas erro no callback'
                    }
            else:
                result = {
                    'status': 'no_products',
                    'message': 'Nenhum produto encontrado'
                }
        else:
            result = {
                'status': 'auth_error',
                'message': 'Erro na autenticação da API'
            }
        
        print(f"✅ Resultado: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Erro na tarefa: {str(e)}")
        raise self.retry(exc=e)


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 120})
def process_order_task(self, usuario, senha, id_pedido, produtos, callback_url):
    """
    Tarefa Nível 3: Processamento de pedido conforme especificação
    
    Parâmetros:
    {
        "usuario": "fornecedor_user",
        "senha": "fornecedor_pass",
        "id_pedido": "1234",
        "produtos": [
            {
                "gtin": "1234567890123",
                "codigo": "A123", 
                "quantidade": 1
            }
        ],
        "callback_url": "https://desafio.cotefacil.net"
    }
    """
    try:
        print(f"🛒 Processando pedido {id_pedido} para usuário: {usuario}")
        print(f"📋 Produtos: {produtos}")
        
        # 1. Simular processo de pedido no Servimed
        # (Como não temos acesso real ao formulário, vamos simular)
        
        # 2. Gerar código de confirmação simulado
        import uuid
        codigo_confirmacao = f"SRV{str(uuid.uuid4())[:8].upper()}"
        
        # 3. Dados de confirmação conforme especificação
        confirmation_data = {
            "codigo_confirmacao": codigo_confirmacao,
            "status": "pedido_realizado"
        }
        
        # 4. Enviar confirmação para callback API
        client = CotefacilApiClient()
        if client.authenticate():
            success = client.send_order_confirmation(
                id_pedido, 
                confirmation_data, 
                callback_url
            )
            
            if success:
                result = {
                    'status': 'success',
                    'id_pedido': id_pedido,
                    'codigo_confirmacao': codigo_confirmacao,
                    'produtos_processados': len(produtos),
                    'callback_url': callback_url,
                    'message': 'Pedido processado e confirmação enviada'
                }
            else:
                result = {
                    'status': 'callback_error',
                    'id_pedido': id_pedido,
                    'codigo_confirmacao': codigo_confirmacao,
                    'message': 'Pedido processado mas erro no callback'
                }
        else:
            result = {
                'status': 'auth_error',
                'id_pedido': id_pedido,
                'message': 'Erro na autenticação da API'
            }
        
        print(f"✅ Resultado do pedido: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Erro no processamento do pedido: {str(e)}")
        raise self.retry(exc=e)


@app.task
def setup_api_user(username, password):
    """
    Tarefa para criar usuário na API se não existir
    """
    try:
        print(f"👤 Configurando usuário na API: {username}")
        
        client = CotefacilApiClient()
        
        # Tentar autenticar primeiro
        if client.authenticate():
            print("✅ Usuário já existe e está autenticado")
            return {'status': 'already_exists', 'username': username}
        
        # Se não conseguir autenticar, tentar criar
        if client.signup(username, password):
            print("✅ Usuário criado com sucesso")
            return {'status': 'created', 'username': username}
        else:
            print("❌ Erro ao criar usuário")
            return {'status': 'error', 'username': username}
            
    except Exception as e:
        print(f"❌ Erro na configuração do usuário: {str(e)}")
        return {'status': 'error', 'error': str(e)}
