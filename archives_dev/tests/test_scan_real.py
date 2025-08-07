#!/usr/bin/env python3
"""
TEST SCAN RÉEL - Central Danone Dashboard
Vérification de la détection réelle des appareils sur le réseau
"""

import socket
import subprocess
import platform
import time
from datetime import datetime

def test_scan_real():
    """Test de détection réelle des appareils"""
    print("🔍 TEST SCAN RÉEL - DÉTECTION DES APPAREILS")
    print("=" * 60)
    print(f"⏰ Début du test : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. DÉTECTION RÉSEAU LOCAL
    print("1️⃣ DÉTECTION RÉSEAU LOCAL")
    print("-" * 30)
    
    try:
        # Obtenir l'IP locale
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"   Nom d'hôte: {hostname}")
        print(f"   IP locale: {local_ip}")
        
        # Détecter le réseau
        ip_parts = local_ip.split('.')
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        print(f"   Réseau détecté: {network}")
        
    except Exception as e:
        print(f"   ❌ Erreur détection réseau: {str(e)}")
        return False
    print()
    
    # 2. TEST PING LOCAL
    print("2️⃣ TEST PING LOCAL")
    print("-" * 30)
    
    # Tester l'hôte local
    if platform.system().lower() == "windows":
        ping_cmd = [r'C:\Windows\System32\ping.exe', '-n', '1', '-w', '1000', '127.0.0.1']
    else:
        ping_cmd = ['ping', '-c', '1', '-W', '1', '127.0.0.1']
    
    try:
        result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ Ping local réussi")
        else:
            print("   ❌ Ping local échoué")
    except Exception as e:
        print(f"   ❌ Erreur ping local: {str(e)}")
    print()
    
    # 3. SCAN RÉSEAU RAPIDE
    print("3️⃣ SCAN RÉSEAU RAPIDE")
    print("-" * 30)
    
    base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
    devices_found = []
    
    # Scanner les adresses courantes
    common_addresses = [
        f"{base_ip}.1",   # Routeur
        f"{base_ip}.2",   # PC
        f"{base_ip}.10",  # Serveur
        f"{base_ip}.100", # Téléphone
        f"{base_ip}.254", # Broadcast
        local_ip         # Votre PC
    ]
    
    for ip in common_addresses:
        start_time = time.time()
        
        if platform.system().lower() == "windows":
            ping_cmd = [r'C:\Windows\System32\ping.exe', '-n', '1', '-w', '500', ip]
        else:
            ping_cmd = ['ping', '-c', '1', '-W', '1', ip]
        
        try:
            result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=2)
            end_time = time.time()
            
            if result.returncode == 0:
                # Essayer de récupérer le nom d'hôte
                hostname = "Unknown"
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    pass
                
                device_info = {
                    'ip': ip,
                    'hostname': hostname,
                    'response_time': f"{end_time-start_time:.3f}s",
                    'status': 'Online'
                }
                devices_found.append(device_info)
                print(f"   ✅ {ip} ({hostname}) - {end_time-start_time:.3f}s")
            else:
                print(f"   ❌ {ip} - Pas de réponse")
                
        except Exception as e:
            print(f"   ❌ {ip} - Erreur: {str(e)}")
    
    print()
    
    # 4. SCAN COMPLET RÉSEAU
    print("4️⃣ SCAN COMPLET RÉSEAU")
    print("-" * 30)
    
    print("   🔍 Scan en cours... (peut prendre quelques secondes)")
    all_devices = []
    
    # Scanner toutes les adresses du réseau
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        
        if platform.system().lower() == "windows":
            ping_cmd = [r'C:\Windows\System32\ping.exe', '-n', '1', '-w', '200', ip]
        else:
            ping_cmd = ['ping', '-c', '1', '-W', '1', ip]
        
        try:
            result = subprocess.run(ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
            
            if result.returncode == 0:
                # Essayer de récupérer le nom d'hôte
                hostname = "Unknown"
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    pass
                
                device_info = {
                    'ip': ip,
                    'hostname': hostname,
                    'status': 'Online'
                }
                all_devices.append(device_info)
                print(f"   ✅ {ip} ({hostname})")
                
        except:
            pass
    
    print()
    
    # 5. ANALYSE RÉSULTATS
    print("5️⃣ ANALYSE RÉSULTATS")
    print("-" * 30)
    
    print(f"   Appareils détectés: {len(all_devices)}")
    print(f"   Votre PC ({local_ip}): {'✅ Détecté' if any(d['ip'] == local_ip for d in all_devices) else '❌ Non détecté'}")
    
    # Analyser les types d'appareils
    device_types = {}
    for device in all_devices:
        hostname = device['hostname'].lower()
        
        if any(keyword in hostname for keyword in ['router', 'gateway', 'modem']):
            device_types['Router'] = device_types.get('Router', 0) + 1
        elif any(keyword in hostname for keyword in ['pc', 'desktop', 'laptop', 'computer']):
            device_types['PC'] = device_types.get('PC', 0) + 1
        elif any(keyword in hostname for keyword in ['phone', 'mobile', 'android', 'iphone']):
            device_types['Téléphone'] = device_types.get('Téléphone', 0) + 1
        elif any(keyword in hostname for keyword in ['server', 'srv']):
            device_types['Serveur'] = device_types.get('Serveur', 0) + 1
        else:
            device_types['Autre'] = device_types.get('Autre', 0) + 1
    
    print("   Répartition par type:")
    for device_type, count in device_types.items():
        print(f"      {device_type}: {count}")
    
    print()
    
    # 6. RÉSUMÉ FINAL
    print("🎯 RÉSUMÉ FINAL - SCAN RÉEL")
    print("=" * 60)
    print(f"⏰ Fin du test : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if len(all_devices) > 0:
        print("✅ DÉTECTION RÉSEAU FONCTIONNELLE")
        print(f"✅ {len(all_devices)} appareils détectés")
        print("✅ Votre PC est détecté" if any(d['ip'] == local_ip for d in all_devices) else "⚠️ Votre PC n'est pas détecté")
        print("✅ Scan complet réussi")
    else:
        print("❌ AUCUN APPAREIL DÉTECTÉ")
        print("❌ Problème de configuration réseau")
        print("❌ Vérifiez les paramètres de pare-feu")
    
    print()
    print("🔧 RECOMMANDATIONS:")
    if len(all_devices) == 0:
        print("   - Vérifiez que le pare-feu autorise les pings")
        print("   - Vérifiez la configuration réseau")
        print("   - Testez avec une adresse IP spécifique")
    elif len(all_devices) < 3:
        print("   - Peu d'appareils détectés, vérifiez le réseau")
        print("   - Certains appareils peuvent être masqués")
    else:
        print("   - Détection réseau fonctionnelle")
        print("   - Le système est prêt pour la production")

if __name__ == "__main__":
    test_scan_real() 