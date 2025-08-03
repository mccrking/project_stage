#!/usr/bin/env python3
"""
Test Final Complet - Dashboard Danone
Vérifie que toutes les améliorations fonctionnent correctement
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
AI_DASHBOARD_URL = f"{BASE_URL}/ai-dashboard"
ALERTS_URL = f"{BASE_URL}/alerts"
REPORTS_URL = f"{BASE_URL}/reports"
SETTINGS_URL = f"{BASE_URL}/settings"

class TestFinalComplet:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Enregistre le résultat d'un test"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        print(f"{status} {test_name}: {message}")
        
    def test_application_running(self):
        """Test 1: Vérifie que l'application est en cours d'exécution"""
        try:
            response = self.session.get(BASE_URL, allow_redirects=False)
            # Devrait rediriger vers /login
            success = response.status_code == 302 and '/login' in response.headers.get('Location', '')
            self.log_test("Application en cours d'exécution", success, 
                         f"Status: {response.status_code}, Redirect: {response.headers.get('Location', 'N/A')}")
            return success
        except Exception as e:
            self.log_test("Application en cours d'exécution", False, f"Erreur: {e}")
            return False
            
    def test_authentication_system(self):
        """Test 2: Vérifie le système d'authentification"""
        try:
            # Test de connexion avec admin
            login_data = {
                'username': 'admin',
                'password': 'admin'
            }
            response = self.session.post(LOGIN_URL, data=login_data, allow_redirects=False)
            success = response.status_code == 302
            self.log_test("Authentification admin", success, f"Status: {response.status_code}")
            
            if success:
                # Test d'accès au dashboard
                response = self.session.get(DASHBOARD_URL, allow_redirects=False)
                success_dashboard = response.status_code == 200
                self.log_test("Accès dashboard après connexion", success_dashboard, f"Status: {response.status_code}")
                
                return success and success_dashboard
            return False
        except Exception as e:
            self.log_test("Authentification", False, f"Erreur: {e}")
            return False
            
    def test_dashboard_realtime(self):
        """Test 3: Vérifie les fonctionnalités temps réel du dashboard"""
        try:
            # Test API statistiques
            response = self.session.get(f"{BASE_URL}/api/statistics")
            success_stats = response.status_code == 200
            self.log_test("API statistiques", success_stats, f"Status: {response.status_code}")
            
            if success_stats:
                data = response.json()
                has_required_fields = all(key in data for key in ['total_devices', 'online_devices', 'offline_devices'])
                self.log_test("Champs requis statistiques", has_required_fields, 
                             f"Champs trouvés: {list(data.keys())}")
                
            # Test API équipements
            response = self.session.get(f"{BASE_URL}/api/devices")
            success_devices = response.status_code == 200
            self.log_test("API équipements", success_devices, f"Status: {response.status_code}")
            
            return success_stats and success_devices
        except Exception as e:
            self.log_test("Dashboard temps réel", False, f"Erreur: {e}")
            return False
            
    def test_ai_dashboard(self):
        """Test 4: Vérifie le dashboard IA"""
        try:
            # Test page IA
            response = self.session.get(AI_DASHBOARD_URL, allow_redirects=False)
            success_page = response.status_code == 200
            self.log_test("Page IA Dashboard", success_page, f"Status: {response.status_code}")
            
            # Test API IA statistiques
            response = self.session.get(f"{BASE_URL}/api/ai/stats")
            success_stats = response.status_code == 200
            self.log_test("API IA statistiques", success_stats, f"Status: {response.status_code}")
            
            # Test API graphiques IA
            response = self.session.get(f"{BASE_URL}/api/ai/chart-data")
            success_charts = response.status_code == 200
            self.log_test("API graphiques IA", success_charts, f"Status: {response.status_code}")
            
            return success_page and success_stats and success_charts
        except Exception as e:
            self.log_test("Dashboard IA", False, f"Erreur: {e}")
            return False
            
    def test_alerts_system(self):
        """Test 5: Vérifie le système d'alertes"""
        try:
            # Test page alertes
            response = self.session.get(ALERTS_URL, allow_redirects=False)
            success_page = response.status_code == 200
            self.log_test("Page Alertes", success_page, f"Status: {response.status_code}")
            
            # Test API alertes
            response = self.session.get(f"{BASE_URL}/api/alerts")
            success_api = response.status_code == 200
            self.log_test("API Alertes", success_api, f"Status: {response.status_code}")
            
            # Test API statistiques alertes
            response = self.session.get(f"{BASE_URL}/api/alerts/stats")
            success_stats = response.status_code == 200
            self.log_test("API statistiques alertes", success_stats, f"Status: {response.status_code}")
            
            return success_page and success_api and success_stats
        except Exception as e:
            self.log_test("Système d'alertes", False, f"Erreur: {e}")
            return False
            
    def test_reports_system(self):
        """Test 6: Vérifie le système de rapports"""
        try:
            # Test page rapports
            response = self.session.get(REPORTS_URL, allow_redirects=False)
            success_page = response.status_code == 200
            self.log_test("Page Rapports", success_page, f"Status: {response.status_code}")
            
            # Test API liste rapports
            response = self.session.get(f"{BASE_URL}/api/reports/list")
            success_list = response.status_code == 200
            self.log_test("API liste rapports", success_list, f"Status: {response.status_code}")
            
            # Test génération rapport
            report_data = {
                'report_type': 'journalier',
                'format': 'pdf'
            }
            response = self.session.post(f"{BASE_URL}/api/reports/generate", json=report_data)
            success_generate = response.status_code == 200
            self.log_test("Génération rapport", success_generate, f"Status: {response.status_code}")
            
            return success_page and success_list and success_generate
        except Exception as e:
            self.log_test("Système de rapports", False, f"Erreur: {e}")
            return False
            
    def test_settings_persistence(self):
        """Test 7: Vérifie la persistance des paramètres"""
        try:
            # Test page paramètres
            response = self.session.get(SETTINGS_URL, allow_redirects=False)
            success_page = response.status_code == 200
            self.log_test("Page Paramètres", success_page, f"Status: {response.status_code}")
            
            # Test API paramètres
            response = self.session.get(f"{BASE_URL}/api/settings")
            success_get = response.status_code == 200
            self.log_test("API récupération paramètres", success_get, f"Status: {response.status_code}")
            
            if success_get:
                data = response.json()
                has_settings = 'network' in data and 'alerts' in data and 'reports' in data
                self.log_test("Structure paramètres", has_settings, f"Sections: {list(data.keys())}")
                
            # Test sauvegarde paramètres réseau
            network_settings = {
                'subnet': '192.168.1.0/24',
                'scan_interval': 300
            }
            response = self.session.post(f"{BASE_URL}/api/settings/network", json=network_settings)
            success_save = response.status_code == 200
            self.log_test("Sauvegarde paramètres réseau", success_save, f"Status: {response.status_code}")
            
            return success_page and success_get and success_save
        except Exception as e:
            self.log_test("Persistance paramètres", False, f"Erreur: {e}")
            return False
            
    def test_file_structure(self):
        """Test 8: Vérifie la structure des fichiers"""
        required_files = [
            'app.py',
            'settings_manager.py',
            'login.html',
            'change_password.html',
            'templates/dashboard.html',
            'templates/ai_dashboard.html',
            'templates/alerts.html',
            'templates/reports.html',
            'templates/settings.html',
            'requirements.txt'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                
        success = len(missing_files) == 0
        self.log_test("Structure fichiers", success, 
                     f"Fichiers manquants: {missing_files if missing_files else 'Aucun'}")
        return success
        
    def test_dependencies(self):
        """Test 9: Vérifie les dépendances"""
        try:
            import flask
            import flask_login
            import sqlalchemy
            import nmap
            import fpdf2
            import openpyxl
            import chart.js
            
            self.log_test("Dépendances Python", True, "Toutes les dépendances sont installées")
            return True
        except ImportError as e:
            self.log_test("Dépendances Python", False, f"Dépendance manquante: {e}")
            return False
            
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 TEST FINAL COMPLET - DASHBOARD DANONE")
        print("=" * 50)
        
        tests = [
            ("Application en cours d'exécution", self.test_application_running),
            ("Système d'authentification", self.test_authentication_system),
            ("Dashboard temps réel", self.test_dashboard_realtime),
            ("Dashboard IA", self.test_ai_dashboard),
            ("Système d'alertes", self.test_alerts_system),
            ("Système de rapports", self.test_reports_system),
            ("Persistance paramètres", self.test_settings_persistence),
            ("Structure fichiers", self.test_file_structure),
            ("Dépendances", self.test_dependencies)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 Test: {test_name}")
            try:
                result = test_func()
                results.append(result)
            except Exception as e:
                print(f"❌ ERREUR: {e}")
                results.append(False)
                
        # Résumé final
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS FINAUX")
        print("=" * 50)
        
        passed = sum(results)
        total = len(results)
        percentage = (passed / total) * 100 if total > 0 else 0
        
        print(f"✅ Tests réussis: {passed}/{total}")
        print(f"📈 Pourcentage de réussite: {percentage:.1f}%")
        
        if percentage >= 90:
            print("🏆 EXCELLENT! Le projet est prêt pour la production!")
        elif percentage >= 80:
            print("✅ BON! Quelques ajustements mineurs nécessaires.")
        elif percentage >= 70:
            print("⚠️ MOYEN! Des améliorations sont nécessaires.")
        else:
            print("❌ PROBLÈME! Des corrections majeures sont nécessaires.")
            
        # Détail des tests
        print("\n📋 Détail des tests:")
        for i, (test_name, _) in enumerate(tests):
            status = "✅" if results[i] else "❌"
            print(f"  {status} {test_name}")
            
        return percentage >= 90

if __name__ == "__main__":
    tester = TestFinalComplet()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 FÉLICITATIONS! Votre projet Danone est 100% fonctionnel!")
    else:
        print("\n🔧 Des améliorations sont encore nécessaires.") 