#!/usr/bin/env python3
"""
Démarrage rapide en mode développement
"""

import os
import sys
import subprocess

def main():
    print("🚀 Démarrage rapide - Mode développement")
    print("=" * 40)
    
    # Vérifier si l'environnement virtuel existe
    if not os.path.exists("venv"):
        print("🔧 Création de l'environnement virtuel...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Activer l'environnement virtuel et démarrer
    if os.name == 'nt':  # Windows
        print("🔄 Activation de l'environnement virtuel...")
        subprocess.run(["venv\\Scripts\\activate.bat", "&&", "python", "app.py"], shell=True)
    else:  # Linux/Mac
        print("🔄 Activation de l'environnement virtuel...")
        subprocess.run(["source", "venv/bin/activate", "&&", "python", "app.py"], shell=True)

if __name__ == "__main__":
    main() 