# 📖 SERVIMED SCRAPER - DOCUMENTAÇÃO COMPLETA

## 🏗️ VISÃO GERAL

O **Servimed Scraper** é um sistema completo de web scraping e processamento de pedidos desenvolvido em Python para o **Desafio CotefFácil**. O projeto implementa uma arquitetura em 3 níveis de complexidade, sempre utilizando o framework **Scrapy** como base.

### 🎯 OBJETIVOS
- ✅ Extrair dados de produtos farmacêuticos do site Servimed
- ✅ Processar pedidos no portal Servimed
- ✅ Integrar com API do desafio CotefFácil
- ✅ Implementar sistema de filas para processamento assíncrono
- ✅ Fornecer códigos de rastreamento únicos para pedidos

## 🚀 INSTALAÇÃO E CONFIGURAÇÃO

### 📋 Pré-requisitos
- **Python 3.10+**
- **Windows 10/11** (ou sistemas compatíveis)
- **Conexão com internet** (para instalação de dependências)

### ⚡ Configuração Rápida

1. **Clone ou baixe o projeto:**
   ```bash
   git clone <repositorio>
   cd servimed-scrapy
   ```

2. **Execute a configuração automática:**
   ```bat
   setup.bat
   ```

   Este script irá:
   - ✅ Criar ambiente virtual Python
   - ✅ Instalar todas as dependências
   - ✅ Configurar Redis para processamento de filas
   - ✅ Preparar arquivo de configuração (.env)

3. **Configurar variáveis de ambiente:**
   - Edite o arquivo `.env` com suas credenciais
   - Configure especialmente `COTEFACIL_EMAIL` e `COTEFACIL_PASSWORD`

## 🎯 USO DO SISTEMA

### Nível 1 - Scrapy Simples
```bash
python main.py nivel1
```
Executa scraping básico usando apenas Scrapy, sem sistema de filas.

### Nível 2 - Scrapy + Celery
```bash
# Terminal 1 - Iniciar Worker (da raiz do projeto):
start_worker.bat
# ou manualmente:
python -m celery -A src.nivel2.celery_app worker --loglevel=info

# Terminal 2 - Executar programa:
python main.py nivel2
```
Adiciona sistema de filas assíncronas com Celery + Redis.

### Nível 3 - Sistema Completo
```bash
# Terminal 1 - Iniciar Worker (da raiz do projeto):
start_worker.bat
# ou manualmente:
python -m celery -A src.nivel2.celery_app worker --loglevel=info

# Terminal 2 - Executar programa:
python main.py nivel3
```
Sistema completo com processamento de pedidos e integração com API CotefFácil.

## 🧪 TESTES

### Executar todos os testes:
```bash
python run_tests.py
```

### Executar testes específicos:
```bash
# Testes de configuração
python -m pytest tests/test_config.py -v

# Testes de funcionalidade básica
python -m pytest tests/test_basic_functionality.py -v

# Testes do main simplificado
python -m pytest tests/test_main_simple.py -v

# Testes do wrapper Scrapy
python -m pytest tests/test_scrapy_wrapper_simple.py -v

# Testes do nível 3
python -m pytest tests/test_nivel3_simple.py -v
```

## 📁 SCRIPTS AUXILIARES

### `setup.bat`
Script de configuração automática que prepara todo o ambiente de desenvolvimento.

### `start_worker.bat`
Script para iniciar o worker Celery de forma simplificada (necessário para níveis 2 e 3).

### `scripts/redis_start.bat`
Script manual para iniciar Redis se necessário.

## ⚠️ SOLUÇÃO DE PROBLEMAS

### ❌ **Problema**: ModuleNotFoundError ao executar worker
```
ModuleNotFoundError: No module named 'src'
```
**✅ Solução**:
```bash
# 1. SEMPRE execute start_worker.bat da RAIZ do projeto
cd /caminho/para/servimed-scrapy
start_worker.bat

# 2. NÃO execute de subpastas como scripts/
# ❌ Errado: scripts\start_worker.bat  
# ✅ Correto: start_worker.bat (da raiz)

# 3. Verificar estrutura:
dir main.py src venv  # Devem existir todos
```

