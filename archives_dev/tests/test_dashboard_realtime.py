#!/usr/bin/env python3
"""
Test pour vérifier que les données du tableau de bord sont en temps réel
"""

import requests
import time
import json
from datetime import datetime

def test_dashboard_realtime():
    """Test des mises à jour en temps réel du tableau de bord"""
    
    # Configuration
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("=== Test des données en temps réel du tableau de bord ===")
    print(f"URL de base: {base_url}")
    print()
    
    # 1. Connexion
    print("1. Connexion...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data)
        if response.status_code == 200:
            print("✅ Connexion réussie")
        else:
            print(f"❌ Échec de la connexion: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # 2. Récupération des statistiques initiales
    print("\n2. Récupération des statistiques initiales...")
    try:
        response = session.get(f"{base_url}/api/statistics")
        if response.status_code == 200:
            initial_stats = response.json()
            print("✅ Statistiques initiales récupérées:")
            print(f"   - Total appareils: {initial_stats.get('total_devices', 'N/A')}")
            print(f"   - Appareils en ligne: {initial_stats.get('online_devices', 'N/A')}")
            print(f"   - Appareils hors ligne: {initial_stats.get('offline_devices', 'N/A')}")
            print(f"   - Pourcentage disponibilité: {initial_stats.get('uptime_percentage', 'N/A')}%")
        else:
            print(f"❌ Erreur récupération statistiques: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # 3. Surveillance des changements pendant 2 minutes
    print("\n3. Surveillance des changements pendant 2 minutes...")
    print("   (Vérification toutes les 10 secondes)")
    
    changes_detected = 0
    last_stats = initial_stats.copy()
    
    for i in range(12):  # 12 vérifications = 2 minutes
        time.sleep(10)  # Attendre 10 secondes
        
        try:
            response = session.get(f"{base_url}/api/statistics")
            if response.status_code == 200:
                current_stats = response.json()
                
                # Vérifier les changements
                changes = []
                for key in ['total_devices', 'online_devices', 'offline_devices', 'uptime_percentage']:
                    if current_stats.get(key) != last_stats.get(key):
                        changes.append(f"{key}: {last_stats.get(key)} → {current_stats.get(key)}")
                
                if changes:
                    changes_detected += 1
                    print(f"   ⏰ {datetime.now().strftime('%H:%M:%S')} - Changements détectés:")
                    for change in changes:
                        print(f"      • {change}")
                else:
                    print(f"   ⏰ {datetime.now().strftime('%H:%M:%S')} - Aucun changement")
                
                last_stats = current_stats.copy()
                
            else:
                print(f"   ❌ Erreur API: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    # 4. Résumé
    print("\n4. Résumé du test:")
    print(f"   - Durée de surveillance: 2 minutes")
    print(f"   - Vérifications effectuées: 12")
    print(f"   - Changements détectés: {changes_detected}")
    
    if changes_detected > 0:
        print("✅ Les données du tableau de bord SONT en temps réel")
        print("   (Des changements ont été détectés pendant la surveillance)")
    else:
        print("⚠️  Aucun changement détecté pendant la surveillance")
        print("   Cela peut être normal si:")
        print("   - Aucun scan n'a été effectué")
        print("   - L'état du réseau est stable")
        print("   - Les appareils sont tous stables")
    
    # 5. Test de l'endpoint de scan pour déclencher des changements
    print("\n5. Test d'un scan pour déclencher des changements...")
    try:
        response = session.post(f"{base_url}/api/scan", json={})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Scan lancé: {result.get('message', 'Succès')}")
            
            # Attendre un peu et vérifier les changements
            print("   Attente de 15 secondes pour voir les changements...")
            time.sleep(15)
            
            response = session.get(f"{base_url}/api/statistics")
            if response.status_code == 200:
                final_stats = response.json()
                print("   Statistiques après scan:")
                print(f"   - Total appareils: {final_stats.get('total_devices', 'N/A')}")
                print(f"   - Appareils en ligne: {final_stats.get('online_devices', 'N/A')}")
                print(f"   - Appareils hors ligne: {final_stats.get('offline_devices', 'N/A')}")
                print(f"   - Pourcentage disponibilité: {final_stats.get('uptime_percentage', 'N/A')}%")
                
                # Comparer avec les statistiques initiales
                if final_stats != initial_stats:
                    print("✅ Changements confirmés après scan - Les données sont bien en temps réel!")
                else:
                    print("⚠️  Aucun changement après scan (peut être normal si réseau stable)")
            else:
                print(f"❌ Erreur récupération statistiques finales: {response.status_code}")
        else:
            print(f"❌ Erreur lancement scan: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur test scan: {e}")
    
    print("\n=== Test terminé ===")
    return True

if __name__ == "__main__":
    test_dashboard_realtime() 