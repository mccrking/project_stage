@echo off
echo ========================================
echo   Central Danone - Supervision Reseau
echo ========================================
echo.

echo [INFO] Demarrage du systeme de supervision...
echo [INFO] Verification des dependances...

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo [INFO] Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

REM Vérifier si les dépendances sont installées
echo [INFO] Verification des packages Python...
python -c "import flask, nmap, sqlalchemy" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances
        pause
        exit /b 1
    )
)

REM Vérifier si Nmap est installé
echo [INFO] Verification de Nmap...
nmap --version >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Nmap n'est pas detecte
    echo [INFO] Veuillez installer Nmap depuis https://nmap.org/download.html
    echo [INFO] L'application utilisera le mode fallback avec ping
    echo.
)

echo [INFO] Demarrage de l'application...
echo [INFO] Interface web disponible sur: http://localhost:5000
echo [INFO] Appuyez sur Ctrl+C pour arreter
echo.

REM Démarrer l'application
python app.py

echo.
echo [INFO] Application arretee
pause 