### Erro: "Redis não conecta"
```
Error 10061 connecting to localhost:6379
```
**Solução:**
1. Execute `start_worker.bat` que inicia Redis automaticamente
2. Ou execute manualmente: `scripts\redis_start.bat`
3. Verifique se `tools/redis-portable/redis-server.exe` existe

### Erro: "ModuleNotFoundError"
**Solução:**
1. Ative o ambiente virtual: `venv\Scripts\activate`
2. Instale dependências: `pip install -r requirements.txt`
3. Execute da raiz do projeto

### Erro: "Token expirado"
**Solução:**
1. Configure o arquivo `.env` com credenciais válidas
2. Verifique `COTEFACIL_EMAIL` e `COTEFACIL_PASSWORD`

### Celery Worker não inicia
**Solução:**
1. Verifique se Redis está rodando
2. Ative o ambiente virtual
3. Execute: `python -m celery -A src.nivel2.celery_app worker --loglevel=info`

## 🔧 DESENVOLVIMENTO

### Estrutura do Código

#### `main.py`
Ponto de entrada principal do sistema. Gerencia a execução dos 3 níveis:
- **Nível 1**: Scrapy direto
- **Nível 2**: Scrapy + Celery 
- **Nível 3**: Sistema completo com API CotefFácil

#### `src/scrapy_wrapper.py`
Wrapper unificado que encapsula todas as funcionalidades do Scrapy, permitindo execução via subprocess para evitar conflitos de reactor.

#### `src/pedido_queue_client.py`
Cliente para enfileiramento e monitoramento de pedidos no sistema de filas Celery.

#### Sistema de Filas (`src/nivel2/`)
- **`celery_app.py`**: Configuração do Celery
- **`tasks.py`**: Tarefas assíncronas para processamento
- **`queue_client.py`**: Cliente para interação com filas

#### Sistema de Pedidos (`src/nivel3/`)
- **`tasks.py`**: Processamento completo de pedidos
- **`pedido_client.py`**: Cliente para interação com portal Servimed

#### API CotefFácil (`src/api_client/`)
- **`callback_client.py`**: Integração com API do desafio

### Configuração de Ambiente

O arquivo `.env` deve conter:
```bash
# Credenciais CotefFácil
COTEFACIL_EMAIL=seu-email@exemplo.com
COTEFACIL_PASSWORD=sua-senha

# URLs da API
COTEFACIL_LOGIN_URL=https://desafio.cotefacil.net/login
COTEFACIL_CHALLENGE_URL=https://desafio.cotefacil.net/challenge

# Configurações Redis/Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER=redis://localhost:6379/0

# Configurações de log
LOG_LEVEL=INFO
```

## 📁 ESTRUTURA DO PROJETO

```
PROVA/
├── 📄 main.py                    # Ponto de entrada principal
├── 📄 setup.bat                  # Configuração automática
├── 📄 start_worker.bat           # Iniciar worker Celery
├── 📄 run_tests.py               # Executar testes
├── 📄 requirements.txt           # Dependências Python
├── 📄 .env.example              # Template de configuração
├── 📄 README.md                 # Esta documentação
├── 
├── 📁 src/                      # Código fonte
│   ├── 📄 scrapy_wrapper.py     # Wrapper principal Scrapy
│   ├── 📄 pedido_queue_client.py # Cliente de pedidos
│   ├── 📁 nivel2/               # Sistema de filas
│   ├── 📁 nivel3/               # Sistema completo
│   ├── 📁 api_client/           # Integração CotefFácil
│   └── 📁 scrapy_servimed/      # Projeto Scrapy
│
├── 📁 tests/                    # Testes automatizados (58 testes)
├── 📁 scripts/                  # Scripts auxiliares
├── 📁 tools/                    # Redis portátil
├── 📁 data/                     # Resultados e logs
└── 📁 config/                   # Configurações
```

## 🔧 TECNOLOGIAS UTILIZADAS

- **Python 3.10+** - Linguagem principal
- **Scrapy 2.13.3** - Framework de web scraping
- **Celery 5.x** - Sistema de filas assíncronas
- **Redis** - Broker de mensagens e cache
- **Requests** - Cliente HTTP
- **Pytest** - Framework de testes automatizados
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

## 📈 STATUS DO PROJETO

