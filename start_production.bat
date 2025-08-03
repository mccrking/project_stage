@echo off
echo ========================================
echo   CENTRAL DANONE - MODE PRODUCTION
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances si nécessaire
echo 📦 Vérification des dépendances...
pip install -r requirements.txt

REM Nettoyer la base de données si demandé
echo.
echo 🧹 Voulez-vous nettoyer la base de données pour la production ?
echo    (supprimer les données de démonstration)
set /p clean_db="   Réponse (oui/non): "

if /i "%clean_db%"=="oui" (
    echo.
    echo 🗑️ Nettoyage de la base de données...
    python clean_production.py
    echo.
)

REM Démarrer l'application
echo 🚀 Démarrage de l'application Central Danone...
echo.
echo 📡 L'application sera accessible sur:
echo    http://localhost:5000
echo    http://192.168.0.104:5000
echo.
echo 🏭 MODE PRODUCTION - Central Danone
echo ========================================
echo.

python app.py

pause 