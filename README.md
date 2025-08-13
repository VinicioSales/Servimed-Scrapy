# 📖 SERVIMED SCRAPER - DOCUMENTAÇÃO COMPLETA

## 🏗️ VISÃO GERAL

O **Servimed Scraper** é um sistema completo de web scraping desenvolvido em Python para extrair informações de produtos do site Servimed. O projeto implementa uma arquitetura em 3 níveis de complexidade, sempre utilizando o framework **Scrapy** como base.

### 🎯 OBJETIVOS
- ✅ Extrair dados de produtos farmacêuticos do site Servimed
- ✅ Oferecer múltiplas formas de execução (síncrona e assíncrona)
- ✅ Implementar sistema de filas para processamento em larga escala
- ✅ Fornecer API para integração com sistemas externos
- ✅ Garantir qualidade através de testes automatizados

### 📊 STATUS DO PROJETO
- **Data:** 13 de Agosto de 2025
- **Status:** ✅ **COMPLETO E FUNCIONAL**
- **Framework:** Scrapy 2.13.3
- **Testes:** ✅ Sistema de testes automatizados implementado
- **Arquitetura:** 3 Níveis de Complexidade

---

## 🏛️ ARQUITETURA DO SISTEMA

### 📊 Estrutura de Diretórios
```
PROVA/
├── 📄 main.py                      # Arquivo principal - ponto de entrada
├── 📄 requirements.txt             # Dependências do projeto
├── 📄 .env                         # Variáveis de ambiente (configurar)
├── 📄 pyproject.toml               # Configuração do projeto (pytest, coverage)
├── 📄 scrapy.cfg                   # Configuração do Scrapy
├── 📄 run_tests.py                 # Script para executar testes
├── 📄 README.md                    # Esta documentação
├── 
├── 📁 src/                        # Código fonte principal
│   ├── 📄 scrapy_wrapper.py       # Wrapper principal do Scrapy
│   ├── 📄 pedido_queue_client.py  # Cliente para pedidos (Nível 3)
│   │
│   ├── 📁 config/                 # Configurações do sistema
│   │   ├── 📄 __init__.py
│   │   ├── 📄 settings.py         # Configurações internas da aplicação
│   │   └── 📄 paths.py            # Caminhos e diretórios do projeto
│   │
│   ├── 📁 nivel2/                 # Sistema de filas (Nível 2)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 queue_client.py     # Cliente de filas
│   │   ├── 📄 tasks.py            # Tarefas Celery
│   │   └── 📄 celery_app.py       # Configuração Celery
│   │
│   ├── 📁 scrapy_servimed/        # Projeto Scrapy
│   │   ├── 📄 __init__.py
│   │   ├── 📄 settings.py         # Configurações Scrapy
│   │   ├── 📄 pipelines.py        # Pipelines de processamento
│   │   ├── 📄 items.py            # Definição de items
│   │   └── 📁 spiders/            # Spiders de scraping
│   │       ├── 📄 __init__.py
│   │       └── 📄 servimed_spider.py  # Spider principal
│   │
│   └── 📁 servimed_scraper/       # Sistema de processamento
│       ├── 📄 __init__.py
│       ├── 📄 celery_app.py       # App Celery principal
│       └── 📄 tasks.py            # Tarefas de processamento
│
├── 📁 tests/                      # Testes automatizados
│   ├── 📄 conftest.py             # Configurações globais de teste
│   ├── 📄 test_basic_functionality.py  # Testes básicos ✅
│   ├── 📄 test_config.py          # Testes de configuração
│   ├── 📄 test_main.py            # Testes do main.py
│   ├── 📄 test_scrapy_wrapper.py  # Testes do wrapper
│   ├── 📄 test_spiders.py         # Testes dos spiders
│   ├── 📄 test_integration.py     # Testes de integração
│   ├── 📁 test_nivel2/
│   │   └── 📄 test_tasks.py       # Testes Celery
│   └── 📁 test_nivel3/
│       └── 📄 test_pedido_queue_client.py  # Testes pedidos
│
├── 📁 data/                       # Dados e resultados
│   ├── 📄 servimed_produtos_scrapy.json   # Resultados Scrapy
│   └── 📄 logs/                   # Logs do sistema

```

