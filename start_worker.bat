@echo off
REM ========================================
REM   WORKER CELERY - SERVIMED SCRAPY
REM ========================================
echo.
echo 👷 INICIANDO WORKER CELERY
echo ========================================
echo.

REM Verificar se estamos na raiz do projeto
if not exist "main.py" (
    echo ❌ Execute este script da raiz do projeto!
    echo    Diretório atual: %CD%
    echo    Procurando por: main.py, src/, venv/
    pause
    exit /b 1
)

if not exist "src" (
    echo ❌ Pasta src/ não encontrada!
    echo    Execute da raiz do projeto onde está main.py
    pause
    exit /b 1
)

echo ✅ Diretório correto detectado

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Ambiente virtual não encontrado
    echo 💡 Execute: setup.bat primeiro
    pause
    exit /b 1
)

REM Verificar se Redis está rodando
echo 🔧 Verificando Redis...
tasklist /FI "IMAGENAME eq redis-server.exe" 2>NUL | find /I /N "redis-server.exe">NUL
if errorlevel 1 (
    echo ⚠️  Redis não está rodando
    echo 🚀 Tentando iniciar Redis...
    
    if exist "tools\redis-portable\redis-server.exe" (
        start /B "Redis" cmd /c "cd tools\redis-portable && redis-server.exe"
        echo ✅ Redis iniciado!
        timeout /t 3 /nobreak >nul
    ) else (
        echo ❌ Redis não encontrado!
        echo 💡 Execute: setup.bat primeiro
        pause
        exit /b 1
    )
) else (
    echo ✅ Redis já está rodando!
)

REM Testar imports antes de iniciar worker
echo 🧪 Testando imports do projeto...
python -c "from src.nivel2.celery_app import app; print('✅ Imports OK')" 2>nul
if errorlevel 1 (
    echo ❌ Erro nos imports - verificar configuração
    echo 💡 Possíveis soluções:
    echo    1. Ativar ambiente virtual: venv\Scripts\activate
    echo    2. Instalar dependências: pip install -r requirements.txt
    echo    3. Executar setup.bat
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando Worker Celery...
echo ========================================
echo.
echo ⚠️  IMPORTANTE:
echo    - Mantenha esta janela aberta para o worker funcionar
echo    - Use outro terminal para executar: python main.py nivel2 ou nivel3
echo    - Para parar: Ctrl+C
echo.
echo 👷 Worker iniciando...
echo.

REM Iniciar worker
python -m celery -A src.nivel2.celery_app worker --loglevel=info

echo.
echo 👋 Worker finalizado.
pause
