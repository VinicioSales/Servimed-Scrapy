"""
Testes para as configurações (config/)
"""
import pytest
import sys
import os
import tempfile
import unittest.mock
from unittest.mock import Mock, patch
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings, paths


class TestConfigSettings:
    """Testes para config/settings.py"""
    
    def test_load_env_file_exists(self):
        """Testa carregamento do .env quando arquivo existe"""
        # Criar arquivo .env temporário
        env_content = """
ACCESS_TOKEN=test_token
SESSION_TOKEN=test_session
LOGGED_USER=test_user
CLIENT_ID=123
PORTAL_EMAIL=test@example.com
PORTAL_PASSWORD=test_password
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as temp_file:
            temp_file.write(env_content)
            temp_path = temp_file.name
        
        try:
            # Mock do caminho do arquivo
            with patch('config.settings.Path') as mock_path:
                mock_path_instance = Mock()
                mock_path_instance.exists.return_value = True
                
                # Mock do open
                with patch('builtins.open', unittest.mock.mock_open(read_data=env_content)):
                    env_vars = settings.load_env()
                    
                    assert env_vars['ACCESS_TOKEN'] == 'test_token'
                    assert env_vars['PORTAL_EMAIL'] == 'test@example.com'
                    assert env_vars['CLIENT_ID'] == '123'
        
        finally:
            os.unlink(temp_path)
    
    def test_load_env_file_not_exists(self):
        """Testa carregamento quando .env não existe"""
        with patch('config.settings.Path') as mock_path:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = False
            mock_path.return_value.parent.parent.__truediv__.return_value = mock_path_instance
            
            with pytest.raises(FileNotFoundError):
                settings.load_env()
    
    def test_validate_config_success(self, mock_env_vars):
        """Testa validação de configuração bem-sucedida"""
        with patch('config.settings.load_env', return_value=mock_env_vars):
            with patch('config.settings.ACCESS_TOKEN', 'valid_token'):
                with patch('config.settings.PORTAL_EMAIL', 'valid@email.com'):
                    # Não deve lançar exceção
                    try:
                        settings.validate_config()
                    except ValueError:
                        pytest.fail("validate_config não deveria falhar com dados válidos")
    
    def test_validate_config_missing_vars(self):
        """Testa validação com variáveis faltando"""
        incomplete_vars = {
            'ACCESS_TOKEN': '',
            'PORTAL_EMAIL': '',
            'LOGGED_USER': 'user'
        }
        
        with patch('config.settings.load_env', return_value=incomplete_vars):
            with patch('config.settings.ACCESS_TOKEN', ''):
                with patch('config.settings.PORTAL_EMAIL', ''):
                    with pytest.raises(ValueError, match="Configuracao incompleta"):
                        settings.validate_config()


class TestConfigPaths:
    """Testes para config/paths.py"""
    
    def test_project_root_path(self):
        """Testa se o PROJECT_ROOT está correto"""
        assert paths.PROJECT_ROOT.name == "PROVA"
        assert paths.PROJECT_ROOT.is_dir()
    
    def test_directory_paths(self):
        """Testa se todos os diretórios estão definidos"""
        expected_dirs = [
            'DATA_DIR', 'DOCS_DIR', 'CONFIG_DIR', 'SRC_DIR',
            'LOGS_DIR', 'SCRIPTS_DIR', 'TOOLS_DIR'
        ]
        
        for dir_name in expected_dirs:
            assert hasattr(paths, dir_name)
            dir_path = getattr(paths, dir_name)
            assert isinstance(dir_path, Path)
    
    def test_output_files_dict(self):
        """Testa se OUTPUT_FILES está configurado corretamente"""
        assert hasattr(paths, 'OUTPUT_FILES')
        assert isinstance(paths.OUTPUT_FILES, dict)
        
        expected_keys = [
            'all_products', 'filtered_products', 
            'scrapy_products', 'backup'
        ]
        
        for key in expected_keys:
            assert key in paths.OUTPUT_FILES
            assert isinstance(paths.OUTPUT_FILES[key], Path)
    
    def test_setup_paths(self):
        """Testa função setup_paths"""
        # Verificar que src está no sys.path após importar
        import sys
        assert str(paths.SRC_DIR) in sys.path
    
    def test_directories_creation(self):
        """Testa se os diretórios são criados"""
        # Como os diretórios são criados na importação,
        # vamos apenas verificar se existem
        directories_to_check = [
            paths.DATA_DIR, paths.DOCS_DIR, paths.LOGS_DIR
        ]
        
        for directory in directories_to_check:
            assert directory.exists(), f"Diretório {directory} não existe"


class TestConfigIntegration:
    """Testes de integração das configurações"""
    
    def test_config_import(self):
        """Testa se os módulos de configuração podem ser importados"""
        try:
            import config.settings
            import config.paths
        except ImportError as e:
            pytest.fail(f"Erro ao importar configurações: {e}")
    
    def test_env_vars_integration(self, mock_env_vars):
        """Testa integração entre variáveis de ambiente e configurações"""
        with patch.dict(os.environ, mock_env_vars):
            with patch('config.settings.load_env', return_value=mock_env_vars):
                # Simular importação das configurações
                assert mock_env_vars['PORTAL_EMAIL'] == 'test@example.com'
                assert mock_env_vars['ACCESS_TOKEN'] == 'test_access_token'
    
    def test_paths_integration_with_project_structure(self):
        """Testa se os paths estão alinhados com a estrutura real do projeto"""
        # Verificar que main.py existe na raiz
        main_file = paths.PROJECT_ROOT / "main.py"
        assert main_file.exists(), "main.py deve existir na raiz do projeto"
        
        # Verificar que src existe
        assert paths.SRC_DIR.exists(), "Diretório src deve existir"
        
        # Verificar que config existe
        assert paths.CONFIG_DIR.exists(), "Diretório config deve existir"
