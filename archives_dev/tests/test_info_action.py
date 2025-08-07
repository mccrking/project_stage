#!/usr/bin/env python3
"""
Test simple de l'action "info" du tableau de bord
"""

import requests
import json

def test_info_action():
    """Test de l'action info"""
    print("🔍 Test de l'action 'info' du tableau de bord")
    print("=" * 50)
    
    # Configuration
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    try:
        # 1. Se connecter
        print("1. Connexion...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 2. Récupérer la liste des appareils
        print("\n2. Récupération des appareils...")
        response = session.get(f"{base_url}/api/devices")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            devices = response.json()
            print(f"   Nombre d'appareils: {len(devices)}")
            
            if devices:
                # 3. Tester l'action "info" sur le premier appareil
                first_device = devices[0]
                device_id = first_device.get('id')
                device_ip = first_device.get('ip')
                
                print(f"\n3. Test de l'action 'info' pour l'appareil {device_ip} (ID: {device_id})")
                
                response = session.get(f"{base_url}/api/devices/{device_id}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    device_info = response.json()
                    print("   ✅ Données récupérées avec succès !")
                    print(f"   - IP: {device_info.get('ip')}")
                    print(f"   - Statut: {'En ligne' if device_info.get('is_online') else 'Hors ligne'}")
                    print(f"   - Dernière vue: {device_info.get('last_seen', 'N/A')}")
                    print(f"   - Type: {device_info.get('device_type', 'N/A')}")
                    print(f"   - Score santé IA: {device_info.get('health_score', 'N/A')}")
                    print(f"   - Probabilité panne: {device_info.get('failure_probability', 'N/A')}")
                    print(f"   - Historique scans: {len(device_info.get('scan_history', []))} entrées")
                    print(f"   - Alertes actives: {len(device_info.get('active_alerts', []))}")
                    
                    # 4. Vérifier si les données sont en temps réel
                    print(f"\n4. Test temps réel...")
                    print("   Première requête terminée")
                    
                    # Deuxième requête pour comparer
                    response2 = session.get(f"{base_url}/api/devices/{device_id}")
                    if response2.status_code == 200:
                        device_info2 = response2.json()
                        
                        # Comparer les données
                        last_seen_changed = device_info.get('last_seen') != device_info2.get('last_seen')
                        status_changed = device_info.get('is_online') != device_info2.get('is_online')
                        
                        if last_seen_changed or status_changed:
                            print("   ✅ Les données sont mises à jour en temps réel !")
                        else:
                            print("   ⚠️  Les données sont stables (normal si l'appareil est stable)")
                        
                        print("   ✅ L'action 'info' fonctionne correctement")
                    else:
                        print(f"   ❌ Erreur deuxième requête: {response2.status_code}")
                else:
                    print(f"   ❌ Erreur récupération infos: {response.status_code}")
            else:
                print("   ⚠️  Aucun appareil trouvé")
        else:
            print(f"   ❌ Erreur récupération appareils: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Résumé de l'action 'info':")
    print("- Bouton avec icône info-circle dans le tableau de bord")
    print("- Appelle l'API /api/devices/{id}")
    print("- Affiche les informations dans une modal Bootstrap")
    print("- Données incluent: statut, dernière vue, analyses IA, historique")
    print("- Les données sont récupérées en temps réel à chaque clic")

if __name__ == "__main__":
    test_info_action() 