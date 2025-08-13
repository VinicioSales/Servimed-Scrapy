# SERVIMED SCRAPER - DOCUMENTAÇÃO COMPLETA
=============================================

## 📋 ÍNDICE
- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Modo de Uso](#modo-de-uso)
- [Nível 1: Execução Direta](#nível-1-execução-direta)
- [Nível 2: Sistema de Filas](#nível-2-sistema-de-filas)
- [Troubleshooting](#troubleshooting)
- [Desenvolvimento](#desenvolvimento)

---

## 🎯 VISÃO GERAL

O Servimed Scraper é uma aplicação Python que coleta produtos do Portal Servimed com suporte a dois modos de operação:

- **Nível 1**: Execução direta e síncrona (modo original)
- **Nível 2**: Sistema de filas assíncronas com integração a API externa

### Características Principais
- ✅ Coleta completa de produtos Servimed
- ✅ Filtros de busca personalizáveis  
- ✅ Sistema de backup automático
- ✅ Processamento assíncrono com Celery
- ✅ Integração OAuth2 com API externa
- ✅ Monitoramento de tarefas em tempo real

---

## 📁 ESTRUTURA DO PROJETO

```
PROVA/
├── main.py                          # Script principal
├── requirements.txt                 # Dependências
├── .env.example                     # Template de configuração
├── README.md                        # Esta documentação
├── data/                           # Arquivos de saída
│   ├── servimed_produtos_completos.json
│   ├── servimed_produtos_filtrados.json
│   └── servimed_backup.json
└── src/
    ├── servimed_scraper/           # Módulo principal de scraping
    │   ├── __init__.py
    │   ├── servimed_scraper_completo.py
    │   ├── auth_manager.py
    │   └── data_processor.py
    ├── nivel2/                     # Sistema de filas (Nível 2)
    │   ├── __init__.py
    │   ├── celery_app.py
    │   ├── tasks.py
    │   └── queue_client.py
    └── api_client/                 # Cliente da API externa
        ├── __init__.py
        └── callback_client.py
```

---

## 🚀 INSTALAÇÃO

### Pré-requisitos
- Python 3.8 ou superior
- Redis Server (para Nível 2)
- Git (opcional)

### 1. Clone ou baixe o projeto
```bash
# Se usando Git
git clone <url-do-repositorio>
cd PROVA

# Ou extraia o arquivo ZIP na pasta desejada
```

### 2. Instale as dependências
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# OU instalar apenas o essencial para Nível 1
pip install scrapy selenium beautifulsoup4 requests pandas numpy
```

### 3. Configuração inicial
```bash
# Copie o template de configuração
copy .env.example .env

# Edite o arquivo .env com seus dados
notepad .env
```

---

## ⚙️ CONFIGURAÇÃO

### 1. Obter Tokens de Autenticação

Para usar o scraper, você precisa dos tokens do Portal Servimed:

1. **Abra o Portal Servimed** no navegador
2. **Faça login** com suas credenciais
3. **Abra DevTools** (F12) > Aba Network
4. **Faça uma busca** qualquer no portal
5. **Encontre a requisição "oculto"** na lista
6. **Copie os valores** dos headers/cookies:

```
ACCESS_TOKEN=xxxxxxxxxxxx
SESSION_TOKEN=yyyyyyyyyyyy
LOGGED_USER=zzzzzzzzzzzz
CLIENT_ID=wwwwwwwwwwww
X_CART=vvvvvvvvvvvv
```

### 2. Configurar arquivo .env

Edite o arquivo `.env` com seus dados:

```bash
# Tokens obrigatórios (obtidos no passo anterior)
ACCESS_TOKEN=seu_token_access_real
SESSION_TOKEN=seu_token_session_real
LOGGED_USER=seu_user_id_real
CLIENT_ID=seu_client_id_real
X_CART=seu_x_cart_real

# Credenciais do portal
PORTAL_EMAIL=seu_email@exemplo.com
PORTAL_PASSWORD=sua_senha_real

# Usuários autorizados
USERS=user1,user2,user3
```

### 3. Configuração para Nível 2 (Opcional)

Se você planeja usar o sistema de filas:

```bash
# API de callback
CALLBACK_API_URL=https://desafio.cotefacil.net
CALLBACK_API_USER=juliano@farmaprevonline.com.br
CALLBACK_API_PASSWORD=a007299A

# Redis (mantenha padrão se local)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

---

## 🔧 MODO DE USO

### Verificar Instalação
```bash
# Teste básico
python main.py --help

# Deve mostrar todas as opções disponíveis
```

---

## 📊 NÍVEL 1: EXECUÇÃO DIRETA

O Nível 1 é o modo **síncrono** original - execução direta e imediata.

### Comandos Básicos

```bash
# Coletar TODOS os produtos
python main.py --nivel 1

# Coletar com filtro
python main.py --nivel 1 --filtro "paracetamol"

# Limitar número de páginas
python main.py --nivel 1 --max-pages 10

# Combinar filtro + limite
python main.py --nivel 1 --filtro "dipirona" --max-pages 5
```

### Exemplos Práticos

```bash
# Medicamentos para dor
python main.py --nivel 1 --filtro "paracetamol" --max-pages 3

# Antibióticos
python main.py --nivel 1 --filtro "amoxicilina" --max-pages 2

# Coleta completa (cuidado: pode demorar horas)
python main.py --nivel 1
```

### Arquivos de Saída

- `data/servimed_produtos_completos.json` - Todos os produtos
- `data/servimed_produtos_filtrados.json` - Produtos filtrados
- `data/servimed_backup.json` - Backup automático

---

## 🔄 NÍVEL 2: SISTEMA DE FILAS

O Nível 2 usa **filas assíncronas** com Celery + Redis para processamento em background e integração com API externa.

### Pré-requisitos para Nível 2

#### 1. Instalar Redis
```bash
# Windows (usando Chocolatey)
choco install redis-64

# OU baixar do site oficial
# https://redis.io/download

# Linux Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis
```

#### 2. Iniciar Redis
```bash
# Windows
redis-server

# Linux/macOS
redis-server
# OU
sudo systemctl start redis
```

#### 3. Verificar Redis
```bash
redis-cli ping
# Deve retornar: PONG
```

### Executar Workers Celery

Em um **terminal separado**, inicie o worker:

```bash
# Navegar para o diretório do projeto
cd C:\Users\6128347\OneDrive - Thomson Reuters Incorporated\Documents\Scrips\Tests\PROVA

# Iniciar worker
celery -A src.nivel2.celery_app worker --loglevel=info

# No Windows, se der erro, usar:
celery -A src.nivel2.celery_app worker --loglevel=info --pool=solo
```

### Comandos do Nível 2

#### Enfileirar Tarefas
```bash
# Enfileirar tarefa básica
python main.py --nivel 2 --enqueue

# Com filtro e limite
python main.py --nivel 2 --enqueue --filtro "paracetamol" --max-pages 3

# Com credenciais personalizadas
python main.py --nivel 2 --enqueue --usuario "seu@email.com" --senha "suasenha"
```

#### Monitorar Tarefas
```bash
# Status de uma tarefa específica
python main.py --nivel 2 --status 12345678-1234-1234-1234-123456789abc

# Status dos workers
python main.py --nivel 2 --worker-status
```

### Fluxo Completo do Nível 2

1. **Enfileirar tarefa**:
   ```bash
   python main.py --nivel 2 --enqueue --filtro "dipirona"
   # Retorna: Task ID: abc123-def456-ghi789
   ```

2. **Monitorar progresso**:
   ```bash
   python main.py --nivel 2 --status abc123-def456-ghi789
   ```

3. **Ver logs do worker** no terminal onde está executando

4. **Verificar resultado** - produtos são enviados automaticamente para a API

### Monitoramento com Flower (Opcional)

Para interface web de monitoramento:

```bash
# Instalar Flower
pip install flower

# Iniciar Flower
celery -A src.nivel2.celery_app flower

# Acessar: http://localhost:5555
```

---

## 🔍 TROUBLESHOOTING

### Problemas Comuns

#### 1. Erro de Import
```
ImportError: No module named 'servimed_scraper'
```
**Solução**: Verificar se está executando da pasta raiz do projeto

#### 2. Tokens Inválidos
```
Erro 401: Unauthorized
```
**Solução**: Atualizar tokens no arquivo `.env`

#### 3. Redis Connection Error (Nível 2)
```
ConnectionError: Error connecting to Redis
```
**Solução**:
```bash
# Verificar se Redis está rodando
redis-cli ping

# Iniciar Redis se necessário
redis-server
```

#### 4. Celery Worker Error (Nível 2)
```
ValueError: not enough values to unpack
```
**Solução**: No Windows, usar `--pool=solo`:
```bash
celery -A src.nivel2.celery_app worker --loglevel=info --pool=solo
```

#### 5. Erro de Autenticação na API (Nível 2)
```
OAuth2 authentication failed
```
**Solução**: Verificar credenciais no `.env`:
```bash
CALLBACK_API_USER=email_correto@dominio.com
CALLBACK_API_PASSWORD=senha_correta
```

### Logs e Debug

#### Habilitar Modo Verbose
Edite `.env`:
```bash
DEBUG=true
VERBOSE=true
LOG_LEVEL=DEBUG
```

#### Verificar Logs do Celery
```bash
# Worker com mais detalhes
celery -A src.nivel2.celery_app worker --loglevel=debug

# Logs em arquivo
celery -A src.nivel2.celery_app worker --loglevel=info --logfile=celery.log
```

---

## 👨‍💻 DESENVOLVIMENTO

### Estrutura de Código

#### Adicionar Novas Funcionalidades

1. **Novo filtro de produtos**:
   - Editar `src/servimed_scraper/servimed_scraper_completo.py`
   - Método `processar_dados()`

2. **Nova API de destino**:
   - Criar novo cliente em `src/api_client/`
   - Registrar em `src/nivel2/tasks.py`

3. **Nova tarefa assíncrona**:
   - Adicionar em `src/nivel2/tasks.py`
   - Atualizar `src/nivel2/queue_client.py`

### Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio

# Executar testes (quando implementados)
pytest tests/

# Teste manual básico
python -c "from src.servimed_scraper.servimed_scraper_completo import ServimedScraperCompleto; print('Import OK')"
```

### Contribuição

1. Mantenha a estrutura modular
2. Adicione documentação para novas features
3. Teste tanto Nível 1 quanto Nível 2
4. Atualize requirements.txt se necessário

---

## 📞 SUPORTE

Para dúvidas ou problemas:

1. **Verificar esta documentação** primeiro
2. **Consultar logs** do Celery/Redis
3. **Testar configuração** passo a passo
4. **Verificar tokens** do Portal Servimed

---

## 📄 LICENÇA

Este projeto é desenvolvido para uso interno e educacional.

**Versão da Documentação**: 1.0
**Última Atualização**: 12/08/2025
**Desenvolvido por**: GitHub Copilot
