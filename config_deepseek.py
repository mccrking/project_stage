#!/usr/bin/env python3
"""
Configuration DeepSeek API
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class DeepSeekConfig:
    """Configuration pour l'API DeepSeek"""
    
    # Clé API DeepSeek
    API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    
    # URL de l'API
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    # Modèle à utiliser
    MODEL = "deepseek-chat"
    
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
🔧 CONFIGURATION DEEPSEEK API

1. Obtenez votre clé API :
   - Allez sur https://platform.deepseek.com/
   - Créez un compte ou connectez-vous
   - Générez une nouvelle clé API

2. Configurez la clé API :
   - Créez un fichier .env dans le répertoire du projet
   - Ajoutez : DEEPSEEK_API_KEY=votre_cle_api_ici

3. Installez les dépendances :
   pip install -r requirements.txt

4. Testez la connexion :
   - Allez dans l'interface IA Avancée
   - Utilisez le bouton "Test DeepSeek"

✅ Avantages de DeepSeek :
- Réponses intelligentes et contextuelles
- Compréhension avancée du français
- Analyse des données réseau en temps réel
- Recommandations personnalisées
- Fallback automatique si l'API n'est pas disponible
""" 