"""
Servimed Scraper - Portal de Produtos

Um scraper profissional para coletar produtos do Portal Servimed
com autenticação JWT e extração de dados específicos.
"""

__version__ = "1.0.0"
__author__ = "Servimed Team"
__email__ = "juliano@farmaprevonline.com.br"

from .scraper import ServimedScraperCompleto

__all__ = ["ServimedScraperCompleto"]
