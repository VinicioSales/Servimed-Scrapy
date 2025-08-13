# 🕷️ Servimed Scraper - Sistema Completo com Scrapy

Sistema completo de scraping do portal Servimed com três níveis de execução, sempre utilizando **Scrapy** como framework principal.

## 📋 Visão Geral

- **Nível 1**: Execução direta (síncrona)
- **Nível 2**: Sistema de filas com Celery (assíncrona)
- **Nível 3**: Sistema completo de pedidos

## 🚀 Instalação

### 1. Dependências
```bash
pip install -r requirements.txt
```

### 2. Configuração
Copie o arquivo `.env.example` para `.env` e configure suas credenciais:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Servimed.

### 3. Redis (para Níveis 2 e 3)
```bash
# Windows - usando Redis portable
redis_start.bat

# Linux/Mac
redis-server
```

## 🎯 Como Usar

### **Nível 1 - Execução Direta**
```bash
# Executar scraping direto
python main.py --nivel 1

# Com filtro
python main.py --nivel 1 --filtro "paracetamol"

# Limitando páginas
python main.py --nivel 1 --filtro "vitamina" --max-pages 5
```

### **Nível 2 - Sistema de Filas**
```bash
# 1. Iniciar worker Celery
start_worker.bat

# 2. Enfileirar tarefa
python main.py --nivel 2 --enqueue --filtro "dipirona"

# 3. Verificar status
python main.py --nivel 2 --status <task_id>
```

### **Nível 3 - Sistema de Pedidos**
```bash
# 1. Iniciar worker Celery
start_worker.bat

# 2. Teste de pedido
python pedido_queue_client.py test

# 3. Pedido personalizado
python pedido_queue_client.py enqueue PEDIDO123 444212 2

# 4. Verificar status
python pedido_queue_client.py status <task_id>
```

## 📁 Estrutura do Projeto

```
├── main.py                     # Script principal
├── pedido_queue_client.py      # Cliente para pedidos (Nível 3)
├── requirements.txt            # Dependências Python
├── .env                       # Configurações (criar a partir do .example)
├── start_worker.bat           # Script para iniciar worker Celery
├── redis_start.bat            # Script para iniciar Redis
├── src/
│   ├── scrapy_servimed/       # Projeto Scrapy
│   ├── scrapy_wrapper.py      # Wrapper do Scrapy
│   ├── servimed_scraper/      # Framework original (fallback)
│   ├── nivel2/               # Sistema de filas
│   │   ├── celery_app.py     # Configuração Celery
│   │   ├── tasks.py          # Tarefas assíncronas
│   │   └── queue_client.py   # Cliente de filas
│   ├── nivel3/               # Sistema de pedidos
│   │   ├── tasks.py          # Tarefas de pedidos
│   │   └── pedido_client.py  # Cliente de pedidos
│   └── api_client/           # Cliente para APIs externas
└── data/                     # Arquivos de saída
```

## 🕷️ Framework Scrapy

O sistema **sempre usa Scrapy** como framework principal:

- ✅ **Performance superior**
- ✅ **Melhor gestão de recursos**
- ✅ **Logs detalhados**
- ✅ **Fallback automático** para framework original em caso de erro

## 🔧 Configurações Importantes

### Credenciais (.env)
```env
# Portal Servimed
PORTAL_EMAIL=seu_email@empresa.com.br
PORTAL_PASSWORD=sua_senha

# API Callback
CALLBACK_API_USER=seu_email@empresa.com.br
CALLBACK_API_PASSWORD=sua_senha
CALLBACK_URL=https://desafio.cotefacil.net
```

### Redis
- **Porta**: 6379 (padrão)
- **Database**: 0
- **Necessário para**: Níveis 2 e 3

### Celery
- **Broker**: Redis
- **Pool**: solo (compatível com Windows)
- **Workers**: Iniciar via `start_worker.bat`

## 📊 Arquivos de Saída

- `data/servimed_produtos_scrapy.json` - Produtos coletados pelo Scrapy
- `data/servimed_backup.json` - Backup automático
- Logs detalhados no console

## 🛠️ Solução de Problemas

### Erro de Import
```bash
# Adicionar src ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:./src"  # Linux/Mac
$env:PYTHONPATH += ";.\src"              # Windows PowerShell
```

### Redis não conecta
```bash
# Verificar se Redis está rodando
redis-cli ping
```

### Worker Celery não inicia
```bash
# Matar processos Python antigos
taskkill /f /im python.exe  # Windows
```

## 📈 Performance

- **Scrapy**: ~2-3 segundos por página
- **Coleta**: 10-50 produtos por página
- **Memory**: ~100MB em uso típico
- **Concorrência**: Suporte a múltiplos workers

## 🔐 Segurança

- ✅ Credenciais em arquivo `.env` (não versionado)
- ✅ Autenticação OAuth2 para APIs
- ✅ Tokens com expiração automática
- ✅ Logs sem dados sensíveis

## 📝 Logs

O sistema gera logs detalhados mostrando:
- Framework utilizado (sempre Scrapy)
- Produtos coletados
- Tempo de execução
- Status das tarefas
- Erros e fallbacks

---

**🕷️ Sistema 100% Scrapy - Framework moderno e eficiente! 🕷️**
