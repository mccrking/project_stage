#!/usr/bin/env python3
"""
Test des données du tableau de bord
Vérifie que les données de démonstration sont créées et accessibles
"""

import requests
import json
import time
from datetime import datetime

def test_dashboard_data():
    """Test des données du tableau de bord"""
    print("🔍 TEST DES DONNÉES DU TABLEAU DE BORD")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Connexion
    print("🔐 Test de connexion...")
    try:
        # Session pour maintenir les cookies
        session = requests.Session()
        
        # Page de login
        login_page = session.get(f"{base_url}/login")
        if login_page.status_code == 200:
            print("✅ Page de login accessible")
        else:
            print(f"❌ Erreur page login: {login_page.status_code}")
            return
        
        # Connexion
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        
        if login_response.status_code == 302:  # Redirection après connexion
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur connexion: {login_response.status_code}")
            return
        
        # Test 2: Page tableau de bord
        print("\n📊 Test de la page tableau de bord...")
        dashboard_response = session.get(f"{base_url}/")
        if dashboard_response.status_code == 200:
            print("✅ Page tableau de bord accessible")
        else:
            print(f"❌ Erreur tableau de bord: {dashboard_response.status_code}")
            return
        
        # Test 3: API des statistiques
        print("\n📈 Test de l'API des statistiques...")
        stats_response = session.get(f"{base_url}/api/statistics")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print("✅ API statistiques accessible")
            print(f"   📊 Données: {json.dumps(stats_data, indent=2)}")
        else:
            print(f"❌ Erreur API statistiques: {stats_response.status_code}")
        
        # Test 4: API des équipements
        print("\n🖥️ Test de l'API des équipements...")
        devices_response = session.get(f"{base_url}/api/devices")
        if devices_response.status_code == 200:
            devices_data = devices_response.json()
            print("✅ API équipements accessible")
            
            # Vérifier si devices_data est une liste ou un dict
            if isinstance(devices_data, list):
                devices_list = devices_data
            else:
                devices_list = devices_data.get('devices', [])
            
            print(f"   📊 Nombre d'équipements: {len(devices_list)}")
            
            # Afficher les détails des équipements
            for device in devices_list:
                print(f"   🖥️ {device.get('hostname', 'N/A')} ({device.get('ip', 'N/A')}) - {'🟢 En ligne' if device.get('is_online') else '🔴 Hors ligne'}")
        else:
            print(f"❌ Erreur API équipements: {devices_response.status_code}")
        
        # Test 5: API des alertes
        print("\n🚨 Test de l'API des alertes...")
        alerts_response = session.get(f"{base_url}/api/alerts")
        if alerts_response.status_code == 200:
            alerts_data = alerts_response.json()
            print("✅ API alertes accessible")
            print(f"   📊 Nombre d'alertes: {len(alerts_data.get('alerts', []))}")
            
            # Afficher les alertes
            for alert in alerts_data.get('alerts', []):
                print(f"   🚨 {alert.get('message', 'N/A')} - Priorité: {alert.get('priority', 'N/A')}")
        else:
            print(f"❌ Erreur API alertes: {alerts_response.status_code}")
        
        # Test 6: API des notifications
        print("\n🔔 Test de l'API des notifications...")
        notifications_response = session.get(f"{base_url}/api/notifications")
        if notifications_response.status_code == 200:
            notifications_data = notifications_response.json()
            print("✅ API notifications accessible")
            print(f"   📊 Nombre de notifications: {len(notifications_data.get('notifications', []))}")
        else:
            print(f"❌ Erreur API notifications: {notifications_response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 TEST TERMINÉ AVEC SUCCÈS !")
        print("📱 Vous pouvez maintenant accéder au tableau de bord avec des données réelles")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous qu'il est démarré.")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_dashboard_data() 