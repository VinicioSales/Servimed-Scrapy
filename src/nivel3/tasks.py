"""
Tasks Celery - Nível 3
=======================

Tasks para processamento de pedidos CONFORME DESAFIO COTEFÁCIL:
1. Após login, buscar produto pelo código no Servimed (usando Scrapy)
2. Realizar pedido via formulário no site Servimed
3. Chamar API do desafio para gerar pedido aleatório
4. Fazer PATCH /pedido/:id com dados de confirmação do pedido
"""

import json
import time
from typing import Dict, Any
from celery import Task

from ..nivel2.celery_app import app
from ..api_client.callback_client import CallbackAPIClient
from .pedido_client import PedidoClient


@app.task(bind=True, name='src.nivel3.tasks.processar_pedido_completo')
def processar_pedido_completo(self: Task, task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa pedido completo: busca produto, realiza pedido, envia callback
    Com suporte a framework Scrapy
    
    Args:
        task_data: {
            "usuario": "email",
            "senha": "senha", 
            "id_pedido": "1234",
            "produtos": [{"gtin": "123", "codigo": "A123", "quantidade": 1}],
            "callback_url": "https://desafio.cotefacil.net",
            "framework": "original" ou "scrapy"
        }
    
    Returns:
        Dict: Resultado da operação
    """
    task_id = self.request.id
    framework = task_data.get('framework', 'original')
    
    try:
        print(f"[{task_id}] === NÍVEL 3 - PROCESSAMENTO DE PEDIDO ({framework}) ===")
        print(f"[{task_id}] Iniciando processamento...")
        
        # Extrair dados da tarefa
        usuario = task_data.get('usuario')
        senha = task_data.get('senha')
        id_pedido = task_data.get('id_pedido')
        produtos = task_data.get('produtos', [])
        callback_url = task_data.get('callback_url', 'https://desafio.cotefacil.net')
        
        print(f"[{task_id}] Framework: {framework}")
        print(f"[{task_id}] ID Pedido: {id_pedido}")
        print(f"[{task_id}] Produtos: {len(produtos)} itens")
        print(f"[{task_id}] Callback URL: {callback_url}")
        
        if not produtos:
            raise ValueError("Nenhum produto especificado para o pedido")
        
        # 0. ETAPA ADICIONAL: Buscar produtos via scraping para verificar disponibilidade
        print(f"[{task_id}] 0. Verificando disponibilidade dos produtos...")
        produtos_verificados = []
        
        for produto in produtos:
            codigo = produto.get('codigo', '')
            gtin = produto.get('gtin', '')
            
            if not codigo and not gtin:
                print(f"[{task_id}] Produto sem código/GTIN, pulando...")
                continue
            
            # Buscar produto via framework escolhido
            produto_encontrado = None
            
            if framework == 'scrapy':
                print(f"[{task_id}] Buscando {codigo} via Scrapy...")
                try:
                    from scrapy_wrapper import ScrapyServimedWrapper
                    
                    wrapper = ScrapyServimedWrapper()
                    resultado = wrapper.run_spider(filtro=codigo, max_pages=1)
                    
                    if resultado:
                        results = wrapper.get_results()
                        if results['success']:
                            for prod in results['produtos']:
                                if prod.get('codigo') == codigo or prod.get('gtin') == gtin:
                                    produto_encontrado = prod
                                    break
                    
                    if produto_encontrado:
                        print(f"[{task_id}] Produto {codigo} encontrado via Scrapy")
                    else:
                        print(f"[{task_id}] Produto {codigo} não encontrado via Scrapy")
                        
                except ImportError:
                    print(f"[{task_id}] Scrapy não disponível, usando sistema original")
                    framework = 'original'
            
            if framework == 'original' or not produto_encontrado:
                print(f"[{task_id}] Buscando {codigo} via sistema original...")
                
                from servimed_scraper.scraper import ServimedScraperCompleto
                
                scraper = ServimedScraperCompleto()
                resultado_scraping = scraper.run(filtro=codigo, max_pages=1)
                
                # Buscar produto nos resultados
                arquivo_produtos = resultado_scraping['arquivo_salvo']
                with open(arquivo_produtos, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                for prod in dados.get('produtos', []):
                    if prod.get('codigo') == codigo or prod.get('gtin') == gtin:
                        produto_encontrado = prod
                        break
                
                if produto_encontrado:
                    print(f"[{task_id}] Produto {codigo} encontrado via sistema original")
                else:
                    print(f"[{task_id}] Produto {codigo} não encontrado")
            
            if produto_encontrado:
                # Adicionar dados do scraping ao produto do pedido
                produto_completo = {
                    **produto,
                    'descricao': produto_encontrado.get('descricao', ''),
                    'preco_fabrica': produto_encontrado.get('preco_fabrica', 0),
                    'estoque_disponivel': produto_encontrado.get('estoque', 0),
                    'verificado_via': framework
                }
                produtos_verificados.append(produto_completo)
            else:
                print(f"[{task_id}] Produto {codigo} não verificado, incluindo mesmo assim")
                produtos_verificados.append(produto)
        
        print(f"[{task_id}] Produtos verificados: {len(produtos_verificados)}/{len(produtos)}")
        
        # 1. Criar cliente de pedidos e autenticar
        print(f"[{task_id}] 1. Autenticando no portal...")
        pedido_client = PedidoClient()
        auth_success = pedido_client.authenticate()
        
        if not auth_success:
            raise ValueError("Falha na autenticação no portal Servimed")
        
        # 2. Realizar pedido
        print(f"[{task_id}] 2. Realizando pedido...")
        codigo_pedido_servimed = pedido_client.realizar_pedido(produtos_verificados)
        
        if not codigo_pedido_servimed:
            raise ValueError("Falha ao realizar pedido no portal")
        
        print(f"[{task_id}] Pedido realizado! Código Servimed: {codigo_pedido_servimed}")
        
        # 3. Chamar API do desafio para gerar pedido aleatório
        print(f"[{task_id}] 3. Chamando API do desafio para gerar pedido aleatório...")
        api_client = CallbackAPIClient(base_url=callback_url)
        
        # Autenticar na API Cotefacil
        api_auth_success = api_client.authenticate()
        if not api_auth_success:
            raise ValueError("Falha na autenticação com API Cotefacil")
        
        # Gerar pedido aleatório conforme requisito do desafio
        pedido_aleatorio_id = gerar_pedido_aleatorio_api(api_client)
        
        if not pedido_aleatorio_id:
            raise ValueError("Falha crítica: não foi possível gerar pedido aleatório na API")
        
        print(f"[{task_id}] Pedido aleatório gerado: {pedido_aleatorio_id}")
        
        # 4. Fazer PATCH /pedido/:id com dados de confirmação
        print(f"[{task_id}] 4. Enviando PATCH para /pedido/{pedido_aleatorio_id}...")
        
        callback_data = {
            "codigo_confirmacao": str(codigo_pedido_servimed),
            "status": "pedido_realizado"
        }
        
        print(f"[{task_id}] Enviando confirmação com código Servimed: {codigo_pedido_servimed}")
        
        # Fazer PATCH conforme especificação do desafio
        patch_success = fazer_patch_pedido(api_client, pedido_aleatorio_id, callback_data)
        
        if not patch_success:
            print(f"[{task_id}] PATCH falhou, mas pedido foi realizado no Servimed")
        
        # Resultado final
        resultado_final = {
            'status': 'success',
            'task_id': task_id,
            'id_pedido_interno': id_pedido,
            'pedido_aleatorio_api': pedido_aleatorio_id,
            'codigo_pedido_servimed': codigo_pedido_servimed,
            'produtos_pedido': len(produtos),
            'patch_enviado': patch_success,
            'callback_url': callback_url,
            'timestamp': time.time()
        }
        
        print(f"[{task_id}] Processamento concluído!")
        return resultado_final
        
    except Exception as e:
        error_msg = f"Erro no pedido {self.request.id}: {str(e)}"
        print(f"[ERROR] {error_msg}")
        
        # Log do erro para debug
        import traceback
        traceback.print_exc()
        
        return {
            'status': 'error',
            'task_id': self.request.id,
            'id_pedido': task_data.get('id_pedido', 'unknown'),
            'error': error_msg,
            'timestamp': time.time()
        }


def gerar_pedido_aleatorio_api(api_client: CallbackAPIClient) -> str:
    """
    Chama a API do desafio para gerar um pedido aleatório
    Conforme requisito: "Chamar a API do desafio para gerar um pedido aleatório"
    
    Args:
        api_client: Cliente da API autenticado
        
    Returns:
        str: ID do pedido aleatório ou string vazia se falhar
    """
    try:
        print("Gerando pedido aleatório conforme requisito do desafio...")
        
        # Tentativa 1: POST /pedido (dados vazios para gerar aleatório)
        response = api_client.session.post(
            f"{api_client.base_url}/pedido",
            json={},  # Dados vazios conforme padrão para gerar aleatório
            timeout=30
        )
        
        print(f"POST /pedido - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            resultado = response.json()
            pedido_id = resultado.get('id')
            if pedido_id:
                print(f"Pedido aleatório gerado: {pedido_id}")
                return str(pedido_id)
        
        # Tentativa 2: Outros endpoints possíveis
        endpoints_alternativos = ["/pedido/random", "/pedido/gerar", "/pedido/novo"]
        
        for endpoint in endpoints_alternativos:
            try:
                print(f"Tentando {endpoint}...")
                response = api_client.session.post(
                    f"{api_client.base_url}{endpoint}",
                    json={},
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    resultado = response.json()
                    pedido_id = resultado.get('id') or resultado.get('pedido_id')
                    if pedido_id:
                        print(f"Pedido aleatório gerado via {endpoint}: {pedido_id}")
                        return str(pedido_id)
            except:
                continue
        
        print("Falha ao gerar pedido aleatório")
        return ""
            
    except Exception as e:
        print(f"Erro ao gerar pedido aleatório: {e}")
        return ""


def fazer_patch_pedido(api_client: CallbackAPIClient, pedido_id: str, callback_data: Dict) -> bool:
    """
    Faz PATCH /pedido/:id com dados de confirmação
    Conforme requisito: "fazer PATCH para /pedido/:id com os dados extraídos"
    
    Args:
        api_client: Cliente da API autenticado
        pedido_id: ID do pedido aleatório gerado
        callback_data: Dados de confirmação {codigo_confirmacao, status}
        
    Returns:
        bool: True se sucesso
    """
    try:
        print(f"Fazendo PATCH /pedido/{pedido_id} conforme requisito...")
        
        response = api_client.session.patch(
            f"{api_client.base_url}/pedido/{pedido_id}",
            json=callback_data,
            timeout=30
        )
        
        print(f"PATCH /pedido/{pedido_id} - Status: {response.status_code}")
        print(f"Request: {json.dumps(callback_data, indent=2)}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 201, 204]:
            print(f"PATCH enviado com sucesso!")
            return True
        else:
            print(f"PATCH falhou: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro no PATCH: {e}")
        return False

