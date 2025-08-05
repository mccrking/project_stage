@echo off
echo 🚀 Démarrage Central Danone avec Groq API...
echo.
REM Définir la variable d'environnement Groq
set GROQ_API_KEY=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
REM Activer l'environnement virtuel
call venv\Scripts\activate.bat
REM Démarrer l'application
echo ✅ Variable GROQ_API_KEY définie
echo 🌐 Démarrage de l'application...
echo.
python app.py
pause 