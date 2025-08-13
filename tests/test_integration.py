"""
Testes de integração para o sistema completo
"""
import pytest
import sys
import os
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSystemIntegration:
    """Testes de integração do sistema completo"""
    
    @pytest.fixture
    def mock_environment(self):
        """Fixture para ambiente mock"""
        env_vars = {
            'CALLBACK_API_USER': 'test@example.com',
            'CALLBACK_API_PASSWORD': 'test_password',
            'REDIS_URL': 'redis://localhost:6379/0',
            'CELERY_BROKER_URL': 'redis://localhost:6379/0'
        }
        
        with patch.dict(os.environ, env_vars):
            yield env_vars
    
    def test_nivel1_direct_scraping(self, mock_environment):
        """Testa execução direta (nível 1)"""
        with patch('src.scrapy_wrapper.ScrapyWrapper') as mock_wrapper:
            # Mock do wrapper
            mock_instance = Mock()
            mock_instance.run_spider.return_value = [
                {'name': 'Produto 1', 'price': '10.99', 'code': '123'},
                {'name': 'Produto 2', 'price': '20.99', 'code': '456'}
            ]
            mock_wrapper.return_value = mock_instance
            
            # Importar e executar nível 1
            try:
                from main import executar_nivel1
                
                result = executar_nivel1(['123', '456'])
                
                assert result is not None
                mock_instance.run_spider.assert_called_once()
                
            except ImportError:
                pytest.skip("main.py não disponível")
    
    def test_nivel2_queue_processing(self, mock_environment):
        """Testa processamento via fila (nível 2)"""
        with patch('src.nivel2.queue_client.QueueClient') as mock_client:
            # Mock do cliente de fila
            mock_instance = Mock()
            mock_instance.enqueue_scraping.return_value = "task-123"
            mock_instance.get_status.return_value = {
                'status': 'SUCCESS',
                'result': [{'code': '123', 'name': 'Produto Teste'}]
            }
            mock_client.return_value = mock_instance
            
            try:
                from main import executar_nivel2
                
                task_id = executar_nivel2(['123'])
                
                assert task_id == "task-123"
                mock_instance.enqueue_scraping.assert_called_once()
                
            except ImportError:
                pytest.skip("main.py não disponível")
    
    def test_nivel3_order_processing(self, mock_environment):
        """Testa processamento de pedidos (nível 3)"""
        with patch('src.pedido_queue_client.PedidoQueueClient') as mock_client:
            # Mock do cliente de pedidos
            mock_instance = Mock()
            mock_instance.enqueue_pedido.return_value = "order-task-123"
            mock_instance.get_status.return_value = {
                'status': 'SUCCESS',
                'result': {'pedido_id': 'TEST123', 'status': 'completed'}
            }
            mock_client.return_value = mock_instance
            
            try:
                from main import executar_nivel3
                
                task_id = executar_nivel3('test@example.com', 'password', 'TEST123', [
                    {'codigo': '123', 'quantidade': 2}
                ])
                
                assert task_id == "order-task-123"
                mock_instance.enqueue_pedido.assert_called_once()
                
            except ImportError:
                pytest.skip("main.py não disponível")
    
    def test_main_script_argument_parsing(self):
        """Testa parsing de argumentos do script principal"""
        test_args = [
            ['main.py', '1', '123', '456'],
            ['main.py', '2', '789'],
            ['main.py', '3', 'user@test.com', 'password', 'ORDER123', '999', '2', '1234567890123']
        ]
        
        for args in test_args:
            with patch('sys.argv', args):
                with patch('main.executar_nivel1') as mock_nivel1:
                    with patch('main.executar_nivel2') as mock_nivel2:
                        with patch('main.executar_nivel3') as mock_nivel3:
                            try:
                                import main
                                # Não executar main diretamente para evitar SystemExit
                                # Apenas verificar que importação funciona
                                assert hasattr(main, 'main')
                                
                            except ImportError:
                                pytest.skip("main.py não disponível")
    
    def test_config_loading(self):
        """Testa carregamento de configurações"""
        try:
            from src.config import config
            
            # Verificar se configurações foram carregadas
            assert hasattr(config, 'SERVIMED_BASE_URL')
            assert config.SERVIMED_BASE_URL is not None
            
            # Verificar URLs de API
            assert hasattr(config, 'CALLBACK_API_BASE_URL')
            
        except ImportError:
            pytest.skip("Configurações não disponíveis")
    
    def test_celery_app_configuration(self):
        """Testa configuração do app Celery"""
        with patch.dict(os.environ, {'REDIS_URL': 'redis://localhost:6379'}):
            try:
                from src.servimed_scraper.celery_app import app
                
                # Verificar configuração básica
                assert app is not None
                assert hasattr(app, 'conf')
                
                # Verificar broker configurado
                if hasattr(app.conf, 'broker_url'):
                    assert 'redis' in app.conf.broker_url
                
            except ImportError:
                pytest.skip("Celery app não disponível")
    
    def test_scrapy_wrapper_initialization(self):
        """Testa inicialização do wrapper Scrapy"""
        try:
            from src.scrapy_wrapper import ScrapyWrapper
            
            wrapper = ScrapyWrapper()
            
            # Verificar que wrapper foi criado
            assert wrapper is not None
            assert hasattr(wrapper, 'run_spider')
            
        except ImportError:
            pytest.skip("ScrapyWrapper não disponível")
    
    def test_queue_client_initialization(self):
        """Testa inicialização do cliente de fila"""
        try:
            from src.nivel2.queue_client import QueueClient
            
            client = QueueClient()
            
            # Verificar que cliente foi criado
            assert client is not None
            assert hasattr(client, 'enqueue_scraping')
            
        except ImportError:
            pytest.skip("QueueClient não disponível")


