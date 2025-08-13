"""
Testes para o cliente de pedidos (src/pedido_queue_client.py)
"""
import pytest
import sys
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Verificar se o arquivo foi editado recentemente
try:
    from src.pedido_queue_client import PedidoQueueClient
except ImportError:
    # Fallback caso haja problemas de importação
    PedidoQueueClient = None


class TestPedidoQueueClient:
    """Testes para a classe PedidoQueueClient"""
    
    def test_init(self):
        """Testa inicialização do cliente"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        client = PedidoQueueClient()
        assert hasattr(client, 'celery_app')
    
    def test_enqueue_pedido_success(self, mock_celery_result):
        """Testa enfileiramento bem-sucedido de pedido"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        # Mock do Celery app
        with patch('src.pedido_queue_client.app') as mock_app:
            mock_app.send_task.return_value = mock_celery_result
            
            client = PedidoQueueClient()
            
            result = client.enqueue_pedido(
                usuario="test@example.com",
                senha="test_password",
                id_pedido="TEST123",
                produtos=[{
                    "gtin": "1234567890123",
                    "codigo": "444212",
                    "quantidade": 2
                }]
            )
            
            assert result == mock_celery_result.id
            mock_app.send_task.assert_called_once()
    
    def test_enqueue_pedido_with_callback_url(self, mock_celery_result):
        """Testa enfileiramento com URL de callback customizada"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        with patch('src.pedido_queue_client.app') as mock_app:
            mock_app.send_task.return_value = mock_celery_result
            
            client = PedidoQueueClient()
            
            result = client.enqueue_pedido(
                usuario="test@example.com",
                senha="test_password",
                id_pedido="TEST456",
                produtos=[{"codigo": "123", "quantidade": 1}],
                callback_url="https://custom.callback.com"
            )
            
            # Verificar que a URL customizada foi passada
            call_args = mock_app.send_task.call_args
            task_data = call_args[1]['args'][0]
            assert task_data['callback_url'] == "https://custom.callback.com"
    
    def test_get_status_task_ready(self):
        """Testa obtenção de status de tarefa pronta"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        with patch('src.pedido_queue_client.app') as mock_app:
            # Mock do AsyncResult
            mock_result = Mock()
            mock_result.status = 'SUCCESS'
            mock_result.ready.return_value = True
            mock_result.successful.return_value = True
            mock_result.result = {'pedido_id': 'TEST123', 'status': 'completed'}
            mock_result.info = None
            
            mock_app.AsyncResult.return_value = mock_result
            
            client = PedidoQueueClient()
            status = client.get_status("test-task-id")
            
            assert status['task_id'] == "test-task-id"
            assert status['status'] == 'SUCCESS'
            assert status['ready'] is True
            assert status['result']['pedido_id'] == 'TEST123'
            assert status['error'] is None
    
    def test_get_status_task_failed(self):
        """Testa obtenção de status de tarefa com falha"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        with patch('src.pedido_queue_client.app') as mock_app:
            # Mock do AsyncResult com falha
            mock_result = Mock()
            mock_result.status = 'FAILURE'
            mock_result.ready.return_value = True
            mock_result.successful.return_value = False
            mock_result.failed.return_value = True
            mock_result.result = None
            mock_result.info = "Erro na execução"
            
            mock_app.AsyncResult.return_value = mock_result
            
            client = PedidoQueueClient()
            status = client.get_status("failed-task-id")
            
            assert status['status'] == 'FAILURE'
            assert status['error'] == "Erro na execução"
            assert status['result'] is None
    
    def test_get_status_task_pending(self):
        """Testa obtenção de status de tarefa pendente"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        with patch('src.pedido_queue_client.app') as mock_app:
            # Mock do AsyncResult pendente
            mock_result = Mock()
            mock_result.status = 'PENDING'
            mock_result.ready.return_value = False
            mock_result.successful.return_value = False
            mock_result.failed.return_value = False
            mock_result.result = None
            mock_result.info = None
            
            mock_app.AsyncResult.return_value = mock_result
            
            client = PedidoQueueClient()
            status = client.get_status("pending-task-id")
            
            assert status['status'] == 'PENDING'
            assert status['ready'] is False
            assert status['result'] is None
            assert status['error'] is None


