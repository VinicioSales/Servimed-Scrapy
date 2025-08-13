#!/usr/bin/env python3
"""
SERVIMED SCRAPER - ARQUIVO PRINCIPAL
====================================

Script principal para execução do scraper Servimed com suporte a dois níveis:
- Nível 1: Execução direta (síncrona)
- Nível 2: Processamento via filas (assíncrona)

Exemplos de uso:
- python main.py --nivel 1 --filtro "paracetamol"      # Nível 1 (direto)
- python main.py --nivel 2 --enqueue                   # Nível 2 (fila)
- python main.py --nivel 2 --status TASK_ID            # Status da tarefa

Autor: GitHub Copilot
Data: 12/08/2025
"""

import argparse
import sys
import json
import time
import os
from pathlib import Path

# Adiciona o diretório src ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from servimed_scraper.scraper import ServimedScraperCompleto
except ImportError:
    # Fallback para estrutura de arquivos alternativa
    from scraper import ServimedScraperCompleto


def executar_nivel_1(args):
    """Execução direta (Nível 1) - Modo original"""
    print("EXECUTANDO NIVEL 1 - MODO DIRETO")
    print("=" * 50)
    
    # Inicializa o scraper
    scraper = ServimedScraperCompleto()
    
    # Exibe informações da execução
    print("SERVIMED SCRAPER - INICIALIZACAO")
    print("=" * 50)
    
    if args.filtro:
        print(f"Coletando produtos com filtro: '{args.filtro}'")
        print(f"Arquivo de saida: data/servimed_produtos_filtrados.json")
    else:
        print("Coletando TODOS os produtos")
        print(f"Arquivo de saida: data/servimed_produtos_completos.json")
    
    if args.max_pages:
        print(f"Limitando a {args.max_pages} paginas")
    else:
        print(f"Sem limite de paginas")
    
    print("Backup automatico: data/servimed_backup.json")
    print()
    
    # Executa coleta
    try:
        resultado = scraper.run(filtro=args.filtro, max_pages=args.max_pages)
        
        print("\nEXECUCAO CONCLUIDA COM SUCESSO!")
        print(f"Total de produtos: {resultado['total_produtos']}")
        print(f"Tempo de execucao: {resultado['tempo_execucao']/60:.1f} minutos")
        print(f"Arquivo salvo: {resultado['arquivo_salvo']}")
        
        return resultado
        
    except KeyboardInterrupt:
        print("\nExecucao interrompida pelo usuario")
        return None
    except Exception as e:
        print(f"\nErro durante a execucao: {e}")
        return None


def executar_nivel_2(args):
    """Execução via filas (Nível 2) - Modo assíncrono"""
    print("EXECUTANDO NIVEL 2 - MODO FILAS")
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
        print("Enfileirando nova tarefa de scraping...")
        
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
            max_pages=args.max_pages or 1
        )
        
        print(f"Tarefa enfileirada com ID: {task_id}")
        print(f"Use --status {task_id} para acompanhar o progresso")
        return {"task_id": task_id}
    
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
    """Função principal com suporte aos dois níveis"""
    parser = argparse.ArgumentParser(
        description='Scraper Servimed - Suporte a Nivel 1 (direto) e Nivel 2 (filas)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

NIVEL 1 (Execução Direta):
  python main.py --nivel 1                             # Todos os produtos
  python main.py --nivel 1 --filtro "paracetamol"     # Filtrar por termo
  python main.py --nivel 1 --max-pages 10             # Limitar páginas

NIVEL 2 (Sistema de Filas):
  python main.py --nivel 2 --enqueue                  # Enfileira tarefa
  python main.py --nivel 2 --enqueue --filtro "dipirona" --max-pages 5
  python main.py --nivel 2 --status TASK_ID           # Status da tarefa
  python main.py --nivel 2 --worker-status            # Status dos workers
  
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
    
    # Argumentos do Nível 1 (originais)
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
        help='[Nivel 2] URL da API de callback (padrao: https://desafio.cotefacil.net)'
    )
    
    args = parser.parse_args()
    
    print(f"SERVIMED SCRAPER - NIVEL {args.nivel}")
    print("=" * 60)
    
    # Executa baseado no nível escolhido
    if args.nivel == 1:
        return executar_nivel_1(args)
    elif args.nivel == 2:
        return executar_nivel_2(args)
    elif args.nivel == 3:
        print("🎯 NÍVEL 3: Sistema de Pedidos")
        print("Use: python pedido_queue_client.py enqueue <id_pedido> <codigo_produto> <quantidade>")
        print("Para verificar: python pedido_queue_client.py status <task_id>")
        print("Teste: python pedido_queue_client.py test")
        return None


if __name__ == "__main__":
    main()