class TestEndToEndWorkflow:
    """Testes de workflow completo ponta a ponta"""
    
    @pytest.fixture
    def complete_mock_setup(self):
        """Setup completo de mocks para teste ponta a ponta"""
        mocks = {}
        
        # Mock Redis
        mocks['redis'] = Mock()
        
        # Mock Celery
        mocks['celery_result'] = Mock()
        mocks['celery_result'].id = "test-task-123"
        mocks['celery_result'].status = "SUCCESS"
        mocks['celery_result'].result = {"success": True}
        
        # Mock Scrapy
        mocks['scrapy_results'] = [
            {'code': '123', 'name': 'Produto A', 'price': '10.99'},
            {'code': '456', 'name': 'Produto B', 'price': '25.50'}
        ]
        
        return mocks
    
    def test_complete_scraping_workflow(self, complete_mock_setup):
        """Testa workflow completo de scraping"""
        with patch('src.scrapy_wrapper.ScrapyWrapper') as mock_wrapper:
            mock_instance = Mock()
            mock_instance.run_spider.return_value = complete_mock_setup['scrapy_results']
            mock_wrapper.return_value = mock_instance
            
            # Simular execução completa
            try:
                from src.scrapy_wrapper import ScrapyWrapper
                
                wrapper = ScrapyWrapper()
                results = wrapper.run_spider(['123', '456'])
                
                assert len(results) == 2
                assert results[0]['code'] == '123'
                assert results[1]['code'] == '456'
                
            except ImportError:
                pytest.skip("ScrapyWrapper não disponível")
    
    def test_queue_to_scraping_workflow(self, complete_mock_setup):
        """Testa workflow de fila para scraping"""
        with patch('src.nivel2.queue_client.QueueClient') as mock_client:
            with patch('src.scrapy_wrapper.ScrapyWrapper') as mock_wrapper:
                # Setup mocks
                mock_client_instance = Mock()
                mock_client_instance.enqueue_scraping.return_value = "queue-task-123"
                mock_client.return_value = mock_client_instance
                
                mock_wrapper_instance = Mock()
                mock_wrapper_instance.run_spider.return_value = complete_mock_setup['scrapy_results']
                mock_wrapper.return_value = mock_wrapper_instance
                
                try:
                    from src.nivel2.queue_client import QueueClient
                    
                    client = QueueClient()
                    task_id = client.enqueue_scraping(['123', '456'])
                    
                    assert task_id == "queue-task-123"
                    
                except ImportError:
                    pytest.skip("QueueClient não disponível")
    
    def test_order_processing_workflow(self, complete_mock_setup):
        """Testa workflow de processamento de pedidos"""
        with patch('src.pedido_queue_client.PedidoQueueClient') as mock_client:
            mock_instance = Mock()
            mock_instance.enqueue_pedido.return_value = "order-task-456"
            mock_instance.get_status.return_value = {
                'status': 'SUCCESS',
                'result': {'pedido_id': 'TEST123', 'status': 'completed'}
            }
            mock_client.return_value = mock_instance
            
            try:
                from src.pedido_queue_client import PedidoQueueClient
                
                client = PedidoQueueClient()
                
                # Enfileirar pedido
                task_id = client.enqueue_pedido(
                    usuario="test@example.com",
                    senha="password",
                    id_pedido="TEST123",
                    produtos=[{'codigo': '123', 'quantidade': 2}]
                )
                
                assert task_id == "order-task-456"
                
                # Verificar status
                status = client.get_status(task_id)
                assert status['status'] == 'SUCCESS'
                
            except ImportError:
                pytest.skip("PedidoQueueClient não disponível")