- ✅ **Nível 1**: Scrapy básico funcional
- ✅ **Nível 2**: Sistema de filas implementado
- ✅ **Nível 3**: Integração CotefFácil completa
- ✅ **Testes**: 58 testes automatizados passando
- ✅ **Documentação**: Completa e atualizada

## 📄 LICENÇA

Este projeto foi desenvolvido para o Desafio CotefFácil e está disponível para fins educacionais e de avaliação.

---

**📞 Desenvolvido para o Desafio CotefFácil | Python + Scrapy + Celery + Redis**
```


---

## 🏛️ ARQUITETURA DO SISTEMA

### 📊 Estrutura de Diretórios
```
PROVA/
├── 📄 main.py                      # Arquivo principal - ponto de entrada
├── 📄 requirements.txt             # Dependências do projeto
├── 📄 .env                         # Variáveis de ambiente (configurar)
├── 📄 pyproject.toml               # Configuração do projeto
├── 📄 scrapy.cfg                   # Configuração do Scrapy
├── 📄 run_tests.py                 # Script para executar testes
├── 📄 README.md                    # Esta documentação
├── 
├── 📁 src/                        # Código fonte principal
│   ├── 📄 scrapy_wrapper.py       # Wrapper principal do Scrapy
│   ├── 📄 pedido_queue_client.py  # Cliente para pedidos (Nível 3)
│   │
│   ├── 📁 config/                 # Configurações do sistema
│   │   ├── 📄 settings.py         # Configurações internas
│   │   └── 📄 paths.py            # Caminhos do projeto
│   │
│   ├── 📁 nivel2/                 # Sistema de filas (Nível 2)
│   │   ├── 📄 queue_client.py     # Cliente de filas
│   │   ├── 📄 tasks.py            # Tarefas Celery
│   │   └── 📄 celery_app.py       # Configuração Celery
│   │
│   ├── 📁 nivel3/                 # Sistema de pedidos (Desafio)
│   │   ├── 📄 tasks.py            # Processamento completo de pedidos
│   │   └── 📄 pedido_client.py    # Cliente do portal Servimed
│   │
│   ├── 📁 api_client/             # Integração CotefFácil
│   │   └── 📄 callback_client.py  # Cliente da API do desafio
│   │
│   ├── � scrapy_servimed/        # Projeto Scrapy
│   │   ├── 📄 settings.py         # Configurações Scrapy
│   │   ├── 📄 pipelines.py        # Pipelines de processamento
│   │   ├── 📄 items.py            # Definição de items
│   │   └── 📁 spiders/            # Spiders de scraping
│   │       └── 📄 servimed_spider.py  # Spider principal
│   │
│   └── 📁 servimed_scraper/       # Sistema de processamento original
│       └── 📄 scraper.py          # Scraper completo standalone
│
├── 📁 tests/                      # Testes automatizados
│   ├── 📄 conftest.py             # Configurações globais de teste
│   ├── 📄 test_basic_functionality.py  # Testes básicos ✅
│   ├── 📄 test_config.py          # Testes de configuração
│   ├── 📄 test_main.py            # Testes do main.py
│   └── 📄 test_scrapy_wrapper.py  # Testes do wrapper
│
├── � data/                       # Dados e resultados
│   ├── � servimed_produtos_scrapy.json   # Resultados Scrapy
│   └── 📄 servimed_produtos_filtrados.json # Resultados filtrados
│
├── 📁 config/                     # Arquivos de configuração
├── � scripts/                    # Scripts auxiliares (Redis, Workers)
└── � tools/                      # Ferramentas (Redis portable)
```

---

## 🚀 INÍCIO RÁPIDO

### 📋 Pré-requisitos
- ✅ Python 3.10+
- ✅ Conexão com Internet
- ✅ Redis (para níveis 2 e 3)

### 🔧 Setup Rápido

#### 1. Instalar dependências:
```bash
pip install -r requirements.txt
```

#### 2. Configurar ambiente (.env):
```bash
# Copiar .env.example para .env e configurar tokens
# Ver seção "Configuração do Ambiente" para detalhes
```

#### 3. Testar funcionamento básico:
```bash
# Nível 1 - Scraping simples
python main.py --nivel 1 --filtro "paracetamol" --max-pages 1
```

### 📝 Exemplos Práticos

#### 🎯 Exemplo 1: Scraping de Produtos
```bash
# Buscar produtos com "dipirona" limitado a 2 páginas
python main.py --nivel 1 --filtro "dipirona" --max-pages 2

