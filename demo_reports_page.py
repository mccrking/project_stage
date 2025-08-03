#!/usr/bin/env python3
"""
Script de démonstration de la page Rapports
Montre toutes les fonctionnalités de la page rapports
"""
import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_DATA = {
    'username': 'admin',
    'password': 'admin123'
}

def login():
    """Connexion à l'application"""
    print("🔐 Connexion à l'application...")
    response = requests.post(f"{BASE_URL}/login", data=LOGIN_DATA, allow_redirects=False)
    if response.status_code == 302:
        print("✅ Connexion réussie")
        return response.cookies
    else:
        print(f"❌ Échec de la connexion: {response.status_code}")
        return None

def display_reports_overview(cookies):
    """Afficher un aperçu des rapports existants"""
    print("\n📊 APERÇU DES RAPPORTS EXISTANTS")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/api/reports/list", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            reports = data.get('reports', [])
            
            if not reports:
                print("📭 Aucun rapport disponible")
                return
            
            print(f"📋 Total: {len(reports)} rapports")
            
            # Statistiques par type
            types_count = {}
            formats_count = {}
            
            for report in reports:
                report_type = report.get('report_type', 'Inconnu')
                format_type = report.get('format', 'Inconnu')
                
                types_count[report_type] = types_count.get(report_type, 0) + 1
                formats_count[format_type] = formats_count.get(format_type, 0) + 1
            
            print("\n📈 Par type:")
            for report_type, count in types_count.items():
                print(f"   • {report_type}: {count}")
            
            print("\n📄 Par format:")
            for format_type, count in formats_count.items():
                print(f"   • {format_type.upper()}: {count}")
            
            # Afficher les 5 plus récents
            print("\n🕒 5 rapports les plus récents:")
            sorted_reports = sorted(reports, key=lambda x: x.get('created', ''), reverse=True)[:5]
            
            for i, report in enumerate(sorted_reports, 1):
                created = report.get('created', 'Inconnu')
                filename = report.get('filename', 'Inconnu')
                size = report.get('size', 'Inconnu')
                print(f"   {i}. {filename} ({size}) - {created}")
        else:
            print(f"❌ Erreur: {data.get('error', 'Erreur inconnue')}")
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")

