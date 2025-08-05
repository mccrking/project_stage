# Script de démarrage Central Danone avec DeepSeek API
Write-Host "🚀 Démarrage Central Danone avec DeepSeek API..." -ForegroundColor Green
Write-Host ""

# Définir la variable d'environnement DeepSeek
$env:DEEPSEEK_API_KEY = "sk-c8e1567f5c6c4caba8467d438d110e01"

# Activer l'environnement virtuel
& ".\venv\Scripts\Activate.ps1"

# Démarrer l'application
Write-Host "✅ Variable DEEPSEEK_API_KEY définie" -ForegroundColor Green
Write-Host "🌐 Démarrage de l'application..." -ForegroundColor Cyan
Write-Host ""

python app.py

Read-Host "Appuyez sur Entrée pour fermer..." 