# Resultado: data/servimed_produtos_scrapy.json
```

#### 🎯 Exemplo 2: Sistema de Pedidos (Desafio CotefFácil)
```bash
# Criar pedido para produto específico
python main.py --nivel 3 --codigo-produto 444212

# O sistema irá:
# 1. Buscar produto no Servimed
# 2. Criar pedido no portal
# 3. Gerar pedido aleatório na API CotefFácil
# 4. Enviar PATCH de confirmação
```

#### 🎯 Exemplo 3: Executar Testes
```bash
# Testes básicos
python -m pytest tests/test_basic_functionality.py -v

# Todos os testes
python run_tests.py
```

---

## 🎯 NÍVEIS DE EXECUÇÃO

### 🎯 NÍVEL 1: SCRAPING DE PRODUTOS (SÍNCRONO)
**Descrição:** Extração de dados de produtos do Servimed usando Scrapy

#### 🔧 Como Usar:
```bash
# Execução básica (todos os produtos)
python main.py --nivel 1

# Com filtro de produtos
python main.py --nivel 1 --filtro "paracetamol"

# Limitando páginas para teste
python main.py --nivel 1 --max-pages 3

# Combinando opções
python main.py --nivel 1 --filtro "antibiotico" --max-pages 2
```

#### 📊 Saída:
- **Arquivo:** `data/servimed_produtos_scrapy.json`
- **Formato:** JSON com lista de produtos
- **Logs:** Console em tempo real
- **Estrutura:** `{produtos: [{gtin, codigo, descricao, preco_fabrica, estoque}]}`

---

### 🎯 NÍVEL 2: SISTEMA DE FILAS (ASSÍNCRONO)
**Descrição:** Processamento via filas usando Celery + Redis  
**Uso:** Para processamento em larga escala e múltiplas tarefas

#### 🔧 Pré-requisitos:
```bash
# 1. Iniciar Redis
# Windows: usar tools/redis-portable/redis-server.exe
# Ou Docker: docker run -d -p 6379:6379 redis:latest

# 2. Iniciar worker Celery
python -m celery -A src.nivel2.celery_app worker --loglevel=info
```

#### 🔧 Como Usar:
```bash
# Verificar status dos workers
python main.py --nivel 2 --worker-status

# Enfileirar nova tarefa de scraping
python main.py --nivel 2 --enqueue --filtro "vitamina"

# Verificar status de tarefa específica
python main.py --nivel 2 --status "task-id-aqui"
```

#### 📊 Saída:
- **Task ID** para acompanhamento
- **Status** da execução via API
- **Resultados** armazenados no Redis

---

### 🎯 NÍVEL 3: SISTEMA DE PEDIDOS (DESAFIO COTEFÁCIL)
**Descrição:** Sistema completo de processamento de pedidos conforme especificação do desafio

#### 🔧 Funcionalidades Implementadas:
1. ✅ **Busca de produtos** no Servimed via Scrapy
2. ✅ **Criação de pedidos** no portal Servimed
3. ✅ **Geração de pedido aleatório** na API CotefFácil
4. ✅ **PATCH de confirmação** com código do pedido
5. ✅ **Códigos únicos de rastreamento** baseados em características do pedido

#### 🔧 Como Usar:
```bash
# Criar pedido para produto específico
python main.py --nivel 3 --codigo-produto 444212

# Modo de teste (sem criar pedido real)
python main.py --nivel 3 --test

# Verificar status de pedido
python main.py --nivel 3 --status "task-id"
```

#### 📊 Fluxo Completo do Nível 3:
```
1. Buscar produto 444212 no Servimed (via Scrapy)
2. Autenticar no portal Servimed 
3. Criar pedido no portal → Recebe: {'executado': 'Ok'}
4. Gerar código único: SERVIMED_13082025_1245_444212_01_7511
5. Chamar API CotefFácil POST /pedido → Recebe: {"id": 47}
6. Enviar PATCH /pedido/47 com {"codigo_fornecedor": "SERVIMED_..."}
7. Confirmação final no CotefFácil
```

#### 🏷️ **Formato do Código de Pedido:**
```
SERVIMED_DDMMAAAA_HHMM_PRODUTO1_QTD_CLIENTE
Exemplo: SERVIMED_13082025_1245_444212_01_7511

