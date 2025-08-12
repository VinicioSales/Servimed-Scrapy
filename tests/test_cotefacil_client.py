import pytest
import sys
import os

# Adicionar projeto ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

from servimed_scraper.servimed_scraper.clients.cotefacil_client import CotefacilApiClient


class TestCotefacilClient:
    """Testes para o cliente da API Cotefácil"""
    
    @pytest.fixture
    def client(self):
        """Fixture para cliente API"""
        return CotefacilApiClient()
    
    def test_client_initialization(self, client):
        """Testar inicialização do cliente"""
        assert client.username is not None
        assert client.password is not None
        assert client.client_id is not None
        assert client.client_secret is not None
        assert client.base_url is not None
    
    def test_authentication(self, client):
        """Testar autenticação OAuth2"""
        result = client.authenticate()
        assert isinstance(result, bool)
        if result:
            assert client.access_token is not None
    
    def test_get_products(self, client):
        """Testar busca de produtos"""
        products = client.get_products()
        assert isinstance(products, list)
        # API pode estar vazia, então só verificamos o tipo
    
    def test_signup_method_exists(self, client):
        """Verificar se método signup existe"""
        assert hasattr(client, 'signup')
        assert callable(getattr(client, 'signup'))
    
    def test_callback_methods_exist(self, client):
        """Verificar se métodos de callback existem"""
        assert hasattr(client, 'send_products_to_callback')
        assert hasattr(client, 'send_order_confirmation')
        assert callable(getattr(client, 'send_products_to_callback'))
        assert callable(getattr(client, 'send_order_confirmation'))
