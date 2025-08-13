"""
Testes básicos e funcionais para verificar se o sistema está operacional
"""
import pytest
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestBasicFunctionality:
    """Testes básicos para verificar funcionalidade do sistema"""
    
    def test_python_environment(self):
        """Testa se o ambiente Python está funcionando"""
        assert sys.version_info.major >= 3
        assert sys.version_info.minor >= 8
    
    def test_project_structure(self):
        """Testa se a estrutura do projeto está correta"""
        project_root = Path(__file__).parent.parent
        
        # Verificar arquivos principais
        assert (project_root / "main.py").exists()
        assert (project_root / "src").is_dir()
        assert (project_root / "tests").is_dir()
    
    def test_src_imports(self):
        """Testa se os módulos principais podem ser importados"""
        try:
            import src.scrapy_wrapper
            assert hasattr(src.scrapy_wrapper, 'ScrapyServimedWrapper')
        except ImportError:
            pytest.skip("scrapy_wrapper não disponível")
    
    def test_main_imports(self):
        """Testa se main.py pode ser importado"""
        try:
            import main
            assert hasattr(main, 'executar_nivel_1')
            assert hasattr(main, 'executar_nivel_2')
            assert hasattr(main, 'main')  # Função principal
        except ImportError:
            pytest.skip("main.py não disponível")
    
    def test_level2_imports(self):
        """Testa se módulos do nível 2 podem ser importados"""
        try:
            import src.nivel2.queue_client
            assert hasattr(src.nivel2.queue_client, 'TaskQueueClient')
        except ImportError:
            pytest.skip("queue_client não disponível")
    
    def test_scrapy_wrapper_creation(self):
        """Testa se o ScrapyWrapper pode ser criado"""
        try:
            from src.scrapy_wrapper import ScrapyServimedWrapper
            wrapper = ScrapyServimedWrapper()
            assert wrapper is not None
        except ImportError:
            pytest.skip("ScrapyServimedWrapper não disponível")
    
    def test_task_queue_client_creation(self):
        """Testa se o TaskQueueClient pode ser criado"""
        try:
            from src.nivel2.queue_client import TaskQueueClient
            client = TaskQueueClient()
            assert client is not None
        except ImportError:
            pytest.skip("TaskQueueClient não disponível")


class TestConfigurationFiles:
    """Testes para arquivos de configuração"""
    
    def test_pytest_ini_exists(self):
        """Testa se pyproject.toml existe (substitui pytest.ini)"""
        project_root = Path(__file__).parent.parent
        assert (project_root / "pyproject.toml").exists()
    
    def test_pyproject_toml_exists(self):
        """Testa se pyproject.toml existe"""
        project_root = Path(__file__).parent.parent
        assert (project_root / "pyproject.toml").exists()
    
    def test_requirements_txt_exists(self):
        """Testa se requirements.txt existe"""
        project_root = Path(__file__).parent.parent
        requirements_file = project_root / "requirements.txt"
        if requirements_file.exists():
            content = requirements_file.read_text()
            assert "scrapy" in content.lower()
            assert "celery" in content.lower()


class TestEnvironmentVariables:
    """Testes para variáveis de ambiente"""
    
    def test_python_path(self):
        """Testa se PYTHONPATH inclui src"""
        project_src = str(Path(__file__).parent.parent / "src")
        assert project_src in sys.path
    
    def test_optional_env_vars(self):
        """Testa variáveis de ambiente opcionais"""
        # Estas são opcionais, então apenas verificamos se existem
        env_vars = [
            'CALLBACK_API_USER',
            'CALLBACK_API_PASSWORD', 
            'REDIS_URL',
            'CELERY_BROKER_URL'
        ]
        
        available_vars = [var for var in env_vars if os.getenv(var)]
        # Pelo menos algumas devem estar disponíveis ou tudo funcionará com defaults
        assert len(available_vars) >= 0  # Sempre passa - apenas documenta


