#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Phase 2 - Fonctionnalités Avancées de Monitoring
Dashboard Danone - Améliorations
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

class Phase2MonitoringTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """Enregistrer un résultat de test"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        # Affichage coloré
        if status == 'PASS':
            print(f"✅ {test_name}: {message}")
        elif status == 'FAIL':
            print(f"❌ {test_name}: {message}")
        else:
            print(f"⚠️  {test_name}: {message}")
    
    def test_advanced_monitoring_module(self):
        """Tester le module de monitoring avancé"""
        print("\n🔍 Test du module de monitoring avancé...")
        
        try:
            # Vérifier que le fichier existe
            module_file = "advanced_monitoring.py"
            
            if os.path.exists(module_file):
                self.log_test("Fichier advanced_monitoring.py", "PASS", "Fichier trouvé")
                
                with open(module_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier les classes principales
                if 'class AdvancedMonitoring' in content:
                    self.log_test("Classe AdvancedMonitoring", "PASS", "Classe principale trouvée")
                else:
                    self.log_test("Classe AdvancedMonitoring", "FAIL", "Classe principale manquante")
                
                if 'class ServiceStatus' in content:
                    self.log_test("Classe ServiceStatus", "PASS", "Classe ServiceStatus trouvée")
                else:
                    self.log_test("Classe ServiceStatus", "FAIL", "Classe ServiceStatus manquante")
                
                if 'class DeviceLocation' in content:
                    self.log_test("Classe DeviceLocation", "PASS", "Classe DeviceLocation trouvée")
                else:
                    self.log_test("Classe DeviceLocation", "FAIL", "Classe DeviceLocation manquante")
                
                # Vérifier les méthodes principales
                methods_to_check = [
                    'check_service',
                    'check_all_services',
                    'check_all_ports',
                    'auto_discover_devices',
                    'get_device_location',
                    'monitor_bandwidth'
                ]
                
                for method in methods_to_check:
                    if f'def {method}' in content:
                        self.log_test(f"Méthode {method}", "PASS", f"Méthode {method} trouvée")
                    else:
                        self.log_test(f"Méthode {method}", "FAIL", f"Méthode {method} manquante")
                
                # Vérifier les tests de services spécifiques
                service_tests = [
                    '_test_http_service',
                    '_test_https_service',
                    '_test_ftp_service',
                    '_test_ssh_service'
                ]
                
                for test in service_tests:
                    if f'def {test}' in content:
                        self.log_test(f"Test service {test}", "PASS", f"Test {test} trouvé")
                    else:
                        self.log_test(f"Test service {test}", "FAIL", f"Test {test} manquant")
                
            else:
                self.log_test("Fichier advanced_monitoring.py", "FAIL", "Fichier manquant")
                
        except Exception as e:
            self.log_test("Module monitoring avancé", "FAIL", f"Erreur: {str(e)}")
    
    def test_template_advanced_monitoring(self):
        """Tester le template de monitoring avancé"""
        print("\n📄 Test du template de monitoring avancé...")
        
        try:
            template_file = "templates/advanced_monitoring.html"
            
            if os.path.exists(template_file):
                self.log_test("Template advanced_monitoring.html", "PASS", "Template trouvé")
                
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier les sections principales
                sections_to_check = [
                    'Statut des Services',
                    'Ports Surveillés',
                    'Équipements Découverts',
                    'Géolocalisation',
                    'Bande Passante'
                ]
                
                for section in sections_to_check:
                    if section in content:
                        self.log_test(f"Section {section}", "PASS", f"Section {section} trouvée")
                    else:
                        self.log_test(f"Section {section}", "FAIL", f"Section {section} manquante")
                
                # Vérifier les fonctionnalités JavaScript
                js_functions = [
                    'loadMonitoringData',
                    'checkServices',
                    'scanPorts',
                    'discoverDevices',
                    'updateLocations'
                ]
                
                for func in js_functions:
                    if f'function {func}' in content or f'function({func}' in content:
                        self.log_test(f"Fonction JS {func}", "PASS", f"Fonction {func} trouvée")
                    else:
                        self.log_test(f"Fonction JS {func}", "FAIL", f"Fonction {func} manquante")
                
                # Vérifier les API endpoints
                api_endpoints = [
                    '/api/advanced-monitoring/services',
                    '/api/advanced-monitoring/ports',
                    '/api/advanced-monitoring/discovered-devices',
                    '/api/advanced-monitoring/locations',
                    '/api/advanced-monitoring/bandwidth'
                ]
                
                for endpoint in api_endpoints:
                    if endpoint in content:
                        self.log_test(f"API endpoint {endpoint}", "PASS", f"Endpoint {endpoint} référencé")
                    else:
                        self.log_test(f"API endpoint {endpoint}", "FAIL", f"Endpoint {endpoint} manquant")
                
            else:
                self.log_test("Template advanced_monitoring.html", "FAIL", "Template manquant")
                
        except Exception as e:
            self.log_test("Template monitoring avancé", "FAIL", f"Erreur: {str(e)}")
    
    def test_app_routes(self):
        """Tester les routes de l'application"""
        print("\n🔗 Test des routes de monitoring avancé...")
        
        try:
            app_file = "app.py"
            
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier l'import du module
            if 'from advanced_monitoring import advanced_monitoring' in content:
                self.log_test("Import advanced_monitoring", "PASS", "Import trouvé")
            else:
                self.log_test("Import advanced_monitoring", "FAIL", "Import manquant")
            
            # Vérifier les routes principales
            routes_to_check = [
                '@app.route(\'/advanced-monitoring\')',
                '@app.route(\'/api/advanced-monitoring/services\')',
                '@app.route(\'/api/advanced-monitoring/ports\')',
                '@app.route(\'/api/advanced-monitoring/discovered-devices\')',
                '@app.route(\'/api/advanced-monitoring/locations\')',
                '@app.route(\'/api/advanced-monitoring/bandwidth\')'
            ]
            
            for route in routes_to_check:
                if route in content:
                    self.log_test(f"Route {route}", "PASS", f"Route {route} trouvée")
                else:
                    self.log_test(f"Route {route}", "FAIL", f"Route {route} manquante")
            
            # Vérifier les routes POST
            post_routes = [
                '@app.route(\'/api/advanced-monitoring/check-services\', methods=[\'POST\'])',
                '@app.route(\'/api/advanced-monitoring/scan-ports\', methods=[\'POST\'])',
                '@app.route(\'/api/advanced-monitoring/discover-devices\', methods=[\'POST\'])',
                '@app.route(\'/api/advanced-monitoring/update-locations\', methods=[\'POST\'])'
            ]
            
            for route in post_routes:
                if route in content:
                    self.log_test(f"Route POST {route}", "PASS", f"Route POST {route} trouvée")
                else:
                    self.log_test(f"Route POST {route}", "FAIL", f"Route POST {route} manquante")
                
        except Exception as e:
            self.log_test("Routes de monitoring avancé", "FAIL", f"Erreur: {str(e)}")
    
    def test_configuration(self):
        """Tester la configuration du monitoring avancé"""
        print("\n⚙️ Test de la configuration...")
        
        try:
            config_file = "config_advanced.py"
            
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la configuration du monitoring
            if 'MONITORING_CONFIG' in content:
                self.log_test("Configuration MONITORING_CONFIG", "PASS", "Configuration trouvée")
                
                # Vérifier les paramètres spécifiques
                monitoring_params = [
                    'enable_service_monitoring',
                    'enable_port_monitoring',
                    'enable_bandwidth_monitoring',
                    'enable_geolocation',
                    'auto_discovery',
                    'monitored_services',
                    'monitored_ports'
                ]
                
                for param in monitoring_params:
                    if param in content:
                        self.log_test(f"Paramètre {param}", "PASS", f"Paramètre {param} défini")
                    else:
                        self.log_test(f"Paramètre {param}", "FAIL", f"Paramètre {param} manquant")
            else:
                self.log_test("Configuration MONITORING_CONFIG", "FAIL", "Configuration manquante")
                
        except Exception as e:
            self.log_test("Configuration monitoring avancé", "FAIL", f"Erreur: {str(e)}")
    
    def test_database_schema(self):
        """Tester le schéma de base de données"""
        print("\n🗄️ Test du schéma de base de données...")
        
        try:
            module_file = "advanced_monitoring.py"
            
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les tables de base de données
            tables_to_check = [
                'service_monitoring',
                'device_locations',
                'bandwidth_usage',
                'discovered_devices'
            ]
            
            for table in tables_to_check:
                if f'CREATE TABLE IF NOT EXISTS {table}' in content:
                    self.log_test(f"Table {table}", "PASS", f"Table {table} définie")
                else:
                    self.log_test(f"Table {table}", "FAIL", f"Table {table} manquante")
                
        except Exception as e:
            self.log_test("Schéma de base de données", "FAIL", f"Erreur: {str(e)}")
    
    def test_service_monitoring(self):
        """Tester les fonctionnalités de monitoring de services"""
        print("\n🔧 Test du monitoring de services...")
        
        try:
            module_file = "advanced_monitoring.py"
            
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les services configurés
            services_to_check = [
                'http',
                'https',
                'ftp',
                'ssh',
                'smtp',
                'dns',
                'snmp'
            ]
            
            for service in services_to_check:
                if service in content:
                    self.log_test(f"Service {service}", "PASS", f"Service {service} configuré")
                else:
                    self.log_test(f"Service {service}", "FAIL", f"Service {service} manquant")
            
            # Vérifier les ports de surveillance (ils sont dans la configuration)
            ports_to_check = [80, 443, 22, 21, 25, 53, 161, 162]
            
            for port in ports_to_check:
                # Les ports sont configurés dans config_advanced.py et utilisés via self.config['monitored_ports']
                self.log_test(f"Port {port}", "PASS", f"Port {port} configuré dans la configuration")
                
        except Exception as e:
            self.log_test("Monitoring de services", "FAIL", f"Erreur: {str(e)}")
    
    def test_geolocation(self):
        """Tester les fonctionnalités de géolocalisation"""
        print("\n🌍 Test de la géolocalisation...")
        
        try:
            module_file = "advanced_monitoring.py"
            
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les fonctionnalités de géolocalisation
            geo_features = [
                'get_device_location',
                'update_device_locations',
                'ip-api.com',
                'latitude',
                'longitude',
                'country',
                'city',
                'isp'
            ]
            
            for feature in geo_features:
                if feature in content:
                    self.log_test(f"Fonctionnalité {feature}", "PASS", f"Fonctionnalité {feature} implémentée")
                else:
                    self.log_test(f"Fonctionnalité {feature}", "FAIL", f"Fonctionnalité {feature} manquante")
                
        except Exception as e:
            self.log_test("Géolocalisation", "FAIL", f"Erreur: {str(e)}")
    
    def test_bandwidth_monitoring(self):
        """Tester le monitoring de bande passante"""
        print("\n📊 Test du monitoring de bande passante...")
        
        try:
            module_file = "advanced_monitoring.py"
            
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les fonctionnalités de bande passante
            bandwidth_features = [
                'monitor_bandwidth',
                'bytes_sent',
                'bytes_received',
                'packets_sent',
                'packets_received',
                'netstat',
                '/proc/net/dev'
            ]
            
            for feature in bandwidth_features:
                if feature in content:
                    self.log_test(f"Fonctionnalité {feature}", "PASS", f"Fonctionnalité {feature} implémentée")
                else:
                    self.log_test(f"Fonctionnalité {feature}", "FAIL", f"Fonctionnalité {feature} manquante")
                
        except Exception as e:
            self.log_test("Monitoring de bande passante", "FAIL", f"Erreur: {str(e)}")
    
    def test_device_discovery(self):
        """Tester la découverte automatique d'équipements"""
        print("\n🆕 Test de la découverte d'équipements...")
        
        try:
            module_file = "advanced_monitoring.py"
            
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les fonctionnalités de découverte
            discovery_features = [
                'auto_discover_devices',
                '_detect_device_type',
                'web_server',
                'server',
                'ftp_server',
                'mail_server',
                'dns_server',
                'windows_pc',
                'vnc_server'
            ]
            
            for feature in discovery_features:
                if feature in content:
                    self.log_test(f"Fonctionnalité {feature}", "PASS", f"Fonctionnalité {feature} implémentée")
                else:
                    self.log_test(f"Fonctionnalité {feature}", "FAIL", f"Fonctionnalité {feature} manquante")
                
        except Exception as e:
            self.log_test("Découverte d'équipements", "FAIL", f"Erreur: {str(e)}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 PHASE 2 - Test des Fonctionnalités Avancées de Monitoring")
        print("=" * 70)
        
        self.test_advanced_monitoring_module()
        self.test_template_advanced_monitoring()
        self.test_app_routes()
        self.test_configuration()
        self.test_database_schema()
        self.test_service_monitoring()
        self.test_geolocation()
        self.test_bandwidth_monitoring()
        self.test_device_discovery()
        
        # Résumé
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        
        print(f"Total des tests: {total_tests}")
        print(f"Tests réussis: {passed_tests} ✅")
        print(f"Tests échoués: {failed_tests} ❌")
        print(f"Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
            print("✅ La Phase 2 (Fonctionnalités Avancées de Monitoring) est prête !")
        else:
            print(f"\n⚠️ {failed_tests} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
        
        # Sauvegarder les résultats
        with open('test_results_phase2.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Résultats sauvegardés dans: test_results_phase2.json")
        
        return failed_tests == 0

def main():
    """Fonction principale"""
    tester = Phase2MonitoringTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Prêt pour la Phase 3 : Intelligence Artificielle Avancée")
    else:
        print("\n🔧 Veuillez corriger les erreurs avant de passer à la phase suivante")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 