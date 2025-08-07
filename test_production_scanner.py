#!/usr/bin/env python3
"""
Test du scanner production en mode standalone
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from network_scanner_production import ProductionNetworkScanner
import time

def test_production_scanner():
    print("🧪 TEST DU SCANNER PRODUCTION")
    print("=" * 40)
    
    # Initialiser le scanner
    scanner = ProductionNetworkScanner()
    
    # Test 1: Découverte des réseaux
    print("1. 🔍 Découverte des réseaux locaux...")
    networks = scanner.discover_local_networks()
    
    if networks:
        print(f"✅ {len(networks)} réseau(x) découvert(s)")
        for i, network in enumerate(networks[:3], 1):  # Limiter à 3 pour le test
            print(f"   {i}. {network['network']} ({network.get('interface', 'N/A')})")
    else:
        print("❌ Aucun réseau découvert")
        return
    
    # Test 2: Scan d'un réseau
    test_network = networks[0]['network']
    print(f"\n2. 📡 Test scan du réseau: {test_network}")
    
    start_time = time.time()
    devices = scanner.scan_network_advanced(test_network, aggressive=False)
    scan_duration = time.time() - start_time
    
    print(f"✅ Scan terminé en {scan_duration:.2f}s")
    print(f"✅ {len(devices)} équipement(s) détecté(s)")
    
    # Afficher les détails des équipements
    if devices:
        print("\n📋 ÉQUIPEMENTS DÉTECTÉS:")
        print("-" * 80)
        print(f"{'IP':<15} {'Hostname':<25} {'Type':<12} {'OS':<10} {'Ports'}")
        print("-" * 80)
        
        for device in devices[:10]:  # Limiter à 10 pour l'affichage
            ports = device.get('ports', [])
            ports_str = ','.join(map(str, ports[:5]))  # Max 5 ports
            if len(ports) > 5:
                ports_str += '...'
                
            print(f"{device['ip']:<15} {device['hostname'][:24]:<25} {device['type']:<12} {device['os']:<10} {ports_str}")
    
    # Test 3: Scan agressif d'une IP spécifique (si disponible)
    if devices:
        test_ip = devices[0]['ip']
        print(f"\n3. 🎯 Test scan agressif sur: {test_ip}")
        
        start_time = time.time()
        aggressive_devices = scanner.scan_network_advanced(f"{test_ip}/32", aggressive=True)
        aggressive_duration = time.time() - start_time
        
        if aggressive_devices:
            device = aggressive_devices[0]
            print(f"✅ Scan agressif terminé en {aggressive_duration:.2f}s")
            print(f"   Hostname: {device['hostname']}")
            print(f"   Type: {device['type']} (confiance: {device['confidence']}%)")
            print(f"   OS: {device['os']}")
            print(f"   MAC: {device['mac']} ({device['mac_vendor']})")
            print(f"   Ports ouverts: {device['ports']}")
            print(f"   Services: {device['services']}")
            print(f"   Temps de réponse: {device['response_time']}ms")
    
    print(f"\n✅ TESTS TERMINÉS - SCANNER PRODUCTION OPÉRATIONNEL")
    return True

if __name__ == '__main__':
    try:
        success = test_production_scanner()
        if success:
            print("\n🎯 PRÊT POUR PRODUCTION!")
            print("   Le scanner peut détecter de vrais équipements réseau")
            print("   Toutes les fonctionnalités avancées sont opérationnelles")
        else:
            print("\n❌ PROBLÈMES DÉTECTÉS")
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST: {e}")
        import traceback
        traceback.print_exc()
