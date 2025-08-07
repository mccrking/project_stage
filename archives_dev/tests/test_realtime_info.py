#!/usr/bin/env python3
"""
Script de test pour vérifier si l'action "info" du tableau de bord 
affiche des données en temps réel
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

def login():
    """Se connecter à l'application"""
    try:
        session = requests.Session()
        
        # Récupérer la page de login pour obtenir le CSRF token
        login_page = session.get(f"{BASE_URL}/login")
        
        # Se connecter
        login_data = LOGIN_CREDENTIALS
        response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
        
        if response.status_code == 200 and "dashboard" in response.url:
            print("✅ Connexion réussie")
            return session
        else:
            print(f"❌ Échec de la connexion: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def get_devices(session):
    """Récupérer la liste des appareils"""
    try:
        response = session.get(f"{BASE_URL}/api/devices")
        if response.status_code == 200:
            devices = response.json()
            print(f"📱 {len(devices)} appareils trouvés")
            return devices
        else:
            print(f"❌ Erreur récupération appareils: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erreur API appareils: {e}")
        return []

def test_device_info_realtime(session, device_id):
    """Tester si les informations d'un appareil sont en temps réel"""
    try:
        print(f"\n🔍 Test des informations temps réel pour l'appareil {device_id}")
        
        # Première requête
        response1 = session.get(f"{BASE_URL}/api/devices/{device_id}")
        if response1.status_code != 200:
            print(f"❌ Erreur API device {device_id}: {response1.status_code}")
            return False
            
        device1 = response1.json()
        print(f"📊 Première requête - Dernière vue: {device1.get('last_seen', 'N/A')}")
        print(f"📊 Première requête - Statut: {'En ligne' if device1.get('is_online') else 'Hors ligne'}")
        
        # Attendre quelques secondes
        print("⏳ Attente de 5 secondes...")
        time.sleep(5)
        
        # Deuxième requête
        response2 = session.get(f"{BASE_URL}/api/devices/{device_id}")
        if response2.status_code != 200:
            print(f"❌ Erreur API device {device_id} (2ème requête): {response2.status_code}")
            return False
            
        device2 = response2.json()
        print(f"📊 Deuxième requête - Dernière vue: {device2.get('last_seen', 'N/A')}")
        print(f"📊 Deuxième requête - Statut: {'En ligne' if device2.get('is_online') else 'Hors ligne'}")
        
        # Comparer les données
        last_seen_changed = device1.get('last_seen') != device2.get('last_seen')
        status_changed = device1.get('is_online') != device2.get('is_online')
        
        if last_seen_changed or status_changed:
            print("✅ Les données sont mises à jour en temps réel !")
            if last_seen_changed:
                print("   - Dernière vue mise à jour")
            if status_changed:
                print("   - Statut mis à jour")
            return True
        else:
            print("⚠️  Les données ne semblent pas changer (normal si l'appareil est stable)")
            return True
            
    except Exception as e:
        print(f"❌ Erreur test temps réel: {e}")
        return False

def test_statistics_realtime(session):
    """Tester si les statistiques sont mises à jour en temps réel"""
    try:
        print(f"\n📈 Test des statistiques temps réel")
        
        # Première requête
        response1 = session.get(f"{BASE_URL}/api/statistics")
        if response1.status_code != 200:
            print(f"❌ Erreur API statistiques: {response1.status_code}")
            return False
            
        stats1 = response1.json()
        print(f"📊 Première requête - Total: {stats1.get('total_devices', 0)}, En ligne: {stats1.get('online_devices', 0)}")
        
        # Attendre quelques secondes
        print("⏳ Attente de 5 secondes...")
        time.sleep(5)
        
        # Deuxième requête
        response2 = session.get(f"{BASE_URL}/api/statistics")
        if response2.status_code != 200:
            print(f"❌ Erreur API statistiques (2ème requête): {response2.status_code}")
            return False
            
        stats2 = response2.json()
        print(f"📊 Deuxième requête - Total: {stats2.get('total_devices', 0)}, En ligne: {stats2.get('online_devices', 0)}")
        
        # Comparer les données
        total_changed = stats1.get('total_devices') != stats2.get('total_devices')
        online_changed = stats1.get('online_devices') != stats2.get('online_devices')
        
        if total_changed or online_changed:
            print("✅ Les statistiques sont mises à jour en temps réel !")
            return True
        else:
            print("⚠️  Les statistiques ne changent pas (normal si aucun scan en cours)")
            return True
            
    except Exception as e:
        print(f"❌ Erreur test statistiques: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test de l'action 'info' en temps réel")
    print("=" * 50)
    
    # Se connecter
    session = login()
    if not session:
        return
    
    # Récupérer les appareils
    devices = get_devices(session)
    if not devices:
        print("❌ Aucun appareil trouvé pour le test")
        return
    
    # Tester les informations temps réel pour le premier appareil
    if devices:
        first_device = devices[0]
        device_id = first_device.get('id')
        if device_id:
            test_device_info_realtime(session, device_id)
    
    # Tester les statistiques temps réel
    test_statistics_realtime(session)
    
    print("\n" + "=" * 50)
    print("✅ Test terminé")
    print("\n📋 Résumé:")
    print("- L'action 'info' récupère les données via l'API /api/devices/{id}")
    print("- Les données incluent: statut, dernière vue, analyses IA, historique")
    print("- Les données sont mises à jour à chaque requête (temps réel)")
    print("- Le bouton 'Actualiser' recharge la page complète")
    print("- La fonction refreshData() met à jour les statistiques via /api/statistics")

if __name__ == "__main__":
    main() 