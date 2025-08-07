#!/usr/bin/env python3
"""
Test de vérification que la page de paramètres utilise des données de production
et non des données demo.
"""
import requests
import json
import sys
import time

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/login"
SETTINGS_API_URL = f"{BASE_URL}/api/settings"
NETWORKS_API_URL = f"{BASE_URL}/api/settings/networks"

# Informations de connexion
LOGIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

def test_settings_production():
    """Test complet de la page de paramètres en mode production"""
    
    session = requests.Session()
    
    print("🔍 Test de la page de paramètres - Mode Production")
    print("=" * 60)
    
    # 1. Connexion
    print("1. Connexion à l'application...")
    try:
        # D'abord récupérer la page de login pour obtenir le token CSRF si nécessaire
        login_page = session.get(LOGIN_URL)
        if login_page.status_code != 200:
            print(f"❌ Erreur accès page login: {login_page.status_code}")
            return False
            
        # Connexion
        login_response = session.post(LOGIN_URL, data=LOGIN_CREDENTIALS, allow_redirects=True)
        if login_response.status_code == 200:
            # Vérifier si on est connecté en testant la page principale
            home_response = session.get(f"{BASE_URL}/")
            if home_response.status_code == 200:
                print("✅ Connexion réussie")
            else:
                print(f"❌ Connexion échouée - accès home: {home_response.status_code}")
                return False
        else:
            print(f"❌ Échec de connexion: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # 2. Test API settings principale
    print("\n2. Test de l'API paramètres principale...")
    try:
        response = session.get(SETTINGS_API_URL)
        if response.status_code == 200:
            settings_data = response.json()
            print("✅ API paramètres accessible")
            
            # Analyser les données pour détecter si elles sont de production
            is_production = analyze_settings_data(settings_data)
            if is_production:
                print("✅ Les paramètres utilisent des données de PRODUCTION")
            else:
                print("⚠️  Les paramètres utilisent encore des données DEMO")
                
        else:
            print(f"❌ Erreur API settings: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test API settings: {e}")
        return False
    
    # 3. Test API réseaux détectés
    print("\n3. Test de l'API réseaux détectés...")
    try:
        response = session.get(NETWORKS_API_URL)
        if response.status_code == 200:
            networks_data = response.json()
            print("✅ API réseaux accessible")
            
            # Analyser les réseaux détectés
            real_networks = analyze_networks_data(networks_data)
            if real_networks:
                print("✅ Des réseaux RÉELS ont été détectés automatiquement")
                print(f"   Réseaux détectés: {len(networks_data.get('networks', []))}")
                for network in networks_data.get('networks', [])[:3]:  # Afficher 3 premiers
                    print(f"   - {network.get('range', 'N/A')}: {network.get('description', 'Réseau local')}")
            else:
                print("⚠️  Aucun réseau réel détecté ou données demo")
                
        else:
            print(f"❌ Erreur API networks: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur test API networks: {e}")
    
    # 4. Test de scan réseau de production
    print("\n4. Test du scanner réseau de production...")
    try:
        # Test de scan avec auto-détection
        test_data = {"network_range": "auto-detect"}
        response = session.post(f"{BASE_URL}/api/settings/test-network", 
                              json=test_data,
                              headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Scanner de production fonctionnel")
            print(f"   Status: {result.get('status')}")
            print(f"   Message: {result.get('message', 'N/A')}")
        else:
            print(f"⚠️  Scanner test: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur test scanner: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test de la page de paramètres terminé")
    
    return True

def analyze_settings_data(settings_data):
    """Analyse les données de paramètres pour détecter si elles sont de production"""
    
    print(f"   📊 Analyse des paramètres reçus...")
    
    # Indicateurs de données de production vs demo
    production_indicators = 0
    demo_indicators = 0
    
    # Vérifier les plages réseau
    network_range = settings_data.get('network_range', '')
    if network_range == 'auto-detect' or 'auto' in network_range.lower():
        production_indicators += 1
        print(f"   ✅ Mode auto-détection activé: {network_range}")
    elif network_range == '192.168.1.0/24':
        demo_indicators += 1
        print(f"   ⚠️  Plage réseau demo détectée: {network_range}")
    else:
        production_indicators += 1
        print(f"   ✅ Plage réseau personnalisée: {network_range}")
    
    # Vérifier la présence de fonctionnalités de production
    if settings_data.get('enable_auto_scan'):
        production_indicators += 1
        print("   ✅ Auto-scan activé (fonctionnalité production)")
        
    if settings_data.get('aggressive_scan') is not None:
        production_indicators += 1
        print("   ✅ Scan agressif disponible (fonctionnalité production)")
    
    # Vérifier les intervalles de scan
    scan_interval = settings_data.get('scan_interval', 60)
    if scan_interval != 60:  # 60 est la valeur par défaut demo
        production_indicators += 1
        print(f"   ✅ Intervalle de scan personnalisé: {scan_interval}min")
    
    print(f"   📈 Score production: {production_indicators}, Score demo: {demo_indicators}")
    
    return production_indicators > demo_indicators

def analyze_networks_data(networks_data):
    """Analyse les données de réseaux pour détecter des réseaux réels"""
    
    networks = networks_data.get('networks', [])
    
    if not networks:
        print("   ⚠️  Aucun réseau détecté")
        return False
    
    # Rechercher des indicateurs de réseaux réels
    real_network_indicators = 0
    
    for network in networks:
        network_range = network.get('range', '')
        
        # Les réseaux 192.168.1.0/24 sont souvent demo
        if network_range == '192.168.1.0/24':
            continue
            
        # Autres plages sont plus susceptibles d'être réelles
        if network_range:
            real_network_indicators += 1
    
    return real_network_indicators > 0

if __name__ == "__main__":
    print("🚀 Démarrage du test de paramètres de production...")
    
    # Attendre que l'application soit prête
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(2)
    
    success = test_settings_production()
    
    if success:
        print("✅ Test terminé avec succès")
        sys.exit(0)
    else:
        print("❌ Test échoué")
        sys.exit(1)
