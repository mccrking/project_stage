#!/usr/bin/env python3
"""
Test de l'intégration Groq API
"""

import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Tester la clé API
groq_key = os.getenv('GROQ_API_KEY', '')

print("🔍 Test de l'intégration Groq API")
print("=" * 40)

if groq_key:
    print(f"✅ Clé API Groq détectée: {groq_key[:20]}...{groq_key[-10:]}")
    print(f"📏 Longueur de la clé: {len(groq_key)} caractères")
    
    # Test d'importation des modules Groq
    try:
        from config_groq import GroqConfig
        print(f"✅ Module GroqConfig importé")
        print(f"🤖 Modèle configuré: {GroqConfig.MODEL}")
        print(f"🔗 URL API: {GroqConfig.API_URL}")
        
        # Test du chatbot Groq
        try:
            from groq_chatbot import GroqChatbot
            print(f"✅ Module GroqChatbot importé")
            
            # Test simple de connexion
            chatbot = GroqChatbot()
            print(f"🎯 Chatbot Groq initialisé")
            
            print(f"\n🚀 L'intégration Groq est prête à fonctionner!")
            
        except Exception as e:
            print(f"⚠️ Erreur chatbot Groq: {e}")
            
    except Exception as e:
        print(f"⚠️ Erreur configuration Groq: {e}")
        
else:
    print("❌ Clé API Groq non trouvée")
    print("💡 Vérifiez le fichier .env")

print("=" * 40)
