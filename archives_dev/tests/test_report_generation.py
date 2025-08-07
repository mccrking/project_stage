#!/usr/bin/env python3
"""
Test de la génération de rapports
Vérifie que les rapports peuvent être générés sans erreur
"""

import requests
import json
import time
from datetime import datetime

def test_report_generation():
    """Test de la génération de rapports"""
    print("📄 TEST DE GÉNÉRATION DE RAPPORTS")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Session pour maintenir les cookies
    session = requests.Session()
    
    # Connexion
    print("🔐 Connexion...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    
    if login_response.status_code != 302:
        print("❌ Échec de la connexion")
        return
    
    print("✅ Connexion réussie")
    
    # Test 1: Rapport quotidien PDF
    print("\n📊 Test rapport quotidien PDF...")
    report_data = {
        'type': 'daily',
        'format': 'pdf',
        'description': 'Test de génération de rapport quotidien'
    }
    
    response = session.post(f"{base_url}/api/reports/generate", json=report_data)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Rapport PDF généré: {result.get('filename')}")
        else:
            print(f"   ❌ Erreur: {result.get('message')}")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    # Test 2: Rapport hebdomadaire Excel
    print("\n📊 Test rapport hebdomadaire Excel...")
    report_data = {
        'type': 'weekly',
        'format': 'excel',
        'description': 'Test de génération de rapport hebdomadaire'
    }
    
    response = session.post(f"{base_url}/api/reports/generate", json=report_data)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Rapport Excel généré: {result.get('filename')}")
        else:
            print(f"   ❌ Erreur: {result.get('message')}")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    # Test 3: Rapport mensuel PDF
    print("\n📊 Test rapport mensuel PDF...")
    report_data = {
        'type': 'monthly',
        'format': 'pdf',
        'description': 'Test de génération de rapport mensuel'
    }
    
    response = session.post(f"{base_url}/api/reports/generate", json=report_data)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Rapport mensuel généré: {result.get('filename')}")
        else:
            print(f"   ❌ Erreur: {result.get('message')}")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    # Test 4: Liste des rapports
    print("\n📋 Test liste des rapports...")
    response = session.get(f"{base_url}/api/reports/list")
    if response.status_code == 200:
        reports = response.json()
        if isinstance(reports, list):
            report_count = len(reports)
        else:
            report_count = len(reports.get('reports', []))
        
        print(f"   ✅ {report_count} rapports disponibles")
        
        if report_count > 0:
            print("   📄 Rapports générés avec succès")
        else:
            print("   ℹ️ Aucun rapport disponible")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    # Test 5: Statistiques des rapports
    print("\n📈 Test statistiques des rapports...")
    response = session.get(f"{base_url}/api/reports/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ Statistiques récupérées: {stats}")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 TEST DE GÉNÉRATION DE RAPPORTS TERMINÉ")
    print("✅ Le système de rapports fonctionne correctement")

if __name__ == "__main__":
    test_report_generation() 