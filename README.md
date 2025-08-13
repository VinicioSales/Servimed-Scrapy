# 📖 SERVIMED SCRAPER - DOCUMENTAÇÃO

## 🏗️ VISÃO GERAL

O **Servimed Scraper** é um sistema completo de web scraping e processamento de pedidos desenvolvido em Python para o **Desafio CotefFácil**. Implementa uma arquitetura em 3 níveis de complexidade, sempre utilizando o framework **Scrapy**.

### 🎯 OBJETIVOS
- ✅ Extrair dados de produtos farmacêuticos do site Servimed
- ✅ Processar pedidos no portal Servimed 
- ✅ Integrar com API do desafio CotefFácil
- ✅ Sistema de filas para processamento assíncrono
- ✅ Códigos únicos de rastreamento para pedidos

---

## 🚀 INSTALAÇÃO RÁPIDA

### 📋 Pré-requisitos
- **Python 3.10+**
- **Windows 10/11** (ou compatível)
- **Conexão com internet**

### ⚡ Setup Automático
```bash
# 1. Execute o setup automático
setup.bat

# 2. Configure suas credenciais no arquivo .env
# (copie .env.example para .env e preencha os dados)

# 3. Teste o funcionamento
python main.py --nivel 1 --max-pages 1
```

**O script `setup.bat` irá:**
- ✅ Criar ambiente virtual Python
- ✅ Instalar todas as dependências 
- ✅ Configurar Redis para filas
- ✅ Preparar arquivo `.env` de configuração

---

## 🎯 COMO USAR

### **Nível 1 - Scraping Direto**
```bash
# Execução básica
python main.py --nivel 1

# Com filtro de produtos
python main.py --nivel 1 --filtro "paracetamol" --max-pages 2
```

### **Nível 2 - Sistema de Filas (PADRÃO: usa filas)**
```bash
# Terminal 1: Iniciar worker
start_worker.bat

# Terminal 2: Enfileirar tarefa (padrão)
python main.py --nivel 2 --filtro "vitamina"

# Verificar status
python main.py --nivel 2 --status TASK_ID

# Modo direto (opcional, sem filas)  
python main.py --nivel 2 --direct
```

### **Nível 3 - Sistema Completo (PADRÃO: usa filas)**
```bash
# Terminal 1: Iniciar worker
start_worker.bat

# Terminal 2: Criar pedido (padrão)
python main.py --nivel 3 --codigo-produto dd 212 --quantidade 5

# Verificar status
python main.py --nivel 3 --status TASK_ID

# Teste do sistema
python main.py --nivel 3 --test
```

---

## ⚙️ CONFIGURAÇÃO

### 🔐 Arquivo .env
Configure o arquivo `.env` copiando de `.env.example` e preenchendo os dados:

```env
# === TOKENS DE AUTENTICAÇÃO (obrigatório) ===
ACCESS_TOKEN=seu_access_token_aqui
SESSION_TOKEN=seu_session_token_aqui

# === CREDENCIAIS DO PORTAL (obrigatório) ===
PORTAL_EMAIL=seu_email@exemplo.com
PORTAL_PASSWORD=sua_senha_aqui

# === USUÁRIO E CLIENTE (obrigatório) ===
LOGGED_USER=seu_user_id
CLIENT_ID=seu_client_id
X_CART=seu_x_cart_hash

# === COTEFÁCIL API (obrigatório para nível 3) ===
CALLBACK_API_USER=seu_email@exemplo.com
CALLBACK_API_PASSWORD=sua_senha_aqui
CALLBACK_URL=https://desafio.cotefacil.net

# === CONFIGURAÇÕES OPCIONAIS ===
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

### 🔑 Como obter os tokens
1. Abra o portal Servimed no navegador
2. Faça login com suas credenciais
3. Abra DevTools (F12) > Network
4. Faça uma busca qualquer
5. Procure pela requisição "oculto"
6. Copie os valores dos headers:
   - `ACCESS_TOKEN` (do header 'accesstoken')
   - `SESSION_TOKEN` (do cookie 'sessiontoken')
   - `LOGGED_USER` (do header 'loggeduser')
   - `X_CART` (do header 'x-cart')

---

## 📁 ESTRUTURA DO PROJETO

```
PROVA/
├── 📄 main.py                    # Ponto de entrada principal
├── 📄 setup.bat                  # Configuração automática
├── 📄 start_worker.bat           # Iniciar worker Celery
├── 📄 run_tests.py               # Executar testes
├── 📄 requirements.txt           # Dependências
├── 📄 .env.example              # Template de configuração
├── 
├── 📁 src/                      # Código fonte
│   ├── 📄 scrapy_wrapper.py     # Wrapper Scrapy
│   ├── 📄 pedido_queue_client.py # Cliente de pedidos
│   ├── 📁 nivel2/               # Sistema de filas
│   ├── 📁 nivel3/               # Sistema completo
│   ├── 📁 api_client/           # Integração CotefFácil
│   └── 📁 scrapy_servimed/      # Projeto Scrapy
├── 
├── 📁 tests/                    # Testes automatizados
├── 📁 tools/                    # Redis portátil
└── 📁 data/                     # Resultados
```

---

## 🧪 TESTES

```bash
# Executar todos os testes
python run_tests.py

