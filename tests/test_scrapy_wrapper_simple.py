"""
Testes simplificados para o Scrapy Wrapper (src/scrapy_wrapper.py)
"""
import pytest
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapy_wrapper import ScrapyServimedWrapper


class TestScrapyWrapperSimple:
    """Testes básicos para o ScrapyServimedWrapper"""
    
    def test_init(self):
        """Testa inicialização do wrapper"""
        wrapper = ScrapyServimedWrapper()
        
        # Verificar atributos básicos (ajustados para implementação real)
        assert hasattr(wrapper, 'setup_logging')
        assert hasattr(wrapper, 'run_spider')
        assert hasattr(wrapper, 'get_results')
        assert wrapper.logger is not None
    
    def test_setup_logging(self):
        """Testa configuração do logging"""
        wrapper = ScrapyServimedWrapper()
        
        # Verifica se o logger foi configurado
        assert wrapper.logger.name == 'src.scrapy_wrapper'
    
    @patch('subprocess.run')
    def test_run_spider_subprocess_success(self, mock_run):
        """Testa execução bem-sucedida do spider via subprocess"""
        wrapper = ScrapyServimedWrapper()
        
        # Mock do subprocess
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Spider executado com sucesso"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Executar
        result = wrapper.run_spider_subprocess("teste", 1)
        
        # Verificações
        assert result is True
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_run_spider_subprocess_failure(self, mock_run):
        """Testa falha na execução do spider via subprocess"""
        wrapper = ScrapyServimedWrapper()
        
        # Mock do subprocess com falha
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Erro no spider"
        mock_run.return_value = mock_result
        
        # Executar
        result = wrapper.run_spider_subprocess("teste", 1)
        
        # Verificações
        assert result is False
        mock_run.assert_called_once()
    
    def test_get_results_file_exists(self):
        """Testa obtenção de resultados quando arquivo existe"""
        wrapper = ScrapyServimedWrapper()
        
        # Criar arquivo temporário com dados
    @patch('pathlib.Path.exists')
    @patch('builtins.open')
    @patch('json.load')
    def test_get_results_file_exists(self, mock_json_load, mock_open, mock_exists):
        """Testa get_results quando arquivo existe"""
        wrapper = ScrapyServimedWrapper()
        
        # Mock do arquivo existir
        mock_exists.return_value = True
        
        # Mock dos dados JSON
        mock_data = {
            'produtos': [{'gtin': '123', 'nome': 'Produto 1'}, {'gtin': '456', 'nome': 'Produto 2'}],
            'metadata': {'total': 2}
        }
        mock_json_load.return_value = mock_data
        
        # Executar
        result = wrapper.get_results()
        
        # Verificações
        assert result['success'] is True
        assert len(result['produtos']) == 2
        assert result['total'] == 2
    
    @patch('pathlib.Path.exists')
    def test_get_results_file_not_exists(self, mock_exists):
        """Testa obtenção de resultados quando arquivo não existe"""
        wrapper = ScrapyServimedWrapper()
        
        # Mock do arquivo não existir
        mock_exists.return_value = False
        
        # Executar
        result = wrapper.get_results()
        
        # Verificações (deve retornar estrutura vazia)
        assert result['success'] is True
        assert result['produtos'] == []
        assert result['total'] == 0


class TestScrapyWrapperIntegration:
    """Testes de integração simplificados do ScrapyWrapper"""
    
    @patch('src.scrapy_wrapper.ScrapyServimedWrapper.run_spider_subprocess')
    def test_run_spider_calls_subprocess(self, mock_subprocess):
        """Testa que run_spider chama run_spider_subprocess"""
        wrapper = ScrapyServimedWrapper()
        mock_subprocess.return_value = True
        
        result = wrapper.run_spider("teste", 1)
        
        # Verificar se foi chamado (ajustado para assinatura real)
        mock_subprocess.assert_called_once()
        assert result is True
    
    def test_error_handling_workflow(self):
        """Testa workflow com tratamento de erros"""
        wrapper = ScrapyServimedWrapper()
        
        # Teste com parâmetros None
        result = wrapper.run_spider(None, None)
        
        # Deve funcionar mesmo com parâmetros None
        assert result is not None
