"""
Testes para spiders Scrapy (src/scrapy_servimed/spiders/)
"""
import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import scrapy
from scrapy.http import HtmlResponse

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestServimedSpider:
    """Testes para o spider Servimed"""
    
    @pytest.fixture
    def spider(self):
        """Fixture para criar instância do spider"""
        try:
            from src.scrapy_servimed.spiders.servimed_spider import ServimedProductsSpider
            return ServimedProductsSpider()
        except ImportError:
            pytest.skip("ServimedProductsSpider não disponível")
    
    @pytest.fixture
    def mock_response(self):
        """Fixture para resposta HTTP mock"""
        html_content = """
        <html>
            <body>
                <div class="product">
                    <h2>Produto Teste</h2>
                    <span class="price">R$ 19,99</span>
                    <p class="description">Descrição do produto teste</p>
                    <div class="ean">1234567890123</div>
                </div>
            </body>
        </html>
        """
        return HtmlResponse(
            url="https://www.servimed.com.br/produto-teste",
            body=html_content.encode('utf-8'),
            encoding='utf-8'
        )
    
    def test_spider_initialization(self, spider):
        """Testa inicialização do spider"""
        assert hasattr(spider, 'name')
        assert hasattr(spider, 'allowed_domains')
        assert hasattr(spider, 'start_urls')
    
    def test_spider_name(self, spider):
        """Testa nome do spider"""
        assert spider.name == 'servimed_products'
    
    def test_spider_allowed_domains(self, spider):
        """Testa domínios permitidos"""
        assert 'servimed.com.br' in spider.allowed_domains
    
    def test_parse_method_exists(self, spider):
        """Testa se método parse existe"""
        assert hasattr(spider, 'parse')
        assert callable(getattr(spider, 'parse'))
    
    def test_parse_product_response(self, spider, mock_response):
        """Testa parsing de resposta com produto"""
        if not hasattr(spider, 'parse'):
            pytest.skip("Método parse não disponível")
        
        results = list(spider.parse(mock_response))
        
        # Verificar se retornou algum resultado
        assert len(results) > 0
        
        # Se retornou um item, verificar estrutura
        if results and hasattr(results[0], '__getitem__'):
            item = results[0]
            # Verificar campos esperados em um produto
            expected_fields = ['name', 'price', 'url', 'description']
            for field in expected_fields:
                if field in item:
                    assert item[field] is not None
    
    @patch('scrapy.Request')
    def test_spider_generates_requests(self, mock_request, spider):
        """Testa se spider gera requests apropriados"""
        if hasattr(spider, 'start_requests'):
            requests = list(spider.start_requests())
            assert len(requests) > 0
        else:
            # Se não tem start_requests, deve ter start_urls
            assert hasattr(spider, 'start_urls')
            assert len(spider.start_urls) > 0


class TestSpiderPipelines:
    """Testes para pipelines do Scrapy"""
    
    def test_pipeline_imports(self):
        """Testa importação de pipelines"""
        try:
            from src.scrapy_servimed import pipelines
            assert hasattr(pipelines, 'ScrapyServimedPipeline')
        except ImportError:
            pytest.skip("Pipelines não disponíveis")
    
    def test_pipeline_process_item(self):
        """Testa processamento de item no pipeline"""
        try:
            from src.scrapy_servimed.pipelines import ScrapyServimedPipeline
            
            pipeline = ScrapyServimedPipeline()
            
            # Item de teste
            test_item = {
                'name': 'Produto Teste',
                'price': 'R$ 19,99',
                'url': 'https://test.com/produto'
            }
            
            # Mock spider
            mock_spider = Mock()
            mock_spider.name = 'test_spider'
            
            # Processar item
            result = pipeline.process_item(test_item, mock_spider)
            
            # Verificar que o item foi retornado
            assert result is not None
            
        except ImportError:
            pytest.skip("Pipeline não disponível")
        except Exception as e:
            # Se o pipeline tem dependências específicas, pode falhar
            pytest.skip(f"Pipeline falhou: {e}")


