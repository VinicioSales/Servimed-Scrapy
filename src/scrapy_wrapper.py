#!/usr/bin/env python3
"""
SCRAPY WRAPPER - SERVIMED
=========================

Wrapper para executar spiders Scrapy integrado ao sistema atual.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import logging

# Adicionar src ao path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(Path(__file__).parent))

from src.scrapy_servimed.spiders.servimed_spider import ServimedProductsSpider


class ScrapyServimedWrapper:
    """Wrapper para executar Scrapy de forma integrada"""
    
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Configura logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def run_spider(self, filtro='', max_pages=1, callback_url=''):
        """
        Executa spider via subprocess para evitar conflitos de reactor
        
        Args:
            filtro: Filtro de busca
            max_pages: Máximo de páginas
            callback_url: URL para callback
        """
        
        return self.run_spider_subprocess(filtro, max_pages, callback_url)
    
    def run_spider_subprocess(self, filtro='', max_pages=1, callback_url=''):
        """
        Executa spider via subprocess (alternativa)
        
        Args:
            filtro: Filtro de busca  
            max_pages: Máximo de páginas
            callback_url: URL para callback
        """
        
        try:
            self.logger.info("Iniciando Scrapy via subprocess...")
            
            # Comando do Scrapy
            cmd = [
                sys.executable, '-m', 'scrapy', 'crawl', 'servimed_products',
                '-a', f'filtro={filtro}',
                '-a', f'max_pages={max_pages}',
                '-a', f'callback_url={callback_url}',
                '-s', 'LOG_LEVEL=INFO'
            ]
            
            # Executar
            result = subprocess.run(
                cmd,
                cwd=current_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            if result.returncode == 0:
                self.logger.info("Scrapy subprocess finalizado com sucesso!")
                self.logger.info(f"Output: {result.stdout}")
                return True
            else:
                self.logger.error(f"Erro no subprocess: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Timeout no subprocess do Scrapy")
            return False
        except Exception as e:
            self.logger.error(f"Erro no subprocess: {e}")
            return False
    
    def get_results(self):
        """Retorna resultados do scraping"""
        
        result_file = Path('data/servimed_produtos_scrapy.json')
        
        if result_file.exists():
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                produtos = data.get('produtos', [])
                metadata = data.get('metadata', {})
                
                self.logger.info(f"Resultados carregados: {len(produtos)} produtos")
                
                return {
                    'success': True,
                    'produtos': produtos,
                    'metadata': metadata,
                    'total': len(produtos)
                }
                
            except Exception as e:
                self.logger.error(f"Erro ao carregar resultados: {e}")
                return {'success': False, 'error': str(e)}
        else:
            self.logger.warning("Arquivo de resultados não encontrado")
            return {'success': False, 'error': 'Arquivo não encontrado'}



