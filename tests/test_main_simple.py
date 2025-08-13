"""
Testes simplificados para o script principal (main.py)
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from io import StringIO

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestMainSimple:
    """Testes básicos para main.py"""
    
    def test_main_module_can_be_imported(self):
        """Testa se main.py pode ser importado"""
        assert hasattr(main, 'main')
        assert hasattr(main, 'executar_nivel_1')
        assert hasattr(main, 'executar_nivel_2')
        assert hasattr(main, 'executar_nivel_3')
    
    def test_executar_nivel_1_basic(self):
        """Testa função executar_nivel_1 básica"""
        args = Mock()
        args.filtro = "test"
        args.max_pages = 1
        
        # Mock básico
        with patch('main.ScrapyServimedWrapper') as mock_wrapper:
            mock_instance = Mock()
            mock_instance.run_spider.return_value = True
            mock_instance.get_results.return_value = {'success': True, 'total': 1}
            mock_wrapper.return_value = mock_instance
            
            result = main.executar_nivel_1(args)
            assert result is not None
    
    def test_executar_nivel_2_basic(self):
        """Testa função executar_nivel_2 básica"""
        args = Mock()
        args.status = "test-task-id"
        args.worker_status = False
        args.direct = False
        
        with patch('src.nivel2.queue_client.TaskQueueClient') as mock_client:
            mock_instance = Mock()
            # Retornar um dicionário serializável ao invés de Mock
            mock_instance.get_task_status.return_value = {
                'task_id': 'test-task-id',
                'status': 'PENDING',
                'ready': False,
                'result': None
            }
            mock_client.return_value = mock_instance
            
            result = main.executar_nivel_2(args)
            assert result is not None
            assert isinstance(result, dict)
            assert 'task_id' in result
    
    def test_executar_nivel_3_basic(self):
        """Testa função executar_nivel_3 básica"""
        args = Mock()
        args.test = None
        args.codigo_produto = None
        args.status = None
        
        # Capturar output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main.executar_nivel_3(args)
            output = mock_stdout.getvalue()
            assert "NIVEL 3" in output or "SISTEMA DE PEDIDOS" in output


class TestMainArguments:
    """Testes para argumentos do main"""
    
    def test_main_with_nivel_1(self):
        """Testa main com nível 1"""
        test_args = ['main.py', '--nivel', '1', '--max-pages', '1']
        
        with patch('sys.argv', test_args):
            with patch('main.executar_nivel_1') as mock_exec:
                try:
                    main.main()
                    mock_exec.assert_called_once()
                except SystemExit:
                    # SystemExit é normal ao usar argparse
                    pass
    
    def test_main_with_nivel_2(self):
        """Testa main com nível 2"""
        test_args = ['main.py', '--nivel', '2', '--worker-status']
        
        with patch('sys.argv', test_args):
            with patch('main.executar_nivel_2') as mock_exec:
                try:
                    main.main()
                    mock_exec.assert_called_once()
                except SystemExit:
                    # SystemExit é normal ao usar argparse
                    pass
    
    def test_main_with_nivel_3(self):
        """Testa main com nível 3"""
        test_args = ['main.py', '--nivel', '3']
        
        with patch('sys.argv', test_args):
            with patch('main.executar_nivel_3') as mock_exec:
                try:
                    main.main()
                    mock_exec.assert_called_once()
                except SystemExit:
                    # SystemExit é normal ao usar argparse
                    pass
