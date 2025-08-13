# 🏥 Servimed Scraper - Estrutura Organizada

Scraper profissional para coletar produtos do Portal Servimed com estrutura modular e nomes de arquivo fixos.

## 📁 Estrutura do Projeto

```
PROVA/
├── 📄 main.py                              # Arquivo principal de execução ⭐
├── 📄 .env                                 # Configurações sensíveis (não commitar)
├── 📄 .env.example                         # Template de configuração
│
├── 📂 src/                                 # Código fonte
│   └── 📂 servimed_scraper/
│       ├── 📄 __init__.py                  # Inicializador do módulo
│       └── 📄 scraper.py                   # Classe principal do scraper
│
├── 📂 config/                              # Configurações
│   ├── 📄 __init__.py                      # Importa todas as configurações
│   ├── 📄 settings.py                      # Configurações principais
│   └── 📄 paths.py                         # Definições de caminhos
│
├── 📂 data/                                # Arquivos de saída ⭐
│   ├── 📄 servimed_produtos_completos.json # Todos os produtos (nome fixo)
│   ├── 📄 servimed_produtos_filtrados.json # Produtos filtrados (nome fixo)
│   └── 📄 servimed_backup.json             # Backup automático (nome fixo)
│
└── 📂 docs/                                # Documentação
    ├── 📄 README.md                        # Este arquivo
    └── 📄 STATUS.md                        # Status do projeto
```

## ✨ Principais Melhorias

### 🎯 **Nomes de Arquivo Fixos** (Sempre Sobrescreve)
- ✅ `data/servimed_produtos_completos.json` - Para busca sem filtro
- ✅ `data/servimed_produtos_filtrados.json` - Para busca com filtro
- ✅ `data/servimed_backup.json` - Backup automático

### 🏗️ **Estrutura Modular**
- ✅ Código organizado em módulos separados
- ✅ Configurações centralizadas
- ✅ Documentação organizada
- ✅ Dados separados do código

### 🚀 **Arquivo Principal Único**
- ✅ `main.py` - Ponto de entrada único do projeto
- ✅ Suporte completo a parâmetros CLI
- ✅ Interface clara e intuitiva

## 🎮 Como Usar

### 1. Execução Básica
```bash
# Todos os produtos (salva em: data/servimed_produtos_completos.json)
python main.py

# Com filtro (salva em: data/servimed_produtos_filtrados.json)
python main.py --filtro "paracetamol"

# Limitando páginas
python main.py --max-pages 10

# Combinando opções
python main.py --filtro "dipirona" --max-pages 5
```

### 2. Visualizar Opções
```bash
python main.py --help
```

## 📊 Arquivos de Saída

### 🔄 **Sistema de Sobrescrita**
Cada execução **sempre sobrescreve** o arquivo anterior, mantendo apenas a versão mais recente:

| Tipo de Busca | Arquivo Gerado | Comportamento |
|---------------|----------------|---------------|
| Sem filtro | `data/servimed_produtos_completos.json` | Sobrescreve sempre |
| Com filtro | `data/servimed_produtos_filtrados.json` | Sobrescreve sempre |
| Backup automático | `data/servimed_backup.json` | Sobrescreve a cada 50 páginas |

### 📋 **Estrutura dos Dados**
```json
{
  "metadados": {
    "total_produtos": 36,
    "data_coleta": "2025-08-12 22:45:15",
    "filtro_usado": "paracetamol",
    "tipo_busca": "FILTRO: 'paracetamol'",
    "fonte": "Portal Servimed - API Completa",
    "usuario": "juliano@farmaprevonline.com.br"
  },
  "produtos": [
    {
      "gtin_ean": "7896004783864",
      "codigo": "442522",
      "descricao": "PARACETAMOL 500MG + FOSFATO DE CODEINA 30MG COM 36 COMPRIMIDOS",
      "preco_fabrica": "45.57",
      "estoque": 377
    }
  ]
}
```

## ⚙️ Configuração

### 1. Pré-requisitos
```bash
pip install requests urllib3
```

### 2. Configuração do .env
```bash
# Copie o template
cp .env.example .env

# Edite com seus dados reais
# O arquivo .env deve conter:
ACCESS_TOKEN=seu_token_aqui
SESSION_TOKEN=seu_session_token_aqui
PORTAL_EMAIL=seu_email@exemplo.com
# ... outras configurações
```

### 3. Estrutura Automática
- As pastas `data/` e `docs/` são criadas automaticamente
- Os arquivos de configuração são carregados automaticamente
- Validação de configuração na inicialização

## 🛡️ Segurança

### ✅ **Proteção de Dados Sensíveis**
- Tokens e credenciais em arquivo `.env` separado
- Configurações não sensíveis no código
- Sistema de validação automática

### ✅ **Organização Limpa**
- Código fonte separado dos dados
- Documentação organizada
- Estrutura profissional

## 📈 Performance

- ⚡ **Rate Limiting**: 2 segundos entre requests
- 💾 **Backup Automático**: A cada 50 páginas
- 🚀 **Velocidade**: ~800-1200 produtos/minuto
- 📦 **Otimização**: Estrutura modular eficiente

## 🎯 Exemplos de Execução

### Coleta Completa
```bash
python main.py
# Resultado: data/servimed_produtos_completos.json (~12.935 produtos)
```

### Coleta Filtrada
```bash
python main.py --filtro "ibuprofeno"
# Resultado: data/servimed_produtos_filtrados.json (produtos específicos)
```

### Teste Rápido
```bash
python main.py --max-pages 5
# Resultado: data/servimed_produtos_completos.json (~125 produtos)
```

## 🚨 Solução de Problemas

### Módulo não encontrado
```bash
# Certifique-se de executar do diretório raiz
cd /caminho/para/PROVA
python main.py
```

### Erro de configuração
```bash
# Verifique se o .env existe e está configurado
ls -la .env
cat .env.example  # Ver exemplo
```

### Erro de permissão na pasta data
```bash
# Crie a pasta manualmente se necessário
mkdir data
chmod 755 data
```

## 📋 Status do Projeto

✅ **Estrutura Organizada**: Módulos separados e organizados  
✅ **Nomes Fixos**: Sistema de sobrescrita implementado  
✅ **Arquivo Principal**: main.py como ponto de entrada único  
✅ **Configuração Modular**: Settings centralizados e seguros  
✅ **Documentação**: Guias completos e atualizados  

**Última atualização**: 12/08/2025 - Estrutura modular com nomes fixos

---

## 🎯 **Diferenças da Versão Anterior**

| Aspecto | Versão Anterior | Versão Atual |
|---------|----------------|--------------|
| **Nomes de Arquivo** | `servimed_produtos_termo_timestamp.json` | `servimed_produtos_filtrados.json` |
| **Estrutura** | Arquivos soltos na raiz | Módulos organizados em pastas |
| **Execução** | `python scraper_todos_produtos.py` | `python main.py` |
| **Configuração** | Imports diretos | Módulo config centralizado |
| **Organização** | Código e dados misturados | Separação clara de responsabilidades |

**🎉 Agora você tem um projeto Python profissional e bem organizado!**
