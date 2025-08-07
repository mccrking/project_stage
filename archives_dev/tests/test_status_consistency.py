#!/usr/bin/env python3
"""
Test pour vérifier la cohérence entre le statut dans le tableau et dans l'action info
"""

import requests
import json
from datetime import datetime

def test_status_consistency():
    """Test de cohérence entre le statut du tableau et l'action info"""
    
    # Configuration
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("=== Test de cohérence des statuts ===")
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
    
    # 2. Récupération de la liste des appareils
    print("\n2. Récupération de la liste des appareils...")
    try:
        response = session.get(f"{base_url}/api/devices")
        if response.status_code == 200:
            devices = response.json()
            print(f"✅ {len(devices)} appareils récupérés")
        else:
            print(f"❌ Erreur récupération appareils: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # 3. Vérification de la cohérence pour chaque appareil
    print("\n3. Vérification de la cohérence des statuts...")
    inconsistencies = 0
    
    for device in devices:
        device_id = device['id']
        table_status = device['is_online']
        
        # Récupérer les détails de l'appareil
        try:
            response = session.get(f"{base_url}/api/devices/{device_id}")
            if response.status_code == 200:
                device_details = response.json()
                info_status = device_details['is_online']
                
                if table_status != info_status:
                    inconsistencies += 1
                    print(f"   ❌ Incohérence détectée pour l'appareil {device['ip']}:")
                    print(f"      - Tableau: {'En ligne' if table_status else 'Hors ligne'}")
                    print(f"      - Info: {'En ligne' if info_status else 'Hors ligne'}")
                else:
                    print(f"   ✅ Cohérence OK pour {device['ip']}: {'En ligne' if table_status else 'Hors ligne'}")
            else:
                print(f"   ❌ Erreur récupération détails pour {device['ip']}: {response.status_code}")
                inconsistencies += 1
                
        except Exception as e:
            print(f"   ❌ Erreur pour {device['ip']}: {e}")
            inconsistencies += 1
    
    # 4. Résumé
    print(f"\n4. Résumé du test:")
    print(f"   - Appareils testés: {len(devices)}")
    print(f"   - Incohérences détectées: {inconsistencies}")
    
    if inconsistencies == 0:
        print("✅ Tous les statuts sont cohérents entre le tableau et l'action info!")
    else:
        print(f"❌ {inconsistencies} incohérence(s) détectée(s)")
    
    # 5. Test de l'API device details
    print("\n5. Test de l'API device details...")
    if devices:
        test_device = devices[0]
        print(f"   Test avec l'appareil: {test_device['ip']}")
        
        try:
            response = session.get(f"{base_url}/api/devices/{test_device['id']}")
            if response.status_code == 200:
                details = response.json()
                print(f"   ✅ Détails récupérés:")
                print(f"      - IP: {details.get('ip', 'N/A')}")
                print(f"      - Hostname: {details.get('hostname', 'N/A')}")
                print(f"      - MAC: {details.get('mac', 'N/A')}")
                print(f"      - Statut: {'En ligne' if details.get('is_online') else 'Hors ligne'}")
                print(f"      - Type: {details.get('device_type', 'N/A')}")
                print(f"      - Dernière vue: {details.get('last_seen', 'N/A')}")
            else:
                print(f"   ❌ Erreur API: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print("\n=== Test terminé ===")
    return inconsistencies == 0

if __name__ == "__main__":
    test_status_consistency() 