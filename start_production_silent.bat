@echo off
REM Script de démarrage en mode production silencieux
REM Réduit les logs pour un environnement de production

echo 🚀 Démarrage Dashboard Danone - Mode Production Silencieux
echo ==========================================================

REM Définir l'environnement de production  
set FLASK_ENV=production
set FLASK_DEBUG=0

REM Démarrer l'application
echo ✅ Application en cours de démarrage...
echo ⚠️ Les logs de requêtes HTTP sont masqués en mode production
echo 📱 Interface web: http://localhost:5000
echo 👤 Connexion: admin / admin123
echo ⏹️ Arrêt: Ctrl+C
echo --------------------------------------------------

python app.py 2>&1 | findstr /V "GET.*HTTP/1.1.*200 GET.*static.*304 INFO:werkzeug.*GET INFO:werkzeug.*POST"
