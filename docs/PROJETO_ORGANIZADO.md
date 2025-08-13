# Organização do Projeto Servimed Scraper

## ✅ Estrutura Final Organizada

```
servimed-scraper/
├── main.py                       # 🎯 SCRIPT PRINCIPAL - Ponto de entrada
├── pedido_queue_client.py        # Cliente de pedidos (nível 3)
├── queue_client.py               # Cliente de filas (nível 2)
├── scrapy.cfg                    # Configuração do Scrapy
├── requirements.txt              # Dependências Python
├── .env                          # Variáveis de ambiente
├── .env.example                  # Exemplo de configuração
│
├── src/                          # 📦 Código fonte principal
│   ├── scrapy_wrapper.py         # Wrapper para Scrapy
│   ├── api_client/               # Clientes de API
│   ├── nivel2/                   # Sistema de filas (Celery)
│   ├── nivel3/                   # Sistema de pedidos
│   ├── scrapy_servimed/          # Spiders Scrapy
│   └── servimed_scraper/         # Scraper original
│
├── config/                       # ⚙️ Configurações
├── data/                         # 📊 Dados coletados
├── docs/                         # 📚 Documentação
├── logs/                         # 📝 Arquivos de log
├── scripts/                      # 🔧 Scripts auxiliares
├── tests/                        # 🧪 Testes automatizados
└── tools/                        # 🛠️ Ferramentas auxiliares
```

## 🚀 Como Executar

### Comando Principal:
```bash
python main.py --help
```

### Exemplos:
```bash
# Nível 1 - Scraping direto
python main.py --nivel 1 --filtro "paracetamol"

# Nível 2 - Sistema de filas
python main.py --nivel 2 --enqueue

# Nível 3 - Sistema de pedidos
python pedido_queue_client.py test
```

## 📁 Organização por Funcionalidade

- **📁 src/**: Todo o código fonte organizado por módulos
- **📁 scripts/**: Scripts de inicialização (Redis, Workers)
- **📁 tools/**: Ferramentas auxiliares (Redis portável)
- **📁 config/**: Configurações centralizadas
- **📁 data/**: Outputs dos scrapings
- **📁 docs/**: Documentação do projeto
- **📁 logs/**: Logs e dumps
- **📁 tests/**: Testes automatizados

## ✅ Verificação

✅ main.py na raiz como ponto de entrada principal
✅ Estrutura organizada por funcionalidade
✅ Separação clara entre código, dados, docs e tools
✅ Scripts auxiliares organizados
✅ Configurações centralizadas
✅ Sistema funcionando perfeitamente

## 🎯 Resultado

Projeto organizado seguindo boas práticas de estruturação Python, mantendo o main.py como ponto de entrada principal na pasta raiz, com organização lógica de todas as funcionalidades.
