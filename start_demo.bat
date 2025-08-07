@echo off
echo.
echo ===============================================
echo    DASHBOARD DANONE - DEMARRAGE SECURISE
echo ===============================================
echo.

echo [1/4] Verification de l'environnement...
if not exist .env (
    echo ❌ ERREUR: Fichier .env manquant
    echo Executez d'abord: fix_security.ps1
    pause
    exit /b 1
)

if not exist network_monitor.db (
    echo [2/4] Initialisation de la base de donnees...
    python init_database.py
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ ERREUR: Echec initialisation DB
        pause
        exit /b 1
    )
) else (
    echo [2/4] Base de donnees OK
)

echo [3/4] Test de fiabilite...
python test_fiabilite.py

echo.
echo [4/4] Demarrage de l'application...
echo.
echo ===============================================
echo  🚀 APPLICATION PRETE - DANONE DASHBOARD
echo ===============================================
echo  📍 URL: http://localhost:5000
echo  👤 Login: admin / admin123
echo  📊 Interface: Dashboard supervision reseau
echo ===============================================
echo.

python app.py

echo.
echo Application fermee.
pause
