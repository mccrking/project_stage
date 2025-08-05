# Script de démarrage Central Danone avec Groq API (GRATUIT)
Write-Host "🚀 Démarrage Central Danone avec Groq API (GRATUIT)..." -ForegroundColor Green
Write-Host ""

# Définir la variable d'environnement Groq
$env:GROQ_API_KEY = "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"

# Activer l'environnement virtuel
& ".\venv\Scripts\Activate.ps1"

# Démarrer l'application
Write-Host "✅ Variable GROQ_API_KEY définie (GRATUIT)" -ForegroundColor Green
Write-Host "🌐 Démarrage de l'application..." -ForegroundColor Cyan
Write-Host ""

python app.py

Read-Host "Appuyez sur Entrée pour fermer..." 