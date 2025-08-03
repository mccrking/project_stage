@echo off
echo ========================================
echo   Serveur de Developpement Central Danone
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo 🔧 Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances si nécessaire
if not exist "venv\Lib\site-packages\flask" (
    echo 📦 Installation des dépendances...
    pip install -r requirements.txt
)

REM Installer watchdog pour l'auto-reload
pip install watchdog

echo.
echo 🚀 Démarrage du serveur de développement...
echo 📱 Interface web: http://localhost:5000
echo 👤 Connexion: admin / admin123
echo 🔄 Auto-reload activé - Modifications automatiques
echo ⏹️  Arrêt: Ctrl+C
echo.

REM Démarrer le serveur de développement
python dev_server.py

pause 