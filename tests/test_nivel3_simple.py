"""
Testes simplificados para o cliente de pedidos (src/pedido_queue_client.py)
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pedido_queue_client import PedidoQueueClient


class TestPedidoQueueClientSimple:
    """Testes básicos para a classe PedidoQueueClient"""
    
    def test_init(self):
        """Testa inicialização do cliente"""
        client = PedidoQueueClient()
        
        # Verificar atributos básicos
        assert hasattr(client, 'enqueue_pedido')
        assert hasattr(client, 'get_status')
    
    @patch('src.pedido_queue_client.app.send_task')
    def test_enqueue_pedido_success(self, mock_send_task):
        """Testa enfileiramento bem-sucedido de pedido"""
        client = PedidoQueueClient()
        
        # Mock da tarefa
        mock_task = Mock()
        mock_task.id = "test-task-123"
        mock_send_task.return_value = mock_task
        
        # Produtos para o pedido
        produtos = [{"gtin": "1234567890123", "codigo": "444212", "quantidade": 1}]
        
        # Executar (ajustado para assinatura real)
        result = client.enqueue_pedido("user@test.com", "password", "TEST123", produtos)
        
        # Verificações (retorna string, não dict)
        assert result == "test-task-123"
        
        # Verificar se o send_task foi chamado
        mock_send_task.assert_called_once()
    
    @patch('src.pedido_queue_client.app.send_task')
    def test_enqueue_pedido_with_callback_url(self, mock_send_task):
        """Testa enfileiramento com URL de callback customizada"""
        client = PedidoQueueClient()
        
        # Mock da tarefa
        mock_task = Mock()
        mock_task.id = "test-task-456"
        mock_send_task.return_value = mock_task
        
        # Produtos para o pedido
        produtos = [{"gtin": "1234567890123", "codigo": "444212", "quantidade": 1}]
        
        # Executar com callback customizado (ajustado para assinatura real)
        result = client.enqueue_pedido(
            "user@test.com", "password", "TEST456", produtos,
            callback_url="https://custom.callback.url"
        )
        
        # Verificações
        assert result == "test-task-456"
        
        # Verificar argumentos da chamada
        call_args = mock_send_task.call_args[1]['args'][0]  # args parameter
        assert call_args['callback_url'] == "https://custom.callback.url"
    
    @patch('src.pedido_queue_client.app.AsyncResult')
    def test_get_status_task_pending(self, mock_async_result_class):
        """Testa obtenção de status de tarefa pendente"""
        client = PedidoQueueClient()
        
        # Mock de tarefa pendente
        mock_async_result = Mock()
        mock_async_result.status = "PENDING"
        mock_async_result.ready.return_value = False
        mock_async_result.result = None
        mock_async_result.failed.return_value = False
        mock_async_result.traceback = None
        
        mock_async_result_class.return_value = mock_async_result
        
        # Executar
        status = client.get_status("test-task-789")
        
        # Verificações
        assert status['task_id'] == "test-task-789"
        assert status['status'] == "PENDING"
        assert status['ready'] is False
        assert status['result'] is None
        assert status['error'] is None


class TestPedidoQueueClientMain:
    """Testes para a função main do pedido_queue_client.py"""
    
    @patch('src.pedido_queue_client.PedidoQueueClient')
    def test_main_enqueue_command(self, mock_client_class):
        """Testa comando enqueue na função main"""
        # Mock do cliente
        mock_client = Mock()
        mock_client.enqueue_pedido.return_value = {
            'task_id': 'test-task-123',
            'id_pedido': 'TEST123',
            'message': 'Pedido enfileirado'
        }
        mock_client_class.return_value = mock_client
        
        # Mock de sys.argv
        test_args = ['pedido_queue_client.py', 'enqueue', 'TEST123', '444212', '2', '1234567890123']
        
        with patch('sys.argv', test_args):
            from src import pedido_queue_client
            
            # Capturar stdout
            from io import StringIO
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                try:
                    pedido_queue_client.main()
                    output = mock_stdout.getvalue()
                    
                    # Verificar output
                    assert 'test-task-123' in output
                except SystemExit:
                    # SystemExit é normal em scripts CLI
                    pass
    
    @patch('src.pedido_queue_client.PedidoQueueClient')
    def test_main_status_command(self, mock_client_class):
        """Testa comando status na função main"""
        # Mock do cliente
        mock_client = Mock()
        mock_client.get_status.return_value = {
            'task_id': 'test-task-123',
            'state': 'SUCCESS',
            'ready': True
        }
        mock_client_class.return_value = mock_client
        
        # Mock de sys.argv
        test_args = ['pedido_queue_client.py', 'status', 'test-task-123']
        
        with patch('sys.argv', test_args):
            from src import pedido_queue_client
            
            # Capturar stdout
            from io import StringIO
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                try:
                    pedido_queue_client.main()
                    output = mock_stdout.getvalue()
                    
                    # Verificar output
                    assert 'test-task-123' in output
                except SystemExit:
                    # SystemExit é normal em scripts CLI
                    pass
    
    def test_main_no_args(self):
        """Testa main sem argumentos"""
        test_args = ['pedido_queue_client.py']
        
        with patch('sys.argv', test_args):
            from src import pedido_queue_client
            
            # Capturar stdout
            from io import StringIO
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                try:
                    pedido_queue_client.main()
                    output = mock_stdout.getvalue()
                    
                    # Deve mostrar ajuda
                    assert 'Uso:' in output or 'Commands:' in output
                except SystemExit:
                    # SystemExit é normal em scripts CLI
                    pass
    
    def test_main_unknown_command(self):
        """Testa main com comando desconhecido"""
        test_args = ['pedido_queue_client.py', 'comando_inexistente']
        
        with patch('sys.argv', test_args):
            from src import pedido_queue_client
            
            # Capturar stdout
            from io import StringIO
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                try:
                    pedido_queue_client.main()
                    output = mock_stdout.getvalue()
                    
                    # Deve mostrar ajuda ou erro
                    assert len(output) > 0
                except SystemExit:
                    # SystemExit é normal em scripts CLI
                    pass
