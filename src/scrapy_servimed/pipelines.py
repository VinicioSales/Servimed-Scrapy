"""
PIPELINES - SCRAPY SERVIMED
===========================

Pipelines para processamento de dados.
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
from itemadapter import ItemAdapter
import logging

logger = logging.getLogger(__name__)


class ServimedPipeline:
    """Pipeline principal para processamento de produtos"""
    
    def __init__(self):
        self.items_processed = 0
        self.produtos = []
        
    def open_spider(self, spider):
        """Inicializa pipeline quando spider abre"""
        logger.info(f'Iniciando pipeline para spider {spider.name}')
        self.start_time = time.time()
    
    def close_spider(self, spider):
        """Finaliza pipeline quando spider fecha"""
        duration = time.time() - self.start_time
        logger.info(f'Pipeline finalizado: {self.items_processed} itens em {duration:.2f}s')
        
        # Salvar dados se houver produtos
        if self.produtos:
            self.save_to_json()
    
    def process_item(self, item, spider):
        """Processa cada item individualmente"""
        adapter = ItemAdapter(item)
        
        # Validação básica
        if not adapter.get('codigo'):
            logger.warning('Item sem código ignorado')
            return item
        
        # Conversões de tipo
        try:
            if adapter.get('preco_fabrica'):
                adapter['preco_fabrica'] = float(adapter['preco_fabrica'])
            if adapter.get('estoque'):
                adapter['estoque'] = int(adapter['estoque'])
        except (ValueError, TypeError) as e:
            logger.warning(f'Erro na conversão de tipos: {e}')
        
        # Adicionar timestamp
        adapter['timestamp'] = datetime.now().isoformat()
        
        # Adicionar à lista
        self.produtos.append(dict(adapter))
        self.items_processed += 1
        
        logger.info(f'Produto processado: {adapter.get("codigo")} - {adapter.get("descricao", "")[:50]}...')
        
        return item
    
    def save_to_json(self):
        """Salva produtos em arquivo JSON"""
        try:
            # Garantir que o diretório existe
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            # Arquivo de saída
            output_file = data_dir / 'servimed_produtos_scrapy.json'
            
            # Metadados
            metadata = {
                'scraped_at': datetime.now().isoformat(),
                'total_produtos': len(self.produtos),
                'scraper': 'scrapy',
                'fonte': 'servimed'
            }
            
            # Dados finais
            data = {
                'metadata': metadata,
                'produtos': self.produtos
            }
            
            # Salvar
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f'Dados salvos em {output_file}')
            
        except Exception as e:
            logger.error(f'Erro ao salvar JSON: {e}')


class CeleryPipeline:
    """Pipeline para integração com Celery (compatibilidade)"""
    
    def __init__(self):
        self.callback_data = []
    
    def process_item(self, item, spider):
        """Prepara dados para callback"""
        adapter = ItemAdapter(item)
        
        # Formato para callback API
        if adapter.get('gtin'):
            callback_item = {
                'gtin': adapter.get('gtin', ''),
                'codigo': adapter.get('codigo', ''),
                'descricao': adapter.get('descricao', ''),
                'preco_fabrica': adapter.get('preco_fabrica', 0.0),
                'estoque': adapter.get('estoque', 0)
            }
            
            self.callback_data.append(callback_item)
        
        return item
    
    def close_spider(self, spider):
        """Envia dados para sistema de callback se necessário"""
        if hasattr(spider, 'callback_url') and self.callback_data:
            logger.info(f'Preparando {len(self.callback_data)} itens para callback')
            
            # Aqui poderia integrar com o sistema de callback existente
            # Por ora, apenas logamos
            logger.info('Dados prontos para integração com sistema atual')
