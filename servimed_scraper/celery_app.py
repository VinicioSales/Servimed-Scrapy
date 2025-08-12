import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Configuração do Celery
app = Celery('servimed_scraper')

# Configurações para teste (sem Redis)
app.conf.update(
    broker_url='memory://',  # Usar broker em memória para teste
    result_backend='cache+memory://',  # Backend em memória para teste
    task_always_eager=True,  # Executar tarefas síncronas para teste
    task_eager_propagates=True,  # Propagar erros imediatamente
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
)

# Auto-descoberta de tarefas
app.autodiscover_tasks(['servimed_scraper.tasks'])
