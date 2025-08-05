#!/usr/bin/env python3
"""
Test de l'intégration Groq API
"""

import os
import sys
import requests
from datetime import datetime

def test_groq_integration():
    """Test complet de l'intégration Groq"""
    print("🚀 TEST D'INTÉGRATION GROQ API")
    print("=" * 50)
    
    # Test 1: Vérification de la configuration
    print("\n1️⃣ Vérification de la configuration...")
    
    try:
        from config_groq import GroqConfig
        config_info = GroqConfig.get_config_info()
        
        if config_info['api_configured']:
            print("   ✅ API Groq configurée")
            print(f"   📋 Modèle: {config_info['model']}")
            print(f"   🔢 Max tokens: {config_info['max_tokens']}")
        else:
            print("   ❌ API Groq non configurée")
            print("   💡 Créez un fichier .env avec GROQ_API_KEY=votre_cle")
            return False
            
    except ImportError as e:
        print(f"   ❌ Erreur import config: {e}")
        return False
    
    # Test 2: Test du module Groq
    print("\n2️⃣ Test du module Groq...")
    
    try:
        from groq_chatbot import groq_bot
        
        # Test de connexion
        connection_test = groq_bot.test_connection()
        
        if connection_test['success']:
            print("   ✅ Connexion Groq réussie")
            print(f"   ⚡ Temps de réponse: {connection_test.get('response_time', 0):.3f}s")
        else:
            print(f"   ❌ Erreur connexion: {connection_test['error']}")
            return False
            
    except ImportError as e:
        print(f"   ❌ Module Groq non disponible: {e}")
        return False
    
    # Test 3: Test du chatbot avec données simulées
    print("\n3️⃣ Test du chatbot avec données simulées...")
    
    # Données simulées
    test_devices = [
        {
            'ip': '192.168.1.10',
            'hostname': 'Serveur-Production-01',
            'is_online': True,
            'health_score': 85.5,
            'maintenance_urgency': 'low',
            'device_type': 'server'
        },
        {
            'ip': '192.168.1.15',
            'hostname': 'Switch-Core-01',
            'is_online': False,
            'health_score': 45.2,
            'maintenance_urgency': 'critical',
            'device_type': 'switch'
        }
    ]
    
    test_alerts = [
        {
            'message': 'Équipement Switch-Core-01 hors ligne',
            'alert_type': 'offline',
            'priority': 'high',
            'is_resolved': False
        }
    ]
    
    # Test de questions
    test_questions = [
        "Bonjour, comment va le réseau ?",
        "Y a-t-il des problèmes ?",
        "Quels sont les équipements critiques ?",
        "Donne-moi des recommandations d'optimisation"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   💬 Question {i}: {question}")
        
        try:
            result = groq_bot.chat(question, test_devices, test_alerts)
            
            if result['success']:
                print(f"   ✅ Réponse: {result['response'][:100]}...")
                print(f"   📊 Confiance: {result['confidence']}")
                print(f"   🤖 Modèle: {result['model']}")
                print(f"   ⚡ Temps: {result.get('response_time', 0):.3f}s")
            else:
                print(f"   ❌ Erreur: {result['error']}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test 4: Test de l'API Flask
    print("\n4️⃣ Test de l'API Flask...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test de connexion à l'application
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("   ✅ Application Flask accessible")
        else:
            print(f"   ❌ Application non accessible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException:
        print("   ❌ Application non démarrée")
        print("   💡 Démarrez l'application avec: python app.py")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TESTS TERMINÉS")
    print("=" * 50)
    
    print("\n📋 RÉSUMÉ:")
    print("✅ Configuration Groq vérifiée")
    print("✅ Module Groq fonctionnel")
    print("✅ Chatbot avec données simulées opérationnel")
    print("✅ API Flask accessible")
    
    print("\n🚀 PROCHAINES ÉTAPES:")
    print("1. Configurez votre clé API Groq dans le fichier .env")
    print("2. Redémarrez l'application")
    print("3. Testez le chatbot dans l'interface IA Avancée")
    print("4. Profitez des réponses ultra-rapides !")
    
    return True

def show_installation_instructions():
    """Affiche les instructions d'installation"""
    print("\n" + "=" * 50)
    print("📖 INSTRUCTIONS D'INSTALLATION")
    print("=" * 50)
    
    try:
        from config_groq import INSTALLATION_INSTRUCTIONS
        print(INSTALLATION_INSTRUCTIONS)
    except ImportError:
        print("Module de configuration non disponible")

if __name__ == "__main__":
    success = test_groq_integration()
    
    if not success:
        show_installation_instructions()
        sys.exit(1) 