#!/usr/bin/env python3
"""
Teste direto do CallbackAPIClient
=================================
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api_client.callback_client import CallbackAPIClient
import json

def test_callback_client():
    """Teste do CallbackAPIClient completo"""
    
    print("=== TESTE CALLBACK CLIENT ===")
    
    # Criar cliente
    client = CallbackAPIClient()
    
    # Autenticar
    print("1. Realizando autenticação...")
    auth_result = client.authenticate()
    
    if not auth_result:
        print("❌ Falha na autenticação")
        return False
    
    # Dados de teste
    test_products = [
        {
            "gtin_ean": "7898636193493",
            "codigo": "444212",
            "descricao": "BEBIDA HIDRATANTE SOROX LIMAO 550ML - TESTE CLIENT",
            "preco_fabrica": 8.18,
            "estoque": 4102
        }
    ]
    
    print("\n2. Enviando produtos...")
    send_result = client.send_products(test_products)
    
    if send_result:
        print("✅ SUCCESS - Produtos enviados!")
        return True
    else:
        print("❌ ERRO - Falha no envio")
        return False

if __name__ == "__main__":
    test_callback_client()
