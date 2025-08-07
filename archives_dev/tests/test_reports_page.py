#!/usr/bin/env python3
"""
Script de test pour la page Rapports
Teste toutes les fonctionnalités de la page rapports
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_DATA = {
    'username': 'admin',
    'password': 'admin123'
}

def test_login():
    """Test de connexion"""
    print("🔐 Test de connexion...")
    response = requests.post(f"{BASE_URL}/login", data=LOGIN_DATA, allow_redirects=False)
    if response.status_code == 302:  # Redirection après connexion réussie
        print("✅ Connexion réussie")
        return response.cookies
    else:
        print(f"❌ Échec de la connexion: {response.status_code}")
        return None

def test_reports_page_access(cookies):
    """Test d'accès à la page rapports"""
    print("\n📄 Test d'accès à la page rapports...")
    response = requests.get(f"{BASE_URL}/reports", cookies=cookies)
    if response.status_code == 200:
        print("✅ Page rapports accessible")
        return True
    else:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")
        return False

def test_api_reports_list(cookies):
    """Test de l'API de liste des rapports"""
    print("\n📋 Test de l'API liste des rapports...")
    response = requests.get(f"{BASE_URL}/api/reports/list", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            reports = data.get('reports', [])
            print(f"✅ Liste des rapports récupérée: {len(reports)} rapports")
            return reports
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return []
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return []

def test_api_reports_stats(cookies):
    """Test de l'API statistiques des rapports"""
    print("\n📊 Test de l'API statistiques...")
    response = requests.get(f"{BASE_URL}/api/reports/stats", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            stats = data.get('stats', {})
            print(f"✅ Statistiques récupérées:")
            print(f"   - Total: {stats.get('total', 0)}")
            print(f"   - Ce mois: {stats.get('this_month', 0)}")
            print(f"   - Taille totale: {stats.get('total_size', '0 MB')}")
            return stats
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return {}
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return {}

def test_generate_report(cookies, report_type="daily", format_type="pdf"):
    """Test de génération d'un rapport"""
    print(f"\n📝 Test de génération d'un rapport {report_type} en {format_type}...")
    
    report_data = {
        "type": report_type,
        "format": format_type,
        "date_from": "2024-01-01",
        "date_to": "2024-12-31",
        "description": f"Rapport de test {datetime.now().strftime('%H:%M:%S')}"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/reports/generate",
        json=report_data,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            filename = data.get('filename')
            print(f"✅ Rapport généré avec succès: {filename}")
            return filename
        else:
            print(f"❌ Erreur de génération: {data.get('message', 'Erreur inconnue')}")
            return None
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return None

def test_download_report(cookies, filename):
    """Test de téléchargement d'un rapport"""
    print(f"\n⬇️ Test de téléchargement: {filename}...")
    
    # Test de la route directe
    response = requests.get(f"{BASE_URL}/download/{filename}", cookies=cookies)
    if response.status_code == 200:
        print(f"✅ Téléchargement réussi (route directe)")
        return True
    else:
        print(f"❌ Échec du téléchargement (route directe): {response.status_code}")
        return False

def test_delete_report(cookies, filename):
    """Test de suppression d'un rapport"""
    print(f"\n🗑️ Test de suppression: {filename}...")
    
    response = requests.delete(f"{BASE_URL}/api/reports/delete/{filename}", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Rapport supprimé avec succès")
            return True
        else:
            print(f"❌ Erreur de suppression: {data.get('message', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_reports_page_content(cookies):
    """Test du contenu de la page rapports"""
    print("\n🔍 Test du contenu de la page...")
    response = requests.get(f"{BASE_URL}/reports", cookies=cookies)
    
    if response.status_code == 200:
        content = response.text
        
        # Vérifier les éléments clés
        checks = [
            ("Formulaire de génération", "Générer un nouveau rapport" in content),
            ("Sélecteur de type", "Type de rapport" in content),
            ("Sélecteur de format", "Format" in content),
            ("Statistiques", "Statistiques des rapports" in content),
            ("Liste des rapports", "Rapports disponibles" in content),
            ("Bouton actualiser", "Actualiser" in content),
            ("Filtres", "Tous" in content and "PDF" in content and "Excel" in content),
            ("Tableau des rapports", "Nom du fichier" in content),
            ("Actions", "Actions" in content),
            ("Modal d'aperçu", "Aperçu du rapport" in content)
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
    else:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")
        return False

def test_report_workflow(cookies):
    """Test du workflow complet de génération"""
    print("\n🔄 Test du workflow complet...")
    
    # 1. Générer un rapport PDF
    filename_pdf = test_generate_report(cookies, "daily", "pdf")
    if not filename_pdf:
        return False
    
    time.sleep(2)  # Attendre la génération
    
    # 2. Vérifier qu'il apparaît dans la liste
    reports = test_api_reports_list(cookies)
    if not any(r['filename'] == filename_pdf for r in reports):
        print("❌ Le rapport généré n'apparaît pas dans la liste")
        return False
    
    # 3. Télécharger le rapport
    if not test_download_report(cookies, filename_pdf):
        return False
    
    # 4. Générer un rapport Excel
    filename_excel = test_generate_report(cookies, "weekly", "excel")
    if not filename_excel:
        return False
    
    time.sleep(2)  # Attendre la génération
    
    # 5. Supprimer le rapport PDF
    if not test_delete_report(cookies, filename_pdf):
        return False
    
    print("✅ Workflow complet réussi")
    return True

def main():
    """Fonction principale"""
    print("🚀 Test de la page Rapports")
    print("=" * 50)
    
    # Connexion
    cookies = test_login()
    if not cookies:
        return
    
    # Tests de base
    if not test_reports_page_access(cookies):
        return
    
    if not test_reports_page_content(cookies):
        return
    
    # Tests des APIs
    reports = test_api_reports_list(cookies)
    stats = test_api_reports_stats(cookies)
    
    # Test du workflow complet
    test_report_workflow(cookies)
    
    print("\n" + "=" * 50)
    print("✅ Tests de la page Rapports terminés")
    print(f"📊 Rapports disponibles: {len(reports)}")
    if stats:
        print(f"📈 Statistiques: {stats.get('total', 0)} total, {stats.get('this_month', 0)} ce mois")

if __name__ == "__main__":
    main() 