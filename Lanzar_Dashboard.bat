@echo off
echo ************************************************************
echo 🚀 LANZANDO NEXUS HUB v8.1 (FUERZA BRUTA)...
echo ************************************************************
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

:: Forzamos el silencio total mediante parámetros directos
".\scout_env\Scripts\streamlit.exe" run "web_builder.py" --browser.gatherUsageStats false --server.headless false

echo ************************************************************
echo ✅ Si el navegador no se abrio solo: http://localhost:8501
echo ************************************************************
pause
