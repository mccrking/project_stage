#!/bin/bash
# Script de démarrage en mode production silencieux
# Réduit les logs pour un environnement de production

echo "🚀 Démarrage Dashboard Danone - Mode Production Silencieux"
echo "=========================================================="

# Définir l'environnement de production
export FLASK_ENV=production
export FLASK_DEBUG=0

# Démarrer l'application avec logs réduits
python app.py 2>&1 | grep -v "GET\|POST\|static\|304\|200"
