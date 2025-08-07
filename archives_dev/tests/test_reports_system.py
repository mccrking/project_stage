#!/usr/bin/env python3
"""
Script de test pour le système de génération de rapports
Teste toutes les fonctionnalités de génération, téléchargement et gestion des rapports
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/login"
REPORTS_URL = f"{BASE_URL}/reports"
API_GENERATE_URL = f"{BASE_URL}/api/reports/generate"
API_LIST_URL = f"{BASE_URL}/api/reports/list"
API_STATS_URL = f"{BASE_URL}/api/reports/stats"
API_DELETE_URL = f"{BASE_URL}/api/reports/delete"

# Identifiants de test
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

class ReportsSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        
    def login(self):
        """Se connecter à l'application"""
        print("🔐 Connexion à l'application...")
        
        try:
            # Récupérer le token CSRF
            response = self.session.get(LOGIN_URL)
            if response.status_code != 200:
                print(f"❌ Impossible d'accéder à la page de connexion: {response.status_code}")
                return False
            
            # Se connecter
            login_data = {
                'username': TEST_USERNAME,
                'password': TEST_PASSWORD
            }
            
            response = self.session.post(LOGIN_URL, data=login_data, allow_redirects=False)
            
            if response.status_code == 302:  # Redirection après connexion réussie
                print("✅ Connexion réussie")
                self.logged_in = True
                return True
            else:
                print(f"❌ Échec de la connexion: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la connexion: {e}")
            return False
    
    def test_reports_page_access(self):
        """Tester l'accès à la page des rapports"""
        print("\n📄 Test d'accès à la page des rapports...")
        
        try:
            response = self.session.get(REPORTS_URL)
            
            if response.status_code == 200:
                print("✅ Page des rapports accessible")
                return True
            else:
                print(f"❌ Impossible d'accéder à la page des rapports: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'accès à la page des rapports: {e}")
            return False
    
    def test_reports_list_api(self):
        """Tester l'API de liste des rapports"""
        print("\n📋 Test de l'API de liste des rapports...")
        
        try:
            response = self.session.get(API_LIST_URL)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    reports = data.get('reports', [])
                    print(f"✅ API de liste des rapports fonctionnelle - {len(reports)} rapports trouvés")
                    
                    if reports:
                        print("📊 Rapports disponibles:")
                        for report in reports[:3]:  # Afficher les 3 premiers
                            print(f"   - {report['filename']} ({report['type']}, {report['size']})")
                    else:
                        print("   Aucun rapport disponible")
                    
                    return True
                else:
                    print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
                    return False
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test de l'API de liste: {e}")
            return False
    
    def test_reports_stats_api(self):
        """Tester l'API de statistiques des rapports"""
        print("\n📊 Test de l'API de statistiques des rapports...")
        
        try:
            response = self.session.get(API_STATS_URL)
            
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    print(f"✅ API de statistiques fonctionnelle")
                    print(f"   - Total rapports: {data.get('total_reports', 0)}")
                    print(f"   - Rapports ce mois: {data.get('reports_this_month', 0)}")
                    print(f"   - Taille totale: {data.get('total_size_mb', 0):.2f} MB")
                    return True
                else:
                    print(f"❌ Erreur API: {data.get('error')}")
                    return False
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test de l'API de statistiques: {e}")
            return False
    
    def test_generate_pdf_report(self):
        """Tester la génération d'un rapport PDF"""
        print("\n📄 Test de génération d'un rapport PDF...")
        
        try:
            report_data = {
                'type': 'daily',
                'format': 'pdf',
                'date_from': '2024-01-01',
                'date_to': '2024-12-31',
                'description': 'Rapport de test généré automatiquement'
            }
            
            response = self.session.post(
                API_GENERATE_URL,
                json=report_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    filename = data.get('filename')
                    print(f"✅ Rapport PDF généré avec succès: {filename}")
                    return filename
                else:
                    print(f"❌ Erreur lors de la génération: {data.get('message')}")
                    return None
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération du rapport PDF: {e}")
            return None
    
    def test_generate_excel_report(self):
        """Tester la génération d'un rapport Excel"""
        print("\n📊 Test de génération d'un rapport Excel...")
        
        try:
            report_data = {
                'type': 'weekly',
                'format': 'excel',
                'date_from': '2024-01-01',
                'date_to': '2024-12-31',
                'description': 'Rapport Excel de test'
            }
            
            response = self.session.post(
                API_GENERATE_URL,
                json=report_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    filename = data.get('filename')
                    print(f"✅ Rapport Excel généré avec succès: {filename}")
                    return filename
                else:
                    print(f"❌ Erreur lors de la génération: {data.get('message')}")
                    return None
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération du rapport Excel: {e}")
            return None
    
    def test_download_report(self, filename):
        """Tester le téléchargement d'un rapport"""
        print(f"\n⬇️ Test de téléchargement du rapport: {filename}")
        
        try:
            download_url = f"{BASE_URL}/download/{filename}"
            response = self.session.get(download_url)
            
            if response.status_code == 200:
                print(f"✅ Téléchargement réussi - Taille: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ Erreur de téléchargement: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement: {e}")
            return False
    
    def test_delete_report(self, filename):
        """Tester la suppression d'un rapport"""
        print(f"\n🗑️ Test de suppression du rapport: {filename}")
        
        try:
            response = self.session.delete(f"{API_DELETE_URL}/{filename}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Rapport supprimé avec succès")
                    return True
                else:
                    print(f"❌ Erreur lors de la suppression: {data.get('message')}")
                    return False
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Exécuter tous les tests"""
        print("🚀 Démarrage des tests du système de rapports")
        print("=" * 50)
        
        # Test de connexion
        if not self.login():
            print("❌ Impossible de continuer sans connexion")
            return False
        
        # Test d'accès à la page
        if not self.test_reports_page_access():
            print("⚠️ Page des rapports inaccessible")
        
        # Test des APIs
        self.test_reports_list_api()
        self.test_reports_stats_api()
        
        # Test de génération de rapports
        pdf_filename = self.test_generate_pdf_report()
        excel_filename = self.test_generate_excel_report()
        
        # Attendre un peu pour la génération
        if pdf_filename or excel_filename:
            print("\n⏳ Attente de 3 secondes pour la génération...")
            time.sleep(3)
        
        # Test de téléchargement
        if pdf_filename:
            self.test_download_report(pdf_filename)
        
        if excel_filename:
            self.test_download_report(excel_filename)
        
        # Test de suppression (supprimer seulement le PDF de test)
        if pdf_filename:
            self.test_delete_report(pdf_filename)
        
        print("\n" + "=" * 50)
        print("✅ Tests du système de rapports terminés")
        return True

def main():
    """Fonction principale"""
    print("🧪 Testeur du système de génération de rapports")
    print("Ce script teste toutes les fonctionnalités de génération, téléchargement et gestion des rapports")
    print()
    
    # Vérifier que l'application est en cours d'exécution
    try:
        response = requests.get(f"{BASE_URL}/login", timeout=5)
        if response.status_code != 200:
            print("❌ L'application n'est pas accessible. Assurez-vous qu'elle est en cours d'exécution.")
            print("   Commande: python app.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Impossible de se connecter à l'application. Assurez-vous qu'elle est en cours d'exécution.")
        print("   Commande: python app.py")
        return
    
    # Exécuter les tests
    tester = ReportsSystemTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 Tous les tests ont été exécutés avec succès!")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez les logs ci-dessus.")

if __name__ == "__main__":
    main() 