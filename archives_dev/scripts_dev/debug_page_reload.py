#!/usr/bin/env python3
"""
Script de diagnostic pour le problème de réinitialisation de page
"""

import requests
import time
from datetime import datetime

def test_page_stability():
    """Teste la stabilité des pages"""
    print("🔍 DIAGNOSTIC DE STABILITÉ DES PAGES")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # 1. Connexion
    print("\n1️⃣ Test de connexion...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = session.post(f"{base_url}/login", data=login_data)
    print(f"   Status: {response.status_code}")
    print(f"   Cookies: {len(session.cookies)}")
    
    if response.status_code != 200:
        print("   ❌ Échec de connexion")
        return
    
    # 2. Test de la page dashboard
    print("\n2️⃣ Test de la page dashboard...")
    for i in range(5):
        start_time = time.time()
        response = session.get(f"{base_url}/")
        end_time = time.time()
        
        print(f"   Test {i+1}: Status {response.status_code}, Temps {end_time-start_time:.3f}s")
        
        if response.status_code != 200:
            print(f"   ❌ Erreur: {response.text[:100]}")
            break
        
        time.sleep(1)
    
    # 3. Test de la page IA Avancée
    print("\n3️⃣ Test de la page IA Avancée...")
    for i in range(5):
        start_time = time.time()
        response = session.get(f"{base_url}/ai-advanced")
        end_time = time.time()
        
        print(f"   Test {i+1}: Status {response.status_code}, Temps {end_time-start_time:.3f}s")
        
        if response.status_code != 200:
            print(f"   ❌ Erreur: {response.text[:100]}")
            break
        
        time.sleep(1)
    
    # 4. Test du chatbot
    print("\n4️⃣ Test du chatbot...")
    for i in range(3):
        start_time = time.time()
        response = session.post(
            f"{base_url}/api/ai-advanced/chatbot",
            json={'message': 'Test de stabilité'},
            timeout=10
        )
        end_time = time.time()
        
        print(f"   Test {i+1}: Status {response.status_code}, Temps {end_time-start_time:.3f}s")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Modèle: {data.get('model', 'N/A')}")
            except:
                print(f"   Réponse: {response.text[:50]}")
        
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("✅ DIAGNOSTIC TERMINÉ")

def check_server_status():
    """Vérifie le statut du serveur"""
    print("\n🔧 VÉRIFICATION DU SERVEUR")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:5000/login", timeout=5)
        print(f"✅ Serveur accessible: {response.status_code}")
        
        # Vérifier les headers
        print(f"📋 Headers:")
        for key, value in response.headers.items():
            if key.lower() in ['content-type', 'server', 'date']:
                print(f"   {key}: {value}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Serveur non accessible: {e}")

if __name__ == "__main__":
    check_server_status()
    test_page_stability() 