#!/usr/bin/env python3
"""
SERVIMED SCRAPER - ARQUIVO PRINCIPAL
====================================

Script principal para execução do scraper Servimed.
Suporta parâmetros de linha de comando para diferentes tipos de busca.

Exemplos de uso:
- python main.py                          # Todos os produtos
- python main.py --filtro "paracetamol"   # Filtrar por termo
- python main.py --max-pages 10           # Limitar páginas
- python main.py -f "dipirona" -p 5       # Combinar filtro e limite

Autor: GitHub Copilot
Data: 12/08/2025
"""

import argparse
import sys
from pathlib import Path

# Adiciona o diretório src ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from servimed_scraper import ServimedScraperCompleto


def main():
    """Função principal com suporte a parâmetros de linha de comando"""
    parser = argparse.ArgumentParser(
        description='Scraper para coletar produtos do Portal Servimed',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                          # Todos os produtos
  python main.py --filtro "paracetamol"   # Filtrar por termo
  python main.py --max-pages 10           # Limitar páginas
  python main.py --filtro "dipirona" --max-pages 5
  
Arquivos de saída (sempre sobrescreve):
  data/servimed_produtos_completos.json   # Todos os produtos
  data/servimed_produtos_filtrados.json   # Produtos filtrados
  data/servimed_backup.json               # Backup automático
        """
    )
    
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
        help='Número máximo de páginas para processar (padrão: sem limite)'
    )
    
    args = parser.parse_args()
    
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


if __name__ == "__main__":
    main()
