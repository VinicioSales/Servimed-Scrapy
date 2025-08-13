"""
Celery App Simplificado para Windows
====================================

Configuração otimizada para funcionamento no Windows
"""

import os
import sys
from pathlib import Path
from celery import Celery

# Configurar path de forma robusta
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent
src_dir = project_root / "src"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Carregar configurações
try:
    from config.settings import configuracao
    print("Configuracao carregada com sucesso!")
    print(f"Usuario: {configuracao.get('PORTAL_EMAIL', 'N/A')}")
    print(f"Token valido ate: {configuracao.get('token_expiry', 'N/A')}")
except Exception as e:
    print(f"Aviso: Erro ao carregar configuracoes: {e}")
    configuracao = {}

# Configuração Redis
REDIS_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

# Criar app Celery
app = Celery(
    'servimed_scraper_simple',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['src.nivel2.tasks']  # Usar tasks
)

# Configurações otimizadas para Windows
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    result_expires=3600,  # 1 hora
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
)

# Configurações específicas para Windows
if os.name == 'nt':  # Windows
    app.conf.update(
        worker_pool='solo',
        worker_concurrency=1,
    )

print(f"Celery app configurado: {app.main}")
print(f"Broker: {REDIS_URL}")

if __name__ == '__main__':
    app.start()
