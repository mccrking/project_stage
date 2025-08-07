#!/usr/bin/env python3
"""
Test simple de l'API Groq
"""

import requests
import json

def test_groq():
    print("🧪 TEST GROQ API")
    print("=" * 30)
    
    # Test 1: Vérifier que l'application fonctionne
    try:
        response = requests.get('http://localhost:5000/login', timeout=5)
        print(f"✅ Application accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Application non accessible: {e}")
        return
    
    # Test 2: Test du chatbot
    try:
        response = requests.post(
            'http://localhost:5000/api/ai-advanced/chatbot',
            json={'message': 'Bonjour'},
            timeout=10
        )
        print(f"✅ Chatbot accessible: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Réponse JSON valide")
                print(f"   Succès: {data.get('success', 'N/A')}")
                print(f"   Modèle: {data.get('model', 'N/A')}")
                print(f"   Réponse: {data.get('response', 'N/A')[:100]}...")
            except json.JSONDecodeError:
                print(f"❌ Réponse non-JSON: {response.text[:100]}")
        else:
            print(f"❌ Erreur HTTP: {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ Erreur chatbot: {e}")

if __name__ == "__main__":
    test_groq() 