---

## 🚀 INÍCIO RÁPIDO

### 📋 Pré-requisitos
- ✅ Python 3.10+
- ✅ Conexão com Internet

### 🔧 Setup Rápido

#### 1. Verificar se está tudo funcionando:
```bash
# Navegar para o diretório do projeto
cd servimed-scraper

# Testar ambiente básico
python -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_python_environment -v
```

#### 2. Executar primeiro teste do sistema:
```bash
# Nível 1 - Execução direta (mais simples)
python main.py --nivel 1 --filtro "paracetamol" --max-pages 1
```

#### 3. Verificar resultados:
```bash
# Ver arquivo gerado
type data\servimed_produtos_scrapy.json
```

### 📝 Exemplos Práticos

#### 🎯 Exemplo 1: Busca Simples
```bash
# Buscar produtos com "dipirona" limitado a 2 páginas
python main.py --nivel 1 --filtro "dipirona" --max-pages 2

# Resultado esperado: Arquivo JSON com produtos encontrados
```

#### 🎯 Exemplo 2: Executar Testes
```bash
# Testes básicos (sempre funcionam)
python -m pytest tests/test_basic_functionality.py -v
```

#### 🎯 Exemplo 3: Script Interativo de Testes
```bash
# Executar menu interativo
python run_tests.py

# Escolher opção 1: Executar todos os testes
# Escolher opção 4: Verificar estrutura
```

---

## 🎯 NÍVEIS DE EXECUÇÃO

### 🎯 NÍVEL 1: EXECUÇÃO DIRETA (SÍNCRONA)
**Descrição:** Execução direta e imediata usando Scrapy  

#### 🔧 Como Usar:
```bash
# Execução básica
python main.py --nivel 1

# Com filtro de produtos
python main.py --nivel 1 --filtro "paracetamol"

# Limitando páginas
python main.py --nivel 1 --max-pages 5

# Combinando opções
python main.py --nivel 1 --filtro "dipirona" --max-pages 3
```

#### 📊 Saída:
- Arquivo: `data/servimed_produtos_scrapy.json`
- Format: JSON com lista de produtos
- Logs: Console em tempo real

---

### 🎯 NÍVEL 2: SISTEMA DE FILAS (ASSÍNCRONA)
**Descrição:** Processamento via filas usando Celery + Redis  
**Uso:** Para processamento em larga escala e produção  
**Framework:** Scrapy + Celery + Redis

#### 🔧 Pré-requisitos:
```bash
# 1. Instalar e iniciar Redis
# Windows: Baixar Redis ou usar Docker
docker run -d -p 6379:6379 redis:latest

# 2. Iniciar worker Celery
python -m celery -A src.nivel2.celery_app worker --loglevel=info
```

#### 🔧 Como Usar:
```bash
# Verificar status dos workers
python main.py --nivel 2 --worker-status

# Enfileirar nova tarefa
python main.py --nivel 2 --enqueue --usuario "user@example.com" --senha "password"

# Verificar status de tarefa
python main.py --nivel 2 --status "task-id-aqui"

# Com filtro
python main.py --nivel 2 --enqueue --filtro "antibiotico"
```

#### 📊 Saída:
- Task ID para acompanhamento
- Callback HTTP para notificação
- Resultados via API status

---

### 🎯 NÍVEL 3: SISTEMA DE PEDIDOS
**Descrição:** Sistema completo de processamento de pedidos  
**Framework:** Scrapy + Celery + Sistema de Pedidos

#### 🔧 Como Usar:
```bash
# Teste do sistema
python src/pedido_queue_client.py test

# Enfileirar pedido
python src/pedido_queue_client.py enqueue "PEDIDO123" "444212" "2" "1234567890123"

# Verificar status do pedido
python src/pedido_queue_client.py status "task-id"

# Via main.py (orientações)
python main.py --nivel 3
```

#### 📊 Saída:
- Task ID do pedido
- Status detalhado via API
- Integração com sistemas externos

---

## ⚙️ CONFIGURAÇÃO DO AMBIENTE

