import requests
import json

headers = {
    'Content-Type': 'application/json',
    'accesstoken': 'a7482dc0-7844-11f0-bf3f-e1173160d98e',
    'loggeduser': '22850',
    'x-cart': '531fde319d8dfb00619966a617e0d29373766210b7c36aabe437a93b87a3630b',
    'Origin': 'https://pedidoeletronico.servimed.com.br',
    'Referer': 'https://pedidoeletronico.servimed.com.br/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

cookies = {
    'accesstoken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RpZ29Vc3VhcmlvIjoyMjg1MCwidG9rZW4iOiJhNzQ4MmRjMC03ODQ0LTExZjAtYmYzZi1lMTE3MzE2MGQ5OGUiLCJpYXQiOjE3NTUwODk2OTEsImV4cCI6MTc1NTEzMjg5MSwiYXVkIjoiaHR0cDovL3NlcnZpbWVkLmNvbS5iciIsImlzcyI6IlNlcnZpbWVkIiwic3ViIjoic2VydmltZWRAU2VydmltZWQuY29tLmJyIn0.K3q15JyAXAUWhi6pFrQBnes2XkNGq6KhSsk2evt1ZeNC-3uSfZpPjGVweGUBtd04A5qUv0Ds3-NiiabKwAN-YQ',
    'sessiontoken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RpZ29Vc3VhcmlvIjoyMjg1MCwidG9rZW4iOiJhNzQ4MmRjMC03ODQ0LTExZjAtYmYzZi1lMTE3MzE2MGQ5OGUiLCJpYXQiOjE3NTUwODk2OTEsImV4cCI6MTc1NTEzMjg5MSwiYXVkIjoiaHR0cDovL3NlcnZpbWVkLmNvbS5iciIsImlzcyI6IlNlcnZpbWVkIiwic3ViIjoic2VydmltZWRAU2VydmltZWQuY29tLmJyIn0.K3q15JyAXAUWhi6pFrQBnes2XkNGq6KhSsk2evt1ZeNC-3uSfZpPjGVweGUBtd04A5qUv0Ds3-NiiabKwAN-YQ'
}

payload = {
    'filtro': 'HIDRATACAO',
    'pagina': 1,
    'registrosPorPagina': 25,
    'ordenarDecrescente': False,
    'colunaOrdenacao': 'nenhuma',
    'clienteId': 267511,
    'tipoVendaId': 1,
    'fabricanteIdFiltro': 0,
    'pIIdFiltro': 0,
    'cestaPPFiltro': False,
    'codigoExterno': 0,
    'codigoUsuario': 22850,
    'promocaoSelecionada': '',
    'indicadorTipoUsuario': 'CLI',
    'kindUser': 0,
    'xlsx': [],
    'principioAtivo': '',
    'master': False,
    'kindSeller': 0,
    'grupoEconomico': '',
    'users': [518565, 267511],
    'list': True
}

print("Testing API with pure requests...")

try:
    response = requests.post(
        'https://peapi.servimed.com.br/api/carrinho/oculto?siteVersion=4.0.27',
        headers=headers,
        cookies=cookies,
        json=payload,
        timeout=10,
        verify=False  # Disable SSL verification for testing
    )
    
    print(f'Status Code: {response.status_code}')
    print(f'Response Headers: {dict(response.headers)}')
    
    if response.status_code == 200:
        print('✅ SUCCESS with pure requests!')
        data = response.json()
        print(f'Total products: {len(data.get("lista", []))}')
        print(f'Total records: {data.get("totalRegistros", 0)}')
    else:
        print(f'❌ FAILED - Response: {response.text[:200]}...')
        
except Exception as e:
    print(f'❌ ERROR: {e}')
