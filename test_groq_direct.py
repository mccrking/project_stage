#!/usr/bin/env python3
"""
Test direct de la nouvelle clé API Groq
"""

from dotenv import load_dotenv
load_dotenv()

from groq_chatbot import groq_bot

print("🔍 Test direct de la nouvelle clé API Groq")
print("=" * 50)

# Test de connexion
print("📡 Test de connexion à l'API...")
result = groq_bot.test_connection()

if result['success']:
    print("✅ SUCCÈS! La clé API Groq fonctionne!")
    print(f"📝 Message: {result.get('message', 'Connexion réussie')}")
    
    # Test d'un message simple
    print("\n🤖 Test d'un message simple...")
    chat_result = groq_bot.chat("Bonjour! Comment allez-vous?")
    
    if chat_result['success']:
        print("✅ SUCCÈS! Le chatbot Groq fonctionne!")
        print(f"🤖 Réponse: {chat_result['response'][:100]}...")
        print(f"🏷️ Modèle: {chat_result.get('model', 'N/A')}")
    else:
        print("❌ Erreur chatbot:", chat_result.get('error', 'Erreur inconnue'))
        
else:
    print("❌ ÉCHEC! Problème avec la clé API:")
    print(f"📝 Erreur: {result.get('error', 'Erreur inconnue')}")

print("=" * 50)
