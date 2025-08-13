#!/usr/bin/env python3
"""
Cliente de Queue - Nível 3
===========================

Cliente para enfileirar e monitorar tarefas de pedidos.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.nivel2.celery_app import app


class PedidoQueueClient:
    """Cliente para gerenciar filas de pedidos"""
    
    def __init__(self):
        self.app = app
    
    def enqueue_pedido(self, usuario: str, senha: str, id_pedido: str, 
                      produtos: List[Dict], callback_url: str = "https://desafio.cotefacil.net") -> str:
        """
        Enfileira uma tarefa de pedido - sempre usa Scrapy
        
        Args:
            usuario: Email do usuário
            senha: Senha do usuário
            id_pedido: ID único do pedido
            produtos: Lista de produtos [{"gtin": "123", "codigo": "A123", "quantidade": 1}]
            callback_url: URL para callback
            
        Returns:
            str: ID da task criada
        """
        task_data = {
            "usuario": usuario,
            "senha": senha,
            "id_pedido": id_pedido,
            "produtos": produtos,
            "callback_url": callback_url,
            "framework": "scrapy"  # Sempre usar Scrapy
        }
        
        # Enviar para a fila
        result = self.app.send_task(
            'src.nivel3.tasks.processar_pedido_completo',
            args=[task_data],
            queue='celery'
        )
        
        return result.id
    
    def get_status(self, task_id: str) -> Dict[str, Any]:
        """
        Verifica status de uma tarefa
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            Dict: Status da tarefa
        """
        result = self.app.AsyncResult(task_id)
        
        return {
            "task_id": task_id,
            "status": result.status,
            "ready": result.ready(),
            "result": result.result if result.ready() else None,
            "error": str(result.traceback) if result.failed() else None
        }


def main():
    """Interface CLI para o cliente"""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python pedido_queue_client.py enqueue <id_pedido> <codigo_produto> <quantidade> [gtin]")
        print("  python pedido_queue_client.py status <task_id>")
        print("  python pedido_queue_client.py test")
        print("")
        print("ℹ️  Sempre usa Scrapy automaticamente")
        return
    
    client = PedidoQueueClient()
    command = sys.argv[1].lower()
    
    if command == "enqueue":
        if len(sys.argv) < 5:
            print("❌ Parâmetros insuficientes")
            print("Uso: python pedido_queue_client.py enqueue <id_pedido> <codigo_produto> <quantidade> [gtin]")
            return
        
        id_pedido = sys.argv[2]
        codigo_produto = sys.argv[3]
        quantidade = int(sys.argv[4])
        gtin = sys.argv[5] if len(sys.argv) > 5 else ""
        
        # Dados do .env
        usuario = os.getenv('CALLBACK_API_USER')
        senha = os.getenv('CALLBACK_API_PASSWORD')
        
        if not usuario or not senha:
            print("❌ Credenciais não encontradas no .env")
            print("Verifique CALLBACK_API_USER e CALLBACK_API_PASSWORD")
            return
        
        produtos = [{
            "gtin": gtin,  # GTIN fornecido ou vazio
            "codigo": codigo_produto,
            "quantidade": quantidade
        }]
        
        print(f"📦 Enfileirando pedido {id_pedido} com Scrapy...")
        print(f"Produto: {codigo_produto} (Qtd: {quantidade})")
        if gtin:
            print(f"GTIN: {gtin}")
        
        task_id = client.enqueue_pedido(usuario, senha, id_pedido, produtos)
        print(f"Task criada: {task_id}")
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ Task ID necessário")
            print("Uso: python pedido_queue_client.py status <task_id>")
            return
        
        task_id = sys.argv[2]
        status = client.get_status(task_id)
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    elif command == "test":
        print("🧪 Testando sistema de pedidos com Scrapy...")
        
        # Criar pedido de teste
        id_pedido = f"TEST{int(time.time())}"
        produtos = [{
            "gtin": "",
            "codigo": "444212",  # Produto hidratante que sabemos que existe
            "quantidade": 2
        }]
        # Dados do .env
        usuario = os.getenv('CALLBACK_API_USER')
        senha = os.getenv('CALLBACK_API_PASSWORD')
        
        if not usuario or not senha:
            print("❌ Credenciais não encontradas no .env")
            print("Verifique CALLBACK_API_USER e CALLBACK_API_PASSWORD")
            return
        
        task_id = client.enqueue_pedido(
            usuario,
            senha, 
            id_pedido,
            produtos
        )
        
        print(f"✅ Pedido de teste criado: {task_id}")
        print(f"ID Pedido: {id_pedido}")
        print("Execute 'status {task_id}' para acompanhar")
    
    else:
        print(f"❌ Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
