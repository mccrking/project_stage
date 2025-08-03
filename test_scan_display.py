#!/usr/bin/env python3
"""
Script pour tester le scan et vérifier l'affichage des données
"""

import requests
import time
import json

def test_scan_and_display():
    """Test du scan et vérification de l'affichage"""
    print("🔍 TEST DU SCAN ET AFFICHAGE DES DONNÉES")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    try:
        # 1. Vérifier l'état initial
        print("📊 État initial du dashboard...")
        response = requests.get(f"{base_url}/", timeout=30)
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
        else:
            print(f"   ❌ Erreur dashboard: {response.status_code}")
            return
        
        # 2. Lancer un scan simple
        print("\n📡 Lancement d'un scan réseau...")
        scan_response = requests.post(f"{base_url}/api/scan", 
                                    json={'network_range': '192.168.0.0/24'},
                                    timeout=60)
        
        if scan_response.status_code == 200:
            scan_data = scan_response.json()
            print(f"   ✅ Scan lancé: {scan_data.get('message', 'N/A')}")
        else:
            print(f"   ❌ Erreur scan: {scan_response.status_code}")
            return
        
        # 3. Attendre que le scan se termine
        print("   ⏳ Attente de la fin du scan...")
        time.sleep(10)
        
        # 4. Vérifier les équipements détectés
        print("\n📱 Vérification des équipements détectés...")
        devices_response = requests.get(f"{base_url}/api/devices", timeout=30)
        
        if devices_response.status_code == 200:
            devices_data = devices_response.json()
            devices = devices_data.get('devices', [])
            
            print(f"   📊 {len(devices)} équipements détectés")
            
            if devices:
                print("\n📋 LISTE DES ÉQUIPEMENTS:")
                print("-" * 50)
                
                for i, device in enumerate(devices, 1):
                    ip = device.get('ip_address', 'N/A')
                    hostname = device.get('hostname', 'N/A')
                    device_type = device.get('device_type', 'Unknown')
                    status = device.get('status', 'unknown')
                    last_seen = device.get('last_seen', 'N/A')
                    
                    status_icon = "🟢" if status == 'online' else "🔴"
                    
                    print(f"{i}. {status_icon} {hostname} ({ip})")
                    print(f"   Type: {device_type}")
                    print(f"   Dernière vue: {last_seen}")
                    print()
                
                # 5. Vérifier les statistiques
                print("📈 Vérification des statistiques...")
                stats_response = requests.get(f"{base_url}/api/statistics", timeout=30)
                
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    print(f"   📊 Total équipements: {stats_data.get('total_devices', 0)}")
                    print(f"   🟢 En ligne: {stats_data.get('online_devices', 0)}")
                    print(f"   🔴 Hors ligne: {stats_data.get('offline_devices', 0)}")
                    print(f"   📊 Disponibilité: {stats_data.get('uptime_percentage', 0):.1f}%")
                else:
                    print(f"   ❌ Erreur statistiques: {stats_response.status_code}")
                
                # 6. Vérifier l'affichage dans le dashboard
                print("\n🌐 Vérification de l'affichage web...")
                dashboard_response = requests.get(f"{base_url}/", timeout=30)
                
                if dashboard_response.status_code == 200:
                    content = dashboard_response.text
                    
                    # Vérifier si les données sont présentes dans le HTML
                    if 'device-row' in content:
                        print("   ✅ Tableau des équipements présent dans le HTML")
                    else:
                        print("   ⚠️ Tableau des équipements non trouvé dans le HTML")
                    
                    if 'stat-number' in content:
                        print("   ✅ Statistiques présentes dans le HTML")
                    else:
                        print("   ⚠️ Statistiques non trouvées dans le HTML")
                    
                    if 'scan-history' in content:
                        print("   ✅ Historique des scans présent dans le HTML")
                    else:
                        print("   ⚠️ Historique des scans non trouvé dans le HTML")
                    
                else:
                    print(f"   ❌ Erreur dashboard: {dashboard_response.status_code}")
                
            else:
                print("   ⚠️ Aucun équipement détecté")
                print("   💡 Cela peut être normal si aucun appareil n'est connecté")
        
        else:
            print(f"   ❌ Erreur récupération équipements: {devices_response.status_code}")
        
        print("\n" + "=" * 60)
        print("✅ Test terminé!")
        print("🌐 Vérifiez le dashboard: http://localhost:5000")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Impossible de se connecter au serveur")
        print("   💡 Assurez-vous que l'application est démarrée")
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")

if __name__ == '__main__':
    test_scan_and_display() 