def demonstrate_report_generation(cookies):
    """Démontrer la génération de différents types de rapports"""
    print("\n📝 DÉMONSTRATION DE GÉNÉRATION DE RAPPORTS")
    print("-" * 40)
    
    # Types de rapports à générer
    report_configs = [
        {"type": "daily", "format": "pdf", "name": "Rapport journalier PDF"},
        {"type": "weekly", "format": "excel", "name": "Rapport hebdomadaire Excel"},
        {"type": "monthly", "format": "pdf", "name": "Rapport mensuel PDF"},
        {"type": "custom", "format": "excel", "name": "Rapport personnalisé Excel"}
    ]
    
    generated_reports = []
    
    for config in report_configs:
        print(f"\n🔄 Génération: {config['name']}...")
        
        # Dates pour le rapport
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        report_data = {
            "type": config["type"],
            "format": config["format"],
            "date_from": start_date.strftime("%Y-%m-%d"),
            "date_to": end_date.strftime("%Y-%m-%d"),
            "description": f"{config['name']} - Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
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
                print(f"✅ Généré avec succès: {filename}")
                generated_reports.append({
                    'filename': filename,
                    'config': config
                })
                
                # Attendre un peu entre les générations
                time.sleep(1)
            else:
                print(f"❌ Erreur: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    
    return generated_reports

def demonstrate_report_management(cookies, reports):
    """Démontrer la gestion des rapports"""
    print("\n🗂️ DÉMONSTRATION DE GESTION DES RAPPORTS")
    print("-" * 40)
    
    if not reports:
        print("📭 Aucun rapport à gérer")
        return
    
    # Télécharger le premier rapport
    first_report = reports[0]
    print(f"\n⬇️ Téléchargement: {first_report['filename']}...")
    
    response = requests.get(f"{BASE_URL}/download/{first_report['filename']}", cookies=cookies)
    if response.status_code == 200:
        print(f"✅ Téléchargement réussi ({len(response.content)} bytes)")
    else:
        print(f"❌ Échec du téléchargement: {response.status_code}")
    
    # Supprimer le dernier rapport (si il y en a plus d'un)
    if len(reports) > 1:
        last_report = reports[-1]
        print(f"\n🗑️ Suppression: {last_report['filename']}...")
        
        response = requests.delete(f"{BASE_URL}/api/reports/delete/{last_report['filename']}", cookies=cookies)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Rapport supprimé avec succès")
            else:
                print(f"❌ Erreur: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")

def demonstrate_statistics(cookies):
    """Démontrer les statistiques des rapports"""
    print("\n📊 DÉMONSTRATION DES STATISTIQUES")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/api/reports/stats", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            stats = data.get('stats', {})
            
            print("📈 Statistiques globales:")
            print(f"   • Total des rapports: {stats.get('total', 0)}")
            print(f"   • Rapports ce mois: {stats.get('this_month', 0)}")
            print(f"   • Taille totale: {stats.get('total_size', '0 MB')}")
            
            # Statistiques par type
            type_stats = stats.get('by_type', {})
            if type_stats:
                print("\n📋 Par type:")
                for report_type, count in type_stats.items():
                    print(f"   • {report_type}: {count}")
            
            # Statistiques par format
            format_stats = stats.get('by_format', {})
            if format_stats:
                print("\n📄 Par format:")
                for format_type, count in format_stats.items():
                    print(f"   • {format_type.upper()}: {count}")
        else:
            print(f"❌ Erreur: {data.get('error', 'Erreur inconnue')}")
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")

def demonstrate_page_features(cookies):
    """Démontrer les fonctionnalités de la page"""
    print("\n🎯 FONCTIONNALITÉS DE LA PAGE RAPPORTS")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/reports", cookies=cookies)
    if response.status_code == 200:
        content = response.text
        
        features = [
            ("Formulaire de génération", "Générer un nouveau rapport"),
            ("Sélecteur de type", "Type de rapport"),
            ("Sélecteur de format", "Format"),
            ("Sélecteur de dates", "Date de début"),
            ("Champ description", "Description"),
            ("Bouton génération", "Générer le rapport"),
            ("Bouton aperçu", "Aperçu"),
            ("Statistiques", "Statistiques des rapports"),
            ("Compteurs", "Total rapports"),
            ("Types de rapports", "Journaliers"),
            ("Liste des rapports", "Rapports disponibles"),
            ("Bouton actualiser", "Actualiser"),
            ("Filtres", "Tous"),
            ("Tableau", "Nom du fichier"),
            ("Actions", "Actions"),
            ("Téléchargement", "Télécharger"),
            ("Suppression", "Supprimer"),
            ("Modal d'aperçu", "Aperçu du rapport")
        ]
        
        print("✅ Fonctionnalités disponibles:")
        for feature_name, search_text in features:
            if search_text in content:
                print(f"   • {feature_name}")
            else:
                print(f"   ❌ {feature_name} (manquant)")
    else:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")

def demonstrate_report_types():
    """Expliquer les types de rapports disponibles"""
    print("\n📋 TYPES DE RAPPORTS DISPONIBLES")
    print("-" * 40)
    
    report_types = {
        "daily": {
            "name": "Rapport journalier",
            "description": "Résumé quotidien de l'état du réseau",
            "contenu": ["Statistiques du jour", "Équipements en ligne/hors ligne", "Alertes du jour", "Graphiques de disponibilité"]
        },
        "weekly": {
            "name": "Rapport hebdomadaire",
            "description": "Analyse hebdomadaire complète",
            "contenu": ["Tendances de la semaine", "Performance des équipements", "Historique des alertes", "Recommandations"]
        },
        "monthly": {
            "name": "Rapport mensuel",
            "description": "Rapport mensuel détaillé pour la direction",
            "contenu": ["Métriques mensuelles", "Analyse des tendances", "Planification maintenance", "Budget et coûts"]
        },
        "custom": {
            "name": "Rapport personnalisé",
            "description": "Rapport sur mesure selon vos besoins",
            "contenu": ["Période personnalisée", "Filtres spécifiques", "Données sélectionnées", "Format adapté"]
        }
    }
    
    for report_type, info in report_types.items():
        print(f"\n📄 {info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Contenu:")
        for item in info['contenu']:
            print(f"     • {item}")

def demonstrate_formats():
    """Expliquer les formats disponibles"""
    print("\n📄 FORMATS DISPONIBLES")
    print("-" * 40)
    
    formats = {
        "pdf": {
            "name": "PDF",
            "description": "Format portable et professionnel",
            "avantages": ["Lecture universelle", "Mise en page fixe", "Sécurité", "Archivage"]
        },
        "excel": {
            "name": "Excel",
            "description": "Format tabulaire et interactif",
            "avantages": ["Données structurées", "Calculs automatiques", "Graphiques", "Filtres"]
        }
    }
    
    for format_type, info in formats.items():
        print(f"\n📊 {info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Avantages:")
        for avantage in info['avantages']:
            print(f"     • {avantage}")

def main():
    """Fonction principale"""
    print("🚀 DÉMONSTRATION DE LA PAGE RAPPORTS")
    print("=" * 60)
    
    # Connexion
    cookies = login()
    if not cookies:
        return
    
    # Aperçu des rapports existants
    display_reports_overview(cookies)
    
    # Démonstration des types et formats
    demonstrate_report_types()
    demonstrate_formats()
    
    # Démonstration des fonctionnalités de la page
    demonstrate_page_features(cookies)
    
    # Démonstration des statistiques
    demonstrate_statistics(cookies)
    
    # Génération de rapports de démonstration
    generated_reports = demonstrate_report_generation(cookies)
    
    # Gestion des rapports
    demonstrate_report_management(cookies, generated_reports)
    
    print("\n" + "=" * 60)
    print("✅ DÉMONSTRATION TERMINÉE")
    print("\n🎯 Points clés de la page Rapports:")
    print("   • Génération de rapports PDF et Excel")
    print("   • 4 types de rapports (journalier, hebdomadaire, mensuel, personnalisé)")
    print("   • Statistiques en temps réel")
    print("   • Téléchargement et suppression")
    print("   • Interface intuitive et responsive")
    print("   • Filtrage et recherche")
    print("   • Aperçu avant génération")

if __name__ == "__main__":
    main() 