#!/usr/bin/env python3
"""
Script de démonstration du système de génération de rapports
Montre toutes les fonctionnalités disponibles et génère des exemples
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/login"
API_GENERATE_URL = f"{BASE_URL}/api/reports/generate"
API_LIST_URL = f"{BASE_URL}/api/reports/list"
API_STATS_URL = f"{BASE_URL}/api/reports/stats"

# Identifiants de test
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

class ReportsSystemDemo:
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        
    def login(self):
        """Se connecter à l'application"""
        print("🔐 Connexion à l'application...")
        
        try:
            login_data = {
                'username': TEST_USERNAME,
                'password': TEST_PASSWORD
            }
            
            response = self.session.post(LOGIN_URL, data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                print("✅ Connexion réussie")
                self.logged_in = True
                return True
            else:
                print(f"❌ Échec de la connexion: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la connexion: {e}")
            return False
    
    def get_current_stats(self):
        """Récupérer les statistiques actuelles"""
        try:
            response = self.session.get(API_STATS_URL)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def generate_daily_report_pdf(self):
        """Générer un rapport journalier PDF"""
        print("\n📄 Génération d'un rapport journalier PDF...")
        
        report_data = {
            'type': 'daily',
            'format': 'pdf',
            'date_from': datetime.now().strftime('%Y-%m-%d'),
            'date_to': datetime.now().strftime('%Y-%m-%d'),
            'description': 'Rapport journalier automatique - Supervision réseau Central Danone'
        }
        
        return self._generate_report(report_data, "journalier PDF")
    
    def generate_weekly_report_excel(self):
        """Générer un rapport hebdomadaire Excel"""
        print("\n📊 Génération d'un rapport hebdomadaire Excel...")
        
        # Date de début de la semaine (lundi)
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        report_data = {
            'type': 'weekly',
            'format': 'excel',
            'date_from': start_of_week.strftime('%Y-%m-%d'),
            'date_to': end_of_week.strftime('%Y-%m-%d'),
            'description': 'Rapport hebdomadaire - Analyse complète des performances réseau'
        }
        
        return self._generate_report(report_data, "hebdomadaire Excel")
    
    def generate_monthly_report_pdf(self):
        """Générer un rapport mensuel PDF"""
        print("\n📈 Génération d'un rapport mensuel PDF...")
        
        # Premier jour du mois
        today = datetime.now()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        report_data = {
            'type': 'monthly',
            'format': 'pdf',
            'date_from': start_of_month.strftime('%Y-%m-%d'),
            'date_to': end_of_month.strftime('%Y-%m-%d'),
            'description': 'Rapport mensuel - Synthèse complète de la supervision réseau'
        }
        
        return self._generate_report(report_data, "mensuel PDF")
    
    def generate_custom_report_excel(self):
        """Générer un rapport personnalisé Excel"""
        print("\n🎯 Génération d'un rapport personnalisé Excel...")
        
        # Période personnalisée (derniers 30 jours)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        report_data = {
            'type': 'custom',
            'format': 'excel',
            'date_from': start_date.strftime('%Y-%m-%d'),
            'date_to': end_date.strftime('%Y-%m-%d'),
            'description': 'Rapport personnalisé - Analyse des 30 derniers jours avec focus sur les anomalies'
        }
        
        return self._generate_report(report_data, "personnalisé Excel")
    
    def _generate_report(self, report_data, report_type):
        """Générer un rapport avec les données fournies"""
        try:
            response = self.session.post(
                API_GENERATE_URL,
                json=report_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    filename = data.get('filename')
                    print(f"✅ Rapport {report_type} généré: {filename}")
                    return filename
                else:
                    print(f"❌ Erreur lors de la génération: {data.get('message')}")
                    return None
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return None
    
    def list_all_reports(self):
        """Lister tous les rapports disponibles"""
        print("\n📋 Liste de tous les rapports disponibles:")
        print("-" * 60)
        
        try:
            response = self.session.get(API_LIST_URL)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    reports = data.get('reports', [])
                    
                    if reports:
                        print(f"{'Nom du fichier':<40} {'Type':<8} {'Taille':<10} {'Date':<20}")
                        print("-" * 80)
                        
                        for report in reports:
                            filename = report['filename'][:38] + ".." if len(report['filename']) > 40 else report['filename']
                            print(f"{filename:<40} {report['type']:<8} {report['size']:<10} {report['created']:<20}")
                        
                        print(f"\n📊 Total: {len(reports)} rapports")
                    else:
                        print("   Aucun rapport disponible")
                    
                    return reports
                else:
                    print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
                    return []
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la liste: {e}")
            return []
    
    def show_statistics(self):
        """Afficher les statistiques des rapports"""
        print("\n📊 Statistiques des rapports:")
        print("-" * 40)
        
        try:
            response = self.session.get(API_STATS_URL)
            
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    print(f"📄 Total des rapports: {data.get('total_reports', 0)}")
                    print(f"📅 Rapports ce mois: {data.get('reports_this_month', 0)}")
                    print(f"💾 Taille totale: {data.get('total_size_mb', 0):.2f} MB")
                    
                    if data.get('total_reports', 0) > 0:
                        avg_size = data.get('total_size_mb', 0) / data.get('total_reports', 1)
                        print(f"📏 Taille moyenne: {avg_size:.2f} MB")
                else:
                    print(f"❌ Erreur: {data.get('error')}")
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des statistiques: {e}")
    
    def run_complete_demo(self):
        """Exécuter la démonstration complète"""
        print("🚀 DÉMONSTRATION DU SYSTÈME DE GÉNÉRATION DE RAPPORTS")
        print("=" * 60)
        print("Ce script démontre toutes les fonctionnalités du système de rapports")
        print("de la plateforme de supervision réseau Central Danone.")
        print()
        
        # Connexion
        if not self.login():
            print("❌ Impossible de continuer sans connexion")
            return False
        
        # Statistiques initiales
        print("📈 ÉTAT INITIAL DU SYSTÈME")
        initial_stats = self.get_current_stats()
        if initial_stats:
            print(f"   Rapports existants: {initial_stats.get('total_reports', 0)}")
            print(f"   Taille totale: {initial_stats.get('total_size_mb', 0):.2f} MB")
        
        # Génération de différents types de rapports
        print("\n🔄 GÉNÉRATION DE RAPPORTS")
        print("=" * 40)
        
        generated_files = []
        
        # Rapport journalier PDF
        pdf_daily = self.generate_daily_report_pdf()
        if pdf_daily:
            generated_files.append(pdf_daily)
        
        # Rapport hebdomadaire Excel
        excel_weekly = self.generate_weekly_report_excel()
        if excel_weekly:
            generated_files.append(excel_weekly)
        
        # Rapport mensuel PDF
        pdf_monthly = self.generate_monthly_report_pdf()
        if pdf_monthly:
            generated_files.append(pdf_monthly)
        
        # Rapport personnalisé Excel
        excel_custom = self.generate_custom_report_excel()
        if excel_custom:
            generated_files.append(excel_custom)
        
        # Attendre la génération
        if generated_files:
            print(f"\n⏳ Attente de 5 secondes pour la génération de {len(generated_files)} rapports...")
            time.sleep(5)
        
        # Statistiques après génération
        print("\n📈 ÉTAT APRÈS GÉNÉRATION")
        final_stats = self.get_current_stats()
        if final_stats:
            new_reports = final_stats.get('total_reports', 0) - initial_stats.get('total_reports', 0)
            print(f"   Nouveaux rapports générés: {new_reports}")
            print(f"   Total actuel: {final_stats.get('total_reports', 0)}")
            print(f"   Taille totale: {final_stats.get('total_size_mb', 0):.2f} MB")
        
        # Liste des rapports
        self.list_all_reports()
        
        # Statistiques détaillées
        self.show_statistics()
        
        # Résumé
        print("\n" + "=" * 60)
        print("✅ DÉMONSTRATION TERMINÉE")
        print(f"📄 Rapports générés: {len(generated_files)}")
        print("🎯 Fonctionnalités testées:")
        print("   ✓ Génération de rapports PDF et Excel")
        print("   ✓ Rapports journaliers, hebdomadaires, mensuels et personnalisés")
        print("   ✓ Liste et statistiques des rapports")
        print("   ✓ Gestion des fichiers de rapports")
        print()
        print("📁 Les rapports générés sont disponibles dans le dossier 'reports/'")
        print("🌐 Accédez à l'interface web pour télécharger et gérer les rapports")
        
        return True

def main():
    """Fonction principale"""
    print("🎬 Démonstrateur du système de génération de rapports")
    print("Plateforme de supervision réseau - Central Danone")
    print()
    
    # Vérifier que l'application est en cours d'exécution
    try:
        response = requests.get(f"{BASE_URL}/login", timeout=5)
        if response.status_code != 200:
            print("❌ L'application n'est pas accessible.")
            print("   Assurez-vous qu'elle est en cours d'exécution avec: python app.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Impossible de se connecter à l'application.")
        print("   Assurez-vous qu'elle est en cours d'exécution avec: python app.py")
        return
    
    # Exécuter la démonstration
    demo = ReportsSystemDemo()
    success = demo.run_complete_demo()
    
    if success:
        print("\n🎉 Démonstration terminée avec succès!")
        print("💡 Conseils d'utilisation:")
        print("   - Utilisez l'interface web pour une gestion complète")
        print("   - Les rapports sont automatiquement organisés par type")
        print("   - Vous pouvez personnaliser les périodes et descriptions")
        print("   - Les formats PDF et Excel sont disponibles")
    else:
        print("\n⚠️ La démonstration a rencontré des problèmes.")
        print("   Vérifiez que l'application fonctionne correctement.")

if __name__ == "__main__":
    main() 