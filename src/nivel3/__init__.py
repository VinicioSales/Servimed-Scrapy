"""
Nível 3 - Sistema de Pedidos
============================

Sistema avançado para realizar pedidos de compra e envio para API de callback.
"""

from .pedido_client import PedidoClient
from .tasks import processar_pedido_completo

__all__ = ["PedidoClient", "processar_pedido_completo"]