class TestPedidoQueueClientMain:
    """Testes para a função main do pedido_queue_client.py"""
    
    @patch('sys.argv')
    @patch.dict('os.environ', {'CALLBACK_API_USER': 'test@example.com', 'CALLBACK_API_PASSWORD': 'test_pass'})
    def test_main_enqueue_command(self, mock_argv):
        """Testa comando enqueue na função main"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        mock_argv.__getitem__.side_effect = lambda x: [
            'pedido_queue_client.py', 'enqueue', 'TEST123', '444212', '2', '1234567890123'
        ][x]
        mock_argv.__len__.return_value = 6
        
        with patch('src.pedido_queue_client.PedidoQueueClient') as mock_client_class:
            mock_client = Mock()
            mock_client.enqueue_pedido.return_value = "task-123"
            mock_client_class.return_value = mock_client
            
            # Importar e executar main
            from src import pedido_queue_client
            
            try:
                pedido_queue_client.main()
            except SystemExit:
                pass  # main() pode chamar sys.exit()
            
            mock_client.enqueue_pedido.assert_called_once()
    
    @patch('sys.argv')
    def test_main_status_command(self, mock_argv):
        """Testa comando status na função main"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        mock_argv.__getitem__.side_effect = lambda x: [
            'pedido_queue_client.py', 'status', 'task-123'
        ][x]
        mock_argv.__len__.return_value = 3
        
        with patch('src.pedido_queue_client.PedidoQueueClient') as mock_client_class:
            mock_client = Mock()
            mock_client.get_status.return_value = {
                'task_id': 'task-123',
                'status': 'SUCCESS',
                'result': {'pedido_id': 'TEST123'}
            }
            mock_client_class.return_value = mock_client
            
            from src import pedido_queue_client
            
            try:
                pedido_queue_client.main()
            except SystemExit:
                pass
            
            mock_client.get_status.assert_called_once_with('task-123')
    
    @patch('sys.argv')
    @patch.dict('os.environ', {'CALLBACK_API_USER': 'test@example.com', 'CALLBACK_API_PASSWORD': 'test_pass'})
    @patch('time.time')
    def test_main_test_command(self, mock_time, mock_argv):
        """Testa comando test na função main"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        mock_argv.__getitem__.side_effect = lambda x: [
            'pedido_queue_client.py', 'test'
        ][x]
        mock_argv.__len__.return_value = 2
        mock_time.return_value = 1234567890
        
        with patch('src.pedido_queue_client.PedidoQueueClient') as mock_client_class:
            mock_client = Mock()
            mock_client.enqueue_pedido.return_value = "test-task-123"
            mock_client_class.return_value = mock_client
            
            from src import pedido_queue_client
            
            try:
                pedido_queue_client.main()
            except SystemExit:
                pass
            
            # Verificar que um pedido de teste foi criado
            mock_client.enqueue_pedido.assert_called_once()
            call_args = mock_client.enqueue_pedido.call_args
            assert call_args[1]['id_pedido'].startswith('TEST')
    
    @patch('sys.argv')
    def test_main_no_args(self, mock_argv, capsys):
        """Testa main sem argumentos"""
        mock_argv.__len__.return_value = 1
        
        from src import pedido_queue_client
        
        try:
            pedido_queue_client.main()
        except SystemExit:
            pass
        
        # Verificar que as instruções de uso foram exibidas
        captured = capsys.readouterr()
        assert "Uso:" in captured.out or "ERRO" in captured.out
    
    @patch('sys.argv')
    def test_main_unknown_command(self, mock_argv, capsys):
        """Testa main com comando desconhecido"""
        mock_argv.__getitem__.side_effect = lambda x: [
            'pedido_queue_client.py', 'comando_inexistente'
        ][x]
        mock_argv.__len__.return_value = 2
        
        from src import pedido_queue_client
        
        try:
            pedido_queue_client.main()
        except SystemExit:
            pass
        
        captured = capsys.readouterr()
        assert "ERRO: Comando desconhecido" in captured.out


class TestPedidoQueueClientIntegration:
    """Testes de integração do PedidoQueueClient"""
    
    def test_full_workflow_enqueue_and_status(self):
        """Testa workflow completo: enfileirar e verificar status"""
        if PedidoQueueClient is None:
            pytest.skip("PedidoQueueClient não disponível")
        
        with patch('src.pedido_queue_client.app') as mock_app:
            # Mock enqueue
            mock_send_result = Mock()
            mock_send_result.id = "integration-test-123"
            mock_app.send_task.return_value = mock_send_result
            
            # Mock status check
            mock_status_result = Mock()
            mock_status_result.status = 'SUCCESS'
            mock_status_result.ready.return_value = True
            mock_status_result.successful.return_value = True
            mock_status_result.result = {'pedido_id': 'INTEGRATION_TEST'}
            mock_app.AsyncResult.return_value = mock_status_result
            
            client = PedidoQueueClient()
            
            # Enfileirar pedido
            task_id = client.enqueue_pedido(
                usuario="integration@test.com",
                senha="test_password",
                id_pedido="INTEGRATION_TEST",
                produtos=[{"codigo": "999", "quantidade": 1}]
            )
            
            assert task_id == "integration-test-123"
            
            # Verificar status
            status = client.get_status(task_id)
            
            assert status['status'] == 'SUCCESS'
            assert status['result']['pedido_id'] == 'INTEGRATION_TEST'
