# Script PowerShell - Démarrage production silencieux
# Réduit les logs pour un environnement de production

Write-Host "🚀 Démarrage Dashboard Danone - Mode Production Silencieux" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

# Définir l'environnement de production
$env:FLASK_ENV = "production"
$env:FLASK_DEBUG = "0"

# Démarrer l'application avec logs filtrés
python app.py | Where-Object { 
    $_ -notmatch "GET.*HTTP/1.1.*200" -and 
    $_ -notmatch "GET.*static.*304" -and 
    $_ -notmatch "INFO:werkzeug.*GET" -and
    $_ -notmatch "INFO:werkzeug.*POST"
}