Onde:
- SERVIMED: Identificador do sistema
- 13082025: Data (13/08/2025)
- 1245: Horário (12:45)
- 444212: Código do primeiro produto
- 01: Quantidade total de itens
- 7511: Últimos 4 dígitos do cliente
```

---

## ⚙️ CONFIGURAÇÃO DO AMBIENTE

### 📋 Dependências Principais
```txt
# === CORE (obrigatórias) ===
scrapy>=2.11.0              # Framework de scraping principal
requests>=2.31.0             # HTTP requests
python-dotenv>=1.0.0         # Variáveis de ambiente

# === NÍVEL 2 e 3 (Sistema de Filas e Pedidos) ===
celery>=5.3.0                # Framework de filas distribuídas
redis>=5.0.0                 # Broker de mensagens

# === DESENVOLVIMENTO ===
pytest>=7.4.0                # Framework de testes
```

### 🔧 Instalação
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar Redis (para níveis 2 e 3)
# Windows: usar tools/redis-portable/redis-server.exe
# Ou Docker: docker run -d -p 6379:6379 redis:latest

# 3. Configurar .env (copiar de .env.example)
```

### 🔐 Variáveis de Ambiente (.env)
```env
# === AUTENTICAÇÃO SERVIMED (obrigatório) ===
ACCESS_TOKEN=seu_access_token_aqui
SESSION_TOKEN=seu_session_token_jwt_aqui
LOGGED_USER=codigo_usuario
CLIENT_ID=codigo_cliente
X_CART=hash_carrinho_usuario

# === CREDENCIAIS PORTAL (obrigatório) ===
PORTAL_EMAIL=seu_email@dominio.com.br
PORTAL_PASSWORD=sua_senha_portal

# === API COTEFÁCIL - Desafio (obrigatório para nível 3) ===
CALLBACK_API_USER=seu_usuario_cotefacil@dominio.com.br
CALLBACK_API_PASSWORD=sua_senha_cotefacil
CALLBACK_URL=https://desafio.cotefacil.net

# === URLS DO SISTEMA (configuração padrão) ===
PORTAL_URL=https://pedidoeletronico.servimed.com.br
BASE_URL=https://peapi.servimed.com.br

# === Redis/Celery (opcional - para níveis 2 e 3) ===
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

### 🔑 Como Obter os Tokens
1. **Abrir DevTools** no navegador (F12)
2. **Fazer login** no portal Servimed
3. **Na aba Network**, procurar requests para `/api/`
4. **Copiar headers**: `accesstoken`, `sessiontoken`, `loggeduser`, etc.
5. **Adicionar no .env**

---

## 🧪 SISTEMA DE TESTES

###  Executando Testes

#### 🎯 Método 1: Script Automatizado
```bash
# Executar script interativo
python run_tests.py
```

#### 🎯 Método 2: Pytest Direto
```bash
# Todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_basic_functionality.py -v
python -m pytest tests/test_config.py -v

# Com cobertura de código
python -m pytest tests/ --cov=src --cov=main
```

### 📋 Tipos de Testes Implementados

#### 🔧 **Testes Básicos** ✅
- ✅ Ambiente Python funcional
- ✅ Estrutura do projeto
- ✅ Importações de módulos
- ✅ Dependências instaladas

#### 🔗 **Testes de Configuração** ✅
- ✅ Paths do projeto
- ✅ Arquivos de configuração
- ✅ Integração de configurações

---

## 🛠️ COMANDOS ESSENCIAIS

### � Para Uso Diário
```bash
# Scraping básico
python main.py --nivel 1 --filtro "produto" --max-pages 1

# Sistema de pedidos (Desafio CotefFácil)
python main.py --nivel 3 --codigo-produto 444212

# Testes básicos
python -m pytest tests/test_basic_functionality.py -v
```

### 🔧 Para Desenvolvimento
```bash
# Iniciar worker Celery (níveis 2 e 3)
python -m celery -A src.nivel2.celery_app worker --loglevel=info

# Verificar status do Redis
redis-cli ping

