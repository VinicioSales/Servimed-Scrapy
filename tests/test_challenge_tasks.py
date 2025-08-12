import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Adicionar projeto ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

from servimed_scraper.servimed_scraper.tasks.challenge_tasks import (
    scrape_products_task,
    process_order_task,
    setup_api_user
)


class TestChallengeTasks:
    """Testes para as tarefas do desafio"""
    
    @patch('servimed_scraper.servimed_scraper.tasks.challenge_tasks.CotefacilApiClient')
    def test_scrape_products_task_success(self, mock_client_class):
        """Testar tarefa de scraping com sucesso"""
        # Mock do cliente
        mock_client = MagicMock()
        mock_client.authenticate.return_value = True
        mock_client.get_products.return_value = [
            {'gtin': '123', 'codigo': 'A123', 'descricao': 'Teste'}
        ]
        mock_client.send_products_to_callback.return_value = True
        mock_client_class.return_value = mock_client
        
        # Executar tarefa
        result = scrape_products_task(
            usuario="test",
            senha="test", 
            callback_url="http://test.com"
        )
        
        # Verificações
        assert result['status'] == 'success'
        assert result['products_sent'] == 1
        mock_client.authenticate.assert_called_once()
        mock_client.get_products.assert_called_once()
    
    @patch('servimed_scraper.servimed_scraper.tasks.challenge_tasks.CotefacilApiClient')
    def test_process_order_task_success(self, mock_client_class):
        """Testar tarefa de pedido com sucesso"""
        # Mock do cliente
        mock_client = MagicMock()
        mock_client.authenticate.return_value = True
        mock_client.send_order_confirmation.return_value = True
        mock_client_class.return_value = mock_client
        
        # Dados do pedido
        produtos = [{'gtin': '123', 'codigo': 'A123', 'quantidade': 1}]
        
        # Executar tarefa
        result = process_order_task(
            usuario="test",
            senha="test",
            id_pedido="PED123",
            produtos=produtos,
            callback_url="http://test.com"
        )
        
        # Verificações
        assert result['status'] == 'success'
        assert result['id_pedido'] == 'PED123'
        assert 'codigo_confirmacao' in result
        mock_client.authenticate.assert_called_once()
        mock_client.send_order_confirmation.assert_called_once()
    
    @patch('servimed_scraper.servimed_scraper.tasks.challenge_tasks.CotefacilApiClient')
    def test_setup_api_user_existing(self, mock_client_class):
        """Testar configuração de usuário existente"""
        # Mock do cliente
        mock_client = MagicMock()
        mock_client.authenticate.return_value = True
        mock_client_class.return_value = mock_client
        
        # Executar tarefa
        result = setup_api_user(username="test", password="test")
        
        # Verificações
        assert result['status'] == 'already_exists'
        assert result['username'] == 'test'
        mock_client.authenticate.assert_called_once()
    
    @patch('servimed_scraper.servimed_scraper.tasks.challenge_tasks.CotefacilApiClient')
    def test_setup_api_user_new(self, mock_client_class):
        """Testar criação de novo usuário"""
        # Mock do cliente
        mock_client = MagicMock()
        mock_client.authenticate.return_value = False
        mock_client.signup.return_value = True
        mock_client_class.return_value = mock_client
        
        # Executar tarefa
        result = setup_api_user(username="newuser", password="newpass")
        
        # Verificações
        assert result['status'] == 'created'
        assert result['username'] == 'newuser'
        mock_client.authenticate.assert_called_once()
        mock_client.signup.assert_called_once_with("newuser", "newpass")
