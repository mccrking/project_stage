@echo off
echo ========================================
echo   Central Danone - Supervision Reseau
echo   Version Production avec Authentification
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo Python detecte: 
python --version
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ERREUR: Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre à jour pip
echo Mise a jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
echo Installation des dependances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dependances
    pause
    exit /b 1
)

REM Créer les répertoires nécessaires
echo Creation des repertoires...
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs
if not exist "ai_models" mkdir ai_models

echo.
echo ========================================
echo   DEMARRAGE DE L'APPLICATION
echo ========================================
echo.
echo Identifiants par defaut:
echo   Admin: admin / admin123
echo   Technicien: technicien / tech123
echo.
echo URL: http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

REM Démarrer l'application
python app.py

pause 