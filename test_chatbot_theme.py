#!/usr/bin/env python3
"""
Test du chatbot avec différents thèmes
"""

import requests
import time

def test_chatbot_theme():
    """Teste le chatbot avec le thème actuel"""
    print("🧪 TEST DU CHATBOT - THÈME")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # 1. Connexion
    print("\n1️⃣ Connexion...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = session.post(f"{base_url}/login", data=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print("   ❌ Échec de connexion")
        return
    
    # 2. Test du chatbot
    print("\n2️⃣ Test du chatbot...")
    test_messages = [
        "Bonjour, comment va le réseau ?",
        "Quels sont les équipements en ligne ?",
        "Y a-t-il des problèmes détectés ?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   💬 Message {i}: {message}")
        try:
            response = session.post(
                f"{base_url}/api/ai-advanced/chatbot",
                json={'message': message},
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        print(f"   ✅ Réponse: {data['response'][:100]}...")
                        print(f"   🤖 Modèle: {data.get('model', 'N/A')}")
                    else:
                        print(f"   ❌ Erreur: {data.get('error', 'Erreur inconnue')}")
                except:
                    print(f"   ⚠️  Réponse non-JSON: {response.text[:50]}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 40)
    print("✅ TEST TERMINÉ")
    print("\n📋 INSTRUCTIONS:")
    print("1. Ouvrez http://localhost:5000 dans votre navigateur")
    print("2. Connectez-vous avec admin/admin123")
    print("3. Cliquez sur le bouton robot en bas à droite")
    print("4. Testez le chatbot en mode clair et sombre")
    print("5. Vérifiez que le texte est visible dans les deux modes")

if __name__ == "__main__":
    test_chatbot_theme() 