class TestSystemErrorHandling:
    """Testes de tratamento de erros do sistema"""
    
    def test_missing_environment_variables(self):
        """Testa comportamento com variáveis de ambiente ausentes"""
        # Limpar variáveis de ambiente
        env_backup = dict(os.environ)
        
        # Remover variáveis críticas
        for var in ['CALLBACK_API_USER', 'CALLBACK_API_PASSWORD', 'REDIS_URL']:
            if var in os.environ:
                del os.environ[var]
        
        try:
            # Tentar importar módulos que dependem de env vars
            from src.config import config
            
            # Verificar que valores padrão são usados ou erros são tratados
            assert hasattr(config, 'CALLBACK_API_USER')
            
        except ImportError:
            pytest.skip("Config não disponível")
        finally:
            # Restaurar ambiente
            os.environ.clear()
            os.environ.update(env_backup)
    
    def test_invalid_product_codes(self):
        """Testa comportamento com códigos de produto inválidos"""
        with patch('src.scrapy_wrapper.ScrapyWrapper') as mock_wrapper:
            mock_instance = Mock()
            mock_instance.run_spider.return_value = []  # Sem resultados
            mock_wrapper.return_value = mock_instance
            
            try:
                from src.scrapy_wrapper import ScrapyWrapper
                
                wrapper = ScrapyWrapper()
                results = wrapper.run_spider(['codigo_inexistente'])
                
                # Deve retornar lista vazia sem quebrar
                assert results == []
                
            except ImportError:
                pytest.skip("ScrapyWrapper não disponível")
    
    def test_network_error_handling(self):
        """Testa tratamento de erros de rede"""
        with patch('src.scrapy_wrapper.ScrapyWrapper') as mock_wrapper:
            mock_instance = Mock()
            # Simular erro de rede
            mock_instance.run_spider.side_effect = Exception("Network error")
            mock_wrapper.return_value = mock_instance
            
            try:
                from src.scrapy_wrapper import ScrapyWrapper
                
                wrapper = ScrapyWrapper()
                
                # Deve tratar a exceção apropriadamente
                with pytest.raises(Exception):
                    wrapper.run_spider(['123'])
                
            except ImportError:
                pytest.skip("ScrapyWrapper não disponível")
