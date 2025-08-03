#!/usr/bin/env python3
"""
Script de test pour l'authentification Central Danone
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/"

def test_login():
    """Test de connexion"""
    print("🔐 Test de connexion...")
    
    # Test avec des identifiants valides
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        # Créer une session
        session = requests.Session()
        
        # Tentative de connexion
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
        
        if response.status_code == 302:  # Redirection après connexion réussie
            print("✅ Connexion réussie avec admin/admin123")
            
            # Tester l'accès au dashboard
            dashboard_response = session.get(DASHBOARD_URL)
            if dashboard_response.status_code == 200:
                print("✅ Accès au dashboard autorisé")
                return True
            else:
                print("❌ Accès au dashboard refusé")
                return False
        else:
            print(f"❌ Échec de connexion (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")
        return False

def test_invalid_login():
    """Test avec des identifiants invalides"""
    print("\n🔐 Test avec identifiants invalides...")
    
    login_data = {
        'username': 'invalid',
        'password': 'wrong'
    }
    
    try:
        session = requests.Session()
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
        
        if response.status_code == 200:  # Reste sur la page de connexion
            print("✅ Connexion refusée avec des identifiants invalides")
            return True
        else:
            print(f"❌ Comportement inattendu (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_protected_routes():
    """Test des routes protégées"""
    print("\n🔒 Test des routes protégées...")
    
    protected_routes = [
        '/',
        '/alerts',
        '/reports',
        '/settings',
        '/ai-dashboard',
        '/api/devices',
        '/api/statistics'
    ]
    
    try:
        # Test sans authentification
        session = requests.Session()
        
        for route in protected_routes:
            response = session.get(f"{BASE_URL}{route}", allow_redirects=False)
            
            if response.status_code == 302:  # Redirection vers login
                print(f"✅ Route {route} protégée (redirection vers login)")
            else:
                print(f"❌ Route {route} non protégée (Status: {response.status_code})")
                
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des routes: {e}")
        return False

def test_technician_login():
    """Test de connexion avec un technicien"""
    print("\n👨‍💼 Test de connexion technicien...")
    
    login_data = {
        'username': 'technicien',
        'password': 'tech123'
    }
    
    try:
        session = requests.Session()
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
        
        if response.status_code == 302:
            print("✅ Connexion technicien réussie")
            
            # Tester l'accès au dashboard
            dashboard_response = session.get(DASHBOARD_URL)
            if dashboard_response.status_code == 200:
                print("✅ Accès technicien au dashboard autorisé")
                return True
            else:
                print("❌ Accès technicien au dashboard refusé")
                return False
        else:
            print(f"❌ Échec de connexion technicien (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test technicien: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test du système d'authentification Central Danone")
    print("=" * 50)
    
    # Attendre que l'application démarre
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(3)
    
    # Tests
    tests = [
        test_login,
        test_invalid_login,
        test_protected_routes,
        test_technician_login
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests réussis: {passed}/{total}")
    print(f"Taux de réussite: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 Tous les tests d'authentification sont passés !")
        print("✅ Le système d'authentification fonctionne correctement")
    else:
        print("⚠️ Certains tests ont échoué")
        print("🔧 Vérifiez la configuration de l'application")

if __name__ == "__main__":
    main() 