### 📋 Dependências Principais
```txt
# === CORE (obrigatórias) ===
scrapy>=2.11.0              # Framework de scraping principal
twisted>=22.10.0             # Engine assíncrono do Scrapy
itemadapter>=0.7.0           # Adaptador de items do Scrapy
requests>=2.31.0             # HTTP requests
urllib3>=2.0.0               # HTTP client base
python-dotenv>=1.0.0         # Variáveis de ambiente

# === NÍVEL 2 (Sistema de Filas) ===
celery>=5.3.0                # Framework de filas distribuídas
redis>=5.0.0                 # Broker de mensagens
kombu>=5.3.0                 # Biblioteca de messaging do Celery

# === DESENVOLVIMENTO ===
pytest>=7.4.0                # Framework de testes
pytest-asyncio>=0.21.0       # Suporte async para pytest
pytest-cov>=4.1.0            # Coverage de código
pytest-mock>=3.11.0          # Mock fixtures

# === OPCIONAIS ===
flower>=2.0.0                 # Monitoramento Celery (web UI)
```

### 🔧 Instalação
```bash
# 1. Clonar/baixar o projeto
cd servimed-scraper

# 2. Instalar dependências
python -m pip install -r requirements.txt

# 3. Configurar variáveis de ambiente (.env)
# Copiar .env.example para .env e ajustar valores
```

### 🔐 Variáveis de Ambiente (.env)
```env
# TOKENS DE AUTENTICAÇÃO (obrigatório - extrair do navegador)
ACCESS_TOKEN=seu_access_token_aqui
SESSION_TOKEN=seu_session_token_jwt_aqui

# CREDENCIAIS DO PORTAL (obrigatório)
PORTAL_EMAIL=seu_email@dominio.com.br
PORTAL_PASSWORD=sua_senha_portal

# CONFIGURAÇÕES DO USUÁRIO (obrigatório)
LOGGED_USER=codigo_usuario
CLIENT_ID=codigo_cliente
CLIENT_SECRET=codigo_secreto_cliente
X_CART=hash_carrinho_usuario

# USUÁRIOS AUTORIZADOS (opcional - separados por vírgula)
USERS=codigo1,codigo2,codigo3

# COTEFACIL API - OAuth2PasswordBearer (obrigatório)
COTEFACIL_BEARER_TOKEN=seu_bearer_token_cotefacil
COTEFACIL_API_URL=https://desafio.cotefacil.net

# CALLBACK API - Credenciais para sistema de callbacks (obrigatório)
CALLBACK_API_USER=seu_usuario_callback@dominio.com.br
CALLBACK_API_PASSWORD=sua_senha_callback
CALLBACK_URL=https://desafio.cotefacil.net

# URLs DO SISTEMA (configuração padrão)
PORTAL_URL=https://pedidoeletronico.servimed.com.br
BASE_URL=https://peapi.servimed.com.br
API_ENDPOINT=/api/carrinho/oculto
SITE_VERSION=4.0.27

# Redis/Celery (opcional - para Nível 2)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Logs (opcional)
LOG_LEVEL=INFO
LOG_FILE=data/logs/servimed_scraper.log
```

---

## 🧪 SISTEMA DE TESTES AUTOMATIZADOS

### 📊 Estatísticas dos Testes
- **Status:** ✅ Testes automatizados implementados
- **Funcionais:** Testes básicos funcionando
- **Categorias:** Unit, Integration, Error Handling

### 🔧 Executando Testes

#### 🎯 Método 1: Script Automatizado
```bash
# Executar script interativo
python run_tests.py

# Opções disponíveis:
# 1. Executar todos os testes
# 2. Executar teste específico
# 3. Instalar dependências de teste
# 4. Verificar estrutura de testes
# 5. Sair
```

#### 🎯 Método 2: Pytest Direto
```bash
# Todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_basic_functionality.py -v
python -m pytest tests/test_config.py -v
python -m pytest tests/test_main.py -v

# Testes por categoria
python -m pytest tests/ -k "test_basic" -v
python -m pytest tests/ -k "integration" -v

# Com cobertura de código
python -m pytest tests/ --cov=src --cov=main --cov-report=html

# Apenas verificar estrutura
python -m pytest tests/ --collect-only
```

