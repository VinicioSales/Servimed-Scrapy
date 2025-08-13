"""
Teste direto do PedidoClient
"""

from src.nivel3.pedido_client import PedidoClient

def test_pedido_direct():
    """Testa o PedidoClient diretamente"""
    
    # Criar cliente
    client = PedidoClient()
    
    print("🔧 Testando autenticação...")
    success = client.authenticate()
    print(f"Autenticação: {'✅ OK' if success else '❌ FALHOU'}")
    
    if not success:
        return False
    
    print("\n🔍 Testando busca de produto...")
    produto = client.buscar_produto_por_codigo("7899803001228")
    print(f"Produto encontrado: {produto is not None}")
    
    if produto:
        print(f"Detalhes: {produto}")
        
        print("\n📦 Testando realização de pedido...")
        resultado = client.realizar_pedido("DIRECT_TEST", [{"codigo": "7899803001228", "quantidade": 1}])
        print(f"Resultado: {resultado}")
    
    return True

if __name__ == "__main__":
    test_pedido_direct()
