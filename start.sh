#!/bin/bash

echo "========================================"
echo "  Central Danone - Supervision Reseau"
echo "========================================"
echo

echo "[INFO] Demarrage du systeme de supervision..."
echo "[INFO] Verification des dependances..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python3 n'est pas installe"
    echo "[INFO] Veuillez installer Python 3.8+"
    echo "       Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "       CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

# Vérifier si les dépendances sont installées
echo "[INFO] Verification des packages Python..."
python3 -c "import flask, nmap, sqlalchemy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Installation des dependances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Echec de l'installation des dependances"
        exit 1
    fi
fi

# Vérifier si Nmap est installé
echo "[INFO] Verification de Nmap..."
if ! command -v nmap &> /dev/null; then
    echo "[ATTENTION] Nmap n'est pas detecte"
    echo "[INFO] Veuillez installer Nmap:"
    echo "       Ubuntu/Debian: sudo apt-get install nmap"
    echo "       CentOS/RHEL: sudo yum install nmap"
    echo "[INFO] L'application utilisera le mode fallback avec ping"
    echo
fi

# Créer les dossiers nécessaires
mkdir -p reports
mkdir -p logs

echo "[INFO] Demarrage de l'application..."
echo "[INFO] Interface web disponible sur: http://localhost:5000"
echo "[INFO] Appuyez sur Ctrl+C pour arreter"
echo

# Démarrer l'application
python3 app.py

echo
echo "[INFO] Application arretee" 