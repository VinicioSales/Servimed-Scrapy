@echo off
chcp 65001 >nul
REM ========================================
REM   CONFIGURACAO AUTOMATICA - SERVIMED
REM ========================================
echo.
echo SERVIMED SCRAPY - CONFIGURACAO AUTOMATICA
echo ========================================
echo Este script vai configurar tudo automaticamente!
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado!
    echo Instale Python 3.10+ primeiro: https://python.org
    pause
    exit /b 1
)

echo Python encontrado!

REM Criar ambiente virtual se nao existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo Ambiente virtual criado!
) else (
    echo Ambiente virtual ja existe!
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar dependencias
    pause
    exit /b 1
)

echo Dependencias instaladas!

REM Verificar arquivo .env
if not exist ".env" (
    if exist ".env.example" (
        echo Criando arquivo .env a partir do template...
        copy .env.example .env >nul
        echo IMPORTANTE: Configure o arquivo .env com seus dados!
        echo    Especialmente COTEFACIL_EMAIL e COTEFACIL_PASSWORD
    ) else (
        echo Arquivo .env nao encontrado - algumas funcionalidades podem nao funcionar
    )
) else (
    echo Arquivo .env encontrado!
)

REM Verificar se Redis portátil existe
if exist "tools\redis-portable\redis-server.exe" (
    echo Redis portátil encontrado!
    
    REM Iniciar Redis em segundo plano
    echo Iniciando Redis...
    start /B "Redis Server" cmd /c "cd tools\redis-portable && redis-server.exe"
    
    REM Aguardar Redis inicializar
    timeout /t 3 /nobreak >nul
    
    REM Verificar se Redis está rodando
    echo Testando conexao Redis...
    python -c "import redis; r = redis.Redis(); r.ping(); print('Redis conectado!')" 2>nul
    if errorlevel 1 (
        echo Redis pode nao estar totalmente iniciado ainda...
        echo    Aguarde alguns segundos e tente novamente se necessario
    )
    
) else (
    echo Redis portatil nao encontrado!
    echo    Apenas o Nivel 1 funcionara (sem Celery)
)

echo.
echo CONFIGURACAO COMPLETA!
echo ========================================
echo.
echo COMO USAR:
echo.
echo NIVEL 1 (Scrapy simples):
echo    python main.py nivel1
echo.
echo NIVEL 2 (Scrapy + Celery):
echo    Terminal 1: python -m celery -A src.nivel2.celery_app worker --loglevel=info
echo    Terminal 2: python main.py nivel2
echo.
echo NIVEL 3 (Sistema completo):
echo    Terminal 1: python -m celery -A src.nivel2.celery_app worker --loglevel=info
echo    Terminal 2: python main.py nivel3
echo.
echo EXECUTAR TESTES:
echo    python run_tests.py
echo.
echo IMPORTANTE: 
echo    - Mantenha o ambiente virtual ativo: venv\Scripts\activate
echo    - Para niveis 2 e 3, mantenha o Redis rodando (ja iniciado automaticamente)
echo    - Para parar Redis: feche a janela ou Ctrl+C
echo.
pause
