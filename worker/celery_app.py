from celery import Celery
import os

# Configuração do Celery
app = Celery('servimed_worker')

# Configuração básica (usar Redis se disponível, senão usar broker em memória)
broker_url = os.getenv('CELERY_BROKER_URL', 'memory://')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'cache+memory://')

app.conf.update(
    broker_url=broker_url,
    result_backend=result_backend,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
)

# Auto-descobrir tasks
app.autodiscover_tasks(['worker'])

if __name__ == '__main__':
    app.start()
