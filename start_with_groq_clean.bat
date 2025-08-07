@echo off
echo 🚀 Démarrage Central Danone avec Groq API...
echo.
echo ⚠️  IMPORTANT: Configurez votre clé API Groq
echo.
REM Définir la variable d'environnement Groq
REM Remplacez YOUR_API_KEY par votre vraie clé API Groq
set GROQ_API_KEY=YOUR_API_KEY_HERE
REM Activer l'environnement virtuel
call venv\Scripts\activate.bat
REM Démarrer l'application
echo ✅ Variable GROQ_API_KEY définie
echo 🌐 Démarrage de l'application...
echo.
python app.py
pause 