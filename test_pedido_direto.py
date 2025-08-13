#!/usr/bin/env python3
"""
Teste direto do sistema de pedidos
==================================
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.nivel3.pedido_client import PedidoClient

def test_pedido_client():
    """Teste direto do cliente de pedidos"""
    
    print("=== TESTE DIRETO PEDIDO CLIENT ===")
    
    # Criar cliente
    client = PedidoClient()
    
    # Autenticar
    print("1. Testando autenticação...")
    auth_result = client.authenticate()
    
    if not auth_result:
        print("❌ Falha na autenticação")
        return False
    
    print("✅ Autenticação OK")
    
    # Buscar produto
    print("\n2. Buscando produto código 444212...")
    produto = client.buscar_produto_por_codigo("444212")
    
    if produto:
        print(f"✅ Produto encontrado: {produto.get('descricao', '')}")
        print(f"   Preço: R$ {produto.get('preco_fabrica', 0)}")
    else:
        print("❌ Produto não encontrado")
        return False
    
    # Simular pedido (sem fazer request real)
    print("\n3. Simulando estrutura do pedido...")
    produtos_pedido = [{
        "gtin": produto.get('gtin_ean', ''),
        "codigo": produto.get('codigo', ''),
        "quantidade": 2
    }]
    
    print(f"Produto: {produtos_pedido[0]['codigo']} (Qtd: 2)")
    print("✅ Estrutura do pedido OK")
    
    print("\n🎯 RESULTADO: Sistema de pedidos está estruturado corretamente!")
    print("Para completar, seria necessário fazer o POST real para /api/Pedido/TrasmitirPedido")
    
    return True

if __name__ == "__main__":
    test_pedido_client()
