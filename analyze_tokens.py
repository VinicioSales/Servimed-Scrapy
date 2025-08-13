#!/usr/bin/env python3
"""
Analisa os JWTs do exemplo para ver quando expiraram
"""

import base64
import json
from datetime import datetime

def decode_jwt(token):
    """Decodifica um JWT para ver seu conteúdo"""
    try:
        # JWT tem 3 partes separadas por pontos: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return None
            
        # Decodifica o payload (segunda parte)
        payload = parts[1]
        
        # Adiciona padding se necessário
        while len(payload) % 4:
            payload += '='
            
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_json = json.loads(decoded_bytes.decode('utf-8'))
        
        return decoded_json
        
    except Exception as e:
        print(f"Erro ao decodificar JWT: {e}")
        return None

def analyze_tokens():
    """Analisa os tokens do exemplo e os nossos"""
    
    print("🔍 ANÁLISE DOS TOKENS JWT\n")
    
    # Token do exemplo cURL
    example_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RpZ29Vc3VhcmlvIjoyMjg1MCwidG9rZW4iOiI5ZGU1NmNlMC02Yzk5LTExZjAtOTdhMS1mNzY4YTU3NGUzMzciLCJpYXQiOjE3NTM4MDY3NzIsImV4cCI6MTc1Mzg0OTk3MiwiYXVkIjoiaHR0cDovL3NlcnZpbWVkLmNvbS5iciIsImlzcyI6IlNlcnZpbWVkIiwic3ViIjoic2VydmltZWRAU2VydmltZWQuY29tLmJyIn0.L1A0mnETOb-JZFixvyak6xf9Cq6dw_thUnL-RlWjvvqOOzcBta4ygzxtWmr49zT_WSML40jJ_dlRqVMfgIOdyg"
    
    # Nosso token atual  
    our_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RpZ29Vc3VhcmlvIjoyMjg1MCwidG9rZW4iOiJhNzQ4MmRjMC03ODQ0LTExZjAtYmYzZi1lMTE3MzE2MGQ5OGUiLCJpYXQiOjE3NTUwODk2OTEsImV4cCI6MTc1NTEzMjg5MSwiYXVkIjoiaHR0cDovL3NlcnZpbWVkLmNvbS5iciIsImlzcyI6IlNlcnZpbWVkIiwic3ViIjoic2VydmltZWRAU2VydmltZWQuY29tLmJyIn0.K3q15JyAXAUWhi6pFrQBnes2XkNGq6KhSsk2evt1ZeNC-3uSfZpPjGVweGUBtd04A5qUv0Ds3-NiiabKwAN-YQ"
    
    print("📅 TOKEN DO EXEMPLO cURL:")
    example_data = decode_jwt(example_token)
    if example_data:
        print(f"  Token UUID: {example_data.get('token', 'N/A')}")
        print(f"  Usuário: {example_data.get('codigoUsuario', 'N/A')}")
        
        if 'iat' in example_data:
            iat = datetime.fromtimestamp(example_data['iat'])
            print(f"  Emitido em: {iat.strftime('%d/%m/%Y %H:%M:%S')}")
            
        if 'exp' in example_data:
            exp = datetime.fromtimestamp(example_data['exp'])
            print(f"  Expira em: {exp.strftime('%d/%m/%Y %H:%M:%S')}")
            
            now = datetime.now()
            if exp < now:
                diff = now - exp
                print(f"  ❌ EXPIRADO há {diff.days} dias, {diff.seconds//3600} horas")
            else:
                diff = exp - now
                print(f"  ✅ Válido por mais {diff.days} dias, {diff.seconds//3600} horas")
    
    print("\n📅 NOSSO TOKEN ATUAL:")
    our_data = decode_jwt(our_token)
    if our_data:
        print(f"  Token UUID: {our_data.get('token', 'N/A')}")
        print(f"  Usuário: {our_data.get('codigoUsuario', 'N/A')}")
        
        if 'iat' in our_data:
            iat = datetime.fromtimestamp(our_data['iat'])
            print(f"  Emitido em: {iat.strftime('%d/%m/%Y %H:%M:%S')}")
            
        if 'exp' in our_data:
            exp = datetime.fromtimestamp(our_data['exp'])
            print(f"  Expira em: {exp.strftime('%d/%m/%Y %H:%M:%S')}")
            
            now = datetime.now()
            if exp < now:
                diff = now - exp
                print(f"  ❌ EXPIRADO há {diff.days} dias, {diff.seconds//3600} horas")
            else:
                diff = exp - now
                print(f"  ✅ Válido por mais {diff.days} dias, {diff.seconds//3600} horas")

if __name__ == "__main__":
    analyze_tokens()
