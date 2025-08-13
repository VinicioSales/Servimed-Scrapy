"""
Configurações dos diretórios
"""

from pathlib import Path

# Diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent

# Diretórios do projeto
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = PROJECT_ROOT / "config"
SRC_DIR = PROJECT_ROOT / "src"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

# Nomes de arquivos fixos (sempre sobrescreve)
OUTPUT_FILES = {
    'all_products': DATA_DIR / "servimed_produtos_completos.json",
    'filtered_products': DATA_DIR / "servimed_produtos_filtrados.json",
    'backup': DATA_DIR / "servimed_backup.json"
}
