# Script de correction simple
Write-Host "Correction securite projet..." -ForegroundColor Green

# 1. Generer cle securisee
$secureKey = -join ((1..32) | ForEach {Get-Random -Input ([char[]](48..57 + 65..90 + 97..122))})

# 2. Creer fichier .env
$envContent = "SECRET_KEY=$secureKey`nFLASK_ENV=development"
$envContent | Out-File -FilePath ".env" -Encoding UTF8

# 3. Installer dependances
pip install flask flask-sqlalchemy flask-login python-dotenv

Write-Host "Corrections appliquees!" -ForegroundColor Green
Write-Host "Fichier .env cree avec cle securisee" -ForegroundColor Cyan
