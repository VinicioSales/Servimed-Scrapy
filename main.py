#!/usr/bin/env python3
"""
SERVIMED SCRAPER - ARQUIVO PRINCIPAL
====================================

Script principal para execução do scraper Servimed.
Sempre usa Scrapy framework em todos os níveis.

- Nível 1: Execução direta (síncrona)
- Nível 2: Processamento via filas (assíncrona)
- Nível 3: Sistema de pedidos
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Carregar configurações
load_dotenv()

# Configurar paths
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Imports condicionais dos scrapers
try:
    from servimed_scraper.scraper import ServimedScraperCompleto
except ImportError:
    try:
        from scraper import ServimedScraperCompleto
    except ImportError:
        ServimedScraperCompleto = None

try:
    from src.scrapy_wrapper import ScrapyServimedWrapper
except ImportError:
    ScrapyServimedWrapper = None


def executar_nivel_1(args):
    """Execução direta (Nível 1) - Sempre usando Scrapy"""
    print("EXECUTANDO NIVEL 1 - MODO DIRETO")
    print("=" * 50)
    print("🕷️ USANDO FRAMEWORK SCRAPY")
    print("=" * 50)
    
    # Verificar se Scrapy está disponível
    if not ScrapyServimedWrapper:
        print("❌ Scrapy wrapper não está disponível")
        print("Verifique se o Scrapy está instalado: pip install scrapy")
        return None
    
    if args.filtro:
        print(f"Coletando produtos com filtro: '{args.filtro}'")
    else:
        print("Coletando produtos via Scrapy")
    
    if args.max_pages:
        print(f"Limitando a {args.max_pages} paginas")
    
    print("Framework: Scrapy 2.13.3")
    print("Arquivo de saida: data/servimed_produtos_scrapy.json")
    print()
    
    # Executar via Scrapy
    try:
        wrapper = ScrapyServimedWrapper()
        resultado = wrapper.run_spider(
            filtro=args.filtro or '', 
            max_pages=args.max_pages or 1
        )
        
        if resultado:
            print("\n✅ EXECUCAO SCRAPY CONCLUIDA COM SUCESSO!")
            
            # Carregar resultados
            results = wrapper.get_results()
            if results['success']:
                print(f"Total de produtos: {results['total']}")
                print(f"Arquivo salvo: data/servimed_produtos_scrapy.json")
                return {
                    'total_produtos': results['total'],
                    'arquivo_salvo': 'data/servimed_produtos_scrapy.json',
                    'framework': 'Scrapy 2.13.3',
                    'success': True
                }
            else:
                print(f"❌ Erro ao carregar resultados: {results.get('error')}")
                return None
        else:
            print("❌ Erro na execução do Scrapy")
            return None
            
    except Exception as e:
        print(f"\n❌ Erro durante execução Scrapy: {e}")
        return None


def executar_nivel_2(args):
    """Execução via filas (Nível 2) - Sempre usando Scrapy"""
    print("EXECUTANDO NIVEL 2 - MODO FILAS")
    print("=" * 50)
    print("🕷️ USANDO FRAMEWORK SCRAPY")
    print("=" * 50)
    
    try:
        from nivel2.queue_client import TaskQueueClient
    except ImportError as e:
        print(f"Erro ao importar cliente de filas: {e}")
        print("Certifique-se de que o Redis e Celery estao instalados:")
        print("pip install celery redis")
        return None
    
    client = TaskQueueClient()
    
    if args.enqueue:
        # Enfileirar nova tarefa
        print("Enfileirando nova tarefa de scraping com Scrapy...")
        
        # Credenciais do .env ou argumentos
        usuario = args.usuario or os.getenv('CALLBACK_API_USER')
        senha = args.senha or os.getenv('CALLBACK_API_PASSWORD')
        callback_url = args.callback_url or os.getenv('CALLBACK_URL', 'https://desafio.cotefacil.net')
        
        if not usuario or not senha:
            print("❌ Credenciais não encontradas")
            print("Forneça via argumentos --usuario/--senha ou configure no .env:")
            print("CALLBACK_API_USER e CALLBACK_API_PASSWORD")
            return
        
        task_id = client.enqueue_scraping_task(
            usuario=usuario,
            senha=senha,
            callback_url=callback_url,
            filtro=args.filtro or "",
            max_pages=args.max_pages or 1,
            framework="scrapy"  # Sempre usar Scrapy
        )
        
        print(f"Tarefa Scrapy enfileirada com ID: {task_id}")
        print(f"Use --status {task_id} para acompanhar o progresso")
        return {"task_id": task_id, "framework": "scrapy"}
    
    elif args.status:
        # Verificar status de tarefa
        print(f"Verificando status da tarefa: {args.status}")
        status = client.get_task_status(args.status)
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return status
    
    elif args.worker_status:
        # Status dos workers
        print("Status dos workers:")
        status = client.get_worker_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return status
    
    else:
        print("Para Nivel 2, use uma das opcoes:")
        print("  --enqueue          : Enfileira nova tarefa")
        print("  --status TASK_ID   : Verifica status de tarefa")
        print("  --worker-status    : Status dos workers")
        return None


def main():
    """Função principal com suporte aos três níveis"""
    parser = argparse.ArgumentParser(
        description='Scraper Servimed - Sempre usando Scrapy em todos os níveis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

NIVEL 1 - Execução Direta com Scrapy:
  python main.py --nivel 1                             # Todos os produtos
  python main.py --nivel 1 --filtro "paracetamol"     # Filtrar por termo
  python main.py --nivel 1 --max-pages 10             # Limitar páginas

NIVEL 2 - Sistema de Filas com Scrapy:
  python main.py --nivel 2 --enqueue                  # Enfileira tarefa
  python main.py --nivel 2 --enqueue --filtro "dipirona" --max-pages 5
  python main.py --nivel 2 --status TASK_ID           # Status da tarefa
  python main.py --nivel 2 --worker-status            # Status dos workers

NIVEL 3 - Sistema de Pedidos com Scrapy:
  python pedido_queue_client.py test                  # Teste de pedido
  python pedido_queue_client.py enqueue <id> <codigo> <qtd>

Pré-requisitos para Nível 2:
  - Redis rodando (redis-server)
  - Worker Celery ativo (celery -A src.nivel2.celery_app worker --loglevel=info)
        """
    )
    
    # Argumento principal: nível
    parser.add_argument(
        '--nivel', '-n',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='Nivel de execucao: 1=Direto, 2=Filas, 3=Pedidos (padrao: 1)'
    )
    
    # Argumentos do Nível 1
    parser.add_argument(
        '--filtro', '-f',
        type=str,
        default="",
        help='Termo para filtrar produtos (ex: "paracetamol", "dipirona")'
    )
    
    parser.add_argument(
        '--max-pages', '-p',
        type=int,
        default=None,
        help='Numero maximo de paginas para processar (padrao: sem limite)'
    )
    
    # Argumentos do Nível 2 (filas)
    parser.add_argument(
        '--enqueue',
        action='store_true',
        help='[Nivel 2] Enfileira nova tarefa de scraping'
    )
    
    parser.add_argument(
        '--status',
        type=str,
        help='[Nivel 2] Verifica status de uma tarefa pelo ID'
    )
    
    parser.add_argument(
        '--worker-status',
        action='store_true',
        help='[Nivel 2] Mostra status dos workers'
    )
    
    parser.add_argument(
        '--usuario',
        type=str,
        help='[Nivel 2] Usuario para autenticacao na API (padrao: do .env)'
    )
    
    parser.add_argument(
        '--senha',
        type=str,
        help='[Nivel 2] Senha para autenticacao na API (padrao: do .env)'
    )
    
    parser.add_argument(
        '--callback-url',
        type=str,
        help='[Nivel 2] URL para callback (padrao: do .env)'
    )
    
    args = parser.parse_args()
    
    # Inicialização comum
    print("SERVIMED SCRAPER - ARQUIVO PRINCIPAL")
    print("=" * 60)
    print("🕷️ FRAMEWORK: SCRAPY EM TODOS OS NÍVEIS")
    print("=" * 60)
    
    # Executar o nível apropriado
    if args.nivel == 1:
        return executar_nivel_1(args)
    elif args.nivel == 2:
        return executar_nivel_2(args)
    elif args.nivel == 3:
        print("🎯 NÍVEL 3: Sistema de Pedidos")
        print("Use: python pedido_queue_client.py enqueue <id_pedido> <codigo_produto> <quantidade> [gtin]")
        print("Para verificar: python pedido_queue_client.py status <task_id>")
        print("Teste: python pedido_queue_client.py test")
        print("")
        print("ℹ️  O Nível 3 sempre usa Scrapy automaticamente.")
        return None


if __name__ == "__main__":
    main()
