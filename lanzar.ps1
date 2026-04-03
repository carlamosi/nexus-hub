# SCRIPT DE LANZAMIENTO SEGURO NEXUS v6.11
$Env:PYTHONIOENCODING = 'utf-8'

# Usamos comillas simples para que el signo '!' sea tratado como texto literal
$projPath = 'c:\Users\carla\Desktop\Stuff!\Estadística\'
Set-Location $projPath

Write-Host "************************************************************" -ForegroundColor Cyan
Write-Host "🚀 LANZANDO NEXUS INTELLIGENCE HUB v6.11 (POWER-SHELL)..." -ForegroundColor Cyan
Write-Host "************************************************************" -ForegroundColor Cyan

# Ejecutamos Streamlit
& '.\scout_env\Scripts\streamlit.exe' run '.\web_builder.py'

Write-Host "************************************************************" -ForegroundColor Yellow
Write-Host "✅ Si el navegador no se abrio solo: http://localhost:8501" -ForegroundColor Yellow
Write-Host "************************************************************" -ForegroundColor Yellow
