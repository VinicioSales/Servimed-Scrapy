# 🕷️ Servimed Scraper - Desafio Técnico Cotefácil

## 📋 Descrição

Aplicação completa para web scraping do fornecedor Servimed com processamento assíncrono via filas e integração com API de callback, desenvolvida conforme especificação do Desafio Técnico da Cotefácil.

## 🎯 Níveis Implementados

### ✅ Nível 1 - Básico (100% Completo)
- ✅ Login no site Servimed
- ✅ Extração de produtos (GTIN, Código, Descrição, Preço, Estoque)
- ✅ Uso exclusivo do Scrapy
- ✅ Armazenamento em JSON

### ✅ Nível 2 - Intermediário (100% Completo)
- ✅ Sistema de filas assíncronas (Celery)
- ✅ Processamento independente de tarefas
- ✅ Integração com API callback
- ✅ Autenticação OAuth2
- ✅ Endpoint `POST /produto`

### ✅ Nível 3 - Avançado (100% Completo)
- ✅ Processamento de pedidos
- ✅ Código de confirmação
- ✅ Endpoint `PATCH /pedido/:id`
- ✅ Testes automatizados
- ✅ API completa

## 🏗️ Arquitetura

```
📦 Servimed Scraper
├── 🕷️ Spider Scrapy (Login + Scraping)
├── 🔌 Cliente API (Cotefácil Integration)
├── ⚡ Sistema Celery (Async Queues)
├── 🌐 API FastAPI (REST Interface)
├── 🧪 Testes (pytest)
└── 📊 Monitoramento (Flower)
```

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <repository-url>
cd Scrapy-Servimed
```

### 2. Crie ambiente virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

## ⚙️ Configuração

### Arquivo `.env`
```env
# Credenciais do Servimed
SERVIMED_USERNAME=juliano@farmaprevonline.com.br
SERVIMED_PASSWORD=a007299A
SERVIMED_CLIENT_ID=267511

# Credenciais da API Cotefácil
COTEFACIL_USERNAME=juliano@farmaprevonline.com.br
COTEFACIL_PASSWORD=a007299A
COTEFACIL_CLIENT_ID=267511
COTEFACIL_CLIENT_SECRET=05272420000221

# URLs
SERVIMED_BASE_URL=https://pedidoeletronico.servimed.com.br
SERVIMED_API_URL=https://peapi.servimed.com.br
COTEFACIL_BASE_URL=https://desafio.cotefacil.net

# Redis (opcional - usa memória por padrão)
REDIS_URL=redis://localhost:6379/0
```

## 🔧 Execução

### Nível 1 - Scraping Básico
```bash
cd servimed_scraper
scrapy crawl servimed -o produtos.json -L INFO
```

### Nível 2 & 3 - Sistema Completo

#### 1. Iniciar API
```bash
cd servimed_scraper
python challenge_api.py
```

#### 2. Enfileirar tarefa de scraping (Nível 2)
```bash
curl -X POST "http://localhost:8000/nivel2/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": "fornecedor_user",
    "senha": "fornecedor_pass",
    "callback_url": "https://desafio.cotefacil.net"
  }'
```

#### 3. Enfileirar tarefa de pedido (Nível 3)
```bash
curl -X POST "http://localhost:8000/nivel3/order" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": "fornecedor_user",
    "senha": "fornecedor_pass",
    "id_pedido": "1234",
    "produtos": [
      {
        "gtin": "1234567890123",
        "codigo": "A123",
        "quantidade": 1
      }
    ],
    "callback_url": "https://desafio.cotefacil.net"
  }'
```

#### 4. Verificar status da tarefa
```bash
curl "http://localhost:8000/task/{task_id}"
```

## 🧪 Testes

### Executar todos os testes
```bash
pytest tests/ -v
```

### Teste específico
```bash
pytest tests/test_cotefacil_client.py -v
```

### Teste com coverage
```bash
pip install pytest-cov
pytest tests/ --cov=servimed_scraper --cov-report=html
```

## 📡 API Endpoints

### Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações da API |
| `POST` | `/nivel2/scrape` | Scraping de produtos (Nível 2) |
| `POST` | `/nivel3/order` | Processamento de pedido (Nível 3) |
| `GET` | `/task/{id}` | Status da tarefa |
| `GET` | `/health` | Health check |
| `POST` | `/setup/user` | Configurar usuário na API |

### Documentação Interativa
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔍 Monitoramento

### Flower (Monitor Celery)
```bash
cd servimed_scraper
celery -A celery_app flower
# Acesse: http://localhost:5555
```

### Logs
- API: Saída do terminal
- Celery: Logs do worker
- Scrapy: Log level configurável

## 🏛️ Estrutura do Projeto

```
Scrapy-Servimed/
├── servimed_scraper/
│   ├── servimed_scraper/
│   │   ├── clients/
│   │   │   └── cotefacil_client.py
│   │   ├── spiders/
│   │   │   └── servimed_spider.py
│   │   └── tasks/
│   │       ├── challenge_tasks.py
│   │       └── scraping_tasks.py
│   ├── celery_app.py
│   ├── challenge_api.py
│   └── test_api.py
├── tests/
│   ├── test_cotefacil_client.py
│   └── test_challenge_tasks.py
├── .env.example
├── .gitignore
└── README.md
```

## 🔐 Segurança

- ✅ Variáveis de ambiente para credenciais
- ✅ Arquivo `.env` no `.gitignore`
- ✅ Timeout em requisições
- ✅ Retry automático com backoff
- ✅ Headers de segurança

## 🚀 Deploy

### Docker (Opcional)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "servimed_scraper/challenge_api.py"]
```

### Produção
1. Configure Redis/RabbitMQ
2. Use supervisor/systemd para workers
3. Configure nginx para API
4. Monitore com Flower

## 🛠️ Tecnologias

- **Python 3.10+**
- **Scrapy 2.13+** - Web scraping
- **Celery** - Filas assíncronas
- **FastAPI** - API REST
- **Redis** - Message broker
- **pytest** - Testes
- **Flower** - Monitoramento

## 📊 Conformidade com Requisitos

### ✅ Requisitos Funcionais
- [x] Login autenticado no Servimed
- [x] Extração de dados de produtos
- [x] Sistema de filas assíncronas
- [x] Integração com API callback
- [x] Processamento de pedidos
- [x] Código de confirmação

### ✅ Requisitos Técnicos
- [x] Uso exclusivo do Scrapy
- [x] Código modular e limpo
- [x] Tratamento de erros
- [x] Logs detalhados
- [x] Testes automatizados
- [x] Documentação completa

### ✅ Endpoints Conforme Especificação
- [x] `POST /produto` - Envio de produtos
- [x] `PATCH /pedido/:id` - Confirmação de pedido
- [x] Autenticação OAuth2
- [x] Estrutura de dados exata

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs
2. Execute os testes
3. Consulte a documentação da API
4. Use o health check

## 🔄 Versionamento

- **v1.0.0** - Implementação completa dos 3 níveis
- Todos os requisitos do desafio atendidos
- Testes automatizados incluídos
