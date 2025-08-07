#!/usr/bin/env python3
"""
Script de test pour scanner le réseau domestique
et voir quels appareils sont détectés
"""

import requests
import json
import time

def test_home_network_scan():
    """Test du scan du réseau domestique"""
    print("🏠 TEST DU SCAN RÉSEAU DOMESTIQUE")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        # 1. Découvrir les réseaux disponibles
        print("🔍 Découverte des réseaux...")
        response = requests.get(f"{base_url}/api/discover-networks", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                networks = data.get('networks', [])
                print(f"   ✅ {len(networks)} réseaux détectés:")
                
                for i, network in enumerate(networks, 1):
                    print(f"      {i}. {network}")
                
                # 2. Scanner le réseau principal (probablement 192.168.1.0/24)
                print("\n📡 Scan du réseau principal...")
                scan_response = requests.post(f"{base_url}/api/scan", 
                                            json={'network_range': '192.168.1.0/24'},
                                            timeout=60)
                
                if scan_response.status_code == 200:
                    scan_data = scan_response.json()
                    if scan_data.get('success'):
                        print("   ✅ Scan terminé avec succès!")
                        print(f"   📊 Message: {scan_data.get('message', 'N/A')}")
                        
                        # 3. Récupérer la liste des appareils
                        print("\n📱 Récupération des appareils détectés...")
                        devices_response = requests.get(f"{base_url}/api/devices", timeout=30)
                        
                        if devices_response.status_code == 200:
                            devices_data = devices_response.json()
                            devices = devices_data.get('devices', [])
                            
                            if devices:
                                print(f"   ✅ {len(devices)} appareils détectés:")
                                print()
                                
                                for i, device in enumerate(devices, 1):
                                    status_icon = "🟢" if device.get('status') == 'online' else "🔴"
                                    device_type = device.get('device_type', 'Unknown')
                                    hostname = device.get('hostname', 'N/A')
                                    ip = device.get('ip_address', 'N/A')
                                    
                                    print(f"   {i}. {status_icon} {hostname}")
                                    print(f"      📍 IP: {ip}")
                                    print(f"      🏷️ Type: {device_type}")
                                    print(f"      📅 Dernière vue: {device.get('last_seen', 'N/A')}")
                                    print()
                            else:
                                print("   ⚠️ Aucun appareil détecté")
                        else:
                            print(f"   ❌ Erreur récupération appareils: {devices_response.status_code}")
                    else:
                        print(f"   ❌ Erreur scan: {scan_data.get('message', 'Erreur inconnue')}")
                else:
                    print(f"   ❌ Erreur scan: {scan_response.status_code}")
            else:
                print(f"   ❌ Erreur découverte réseaux: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Impossible de se connecter au serveur")
        print("   💡 Assurez-vous que l'application est démarrée avec 'python app.py'")
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")

def test_scan_all_networks():
    """Test du scan multi-réseaux"""
    print("\n🌐 TEST DU SCAN MULTI-RÉSEAUX")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        print("🚀 Lancement du scan multi-réseaux...")
        response = requests.post(f"{base_url}/api/scan-all-networks", timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("   ✅ Scan multi-réseaux lancé avec succès!")
                print(f"   📊 Message: {data.get('message', 'N/A')}")
                
                # Attendre un peu pour que le scan se termine
                print("   ⏳ Attente de la fin du scan...")
                time.sleep(10)
                
                # Récupérer les résultats
                devices_response = requests.get(f"{base_url}/api/devices", timeout=30)
                if devices_response.status_code == 200:
                    devices_data = devices_response.json()
                    devices = devices_data.get('devices', [])
                    
                    print(f"   📱 {len(devices)} appareils détectés au total:")
                    
                    # Grouper par réseau
                    networks = {}
                    for device in devices:
                        ip = device.get('ip_address', '')
                        network = '.'.join(ip.split('.')[:3]) + '.0/24' if ip else 'Unknown'
                        
                        if network not in networks:
                            networks[network] = []
                        networks[network].append(device)
                    
                    for network, network_devices in networks.items():
                        print(f"\n   🌐 Réseau {network}:")
                        for device in network_devices:
                            status_icon = "🟢" if device.get('status') == 'online' else "🔴"
                            hostname = device.get('hostname', 'N/A')
                            ip = device.get('ip_address', 'N/A')
                            device_type = device.get('device_type', 'Unknown')
                            
                            print(f"      {status_icon} {hostname} ({ip}) - {device_type}")
            else:
                print(f"   ❌ Erreur scan multi-réseaux: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")

def main():
    """Fonction principale"""
    print("🏠 CENTRAL DANONE - TEST RÉSEAU DOMESTIQUE")
    print("=" * 60)
    print("Ce script va scanner votre réseau domestique pour détecter")
    print("tous les appareils connectés (téléphones, PC, TV, etc.)")
    print()
    
    # Test du scan simple
    test_home_network_scan()
    
    # Test du scan multi-réseaux
    test_scan_all_networks()
    
    print("\n" + "=" * 60)
    print("✅ Test terminé!")
    print("🏠 Vous pouvez maintenant voir tous vos appareils domestiques")
    print("🌐 dans l'interface web: http://localhost:5000")

if __name__ == '__main__':
    main() 