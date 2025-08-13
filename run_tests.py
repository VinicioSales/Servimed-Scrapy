"""
Script para executar testes pytest com diferentes configurações
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Comando: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Código de retorno: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return False


def main():
    """Função principal para executar testes"""
    print("Iniciando execução dos testes automatizados")
    print(f"Diretório atual: {os.getcwd()}")
    
    # Verificar se pytest está instalado
    print("\nVerificando instalação do pytest...")
    if not run_command("python -m pytest --version", "Verificação do pytest"):
        print("Pytest não está instalado ou não está funcionando")
        print("Execute: pip install pytest")
        return False
    
    # Lista de comandos de teste
    test_commands = [
        # Testes básicos
        ("python -m pytest tests/ -v", "Todos os testes com output detalhado"),
        
        # Testes por categoria (apenas arquivos que existem)
        ("python -m pytest tests/test_main_simple.py -v", "Testes do main.py (simplificado)"),
        ("python -m pytest tests/test_scrapy_wrapper_simple.py -v", "Testes do ScrapyWrapper (simplificado)"),
        ("python -m pytest tests/test_nivel3_simple.py -v", "Testes do Nível 3 (simplificado)"),
        ("python -m pytest tests/test_config.py -v", "Testes de configuração"),
        ("python -m pytest tests/test_basic_functionality.py -v", "Testes de funcionalidade básica"),
        
        # Testes com markers
        ("python -m pytest tests/ -m integration -v", "Apenas testes de integração"),
        
        # Testes com cobertura (se coverage estiver instalado)
        ("python -m pytest tests/ --cov=src --cov=main --cov-report=term-missing", "Testes com cobertura de código"),
        
        # Testes resumidos
        ("python -m pytest tests/ --tb=line", "Testes com output resumido"),
        
        # Apenas verificar se os testes podem ser coletados
        ("python -m pytest tests/ --collect-only", "Coleta de testes (verificação)"),
    ]
    
    # Executar comandos
    success_count = 0
    total_count = len(test_commands)
    
    for command, description in test_commands:
        success = run_command(command, description)
        if success:
            success_count += 1
            print("Sucesso")
        else:
            print("Falhou")
    
    # Resumo final
    print(f"\n{'='*60}")
    print(f"RESUMO FINAL")
    print(f"{'='*60}")
    print(f"Comandos executados: {total_count}")
    print(f"Sucessos: {success_count}")
    print(f"Falhas: {total_count - success_count}")
    print(f"Taxa de sucesso: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("Todos os testes foram executados com sucesso!")
        return True
    else:
        print("Alguns testes falharam. Verifique os logs acima.")
        return False


def run_specific_test(test_path=""):
    """Executa um teste específico"""
    if not test_path:
        test_path = input("Digite o caminho do teste (ex: tests/test_main.py::TestMainScript::test_argument_parsing): ")
    
    if test_path:
        command = f"python -m pytest {test_path} -v -s"
        return run_command(command, f"Teste específico: {test_path}")
    else:
        print("Caminho do teste não fornecido")
        return False


def install_test_dependencies():
    """Instala dependências de teste"""
    dependencies = [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.11.0",
        "pytest-timeout>=2.1.0"
    ]
    
    print("Instalando dependências de teste...")
    
    for dep in dependencies:
        command = f"pip install {dep}"
        success = run_command(command, f"Instalando {dep}")
        if not success:
            print(f"Falha ao instalar {dep}")
            return False
    
    print("Todas as dependências foram instaladas com sucesso!")
    return True


if __name__ == "__main__":
    print("PYTEST RUNNER - Sistema de Testes Automatizados")
    print("=" * 60)
    
    # Menu de opções
    while True:
        print("\nOpções:")
        print("1. Executar todos os testes")
        print("2. Executar teste específico")
        print("3. Instalar dependências de teste")
        print("4. Verificar estrutura de testes")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            main()
        
        elif choice == "2":
            run_specific_test()
        
        elif choice == "3":
            install_test_dependencies()
        
        elif choice == "4":
            run_command("dir tests\\*.py /s /b", "Estrutura de arquivos de teste")
            run_command("python -m pytest tests/ --collect-only", "Coleta de testes")
        
        elif choice == "5":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")
    
    print("\nExecução finalizada.")
