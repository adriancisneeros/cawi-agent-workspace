@echo off
title CAWI - Kowey Agent Hub

:inicio
cls
echo ===================================================
echo        CAWI AGENT WORKSPACE - THINKPAD SESSION
echo ===================================================
echo.
echo Selecciona la accion:
echo [1] Iniciar Centinela Continuo (Watcher en segundo plano)
echo [2] Procesar cola de logs manualmente (logs_inbox)
echo [3] Evaluacion directa de prueba (evaluador_metricas.py)
echo [4] Iniciar Dashboard Streamlit (0.0.0.0:8501)
echo [5] Ver ultimos registros de metricas_cawi.csv
echo [6] Salir
echo.
set /p opcion="Opcion: "

if "%opcion%"=="1" (
    echo.
    python log_watcher.py
    pause
    goto inicio
)
if "%opcion%"=="2" (
    echo.
    echo Procesando archivos pendientes en logs_inbox...
    python log_ingestion.py
    pause
    goto inicio
)
if "%opcion%"=="3" (
    echo.
    echo Ejecutando evaluacion estructurada de prueba...
    python evaluador_metricas.py
    pause
    goto inicio
)
if "%opcion%"=="4" (
    echo.
    echo Iniciando interfaz de usuario en red local...
    streamlit run server.py --server.address 0.0.0.0
    pause
    goto inicio
)
if "%opcion%"=="5" (
    echo.
    echo Ultimos registros en metricas_cawi.csv:
    powershell -Command "Get-Content .\metricas_cawi.csv -Tail 5"
    echo.
    pause
    goto inicio
)
if "%opcion%"=="6" exit
goto inicio
