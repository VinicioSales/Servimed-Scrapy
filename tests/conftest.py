"""
Configurações compartilhadas para testes
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Adicionar src ao path
project_root = Path(__file__).parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

# Fixtures globais
@pytest.fixture
def mock_env_vars():
    """Mock das variáveis de ambiente para testes"""
    return {
        'ACCESS_TOKEN': 'test_access_token',
        'SESSION_TOKEN': 'test_session_token',
        'LOGGED_USER': 'test_user',
        'CLIENT_ID': '123',
        'X_CART': 'test_cart',
        'PORTAL_EMAIL': 'test@example.com',
        'PORTAL_PASSWORD': 'test_password',
        'CALLBACK_API_USER': 'callback_user',
        'CALLBACK_API_PASSWORD': 'callback_pass',
        'CALLBACK_URL': 'https://test.example.com'
    }

@pytest.fixture
def sample_product_data():
    """Dados de exemplo de um produto"""
    return {
        'codigo': '444212',
        'descricao': 'Produto de Teste',
        'preco': '19.99',
        'disponibilidade': 'Disponível',
        'fabricante': 'Teste Lab',
        'principio_ativo': 'Ácido Teste',
        'url': 'https://test.servimed.com/produto/444212'
    }

@pytest.fixture
def sample_pedido_data():
    """Dados de exemplo de um pedido"""
    return {
        'id_pedido': 'TEST123',
        'produtos': [
            {
                'gtin': '7894567890123',
                'codigo': '444212',
                'quantidade': 2
            }
        ],
        'usuario': 'test@example.com',
        'senha': 'test_password'
    }

@pytest.fixture
def mock_redis():
    """Mock do Redis para testes"""
    return Mock()

@pytest.fixture
def mock_celery_result():
    """Mock do resultado Celery"""
    result = Mock()
    result.id = 'test-task-id-123'
    result.status = 'SUCCESS'
    result.ready.return_value = True
    result.successful.return_value = True
    result.result = {'status': 'success', 'total': 1}
    return result
