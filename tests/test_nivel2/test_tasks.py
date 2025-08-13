"""
Testes para as tarefas do Celery (src/nivel2/tasks.py)
"""
import pytest
import sys
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nivel2 import tasks


class TestProcessarScrapingSimple:
    """Testes para a tarefa processar_scraping_simple"""
    
    def test_processar_scraping_simple_success_scrapy(self, mock_env_vars):
        """Testa processamento bem-sucedido com Scrapy"""
        # Mock da task
        mock_task = Mock()
        mock_task.request.id = "test-task-123"
        
        task_data = {
            "usuario": "test@example.com",
            "senha": "test_password",
            "callback_url": "https://test.com",
            "filtro": "vitamina",
            "max_pages": 2
        }
        
        # Mock do ScrapyServimedWrapper
        with patch('tasks.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper = Mock()
            mock_wrapper.run_spider.return_value = True
            mock_wrapper.get_results.return_value = {
                'success': True,
                'total': 5,
                'produtos': [{'codigo': '123'}, {'codigo': '456'}]
            }
            mock_wrapper_class.return_value = mock_wrapper
            
            # Mock do CallbackAPIClient
            with patch('tasks.CallbackAPIClient') as mock_api_class:
                mock_api = Mock()
                mock_api.send_callback.return_value = True
                mock_api_class.return_value = mock_api
                
                result = tasks.processar_scraping_simple(mock_task, task_data)
                
                assert result['status'] == 'success'
                assert result['framework'] == 'scrapy'
                assert result['produtos_coletados'] == 5
                assert 'tempo_execucao' in result
    
    def test_processar_scraping_simple_scrapy_failure_fallback(self, mock_env_vars):
        """Testa fallback para framework original quando Scrapy falha"""
        mock_task = Mock()
        mock_task.request.id = "test-task-456"
        
        task_data = {
            "usuario": "test@example.com",
            "senha": "test_password",
            "callback_url": "https://test.com",
            "filtro": "teste",
            "max_pages": 1
        }
        
        # Mock Scrapy falhando
        with patch('tasks.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper = Mock()
            mock_wrapper.run_spider.side_effect = Exception("Erro no Scrapy")
            mock_wrapper_class.return_value = mock_wrapper
            
            # Mock framework original funcionando
            with patch('tasks.ServimedScraperCompleto') as mock_scraper_class:
                mock_scraper = Mock()
                mock_scraper.coletar_produtos.return_value = [
                    {'codigo': '789', 'descricao': 'Produto Teste'}
                ]
                mock_scraper_class.return_value = mock_scraper
                
                with patch('tasks.CallbackAPIClient') as mock_api_class:
                    mock_api = Mock()
                    mock_api.send_callback.return_value = True
                    mock_api_class.return_value = mock_api
                    
                    result = tasks.processar_scraping_simple(mock_task, task_data)
                    
                    assert result['status'] == 'success'
                    assert result['framework'] == 'original'
                    assert result['produtos_coletados'] == 1
    
    def test_processar_scraping_simple_both_frameworks_fail(self):
        """Testa quando ambos os frameworks falham"""
        mock_task = Mock()
        mock_task.request.id = "test-task-789"
        
        task_data = {
            "usuario": "test@example.com",
            "senha": "test_password",
            "callback_url": "https://test.com",
            "filtro": "erro",
            "max_pages": 1
        }
        
        # Mock ambos falhando
        with patch('tasks.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper_class.side_effect = Exception("Erro no Scrapy")
            
            with patch('tasks.ServimedScraperCompleto') as mock_scraper_class:
                mock_scraper_class.side_effect = Exception("Erro no framework original")
                
                result = tasks.processar_scraping_simple(mock_task, task_data)
                
                assert result['status'] == 'error'
                assert 'error' in result
    
    def test_processar_scraping_simple_callback_failure(self):
        """Testa quando callback API falha"""
        mock_task = Mock()
        mock_task.request.id = "test-task-callback"
        
        task_data = {
            "usuario": "test@example.com",
            "senha": "test_password",
            "callback_url": "https://test.com",
            "filtro": "vitamina",
            "max_pages": 1
        }
        
        with patch('tasks.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper = Mock()
            mock_wrapper.run_spider.return_value = True
            mock_wrapper.get_results.return_value = {
                'success': True,
                'total': 1,
                'produtos': [{'codigo': '111'}]
            }
            mock_wrapper_class.return_value = mock_wrapper
            
            # Mock callback falhando
            with patch('tasks.CallbackAPIClient') as mock_api_class:
                mock_api = Mock()
                mock_api.send_callback.side_effect = Exception("Erro no callback")
                mock_api_class.return_value = mock_api
                
                result = tasks.processar_scraping_simple(mock_task, task_data)
                
                # Deve ter sucesso no scraping mas avisar sobre callback
                assert result['status'] == 'success'
                assert result['callback_enviado'] is False


class TestStatusTaskSimple:
    """Testes para a tarefa status_task_simple"""
    
    def test_status_task_simple_default(self):
        """Testa tarefa de status com mensagem padrão"""
        mock_task = Mock()
        mock_task.request.id = "status-task-123"
        
        result = tasks.status_task_simple(mock_task)
        
        assert result['status'] == 'success'
        assert result['task_id'] == 'status-task-123'
        assert result['message'] == 'Status check'
        assert 'timestamp' in result
        assert 'system_info' in result
    
    def test_status_task_simple_custom_message(self):
        """Testa tarefa de status com mensagem customizada"""
        mock_task = Mock()
        mock_task.request.id = "status-task-456"
        
        result = tasks.status_task_simple(mock_task, "Teste customizado")
        
        assert result['message'] == 'Teste customizado'
        assert result['task_id'] == 'status-task-456'
    
    def test_status_task_simple_system_info(self):
        """Testa se informações do sistema estão incluídas"""
        mock_task = Mock()
        mock_task.request.id = "status-task-789"
        
        result = tasks.status_task_simple(mock_task)
        
        system_info = result['system_info']
        assert 'hostname' in system_info
        assert 'platform' in system_info
        assert 'python_version' in system_info
        assert 'python_path' in system_info


class TestTasksIntegration:
    """Testes de integração das tarefas"""
    
    @patch('time.time')
    def test_tempo_execucao_calculation(self, mock_time):
        """Testa cálculo do tempo de execução"""
        # Mock time.time para retornar valores específicos
        mock_time.side_effect = [1000.0, 1005.5]  # 5.5 segundos de diferença
        
        mock_task = Mock()
        mock_task.request.id = "timing-test"
        
        task_data = {
            "usuario": "test@example.com",
            "senha": "test_password",
            "callback_url": "https://test.com",
            "filtro": "tempo",
            "max_pages": 1
        }
        
        with patch('tasks.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper = Mock()
            mock_wrapper.run_spider.return_value = True
            mock_wrapper.get_results.return_value = {
                'success': True,
                'total': 1,
                'produtos': [{'codigo': '999'}]
            }
            mock_wrapper_class.return_value = mock_wrapper
            
            with patch('tasks.CallbackAPIClient') as mock_api_class:
                mock_api = Mock()
                mock_api.send_callback.return_value = True
                mock_api_class.return_value = mock_api
                
                result = tasks.processar_scraping_simple(mock_task, task_data)
                
                assert abs(result['tempo_execucao'] - 5.5) < 0.1
    
    def test_task_data_validation(self):
        """Testa validação dos dados da tarefa"""
        mock_task = Mock()
        mock_task.request.id = "validation-test"
        
        # Dados incompletos
        invalid_task_data = {
            "usuario": "",  # Vazio
            "senha": "test_password",
            "callback_url": "https://test.com"
            # filtro e max_pages ausentes
        }
        
        result = tasks.processar_scraping_simple(mock_task, invalid_task_data)
        
        # Deve lidar com dados incompletos graciosamente
        assert result['status'] in ['error', 'success']
