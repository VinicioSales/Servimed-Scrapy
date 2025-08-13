"""
Testes para o Scrapy Wrapper (src/scrapy_wrapper.py)
"""
import pytest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapy_wrapper import ScrapyServimedWrapper


class TestScrapyWrapper:
    """Testes para o ScrapyServimedWrapper"""
    
    def test_init(self):
        """Testa inicialização do wrapper"""
        wrapper = ScrapyServimedWrapper()
        
        assert wrapper.logger is not None
        assert hasattr(wrapper, 'results_file')
    
    def test_setup_logging(self):
        """Testa configuração do logging"""
        wrapper = ScrapyServimedWrapper()
        
        # Verifica se o logger foi configurado
        assert wrapper.logger.name == 'src.scrapy_wrapper'
    
    @patch('subprocess.run')
    def test_run_spider_subprocess_success(self, mock_subprocess):
        """Testa execução bem-sucedida do spider via subprocess"""
        # Mock do subprocess
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Spider executado com sucesso"
        mock_subprocess.return_value.stderr = ""
        
        wrapper = ScrapyServimedWrapper()
        
        result = wrapper.run_spider_subprocess(
            filtro="vitamina", 
            max_pages=2, 
            callback_url="https://test.com"
        )
        
        assert result is True
        mock_subprocess.assert_called_once()
        
        # Verifica argumentos do comando
        call_args = mock_subprocess.call_args[0][0]
        assert 'scrapy' in call_args
        assert 'crawl' in call_args
        assert 'servimed_products' in call_args
    
    @patch('subprocess.run')
    def test_run_spider_subprocess_failure(self, mock_subprocess):
        """Testa falha na execução do spider via subprocess"""
        # Mock do subprocess com erro
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stdout = ""
        mock_subprocess.return_value.stderr = "Erro no spider"
        
        wrapper = ScrapyServimedWrapper()
        
        result = wrapper.run_spider_subprocess(filtro="test")
        
        assert result is False
    
    def test_get_results_file_exists(self, sample_product_data):
        """Testa obtenção de resultados quando arquivo existe"""
        wrapper = ScrapyServimedWrapper()
        
        # Criar arquivo temporário com dados de teste
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump([sample_product_data], temp_file)
            temp_path = temp_file.name
        
        try:
            # Mock do caminho do arquivo
            wrapper.results_file = Path(temp_path)
            
            results = wrapper.get_results()
            
            assert results['success'] is True
            assert results['total'] == 1
            assert len(results['produtos']) == 1
            assert results['produtos'][0]['codigo'] == '444212'
        
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_get_results_file_not_exists(self):
        """Testa obtenção de resultados quando arquivo não existe"""
        wrapper = ScrapyServimedWrapper()
        wrapper.results_file = Path("/arquivo/inexistente.json")
        
        results = wrapper.get_results()
        
        assert results['success'] is False
        assert results['total'] == 0
        assert 'error' in results
    
    def test_get_results_invalid_json(self):
        """Testa obtenção de resultados com JSON inválido"""
        wrapper = ScrapyServimedWrapper()
        
        # Criar arquivo com JSON inválido
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_file.write("{invalid json}")
            temp_path = temp_file.name
        
        try:
            wrapper.results_file = Path(temp_path)
            
            results = wrapper.get_results()
            
            assert results['success'] is False
            assert 'error' in results
        
        finally:
            os.unlink(temp_path)
    
    @patch('src.scrapy_wrapper.ScrapyServimedWrapper.run_spider_subprocess')
    def test_run_spider_calls_subprocess(self, mock_subprocess):
        """Testa que run_spider chama run_spider_subprocess"""
        mock_subprocess.return_value = True
        
        wrapper = ScrapyServimedWrapper()
        
        result = wrapper.run_spider(
            filtro="aspirina", 
            max_pages=3, 
            callback_url="https://callback.test"
        )
        
        assert result is True
        mock_subprocess.assert_called_once_with(
            "aspirina", 
            3, 
            "https://callback.test"
        )


class TestScrapyWrapperIntegration:
    """Testes de integração do ScrapyWrapper"""
    
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_full_workflow_success(self, mock_exists, mock_subprocess, sample_product_data):
        """Testa workflow completo: executar spider e obter resultados"""
        # Mock subprocess success
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Success"
        mock_subprocess.return_value.stderr = ""
        
        # Mock file exists
        mock_exists.return_value = True
        
        wrapper = ScrapyServimedWrapper()
        
        # Mock do arquivo de resultados
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump([sample_product_data, sample_product_data], temp_file)
            temp_path = temp_file.name
        
        try:
            wrapper.results_file = Path(temp_path)
            
            # Executar spider
            spider_result = wrapper.run_spider(filtro="teste", max_pages=1)
            assert spider_result is True
            
            # Obter resultados
            results = wrapper.get_results()
            assert results['success'] is True
            assert results['total'] == 2
            assert len(results['produtos']) == 2
        
        finally:
            os.unlink(temp_path)
    
    def test_error_handling_workflow(self):
        """Testa workflow com tratamento de erros"""
        wrapper = ScrapyServimedWrapper()
        
        # Simular erro na execução
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.side_effect = Exception("Erro de sistema")
            
            result = wrapper.run_spider_subprocess(filtro="test")
            
            assert result is False


class TestScrapyWrapperEdgeCases:
    """Testes de casos extremos do ScrapyWrapper"""
    
    def test_empty_results_file(self):
        """Testa arquivo de resultados vazio"""
        wrapper = ScrapyServimedWrapper()
        
        # Criar arquivo vazio
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_file.write("[]")
            temp_path = temp_file.name
        
        try:
            wrapper.results_file = Path(temp_path)
            
            results = wrapper.get_results()
            
            assert results['success'] is True
            assert results['total'] == 0
            assert results['produtos'] == []
        
        finally:
            os.unlink(temp_path)
    
    def test_run_spider_with_none_parameters(self):
        """Testa execução com parâmetros None"""
        wrapper = ScrapyServimedWrapper()
        
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value.returncode = 0
            mock_subprocess.return_value.stdout = "Success"
            mock_subprocess.return_value.stderr = ""
            
            result = wrapper.run_spider(filtro=None, max_pages=None)
            
            # Deve funcionar com valores padrão
            assert result is True