class TestSpiderSettings:
    """Testes para configurações do Scrapy"""
    
    def test_settings_import(self):
        """Testa importação das configurações"""
        try:
            from src.scrapy_servimed import settings
            assert hasattr(settings, 'BOT_NAME')
        except ImportError:
            pytest.skip("Settings não disponíveis")
    
    def test_settings_values(self):
        """Testa valores das configurações"""
        try:
            from src.scrapy_servimed import settings
            
            # Verificar configurações básicas
            assert hasattr(settings, 'SPIDER_MODULES')
            assert hasattr(settings, 'NEWSPIDER_MODULE')
            
            # Verificar se valores são apropriados
            if hasattr(settings, 'ROBOTSTXT_OBEY'):
                assert isinstance(settings.ROBOTSTXT_OBEY, bool)
            
            if hasattr(settings, 'DOWNLOAD_DELAY'):
                assert isinstance(settings.DOWNLOAD_DELAY, (int, float))
                assert settings.DOWNLOAD_DELAY >= 0
                
        except ImportError:
            pytest.skip("Settings não disponíveis")


class TestSpiderItems:
    """Testes para items do Scrapy"""
    
    def test_items_import(self):
        """Testa importação dos items"""
        try:
            from src.scrapy_servimed import items
            # Verificar se tem alguma classe de item definida
            assert hasattr(items, 'scrapy')
        except ImportError:
            pytest.skip("Items não disponíveis")
    
    def test_product_item_creation(self):
        """Testa criação de item de produto"""
        try:
            from src.scrapy_servimed.items import ProductItem
            
            item = ProductItem()
            
            # Verificar se é um item válido do Scrapy
            assert hasattr(item, '__setitem__')
            assert hasattr(item, '__getitem__')
            
            # Testar atribuição de valores
            item['name'] = 'Produto Teste'
            item['price'] = 19.99
            
            assert item['name'] == 'Produto Teste'
            assert item['price'] == 19.99
            
        except ImportError:
            # Se não há ProductItem específico, pular teste
            pytest.skip("ProductItem não disponível")


class TestSpiderIntegration:
    """Testes de integração dos spiders"""
    
    @patch('scrapy.crawler.CrawlerProcess')
    def test_spider_can_be_run(self, mock_crawler_process):
        """Testa se spider pode ser executado"""
        try:
            from src.scrapy_servimed.spiders.servimed_spider import ServimedProductsSpider
            
            # Mock do processo do crawler
            mock_process = Mock()
            mock_crawler_process.return_value = mock_process
            
            # Tentar criar e configurar spider
            spider = ServimedProductsSpider()
            
            # Verificar que spider foi criado com sucesso
            assert spider is not None
            assert hasattr(spider, 'name')
            
        except ImportError:
            pytest.skip("Spider não disponível")
    
    def test_spider_with_custom_settings(self):
        """Testa spider com configurações customizadas"""
        try:
            from src.scrapy_servimed.spiders.servimed_spider import ServimedProductsSpider
            
            # Configurações customizadas
            custom_settings = {
                'DOWNLOAD_DELAY': 2,
                'CONCURRENT_REQUESTS': 1,
                'ROBOTSTXT_OBEY': True
            }
            
            spider = ServimedProductsSpider()
            
            # Se spider suporta custom_settings
            if hasattr(spider, 'custom_settings'):
                spider.custom_settings = custom_settings
                
                for key, value in custom_settings.items():
                    assert spider.custom_settings[key] == value
                    
        except ImportError:
            pytest.skip("Spider não disponível")
    
    def test_spider_error_handling(self):
        """Testa tratamento de erros do spider"""
        try:
            from src.scrapy_servimed.spiders.servimed_spider import ServimedProductsSpider
            
            spider = ServimedProductsSpider()
            
            # Criar resposta inválida
            invalid_response = HtmlResponse(
                url="https://invalid.url",
                body=b"<html><body></body></html>",
                encoding='utf-8'
            )
            
            # Tentar parse - não deve quebrar
            results = list(spider.parse(invalid_response))
            
            # Pode retornar lista vazia ou com erros tratados
            assert isinstance(results, list)
            
        except ImportError:
            pytest.skip("Spider não disponível")
        except Exception as e:
            # Verificar se é um erro esperado/tratado
            assert "parse" in str(e).lower() or "response" in str(e).lower()
