"""
Configurações dos diretórios e paths
"""

import sys
from pathlib import Path

# Diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent

# Diretórios do projeto
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = PROJECT_ROOT / "config"
SRC_DIR = PROJECT_ROOT / "src"
BIN_DIR = PROJECT_ROOT / "bin"
LOGS_DIR = PROJECT_ROOT / "logs"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TOOLS_DIR = PROJECT_ROOT / "tools"
TESTS_DIR = PROJECT_ROOT / "tests"

# Configurar sys.path para importações
def setup_paths():
    """Configura os paths do Python para importações corretas"""
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))

# Auto-configurar quando importado
setup_paths()

# Criar diretórios se não existirem
for directory in [DATA_DIR, DOCS_DIR, LOGS_DIR, BIN_DIR, SCRIPTS_DIR, TOOLS_DIR, TESTS_DIR]:
    directory.mkdir(exist_ok=True)

# Nomes de arquivos fixos (sempre sobrescreve)
OUTPUT_FILES = {
    'all_products': DATA_DIR / "servimed_produtos_completos.json",
    'filtered_products': DATA_DIR / "servimed_produtos_filtrados.json",
    'scrapy_products': DATA_DIR / "servimed_produtos_scrapy.json",
    'backup': DATA_DIR / "servimed_backup.json"
}
