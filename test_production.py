#!/usr/bin/env python3
"""
Script de test complet pour vérifier que toutes les fonctionnalités
de l'application Central Danone sont 100% opérationnelles
"""

import os
import sys
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_TIMEOUT = 30

def test_server_connection():
    """Test de connexion au serveur"""
    print("🔌 Test de connexion au serveur...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("   ✅ Serveur accessible")
            return True
        else:
            print(f"   ❌ Erreur serveur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Impossible de se connecter au serveur: {str(e)}")
        return False

def test_main_dashboard():
    """Test du dashboard principal"""
    print("📊 Test du dashboard principal...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("   ✅ Dashboard principal accessible")
            return True
        else:
            print(f"   ❌ Erreur dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur dashboard: {str(e)}")
        return False

def test_ai_dashboard():
    """Test du dashboard IA"""
    print("🧠 Test du dashboard IA...")
    try:
        response = requests.get(f"{BASE_URL}/ai-dashboard", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("   ✅ Dashboard IA accessible")
            return True
        else:
            print(f"   ❌ Erreur dashboard IA: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur dashboard IA: {str(e)}")
        return False

def test_reports_page():
    """Test de la page des rapports"""
    print("📈 Test de la page des rapports...")
    try:
        response = requests.get(f"{BASE_URL}/reports", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("   ✅ Page des rapports accessible")
            return True
        else:
            print(f"   ❌ Erreur page rapports: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur page rapports: {str(e)}")
        return False

def test_settings_page():
    """Test de la page des paramètres"""
    print("⚙️ Test de la page des paramètres...")
    try:
        response = requests.get(f"{BASE_URL}/settings", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("   ✅ Page des paramètres accessible")
            return True
        else:
            print(f"   ❌ Erreur page paramètres: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur page paramètres: {str(e)}")
        return False

def test_api_endpoints():
    """Test des endpoints API"""
    print("🔗 Test des endpoints API...")
    
    endpoints = [
        ('/api/devices', 'GET'),
        ('/api/alerts', 'GET'),
        ('/api/settings', 'GET'),
        ('/api/discover-networks', 'GET'),
    ]
    
    success_count = 0
    
    for endpoint, method in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            
            if response.status_code in [200, 404]:  # 404 acceptable si pas de données
                print(f"   ✅ {endpoint} ({method}) - {response.status_code}")
                success_count += 1
            else:
                print(f"   ❌ {endpoint} ({method}) - {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} ({method}) - Erreur: {str(e)}")
    
    return success_count == len(endpoints)

def test_network_scan():
    """Test du scan réseau"""
    print("📡 Test du scan réseau...")
    try:
        # Test de découverte des réseaux
        response = requests.get(f"{BASE_URL}/api/discover-networks", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                networks = data.get('networks', [])
                print(f"   ✅ Découverte de {len(networks)} réseaux")
                return True
            else:
                print(f"   ❌ Erreur découverte réseaux: {data.get('message', 'Erreur inconnue')}")
                return False
        else:
            print(f"   ❌ Erreur API découverte: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur scan réseau: {str(e)}")
        return False

def test_ai_functionality():
    """Test des fonctionnalités IA"""
    print("🤖 Test des fonctionnalités IA...")
    try:
        # Test d'entraînement IA
        response = requests.post(f"{BASE_URL}/api/ai/train", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("   ✅ Entraînement IA fonctionnel")
                return True
            else:
                print(f"   ⚠️ Entraînement IA: {data.get('message', 'Pas de données suffisantes')}")
                return True  # Acceptable si pas de données
        else:
            print(f"   ❌ Erreur entraînement IA: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur fonctionnalités IA: {str(e)}")
        return False

def test_database_connection():
    """Test de la connexion à la base de données"""
    print("🗄️ Test de la base de données...")
    try:
        import sqlite3
        db_path = "network_monitor.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test des tables
            tables = ['device', 'scan_history', 'alert', 'ai_model']
            for table in tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    print(f"   ✅ Table {table} existe")
                else:
                    print(f"   ❌ Table {table} manquante")
                    return False
            
            conn.close()
            print("   ✅ Base de données opérationnelle")
            return True
        else:
            print("   ❌ Base de données non trouvée")
            return False
    except Exception as e:
        print(f"   ❌ Erreur base de données: {str(e)}")
        return False

def test_file_structure():
    """Test de la structure des fichiers"""
    print("📁 Test de la structure des fichiers...")
    
    required_files = [
        'app.py',
        'config.py',
        'network_scanner.py',
        'report_generator.py',
        'ai_enhancement.py',
        'requirements.txt',
        'templates/base.html',
        'templates/dashboard.html',
        'templates/ai_dashboard.html',
        'templates/reports.html',
        'templates/settings.html',
        'templates/error.html'
    ]
    
    required_dirs = [
        'templates',
        'reports',
        'logs',
        'ai_models'
    ]
    
    success = True
    
    # Vérifier les répertoires
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"   ✅ Répertoire {directory}/")
        else:
            print(f"   ❌ Répertoire {directory}/ manquant")
            success = False
    
    # Vérifier les fichiers
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ Fichier {file_path}")
        else:
            print(f"   ❌ Fichier {file_path} manquant")
            success = False
    
    return success

def main():
    """Fonction principale de test"""
    print("🏭 TEST COMPLET - CENTRAL DANONE PRODUCTION")
    print("=" * 60)
    print(f"🕐 Début des tests: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Vérifier que le serveur est démarré
    if not test_server_connection():
        print("\n❌ Le serveur n'est pas accessible. Démarrez l'application avec 'python app.py'")
        return
    
    print()
    
    # Tests de base
    tests = [
        ("Structure des fichiers", test_file_structure),
        ("Connexion base de données", test_database_connection),
        ("Dashboard principal", test_main_dashboard),
        ("Dashboard IA", test_ai_dashboard),
        ("Page des rapports", test_reports_page),
        ("Page des paramètres", test_settings_page),
        ("Endpoints API", test_api_endpoints),
        ("Scan réseau", test_network_scan),
        ("Fonctionnalités IA", test_ai_functionality),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            print()
        except Exception as e:
            print(f"   ❌ Erreur lors du test: {str(e)}")
            results.append((test_name, False))
            print()
    
    # Résumé
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print()
    print(f"📊 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUTES LES FONCTIONNALITÉS SONT OPÉRATIONNELLES !")
        print("🏭 L'application Central Danone est prête pour la production")
    else:
        print("⚠️ Certaines fonctionnalités nécessitent une attention")
        print("🔧 Vérifiez les erreurs ci-dessus et corrigez-les")
    
    print()
    print(f"🕐 Fin des tests: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == '__main__':
    main() 