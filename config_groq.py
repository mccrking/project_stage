#!/usr/bin/env python3
"""
Configuration Groq API
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class GroqConfig:
    """Configuration pour l'API Groq"""
    
    # Clé API Groq
    API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # URL de l'API
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # Modèle à utiliser (gratuit et rapide)
    MODEL = "llama3-8b-8192"  # Modèle gratuit et performant
    
    # Paramètres de génération
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Timeout pour les requêtes
    TIMEOUT = 30
    
    @classmethod
    def is_configured(cls) -> bool:
        """Vérifie si l'API est configurée"""
        return bool(cls.API_KEY)
    
    @classmethod
    def get_config_info(cls) -> dict:
        """Retourne les informations de configuration"""
        return {
            'api_configured': cls.is_configured(),
            'model': cls.MODEL,
            'max_tokens': cls.MAX_TOKENS,
            'temperature': cls.TEMPERATURE,
            'timeout': cls.TIMEOUT
        }

# Instructions d'installation
INSTALLATION_INSTRUCTIONS = """
🔧 CONFIGURATION GROQ API

1. Obtenez votre clé API GRATUITE :
   - Allez sur https://console.groq.com/
   - Créez un compte gratuit
   - Générez une nouvelle clé API

2. Configurez la clé API :
   - Créez un fichier .env dans le répertoire du projet
   - Ajoutez : GROQ_API_KEY=gsk_votre_cle_api_ici

3. Installez les dépendances :
   pip install -r requirements.txt

4. Testez la connexion :
   - Allez dans l'interface IA Avancée
   - Utilisez le bouton "Test Groq"

✅ Avantages de Groq :
- COMPLETEMENT GRATUIT
- Réponses ultra-rapides (millisecondes)
- Qualité élevée
- Pas de limite de solde
- Infrastructure fiable
""" 