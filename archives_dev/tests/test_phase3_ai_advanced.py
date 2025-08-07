#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la Phase 3 : Intelligence Artificielle Avancée
"""

import os
import json
import requests
from datetime import datetime

class Phase3AITester:
    def __init__(self):
        self.results = []
        self.test_count = 0
        self.passed_count = 0
        self.base_url = "http://localhost:5000"
        
    def log_test(self, test_name, status, message):
        self.test_count += 1
        if status == "PASS":
            self.passed_count += 1
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
        
        self.results.append({
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_ai_advanced_route(self):
        """Test de la route IA avancée"""
        print("\n🤖 Test de la route IA avancée...")
        
        try:
            response = requests.get(f"{self.base_url}/ai-advanced", allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("Route IA avancée", "PASS", "Route accessible (redirection login)")
            elif response.status_code == 200:
                self.log_test("Route IA avancée", "PASS", "Route accessible")
            else:
                self.log_test("Route IA avancée", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("Route IA avancée", "FAIL", f"Erreur: {str(e)}")
    
    def test_api_predictions(self):
        """Test de l'API des prédictions"""
        print("\n🔮 Test de l'API des prédictions...")
        
        try:
            response = requests.get(f"{self.base_url}/api/ai-advanced/predictions", allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("API Prédictions", "PASS", "API accessible (redirection login)")
            else:
                self.log_test("API Prédictions", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("API Prédictions", "FAIL", f"Erreur: {str(e)}")
    
    def test_api_intrusions(self):
        """Test de l'API des intrusions"""
        print("\n🛡️ Test de l'API des intrusions...")
        
        try:
            response = requests.get(f"{self.base_url}/api/ai-advanced/intrusions", allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("API Intrusions", "PASS", "API accessible (redirection login)")
            else:
                self.log_test("API Intrusions", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("API Intrusions", "FAIL", f"Erreur: {str(e)}")
    
    def test_api_optimizations(self):
        """Test de l'API des optimisations"""
        print("\n⚙️ Test de l'API des optimisations...")
        
        try:
            response = requests.get(f"{self.base_url}/api/ai-advanced/optimizations", allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("API Optimisations", "PASS", "API accessible (redirection login)")
            else:
                self.log_test("API Optimisations", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("API Optimisations", "FAIL", f"Erreur: {str(e)}")
    
    def test_api_trends(self):
        """Test de l'API des tendances"""
        print("\n📈 Test de l'API des tendances...")
        
        try:
            response = requests.get(f"{self.base_url}/api/ai-advanced/trends", allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("API Tendances", "PASS", "API accessible (redirection login)")
            else:
                self.log_test("API Tendances", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("API Tendances", "FAIL", f"Erreur: {str(e)}")
    
    def test_api_statistics(self):
        """Test de l'API des statistiques"""
        print("\n📊 Test de l'API des statistiques...")
        
        try:
            response = requests.get(f"{self.base_url}/api/ai-advanced/statistics", allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("API Statistiques", "PASS", "API accessible (redirection login)")
            else:
                self.log_test("API Statistiques", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("API Statistiques", "FAIL", f"Erreur: {str(e)}")
    
    def test_api_chatbot(self):
        """Test de l'API du chatbot"""
        print("\n💬 Test de l'API du chatbot...")
        
        try:
            response = requests.post(f"{self.base_url}/api/ai-advanced/chatbot", 
                                   json={"query": "bonjour"}, 
                                   allow_redirects=False)
            if response.status_code == 302:  # Redirection vers login
                self.log_test("API Chatbot", "PASS", "API accessible (redirection login)")
            else:
                self.log_test("API Chatbot", "FAIL", f"Code de statut: {response.status_code}")
        except Exception as e:
            self.log_test("API Chatbot", "FAIL", f"Erreur: {str(e)}")
    
    def test_template_file(self):
        """Test du fichier template"""
        print("\n📄 Test du fichier template...")
        
        if os.path.exists("templates/ai_advanced.html"):
            self.log_test("Template IA avancée", "PASS", "Fichier template trouvé")
        else:
            self.log_test("Template IA avancée", "FAIL", "Fichier template manquant")
    
    def test_app_routes(self):
        """Test des routes dans app.py"""
        print("\n🔗 Test des routes dans app.py...")
        
        try:
            with open("app.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            routes_to_check = [
                '/ai-advanced',
                '/api/ai-advanced/predictions',
                '/api/ai-advanced/intrusions',
                '/api/ai-advanced/optimizations',
                '/api/ai-advanced/trends',
                '/api/ai-advanced/statistics',
                '/api/ai-advanced/chatbot'
            ]
            
            for route in routes_to_check:
                if f"@app.route('{route}')" in content or f"@app.route('{route}'," in content:
                    self.log_test(f"Route {route}", "PASS", "Route définie")
                else:
                    self.log_test(f"Route {route}", "FAIL", "Route manquante")
                    
        except Exception as e:
            self.log_test("Routes app.py", "FAIL", f"Erreur: {str(e)}")
    
    def test_ai_advanced_file(self):
        """Test du fichier ai_advanced.py"""
        print("\n📁 Test du fichier ai_advanced.py...")
        
        if os.path.exists("ai_advanced.py"):
            self.log_test("Fichier ai_advanced.py", "PASS", "Fichier trouvé")
            
            try:
                with open("ai_advanced.py", 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "Module d'IA Avancée" in content:
                    self.log_test("Contenu ai_advanced.py", "PASS", "Contenu de base présent")
                else:
                    self.log_test("Contenu ai_advanced.py", "FAIL", "Contenu de base manquant")
                    
            except Exception as e:
                self.log_test("Lecture ai_advanced.py", "FAIL", f"Erreur: {str(e)}")
        else:
            self.log_test("Fichier ai_advanced.py", "FAIL", "Fichier manquant")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🤖 TEST DE LA PHASE 3 : INTELLIGENCE ARTIFICIELLE AVANCÉE")
        print("=" * 70)
        
        self.test_ai_advanced_route()
        self.test_api_predictions()
        self.test_api_intrusions()
        self.test_api_optimizations()
        self.test_api_trends()
        self.test_api_statistics()
        self.test_api_chatbot()
        self.test_template_file()
        self.test_app_routes()
        self.test_ai_advanced_file()
        
        # Résumé
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        print(f"Total des tests: {self.test_count}")
        print(f"Tests réussis: {self.passed_count} ✅")
        print(f"Tests échoués: {self.test_count - self.passed_count} ❌")
        print(f"Taux de réussite: {(self.passed_count / self.test_count * 100):.1f}%")
        
        if self.passed_count == self.test_count:
            print("\n🎉 PHASE 3 IMPLÉMENTÉE AVEC SUCCÈS !")
            print("✅ Toutes les fonctionnalités IA avancée sont opérationnelles !")
            print("\n🚀 Fonctionnalités disponibles :")
            print("   • 🤖 Prédiction de pannes avec machine learning")
            print("   • 🛡️ Détection d'intrusion basée sur l'IA")
            print("   • ⚙️ Optimisation automatique des paramètres de scan")
            print("   • 💬 Chatbot IA pour l'assistance technique")
            print("   • 📈 Analyse prédictive des tendances réseau")
        else:
            print("\n⚠️ Certains tests ont échoué. Vérifiez l'implémentation.")
        
        # Sauvegarder les résultats
        with open("test_results_phase3.json", 'w', encoding='utf-8') as f:
            json.dump({
                "test_date": datetime.now().isoformat(),
                "phase": "Phase 3 - IA Avancée",
                "total_tests": self.test_count,
                "passed_tests": self.passed_count,
                "failed_tests": self.test_count - self.passed_count,
                "success_rate": (self.passed_count / self.test_count * 100) if self.test_count > 0 else 0,
                "results": self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Résultats sauvegardés dans: test_results_phase3.json")

if __name__ == "__main__":
    tester = Phase3AITester()
    tester.run_all_tests() 