# Testes específicos
python -m pytest tests/test_basic_functionality.py -v
python -m pytest tests/test_main_simple.py -v
```

**Status dos testes:** ✅ 58 testes passando

---

## 🎯 DETALHES DOS NÍVEIS

### **🔹 Nível 1: Scraping Direto**
- **Descrição:** Extração básica usando apenas Scrapy
- **Uso:** `python main.py --nivel 1`
- **Saída:** `data/servimed_produtos_scrapy.json`
- **Características:** Síncrono, sem filas

### **🔹 Nível 2: Sistema de Filas**
- **Descrição:** Processamento assíncrono via Celery + Redis
- **Uso:** `python main.py --nivel 2` (padrão: usa filas)
- **Pré-requisito:** Worker ativo (`start_worker.bat`)
- **Características:** Assíncrono, escalável

### **🔹 Nível 3: Sistema Completo**
- **Descrição:** Processamento de pedidos + integração CotefFácil
- **Uso:** `python main.py --nivel 3 --codigo-produto ABC`
- **Pré-requisito:** Worker ativo + credenciais configuradas
- **Características:** Workflow completo do desafio

#### 📊 **Fluxo Nível 3 (Desafio CotefFácil):**
```
1. Buscar produto no Servimed (Scrapy)
2. Autenticar no portal Servimed  
3. Criar pedido → {"executado": "Ok"}
4. Gerar código único: SERVIMED_13082025_1245_444212_01_7511
5. API CotefFácil POST /pedido → {"id": 47}
6. PATCH /pedido/47 com código confirmação
7. Confirmação final ✅
```

#### 🏷️ **Formato Código Único:**
```
SERVIMED_DDMMAAAA_HHMM_PRODUTO_QTD_CLIENTE
Exemplo: SERVIMED_13082025_1245_444212_01_7511
```

---

## 🔧 TECNOLOGIAS

- **Python 3.10+** - Linguagem principal
- **Scrapy 2.13.3** - Framework de web scraping
- **Celery 5.x** - Sistema de filas assíncronas
- **Redis** - Broker de mensagens
- **Requests** - Cliente HTTP
- **Pytest** - Testes automatizados

---

## 🚨 SOLUÇÃO DE PROBLEMAS

### ❌ **Redis não conecta**
```bash
# Erro: Error 10061 connecting to localhost:6379
# Solução: Iniciar Redis
start_worker.bat  # Inicia Redis automaticamente
```

### ❌ **ModuleNotFoundError ao executar worker**
```bash
# Solução: Execute da RAIZ do projeto
cd /caminho/para/servimed-scrapy
start_worker.bat  # Não execute de subpastas
```

### ❌ **Tokens expirados**
```bash
# Erro: Token válido até: [data passada]
# Solução: Atualizar tokens no .env (extrair do DevTools)
```

### ❌ **Dependências faltando**
```bash
# Solução: Reinstalar dependências
pip install -r requirements.txt
```

---

## 📈 STATUS DO PROJETO

- ✅ **Nível 1:** Scrapy básico funcional
- ✅ **Nível 2:** Sistema de filas implementado  
- ✅ **Nível 3:** Integração CotefFácil completa
- ✅ **Testes:** Testes automatizados passando
- ✅ **Documentação:** Completa e atualizada

---

## 🎯 COMANDOS ESSENCIAIS

### Para uso diário:
```bash
# Scraping básico
python main.py --nivel 1 --filtro "produto" --max-pages 1

# Sistema de pedidos
python main.py --nivel 3 --codigo-produto 444212

# Executar testes
python run_tests.py
```

### Para desenvolvimento:
```bash
# Iniciar worker (níveis 2 e 3)
start_worker.bat

# Debug de imports
python -c "import sys; sys.path.insert(0, 'src'); import scrapy_wrapper; print('OK')"

# Verificar Redis
redis-cli ping
```

### Para troubleshooting:
```bash
# Verificar estrutura
python -c "import os; print(os.listdir('.'))"

# Testar Scrapy
python -c "import scrapy; print(f'Scrapy {scrapy.__version__} OK')"
```

---

## 📞 SUPORTE RÁPIDO

### ✅ **Para começar:**
```bash
# 1. Setup automático
setup.bat

# 2. Teste básico
python main.py --nivel 1 --max-pages 1

# 3. Para o desafio CotefFácil
python main.py --nivel 3 --codigo-produto 444212
```

### 🚨 **Se algo não funcionar:**
```bash
# 1. Verificar ambiente
python -m pytest tests/test_basic_functionality.py -v

# 2. Reinstalar dependências  
pip install -r requirements.txt

# 3. Para níveis 2/3: verificar Redis
start_worker.bat
```

---
