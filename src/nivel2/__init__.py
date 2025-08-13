"""
Nível 2 - Sistema de Filas
==========================

Sistema assíncrono para processamento de tarefas de scraping com filas.
"""

from .celery_app import app as celery_app

__all__ = ["celery_app"]
