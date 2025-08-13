@echo off
REM Script para iniciar Redis local - Execute da raiz do projeto
echo ========================================
echo    INICIANDO REDIS LOCAL - SERVIMED
echo ========================================
echo.

REM Verificar se estamos na raiz do projeto
if not exist "tools\redis-portable" (
    echo [ERRO] Execute este script na raiz do projeto!
    echo        Ou mova para onde existe tools\redis-portable\
    echo.
    echo Diretório atual: %CD%
    pause
    exit /b 1
)

if exist "tools\redis-portable\redis-server.exe" (
    echo [OK] Redis encontrado!
    echo Iniciando servidor Redis...
    echo.
    echo ⚠️  IMPORTANTE: Mantenha esta janela aberta!
    echo.
    echo Para parar: Ctrl+C
    echo ========================================
    cd tools\redis-portable
    redis-server.exe
) else (
    echo [ERRO] Redis nao encontrado em tools\redis-portable\!
    echo.
    echo 💡 SOLUÇÕES:
    echo    1. Copie tools\redis-portable\ da máquina original
    echo    2. Execute: python setup_machine.py
    echo    3. Use Docker: docker run -d -p 6379:6379 redis:alpine
    pause
)