#### 🎯 Método 3: Testes Específicos
```bash
# Teste de funcionalidade básica (sempre funciona)
python -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_python_environment -v

# Testes de configuração de paths
python -m pytest tests/test_config.py::TestConfigPaths -v

# Testes do ScrapyWrapper
python -m pytest tests/test_scrapy_wrapper.py::TestScrapyWrapper::test_setup_logging -v
```

### 📋 Tipos de Testes Implementados

#### 🔧 **Testes Básicos** ✅
- ✅ Ambiente Python funcional
- ✅ Estrutura do projeto
- ✅ Importações de módulos
- ✅ Criação de objetos principais
- ✅ Operações de arquivo
- ✅ Dependências instaladas

#### 🔗 **Testes de Configuração** ✅
- ✅ Paths do projeto
- ✅ Diretórios de trabalho
- ✅ Arquivos de configuração
- ✅ Variáveis de ambiente
- ✅ Integração de configurações

#### 🚀 **Testes do Sistema**
- ScrapyWrapper functionality
- Sistema de filas Celery
- Cliente de pedidos
- Integração end-to-end
- Tratamento de erros

---

## 🛠️ GUIA DE DESENVOLVIMENTO

### 🔍 Debug e Logs
```bash
# Logs detalhados do Scrapy
python main.py --nivel 1 --filtro "test" --max-pages 1

# Logs do Celery (Nível 2)
python -m celery -A src.nivel2.celery_app worker --loglevel=debug

# Verificar logs em arquivo
# Windows: type data\logs\servimed_scraper.log
# Linux/Mac: cat data/logs/servimed_scraper.log
```

### 🔧 Estrutura do Código

#### 📄 main.py - Ponto de Entrada
```python
# Funções principais:
def executar_nivel_1(args)  # Execução direta
def executar_nivel_2(args)  # Sistema de filas  
def main()                  # Parser de argumentos e orquestração
```

#### 📄 src/scrapy_wrapper.py - Wrapper Scrapy
```python
class ScrapyServimedWrapper:
    def run_spider(filtro="", max_pages=1)    # Executar spider
    def get_results()                          # Obter resultados
    def run_spider_subprocess(...)             # Execução via subprocess
```

#### 📄 src/nivel2/queue_client.py - Cliente de Filas
```python
class TaskQueueClient:
    def enqueue_scraping_task(...)             # Enfileirar scraping
    def get_task_status(task_id)               # Status da tarefa
    def get_worker_status()                    # Status dos workers
```

#### 📄 src/pedido_queue_client.py - Cliente de Pedidos
```python
class PedidoQueueClient:
    def enqueue_pedido(...)                    # Enfileirar pedido
    def get_status(task_id)                    # Status do pedido
```

### 📊 Fluxo de Dados

#### Nível 1: Direto
```
main.py → ScrapyWrapper → Scrapy Spider → JSON File → Results
```

#### Nível 2: Filas
```
main.py → TaskQueueClient → Celery Task → ScrapyWrapper → Callback API
```

#### Nível 3: Pedidos
```
pedido_queue_client.py → Celery Task → Order Processing → External API
```

---

## 🚨 TROUBLESHOOTING

### ❌ Problemas Comuns

#### 1. **Redis não está rodando**
```bash
# Erro: ConnectionError: Error 10061 connecting to localhost:6379
# Solução: Iniciar Redis
docker run -d -p 6379:6379 redis:latest
```

#### 2. **Workers Celery não ativos**
```bash
# Erro: No workers available
# Solução: Iniciar worker
python -m celery -A src.nivel2.celery_app worker --loglevel=info
```

#### 3. **Dependências faltando**
```bash
# Erro: ModuleNotFoundError
# Solução: Instalar dependências
python -m pip install -r requirements.txt
```

#### 4. **Testes falhando**
```bash
# Verificar ambiente básico primeiro
python -m pytest tests/test_basic_functionality.py -v

# Se básicos passarem, problema é nos mocks/imports específicos
```

#### 5. **Arquivo .env não configurado**
```bash
# Criar .env com variáveis necessárias
# Ver seção "Variáveis de Ambiente" acima
```

