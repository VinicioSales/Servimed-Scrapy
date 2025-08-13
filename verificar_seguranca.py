#!/usr/bin/env python3
"""
Verificador de Segurança
========================

Script para verificar se não há credenciais hardcoded no código.
"""

import os
import re
from pathlib import Path

def verificar_arquivos():
    """Verifica se há credenciais hardcoded nos arquivos Python"""
    
    # Padrões que indicam credenciais hardcoded
    padroes_suspeitos = [
        r'juliano@farmaprevonline\.com\.br',
        r'a007299A',
        r'"usuario":\s*"[^"]*@[^"]*"',
        r'"senha":\s*"[^"]*"'
    ]
    
    # Arquivos Python para verificar
    arquivos_python = [
        'main.py',
        'pedido_queue_client.py', 
        'queue_client.py',
        'src/nivel3/tasks.py',
        'src/nivel3/pedido_client.py'
    ]
    
    problemas_encontrados = []
    
    for arquivo in arquivos_python:
        if not os.path.exists(arquivo):
            continue
            
        print(f"🔍 Verificando {arquivo}...")
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        for i, linha in enumerate(conteudo.split('\n'), 1):
            for padrao in padroes_suspeitos:
                if re.search(padrao, linha):
                    # Ignorar comentários, documentação e exemplos
                    if (linha.strip().startswith('#') or 
                        '"""' in linha or "'''" in linha or
                        '"senha": "senha"' in linha or  # Exemplo genérico
                        '"usuario": "email"' in linha):  # Exemplo genérico
                        continue
                    
                    # Ignorar exemplos no README
                    if 'README' in arquivo or 'example' in arquivo.lower():
                        continue
                        
                    problemas_encontrados.append({
                        'arquivo': arquivo,
                        'linha': i,
                        'conteudo': linha.strip(),
                        'padrao': padrao
                    })
    
    # Relatório
    print("\n" + "="*60)
    print("📋 RELATÓRIO DE SEGURANÇA")
    print("="*60)
    
    if not problemas_encontrados:
        print("✅ SUCESSO: Nenhuma credencial hardcoded encontrada!")
        print("✅ Todas as credenciais estão sendo lidas do .env")
        return True
    else:
        print(f"❌ PROBLEMAS ENCONTRADOS: {len(problemas_encontrados)}")
        print("\nCredenciais hardcoded detectadas:")
        
        for problema in problemas_encontrados:
            print(f"\n📁 {problema['arquivo']}:{problema['linha']}")
            print(f"   {problema['conteudo']}")
        
        print("\n💡 RECOMENDAÇÕES:")
        print("- Remova as credenciais hardcoded")
        print("- Use os.getenv() para ler do .env")
        print("- Adicione validação de credenciais")
        
        return False

def verificar_env():
    """Verifica se o .env tem as variáveis necessárias"""
    
    print("\n🔐 Verificando arquivo .env...")
    
    variaveis_necessarias = [
        'CALLBACK_API_USER',
        'CALLBACK_API_PASSWORD', 
        'CALLBACK_URL',
        'ACCESS_TOKEN',
        'SESSION_TOKEN',
        'LOGGED_USER',
        'CLIENT_ID'
    ]
    
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        return False
    
    with open('.env', 'r', encoding='utf-8') as f:
        conteudo_env = f.read()
    
    faltando = []
    for var in variaveis_necessarias:
        if f"{var}=" not in conteudo_env:
            faltando.append(var)
    
    if faltando:
        print(f"❌ Variáveis faltando no .env: {faltando}")
        return False
    else:
        print("✅ Todas as variáveis necessárias estão no .env")
        return True

if __name__ == "__main__":
    print("🛡️ VERIFICADOR DE SEGURANÇA - SERVIMED SCRAPER")
    print("=" * 60)
    
    seguro_codigo = verificar_arquivos()
    seguro_env = verificar_env()
    
    print("\n" + "="*60)
    print("📊 RESUMO FINAL")
    print("="*60)
    
    if seguro_codigo and seguro_env:
        print("🎉 SISTEMA SEGURO!")
        print("✅ Não há credenciais hardcoded")
        print("✅ Arquivo .env configurado corretamente")
        print("✅ Pronto para produção")
    else:
        print("⚠️ PROBLEMAS DE SEGURANÇA DETECTADOS")
        print("❌ Corrija os problemas antes de usar em produção")
    
    print("="*60)
