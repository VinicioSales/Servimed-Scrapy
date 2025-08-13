"""
ITEMS - SCRAPY SERVIMED
======================

Definição dos items para o scraping.
"""

import scrapy
from itemadapter import ItemAdapter


class ProdutoItem(scrapy.Item):
    """Item para produtos do Servimed"""
    gtin = scrapy.Field()
    codigo = scrapy.Field()
    descricao = scrapy.Field()
    preco_fabrica = scrapy.Field()
    estoque = scrapy.Field()
    
    # Metadados
    url = scrapy.Field()
    timestamp = scrapy.Field()
    usuario = scrapy.Field()