### 🔧 Debug Mode
```bash
# Scrapy com debug
python -c "
import sys
sys.path.insert(0, 'src')
from scrapy_wrapper import ScrapyServimedWrapper
wrapper = ScrapyServimedWrapper()
print('Wrapper criado com sucesso!')
"

# Celery com debug
python -c "
import sys
sys.path.insert(0, 'src')
from nivel2.queue_client import TaskQueueClient
client = TaskQueueClient()
print('Cliente criado com sucesso!')
"
```

---

## 📈 MÉTRICAS E PERFORMANCE

### 🔍 Monitoramento
```bash
# Status do sistema
python main.py --nivel 2 --worker-status

# Logs em tempo real
# Windows PowerShell: Get-Content data\logs\servimed_scraper.log -Wait
# Linux/Mac: tail -f data/logs/servimed_scraper.log
```

---

## 🔧 COMANDOS ESSENCIAIS

### 📊 Para Desenvolvimento
```bash
# Executar scraping básico
python main.py --nivel 1 --max-pages 1

# Executar testes básicos
python -m pytest tests/test_basic_functionality.py -v

# Ver estrutura de testes
python -m pytest tests/ --collect-only

# Executar teste específico
python -m pytest tests/test_config.py::TestConfigPaths::test_project_root_path -v
```

### 🚨 Para Troubleshooting
```bash
# Verificar se arquivos existem
# Windows: dir main.py / dir src\scrapy_wrapper.py / dir tests\test_basic_functionality.py
# Linux/Mac: ls main.py / ls src/scrapy_wrapper.py / ls tests/test_basic_functionality.py

# Testar imports manualmente
python -c "import main; print('main.py OK')"
python -c "import sys; sys.path.insert(0, 'src'); import scrapy_wrapper; print('scrapy_wrapper OK')"

# Ver conteúdo de arquivos importantes
# Windows: type pytest.ini / type requirements.txt
# Linux/Mac: cat pytest.ini / cat requirements.txt
```

### 📈 Para Produção (Níveis 2 e 3)
```bash
# Nível 2 - Setup (requer Redis)
# 1. Instalar Redis: docker run -d -p 6379:6379 redis:latest
# 2. Iniciar worker: python -m celery -A src.nivel2.celery_app worker --loglevel=info
# 3. Enfileirar: python main.py --nivel 2 --enqueue --usuario "test@example.com" --senha "password"

# Nível 3 - Pedidos
python src/pedido_queue_client.py test
python main.py --nivel 3
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### 🧪 Checklist de Funcionalidades

#### ✅ Core Functionalities
- [x] **Scraping Básico** - Nível 1 funcionando
- [x] **Testes Automatizados** - Testes básicos implementados
- [x] **Estrutura Modular** - Imports e módulos OK
- [x] **Configurações** - Paths e settings funcionando
- [x] **Logging** - Sistema de logs ativo
- [x] **Error Handling** - Tratamento de erros implementado

#### 🔄 Advanced Features (configuração adicional necessária)
- [ ] **Sistema de Filas** - Requer Redis + Celery workers
- [ ] **API de Pedidos** - Requer configuração de credenciais
- [ ] **Callbacks HTTP** - Requer endpoints externos
- [ ] **Monitoramento** - Requer dashboard setup

#### 🧪 Quality Assurance
- [x] **Unit Tests** - Testes unitários funcionando
- [x] **Integration Tests** - Testes básicos de integração
- [x] **Environment Tests** - Validação de ambiente
- [x] **Configuration Tests** - Testes de configuração
- [x] **Documentation** - Documentação completa


---


## 📞 SUPORTE RÁPIDO

### ❌ Se algo não funcionar:
1. **Execute primeiro:** `python -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_python_environment -v`
2. **Se falhar:** Problema no ambiente Python
3. **Se passar:** Execute teste completo: `python -m pytest tests/test_basic_functionality.py -v`
4. **Para debug:** Use comandos da seção troubleshooting

### ✅ Se tudo funcionar:
1. **Continue** com scraping básico: `python main.py --nivel 1 --max-pages 1`
2. **Explore** filtros: `python main.py --nivel 1 --filtro "seu_termo" --max-pages 2`
3. **Avance** para níveis superiores conforme necessidade

### 📚 Recursos Adicionais
- **Scrapy Docs:** https://docs.scrapy.org/
- **Celery Docs:** https://docs.celeryproject.org/
- **Pytest Docs:** https://docs.pytest.org/

