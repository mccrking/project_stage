@echo off
echo 🚀 Démarrage Central Danone avec DeepSeek API...
echo.

REM Définir la variable d'environnement DeepSeek
set DEEPSEEK_API_KEY=sk-c8e1567f5c6c4caba8467d438d110e01

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Démarrer l'application
echo ✅ Variable DEEPSEEK_API_KEY définie
echo 🌐 Démarrage de l'application...
echo.
python app.py

pause 