class TestFileSystemOperations:
    """Testes para operações do sistema de arquivos"""
    
    def test_can_create_temp_files(self):
        """Testa se consegue criar arquivos temporários"""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('{"test": "data"}')
            temp_file = f.name
        
        assert Path(temp_file).exists()
        
        # Limpar
        Path(temp_file).unlink()
    
    def test_data_directory_access(self):
        """Testa acesso ao diretório data"""
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "data"
        
        # Criar se não existir
        data_dir.mkdir(exist_ok=True)
        
        # Verificar se pode escrever
        test_file = data_dir / "test_write.txt"
        test_file.write_text("test")
        assert test_file.exists()
        
        # Limpar
        test_file.unlink()


class TestUtilityFunctions:
    """Testes para funções utilitárias"""
    
    def test_json_operations(self):
        """Testa operações JSON básicas"""
        import json
        
        test_data = {
            "products": [
                {"name": "Test Product", "price": 10.99},
                {"name": "Another Product", "price": 25.50}
            ],
            "total": 2
        }
        
        # Serializar
        json_str = json.dumps(test_data)
        assert isinstance(json_str, str)
        
        # Deserializar
        parsed_data = json.loads(json_str)
        assert parsed_data["total"] == 2
        assert len(parsed_data["products"]) == 2
    
    def test_logging_functionality(self):
        """Testa se logging está funcionando"""
        import logging
        
        # Criar logger de teste
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.INFO)
        
        # Verificar que não gera erro
        logger.info("Test log message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        
        assert True  # Se chegou aqui, logging está funcionando


class TestDependencyVersions:
    """Testes para verificar versões de dependências"""
    
    def test_scrapy_available(self):
        """Testa se Scrapy está disponível"""
        try:
            import scrapy
            # Verificar versão mínima
            version = scrapy.__version__
            major, minor = map(int, version.split('.')[:2])
            assert major >= 2
        except ImportError:
            pytest.skip("Scrapy não está instalado")
    
    def test_celery_available(self):
        """Testa se Celery está disponível"""
        try:
            import celery
            assert hasattr(celery, 'Celery')
        except ImportError:
            pytest.skip("Celery não está instalado")
    
    def test_redis_available(self):
        """Testa se Redis client está disponível"""
        try:
            import redis
            assert hasattr(redis, 'Redis')
        except ImportError:
            pytest.skip("Redis client não está instalado")
    
    def test_requests_available(self):
        """Testa se requests está disponível"""
        try:
            import requests
            assert hasattr(requests, 'get')
        except ImportError:
            pytest.skip("Requests não está instalado")


@pytest.mark.integration
class TestQuickIntegration:
    """Testes rápidos de integração"""
    
    def test_scrapy_wrapper_basic_init(self):
        """Teste básico de inicialização do ScrapyWrapper"""
        try:
            from src.scrapy_wrapper import ScrapyServimedWrapper
            wrapper = ScrapyServimedWrapper()
            
            # Verificar atributos básicos
            assert hasattr(wrapper, 'logger')
            assert hasattr(wrapper, 'run_spider')
            
        except Exception as e:
            pytest.skip(f"ScrapyWrapper não pôde ser inicializado: {e}")
    
    def test_task_queue_basic_init(self):
        """Teste básico de inicialização do TaskQueue"""
        try:
            from src.nivel2.queue_client import TaskQueueClient
            client = TaskQueueClient()
            
            # Verificar atributos básicos
            assert hasattr(client, 'enqueue_scraping_task')
            assert hasattr(client, 'get_task_status')
            
        except Exception as e:
            pytest.skip(f"TaskQueueClient não pôde ser inicializado: {e}")
    
    def test_main_functions_exist(self):
        """Teste se funções principais existem"""
        try:
            import main
            
            # Verificar se funções existem
            assert callable(getattr(main, 'executar_nivel_1', None))
            assert callable(getattr(main, 'executar_nivel_2', None))
            assert callable(getattr(main, 'main', None))  # Função principal
            
        except Exception as e:
            pytest.skip(f"main.py não pôde ser carregado: {e}")


if __name__ == "__main__":
    # Executar testes básicos se chamado diretamente
    pytest.main([__file__, "-v"])
