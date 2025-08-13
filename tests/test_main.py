"""
Testes para o script principal (main.py)
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestMainScript:
    """Testes para as funções principais do main.py"""
    
    def test_executar_nivel_1_com_scrapy_disponivel(self, mock_env_vars):
        """Testa execução do nível 1 com Scrapy disponível"""
        # Mock dos argumentos
        args = Mock()
        args.filtro = "test"
        args.max_pages = 1
        
        # Mock do ScrapyServimedWrapper
        with patch('main.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper = Mock()
            mock_wrapper.run_spider.return_value = True
            mock_wrapper.get_results.return_value = {
                'success': True,
                'total': 1,
                'produtos': [{'codigo': '444212', 'descricao': 'Teste'}]
            }
            mock_wrapper_class.return_value = mock_wrapper
            
            # Executar
            result = main.executar_nivel_1(args)
            
            # Verificações
            assert result is not None
            mock_wrapper.run_spider.assert_called_once_with(
                filtro="test", 
                max_pages=1
            )
    
    def test_executar_nivel_1_sem_scrapy(self):
        """Testa execução do nível 1 sem Scrapy disponível"""
        args = Mock()
        args.filtro = "test"
        
        # Mock ScrapyServimedWrapper como None
        with patch('main.ScrapyServimedWrapper', None):
            result = main.executar_nivel_1(args)
            assert result is None
    
    def test_executar_nivel_2_worker_status(self, mock_env_vars):
        """Testa verificação de status dos workers no nível 2"""
        args = Mock()
        args.worker_status = True
        args.enqueue = False
        args.status = None
        
        # Mock do TaskQueueClient
        with patch('main.TaskQueueClient') as mock_client_class:
            mock_client = Mock()
            mock_client.get_worker_status.return_value = {
                'workers_active': 1,
                'active_tasks': []
            }
            mock_client_class.return_value = mock_client
            
            result = main.executar_nivel_2(args)
            
            mock_client.get_worker_status.assert_called_once()
    
    def test_executar_nivel_2_enqueue(self, mock_env_vars):
        """Testa enfileiramento de tarefa no nível 2"""
        args = Mock()
        args.enqueue = True
        args.worker_status = False
        args.status = None
        args.filtro = "vitamina"
        args.max_pages = 5
        args.usuario = None
        args.senha = None
        args.callback_url = None
        
        # Mock das variáveis de ambiente
        with patch.dict(os.environ, mock_env_vars):
            with patch('main.TaskQueueClient') as mock_client_class:
                mock_client = Mock()
                mock_client.enqueue_scraping_task.return_value = "task-123"
                mock_client_class.return_value = mock_client
                
                result = main.executar_nivel_2(args)
                
                mock_client.enqueue_scraping_task.assert_called_once()
    
    def test_executar_nivel_2_status_check(self, mock_env_vars):
        """Testa verificação de status de tarefa no nível 2"""
        args = Mock()
        args.status = "task-123"
        args.enqueue = False
        args.worker_status = False
        
        with patch('main.TaskQueueClient') as mock_client_class:
            mock_client = Mock()
            mock_client.get_task_status.return_value = {
                'task_id': 'task-123',
                'status': 'SUCCESS',
                'result': {'total': 5}
            }
            mock_client_class.return_value = mock_client
            
            result = main.executar_nivel_2(args)
            
            mock_client.get_task_status.assert_called_once_with("task-123")


class TestMainIntegration:
    """Testes de integração do main.py"""
    
    def test_main_function_nivel_1(self):
        """Testa função main com nível 1"""
        test_args = ['main.py', '--nivel', '1', '--filtro', 'test']
        
        with patch('sys.argv', test_args):
            with patch('main.executar_nivel_1') as mock_exec:
                mock_exec.return_value = {'status': 'success'}
                
                result = main.main()
                
                mock_exec.assert_called_once()
    
    def test_main_function_nivel_2(self):
        """Testa função main com nível 2"""
        test_args = ['main.py', '--nivel', '2', '--worker-status']
        
        with patch('sys.argv', test_args):
            with patch('main.executar_nivel_2') as mock_exec:
                mock_exec.return_value = {'workers': 1}
                
                result = main.main()
                
                mock_exec.assert_called_once()
    
    def test_main_function_nivel_3(self, capsys):
        """Testa função main com nível 3"""
        test_args = ['main.py', '--nivel', '3']
        
        with patch('sys.argv', test_args):
            result = main.main()
            
            # Verifica se as instruções do nível 3 foram exibidas
            captured = capsys.readouterr()
            assert "NÍVEL 3: Sistema de Pedidos" in captured.out
            assert "python src/pedido_queue_client.py" in captured.out


class TestMainErrorHandling:
    """Testes de tratamento de erros do main.py"""
    
    def test_executar_nivel_1_com_erro_scrapy(self):
        """Testa tratamento de erro no Scrapy"""
        args = Mock()
        args.filtro = "test"
        args.max_pages = 1
        
        with patch('main.ScrapyServimedWrapper') as mock_wrapper_class:
            mock_wrapper = Mock()
            mock_wrapper.run_spider.side_effect = Exception("Erro no Scrapy")
            mock_wrapper_class.return_value = mock_wrapper
            
            result = main.executar_nivel_1(args)
            
            # Deve retornar None em caso de erro
            assert result is None
    
    def test_executar_nivel_2_sem_credenciais(self):
        """Testa nível 2 sem credenciais"""
        args = Mock()
        args.enqueue = True
        args.worker_status = False
        args.status = None
        args.usuario = None
        args.senha = None
        
        # Mock ambiente sem credenciais
        with patch.dict(os.environ, {}, clear=True):
            with patch('main.TaskQueueClient'):
                result = main.executar_nivel_2(args)
                
                # Deve retornar None devido à falta de credenciais
                assert result is None
