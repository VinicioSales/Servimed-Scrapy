# Servimed Scraper

Sistema completo de scraping e pedidos para o portal Servimed, desenvolvido com Scrapy framework.

## 📁 Estrutura do Projeto

```
servimed-scraper/
├── main.py                       # Script principal - 3 níveis
├── pedido_queue_client.py        # Cliente de pedidos (nível 3)
├── queue_client.py               # Cliente de filas (nível 2)
├── scrapy.cfg                    # Configuração do Scrapy
├── requirements.txt              # Dependências Python
├── .env                          # Variáveis de ambiente (não versionado)
├── .env.example                  # Exemplo de configuração
│
├── src/                          # Código fonte principal
│   ├── scrapy_wrapper.py         # Wrapper para Scrapy
│   ├── api_client/               # Clientes de API
│   ├── nivel2/                   # Sistema de filas (Celery)
│   ├── nivel3/                   # Sistema de pedidos
│   ├── scrapy_servimed/          # Spiders Scrapy
│   └── servimed_scraper/         # Scraper original
│
├── config/                       # Configurações
├── data/                         # Dados coletados
├── docs/                         # Documentação
├── logs/                         # Arquivos de log
├── scripts/                      # Scripts auxiliares
├── tests/                        # Testes automatizados
└── tools/                        # Ferramentas auxiliares
```
│   ├── pedido_queue_client.py    # Cliente de pedidos (Nível 3)
│   └── queue_client.py           # Cliente de filas (Nível 2)
├── src/                          # Código fonte do sistema
│   ├── api_client/               # Clientes para APIs externas
│   ├── nivel2/                   # Sistema de filas (Celery/Redis)
│   ├── nivel3/                   # Sistema de pedidos
│   ├── scrapy_servimed/          # Spiders do Scrapy
│   └── scrapy_wrapper.py         # Wrapper do Scrapy
├── scripts/                      # Scripts de utilitários
│   ├── start_worker.bat          # Inicia worker Celery
│   └── redis_start.bat           # Inicia Redis
├── tools/                        # Ferramentas auxiliares
│   └── redis-portable/           # Redis portável
├── config/                       # Configurações do sistema
├── data/                         # Dados gerados pelo scraping
├── docs/                         # Documentação
├── logs/                         # Logs do sistema
├── tests/                        # Testes unitários
├── servimed.bat                  # Executável principal (Windows)
├── pedidos.bat                   # Executável de pedidos (Windows)
├── .env                          # Variáveis de ambiente
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```

## 🚀 Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd servimed-scraper
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o ambiente:**
   ```bash
   cp .env.example .env
   # Edite o .env com suas credenciais
   ```

## 🎯 Uso

### Nível 1 - Execução Direta (Síncrona)

Execução simples e direta do scraper:

```bash
# Executar scraping básico
python main.py --nivel 1

# Com filtro de produto
python main.py --nivel 1 --filtro "paracetamol"

# Limitando páginas
python main.py --nivel 1 --max-pages 5
```

```bash
# Windows
servimed.bat --nivel 1 --filtro "paracetamol"

# Linux/Mac  
python bin/main.py --nivel 1 --filtro "paracetamol"
```

### Nível 2 - Sistema de Filas (Assíncrona)

1. **Inicie o Redis:**
   ```bash
   scripts/redis_start.bat
   ```

2. **Inicie o Worker:**
   ```bash
   scripts/start_worker.bat
   ```

3. **Enfileire tarefas:**
   ```bash
   python bin/main.py --nivel 2 --enqueue --filtro "dipirona"
   ```

### Nível 3 - Sistema de Pedidos

```bash
# Teste do sistema
pedidos.bat test

# Criar pedido
pedidos.bat enqueue PEDIDO001 444212 2

# Verificar status
pedidos.bat status <task_id>
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# Autenticação Servimed
SERVIMED_EMAIL=seu_email@exemplo.com
SERVIMED_SENHA=sua_senha

# API Cotefacil
CALLBACK_API_USER=usuario_api
CALLBACK_API_PASSWORD=senha_api
CALLBACK_URL=https://desafio.cotefacil.net

# Tokens de sessão (extraídos do navegador)
ACCESS_TOKEN=seu_access_token
SESSION_TOKEN=seu_session_token
LOGGED_USER=seu_user_id
CLIENT_ID=seu_client_id
X_CART=seu_x_cart
```

## 🏗️ Arquitetura

### Framework Único: Scrapy
- Todos os níveis usam Scrapy automaticamente
- Sistema otimizado e padronizado
- Melhor performance e manutenibilidade

### Níveis de Funcionamento:

1. **Nível 1**: Execução direta com Scrapy
2. **Nível 2**: Sistema de filas com Celery + Redis + Scrapy  
3. **Nível 3**: Sistema completo de pedidos + Scrapy

### Componentes Principais:

- **Scrapy Spiders**: Coleta de dados do portal
- **Celery Tasks**: Processamento assíncrono
- **API Client**: Integração com APIs externas
- **Queue System**: Gerenciamento de filas Redis

## 📊 Dados Coletados

Para cada produto:
- GTIN (Código de barras)
- Código interno
- Descrição
- Preço de fábrica
- Estoque disponível

Formatos de saída:
- JSON estruturado
- Logs detalhados
- Relatórios de status

## 🛠️ Desenvolvimento

### Estrutura de Desenvolvimento:
```bash
# Instalar em modo desenvolvimento
pip install -e .

# Executar testes
python -m pytest tests/

# Verificar qualidade do código
flake8 src/
```

### Contribuindo:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.
