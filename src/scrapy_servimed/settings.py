"""
SCRAPY PROJECT - SERVIMED SCRAPER
=================================

Projeto Scrapy para scraping do portal Servimed.
Mantém compatibilidade com o sistema atual.
"""

BOT_NAME = 'servimed_scrapy'

SPIDER_MODULES = ['src.scrapy_servimed.spiders']
NEWSPIDER_MODULE = 'src.scrapy_servimed.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS = 1

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    'src.scrapy_servimed.middlewares.OAuth2AuthMiddleware': 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'src.scrapy_servimed.middlewares.ServimedSessionMiddleware': 543,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'src.scrapy_servimed.pipelines.ServimedPipeline': 300,
    'src.scrapy_servimed.pipelines.CeleryPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Configurações de segurança
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Logs
LOG_LEVEL = 'INFO'

# Configurações customizadas
SERVIMED_BASE_URL = 'https://peapi.servimed.com.br'
SERVIMED_PORTAL_URL = 'https://pedidoeletronico.servimed.com.br'