# Debug de imports
python -c "import sys; sys.path.insert(0, 'src'); import scrapy_wrapper; print('OK')"
```

### � Para Troubleshooting
```bash
# Verificar estrutura
python -c "import os; print(os.listdir('.'))"

# Testar Scrapy
python -c "import scrapy; print(f'Scrapy {scrapy.__version__} OK')"

# Verificar dependências
pip list | grep -E "(scrapy|celery|redis|requests)"
```

---

## 🚨 TROUBLESHOOTING

### ❌ Problemas Comuns

#### 1. **Redis não está rodando** (Níveis 2 e 3)
```bash
# Erro: ConnectionError: Error 10061 connecting to localhost:6379
# Solução: Iniciar Redis
# Windows: tools/redis-portable/redis-server.exe
# Docker: docker run -d -p 6379:6379 redis:latest
```

#### 2. **Tokens expirados** (Nível 3)
```bash
# Erro: Token valido ate: [data passada]
# Solução: Atualizar tokens no .env (extrair do navegador)
```

#### 3. **Workers Celery não ativos** (Níveis 2 e 3)
```bash
# Erro: No workers available
# Solução: Iniciar worker
python -m celery -A src.nivel2.celery_app worker --loglevel=info
```

#### 4. **Dependências faltando**
```bash
# Erro: ModuleNotFoundError
# Solução: Instalar dependências
pip install -r requirements.txt
```

---

## 📈 RECURSOS DO SISTEMA

### 🎯 **Nível 1: Scraping**
- Framework Scrapy para extração robusta
- Filtros de busca personalizáveis
- Controle de paginação
- Resultados em JSON estruturado

### 🎯 **Nível 2: Filas Assíncronas**
- Processamento via Celery + Redis
- Múltiplas tarefas simultâneas
- Monitoramento de status
- Escalabilidade horizontal

### 🎯 **Nível 3: Sistema de Pedidos (Desafio CotefFácil)**
- ✅ Integração completa com portal Servimed
- ✅ Criação real de pedidos
- ✅ Códigos únicos de rastreamento
- ✅ Integração com API CotefFácil
- ✅ PATCH automático de confirmação
- ✅ Workflow completo do desafio

### 🏷️ **Sistema de Códigos Únicos**
```
Formato: SERVIMED_DDMMAAAA_HHMM_PRODUTO_QTD_CLIENTE
Exemplo: SERVIMED_13082025_1245_444212_01_7511

Benefícios:
- 👁️ Legível por humanos
- 🔍 Rastreável por características
- 🔒 Único por timestamp + dados
- 📊 Fácil auditoria e debug
```

---

## ✅ RESUMO DO PROJETO

### 🎯 **Funcionalidades Implementadas:**
- [x] **Scraping de produtos** via Scrapy (Nível 1)
- [x] **Sistema de filas** com Celery (Nível 2)
- [x] **Processamento de pedidos** completo (Nível 3)
- [x] **Integração CotefFácil** 100% funcional
- [x] **Códigos únicos** de rastreamento
- [x] **Testes automatizados** básicos

### 🏆 **Desafio CotefFácil: Status COMPLETO**
1. ✅ Busca de produtos no Servimed
2. ✅ Criação de pedidos via portal
3. ✅ Geração de pedido aleatório na API
4. ✅ PATCH de confirmação automático
5. ✅ Códigos de rastreamento únicos

### 🔧 **Tecnologias Utilizadas:**
- **Python 3.10+**
- **Scrapy 2.13.3** (Web Scraping)
- **Celery 5.x** (Filas Assíncronas)
- **Redis** (Broker de Mensagens)
- **Requests** (HTTP Client)
- **Pytest** (Testes Automatizados)

---

## 📞 SUPORTE RÁPIDO

### ✅ **Para começar rapidamente:**
```bash
# 1. Teste básico
python main.py --nivel 1 --max-pages 1

# 2. Se funcionou, teste com filtro
python main.py --nivel 1 --filtro "vitamina" --max-pages 1

# 3. Para o desafio CotefFácil
python main.py --nivel 3 --codigo-produto 444212
```

### 🚨 **Se algo não funcionar:**
```bash
# 1. Verificar ambiente
python -m pytest tests/test_basic_functionality.py -v

# 2. Verificar dependências
pip install -r requirements.txt

# 3. Para nível 3, verificar .env e Redis
```

