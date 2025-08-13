# 🚀 GUIA DE INÍCIO RÁPIDO - SERVIMED SCRAPER

## ⚡ START EM 5 MINUTOS

### 📋 Pré-requisitos
- ✅ Python 3.10+ (já configurado em `C:/Python3.10_x64/Python310/python.exe`)
- ✅ Windows PowerShell
- ✅ Conexão com Internet

### 🔧 Setup Rápido

#### 1. Verificar se está tudo funcionando:
```bash
# Navegar para o diretório
cd "C:\Users\6128347\OneDrive - Thomson Reuters Incorporated\Documents\Scrips\Tests\PROVA"

# Testar ambiente básico
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_python_environment -v
```

#### 2. Executar primeiro teste do sistema:
```bash
# Nível 1 - Execução direta (mais simples)
C:/Python3.10_x64/Python310/python.exe main.py --nivel 1 --filtro "paracetamol" --max-pages 1
```

#### 3. Verificar resultados:
```bash
# Ver arquivo gerado
type data\servimed_produtos_scrapy.json
```

---

## 📝 EXEMPLOS PRÁTICOS

### 🎯 Exemplo 1: Busca Simples
```bash
# Buscar produtos com "dipirona" limitado a 2 páginas
C:/Python3.10_x64/Python310/python.exe main.py --nivel 1 --filtro "dipirona" --max-pages 2

# Resultado esperado: Arquivo JSON com produtos encontrados
```

### 🎯 Exemplo 2: Executar Testes
```bash
# Testes básicos (sempre funcionam)
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py -v

# Resultado esperado: 23 testes passando
```

### 🎯 Exemplo 3: Script Interativo de Testes
```bash
# Executar menu interativo
C:/Python3.10_x64/Python310/python.exe run_tests.py

# Escolher opção 1: Executar todos os testes
# Escolher opção 4: Verificar estrutura
```

### 🎯 Exemplo 4: Debug Básico
```bash
# Verificar se módulos carregam
C:/Python3.10_x64/Python310/python.exe -c "
import sys
sys.path.insert(0, 'src')
from scrapy_wrapper import ScrapyServimedWrapper
print('✅ ScrapyWrapper funcionando!')
"
```

---

## 🧪 TESTANDO O SISTEMA

### ✅ Checklist de Verificação

#### Teste 1: Ambiente Python ✅
```bash
C:/Python3.10_x64/Python310/python.exe -c "import sys; print(f'Python {sys.version}')"
# Esperado: Python 3.10.0 (ou superior)
```

#### Teste 2: Estrutura do Projeto ✅
```bash
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_project_structure -v
# Esperado: PASSED
```

#### Teste 3: Imports Funcionando ✅
```bash
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_src_imports -v
# Esperado: PASSED
```

#### Teste 4: ScrapyWrapper ✅
```bash
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_scrapy_wrapper_creation -v
# Esperado: PASSED
```

#### Teste 5: Configurações ✅
```bash
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_config.py::TestConfigPaths -v
# Esperado: 5 PASSED
```

---

## 🔧 COMANDOS ESSENCIAIS

### 📊 Para Desenvolvimento
```bash
# Executar scraping básico
C:/Python3.10_x64/Python310/python.exe main.py --nivel 1 --max-pages 1

# Executar testes básicos
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py -v

# Ver estrutura de testes
C:/Python3.10_x64/Python310/python.exe -m pytest tests/ --collect-only

# Executar teste específico
C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_config.py::TestConfigPaths::test_project_root_path -v
```

### 🚨 Para Troubleshooting
```bash
# Verificar se arquivos existem
dir main.py
dir src\scrapy_wrapper.py
dir tests\test_basic_functionality.py

# Testar imports manualmente
C:/Python3.10_x64/Python310/python.exe -c "import main; print('main.py OK')"
C:/Python3.10_x64/Python310/python.exe -c "import sys; sys.path.insert(0, 'src'); import scrapy_wrapper; print('scrapy_wrapper OK')"

# Ver conteúdo de arquivos importantes
type pytest.ini
type requirements.txt
```

### 📈 Para Produção (Níveis 2 e 3)
```bash
# Nível 2 - Setup (requer Redis)
# 1. Instalar Redis: docker run -d -p 6379:6379 redis:latest
# 2. Iniciar worker: C:/Python3.10_x64/Python310/python.exe -m celery -A src.nivel2.celery_app worker --loglevel=info
# 3. Enfileirar: C:/Python3.10_x64/Python310/python.exe main.py --nivel 2 --enqueue --usuario "test@example.com" --senha "password"

# Nível 3 - Pedidos
C:/Python3.10_x64/Python310/python.exe src/pedido_queue_client.py test
C:/Python3.10_x64/Python310/python.exe main.py --nivel 3
```

---

## 📋 CHECKLIST DE FUNCIONALIDADES

### ✅ Core Funcionalities
- [x] **Scraping Básico** - Nível 1 funcionando
- [x] **Testes Automatizados** - 23 testes básicos passando
- [x] **Estrutura Modular** - Imports e módulos OK
- [x] **Configurações** - Paths e settings funcionando
- [x] **Logging** - Sistema de logs ativo
- [x] **Error Handling** - Tratamento de erros implementado

### 🔄 Advanced Features (configuração adicional necessária)
- [ ] **Sistema de Filas** - Requer Redis + Celery workers
- [ ] **API de Pedidos** - Requer configuração de credenciais
- [ ] **Callbacks HTTP** - Requer endpoints externos
- [ ] **Monitoramento** - Requer dashboard setup

### 🧪 Quality Assurance
- [x] **Unit Tests** - Testes unitários funcionando
- [x] **Integration Tests** - Testes básicos de integração
- [x] **Environment Tests** - Validação de ambiente
- [x] **Configuration Tests** - Testes de configuração
- [x] **Documentation** - Documentação completa

---

## 🎯 PRÓXIMOS PASSOS SUGERIDOS

### 🚀 Para Uso Imediato
1. **Execute** os testes básicos para confirmar funcionamento
2. **Teste** o scraping nível 1 com filtro simples
3. **Verifique** os resultados no arquivo JSON gerado
4. **Explore** as opções de filtro e paginação

### 🔧 Para Desenvolvimento
1. **Configure** variáveis de ambiente (.env)
2. **Execute** testes mais avançados
3. **Personalize** filtros e configurações
4. **Implemente** novos spiders se necessário

### 🏗️ Para Produção
1. **Configure** Redis para sistema de filas
2. **Setup** workers Celery
3. **Configure** callbacks e webhooks
4. **Implemente** monitoramento

---

## 📞 Suporte Rápido

### ❌ Se algo não funcionar:
1. **Execute primeiro:** `C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_python_environment -v`
2. **Se falhar:** Problema no ambiente Python
3. **Se passar:** Execute teste completo: `C:/Python3.10_x64/Python310/python.exe -m pytest tests/test_basic_functionality.py -v`
4. **Para debug:** Use comandos da seção troubleshooting

### ✅ Se tudo funcionar:
1. **Continue** com scraping básico: `C:/Python3.10_x64/Python310/python.exe main.py --nivel 1 --max-pages 1`
2. **Explore** filtros: `C:/Python3.10_x64/Python310/python.exe main.py --nivel 1 --filtro "seu_termo" --max-pages 2`
3. **Avance** para níveis superiores conforme necessidade

---

**🎊 Sistema pronto para uso! Comece com os comandos básicos acima.**

*Tempo estimado de setup: 5 minutos*  
*Primeiro scraping: 2 minutos*  
*Primeiro teste: 30 segundos*
