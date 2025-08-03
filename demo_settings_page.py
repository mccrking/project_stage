#!/usr/bin/env python3
"""
Script de démonstration de la page Paramètres
Montre toutes les fonctionnalités de la page paramètres
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

def display_settings_overview(cookies):
    """Afficher un aperçu des paramètres actuels"""
    print("\n⚙️ APERÇU DES PARAMÈTRES ACTUELS")
    print("-" * 40)
    
    # Récupérer les paramètres réseau
    response = requests.get(f"{BASE_URL}/api/settings", cookies=cookies)
    if response.status_code == 200:
        settings = response.json()
        print("📋 Configuration réseau:")
        print(f"   • Plage réseau: {settings.get('network_range', 'N/A')}")
        print(f"   • Intervalle scan: {settings.get('scan_interval', 'N/A')} secondes")
        print(f"   • Timeout scan: {settings.get('scan_timeout', 'N/A')} secondes")
        print(f"   • Réseaux production: {len(settings.get('production_networks', []))}")
        print(f"   • Entraînement IA: {settings.get('ai_training_interval', 'N/A')} secondes")
    
    # Récupérer la configuration email
    response = requests.get(f"{BASE_URL}/api/settings/email", cookies=cookies)
    if response.status_code == 200:
        email_settings = response.json()
        if 'error' not in email_settings:
            print("\n📧 Configuration email:")
            print(f"   • Activé: {'Oui' if email_settings.get('enabled') else 'Non'}")
            print(f"   • Serveur SMTP: {email_settings.get('smtp_server', 'N/A')}")
            print(f"   • Port: {email_settings.get('smtp_port', 'N/A')}")
            print(f"   • Email destination: {email_settings.get('to_email', 'N/A')}")

def demonstrate_network_settings(cookies):
    """Démontrer la configuration réseau"""
    print("\n🌐 DÉMONSTRATION DE LA CONFIGURATION RÉSEAU")
    print("-" * 40)
    
    # Récupérer les réseaux disponibles
    response = requests.get(f"{BASE_URL}/api/settings/networks", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            networks = data.get('networks', [])
            production_networks = data.get('production_networks', [])
            
            print("📡 Réseaux découverts:")
            for i, network in enumerate(networks[:5], 1):  # Limiter à 5
                print(f"   {i}. {network}")
            
            print(f"\n🏭 Réseaux production Central Danone ({len(production_networks)}):")
            for network in production_networks:
                print(f"   • {network}")
    
    # Tester différents paramètres réseau
    test_configs = [
        {
            'name': 'Configuration rapide',
            'settings': {
                'network_range': '192.168.1.0/24',
                'scan_interval': 300,  # 5 minutes
                'scan_timeout': 5,
                'max_retries': 1,
                'enable_auto_scan': True
            }
        },
        {
            'name': 'Configuration complète',
            'settings': {
                'network_range': '192.168.1.0/24',
                'scan_interval': 600,  # 10 minutes
                'scan_timeout': 10,
                'max_retries': 3,
                'enable_auto_scan': True
            }
        }
    ]
    
    for config in test_configs:
        print(f"\n🔄 Test: {config['name']}")
        response = requests.post(
            f"{BASE_URL}/api/settings",
            json=config['settings'],
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {config['name']} appliquée avec succès")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")

def demonstrate_network_testing(cookies):
    """Démontrer les tests réseau"""
    print("\n🔍 DÉMONSTRATION DES TESTS RÉSEAU")
    print("-" * 40)
    
    test_networks = [
        '192.168.1.0/24',
        '192.168.2.0/24',
        '10.0.0.0/24'
    ]
    
    for network in test_networks:
        print(f"\n🌐 Test du réseau: {network}")
        
        response = requests.post(
            f"{BASE_URL}/api/settings/test-network",
            json={'network_range': network},
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                devices_found = data.get('devices_found', 0)
                devices = data.get('devices', [])
                
                print(f"   ✅ Appareils trouvés: {devices_found}")
                if devices:
                    print("   📱 Aperçu des appareils:")
                    for device in devices[:3]:  # Limiter à 3
                        print(f"      • {device.get('ip', 'N/A')} - {device.get('hostname', 'N/A')}")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")

def demonstrate_alert_settings(cookies):
    """Démontrer la configuration des alertes"""
    print("\n🚨 DÉMONSTRATION DE LA CONFIGURATION DES ALERTES")
    print("-" * 40)
    
    alert_configs = [
        {
            'name': 'Configuration standard',
            'settings': {
                'alert_threshold': 85,
                'alert_device_offline': True,
                'alert_device_online': True,
                'alert_low_uptime': True,
                'alert_scan_failed': False
            }
        },
        {
            'name': 'Configuration critique',
            'settings': {
                'alert_threshold': 95,
                'alert_device_offline': True,
                'alert_device_online': False,
                'alert_low_uptime': True,
                'alert_scan_failed': True
            }
        }
    ]
    
    for config in alert_configs:
        print(f"\n⚙️ {config['name']}:")
        settings = config['settings']
        print(f"   • Seuil d'alerte: {settings['alert_threshold']}%")
        print(f"   • Appareil hors ligne: {'Oui' if settings['alert_device_offline'] else 'Non'}")
        print(f"   • Appareil en ligne: {'Oui' if settings['alert_device_online'] else 'Non'}")
        print(f"   • Disponibilité faible: {'Oui' if settings['alert_low_uptime'] else 'Non'}")
        print(f"   • Échec de scan: {'Oui' if settings['alert_scan_failed'] else 'Non'}")
        
        # Sauvegarder la configuration
        response = requests.post(
            f"{BASE_URL}/api/settings/save",
            json=settings,
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {config['name']} sauvegardée")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")

def demonstrate_email_configuration(cookies):
    """Démontrer la configuration email"""
    print("\n📧 DÉMONSTRATION DE LA CONFIGURATION EMAIL")
    print("-" * 40)
    
    # Configurations email de test
    email_configs = [
        {
            'name': 'Configuration Gmail',
            'settings': {
                'enabled': True,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'username': 'supervision.centraldanone@gmail.com',
                'password': 'app_password_here',
                'from_email': 'supervision@centraldanone.com',
                'to_email': 'admin@centraldanone.com'
            }
        },
        {
            'name': 'Configuration Outlook',
            'settings': {
                'enabled': True,
                'smtp_server': 'smtp-mail.outlook.com',
                'smtp_port': 587,
                'username': 'supervision@centraldanone.com',
                'password': 'password_here',
                'from_email': 'supervision@centraldanone.com',
                'to_email': 'mehdi.chmiti2000@gmail.com'
            }
        }
    ]
    
    for config in email_configs:
        print(f"\n📧 {config['name']}:")
        settings = config['settings']
        print(f"   • Serveur: {settings['smtp_server']}:{settings['smtp_port']}")
        print(f"   • Utilisateur: {settings['username']}")
        print(f"   • De: {settings['from_email']}")
        print(f"   • À: {settings['to_email']}")
        
        # Sauvegarder la configuration
        response = requests.post(
            f"{BASE_URL}/api/settings/email",
            json=settings,
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {config['name']} sauvegardée")
                
                # Tester la configuration
                print(f"   🧪 Test de la configuration...")
                test_response = requests.post(
                    f"{BASE_URL}/api/settings/email/test",
                    cookies=cookies
                )
                
                if test_response.status_code == 200:
                    test_data = test_response.json()
                    if test_data.get('status') == 'success':
                        print(f"   ✅ Test réussi")
                    else:
                        print(f"   ❌ Test échoué: {test_data.get('message', 'Erreur inconnue')}")
                else:
                    print(f"   ❌ Erreur test: {test_response.status_code}")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")

def demonstrate_test_alerts(cookies):
    """Démontrer les tests d'alertes"""
    print("\n🚨 DÉMONSTRATION DES TESTS D'ALERTES")
    print("-" * 40)
    
    test_alerts = [
        {
            'name': 'Alerte critique',
            'data': {
                'subject': 'ALERTE CRITIQUE - Équipement hors ligne',
                'message': 'L\'équipement 192.168.1.100 est hors ligne depuis plus de 30 minutes. Intervention immédiate requise.',
                'priority': 'critical'
            }
        },
        {
            'name': 'Alerte de maintenance',
            'data': {
                'subject': 'Maintenance préventive recommandée',
                'message': 'L\'équipement 192.168.2.50 présente des signes de dégradation. Maintenance préventive recommandée dans les 48h.',
                'priority': 'medium'
            }
        },
        {
            'name': 'Rapport quotidien',
            'data': {
                'subject': 'Rapport quotidien - Central Danone',
                'message': 'Rapport quotidien de supervision réseau Central Danone. Disponibilité: 98.5%, Équipements en ligne: 45/46.',
                'priority': 'low'
            }
        }
    ]
    
    for alert in test_alerts:
        print(f"\n📤 Envoi: {alert['name']}")
        
        response = requests.post(
            f"{BASE_URL}/api/settings/email/alert",
            json=alert['data'],
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {alert['name']} envoyée avec succès")
            else:
                print(f"   ❌ Erreur: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
        
        time.sleep(1)  # Pause entre les envois

def demonstrate_report_settings(cookies):
    """Démontrer la configuration des rapports"""
    print("\n📊 DÉMONSTRATION DE LA CONFIGURATION DES RAPPORTS")
    print("-" * 40)
    
    report_configs = [
        {
            'name': 'Rapport journalier',
            'settings': {
                'auto_report': 'daily',
                'report_format': 'pdf',
                'report_time': '08:00',
                'report_retention': 30,
                'include_charts': True,
                'include_alerts': True
            }
        },
        {
            'name': 'Rapport hebdomadaire',
            'settings': {
                'auto_report': 'weekly',
                'report_format': 'excel',
                'report_time': '09:00',
                'report_retention': 90,
                'include_charts': True,
                'include_alerts': True
            }
        }
    ]
    
    for config in report_configs:
        print(f"\n📋 {config['name']}:")
        settings = config['settings']
        print(f"   • Type: {settings['auto_report']}")
        print(f"   • Format: {settings['report_format'].upper()}")
        print(f"   • Heure: {settings['report_time']}")
        print(f"   • Rétention: {settings['report_retention']} jours")
        print(f"   • Graphiques: {'Oui' if settings['include_charts'] else 'Non'}")
        print(f"   • Alertes: {'Oui' if settings['include_alerts'] else 'Non'}")
        
        # Sauvegarder la configuration
        response = requests.post(
            f"{BASE_URL}/api/settings/save",
            json=settings,
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {config['name']} configuré")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")

def demonstrate_system_actions(cookies):
    """Démontrer les actions système"""
    print("\n🖥️ DÉMONSTRATION DES ACTIONS SYSTÈME")
    print("-" * 40)
    
    actions = [
        {
            'name': 'Sauvegarde de la base de données',
            'description': 'Création d\'une sauvegarde complète de la base de données'
        },
        {
            'name': 'Vider le cache',
            'description': 'Nettoyage du cache système pour améliorer les performances'
        },
        {
            'name': 'Réinitialiser les paramètres',
            'description': 'Retour aux paramètres par défaut (ATTENTION: action irréversible)'
        }
    ]
    
    for action in actions:
        print(f"\n⚙️ {action['name']}:")
        print(f"   📝 {action['description']}")
        print(f"   ℹ️  Cette action est disponible via l'interface web")
        print(f"   🔧 Utilisez le bouton correspondant dans la section 'Actions système'")

def demonstrate_page_features(cookies):
    """Démontrer les fonctionnalités de la page"""
    print("\n🎯 FONCTIONNALITÉS DE LA PAGE PARAMÈTRES")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/settings", cookies=cookies)
    if response.status_code == 200:
        content = response.text
        
        features = [
            ("Configuration réseau", "Configuration réseau"),
            ("Plage réseau", "Plage réseau à scanner"),
            ("Intervalle de scan", "Intervalle de scan"),
            ("Timeout de scan", "Timeout de scan"),
            ("Scan automatique", "Activer le scan automatique"),
            ("Configuration alertes", "Configuration des alertes"),
            ("Seuil d'alerte", "Seuil d'alerte"),
            ("Types d'alertes", "Types d'alertes"),
            ("Configuration rapports", "Configuration des rapports"),
            ("Rapport automatique", "Rapport automatique"),
            ("Format par défaut", "Format par défaut"),
            ("Heure de génération", "Heure de génération"),
            ("Configuration email", "Configuration des alertes par email"),
            ("Serveur SMTP", "Serveur SMTP"),
            ("Test configuration", "Tester la configuration"),
            ("Envoi alerte test", "Envoyer une alerte de test"),
            ("Paramètres système", "Paramètres système"),
            ("Sauvegarde BDD", "Sauvegarde de la base de données"),
            ("Vider cache", "Vider le cache"),
            ("Réinitialiser", "Réinitialiser les paramètres"),
            ("Informations réseau", "Informations réseau"),
            ("Statut du scan", "Statut du scan"),
            ("Performance", "Performance"),
            ("Test des alertes", "Test des alertes"),
            ("Aide configuration", "Aide configuration email"),
            ("Formulaires", "Sauvegarder les paramètres"),
            ("Boutons d'action", "Tester une alerte"),
            ("Statistiques rapports", "Statistiques des rapports")
        ]
        
        print("✅ Fonctionnalités disponibles:")
        for feature_name, search_text in features:
            if search_text in content:
                print(f"   • {feature_name}")
            else:
                print(f"   ❌ {feature_name} (manquant)")
    else:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")

def demonstrate_settings_categories():
    """Expliquer les catégories de paramètres"""
    print("\n📋 CATÉGORIES DE PARAMÈTRES")
    print("-" * 40)
    
    categories = {
        "Réseau": {
            "description": "Configuration du scan et de la surveillance réseau",
            "paramètres": [
                "Plage réseau à scanner (CIDR)",
                "Intervalle de scan automatique",
                "Timeout de scan par appareil",
                "Nombre de tentatives",
                "Activation du scan automatique"
            ]
        },
        "Alertes": {
            "description": "Configuration des seuils et types d'alertes",
            "paramètres": [
                "Seuil de disponibilité pour alerte",
                "Types d'alertes à activer",
                "Email de destination pour alertes simples",
                "Configuration SMTP complète"
            ]
        },
        "Rapports": {
            "description": "Configuration de la génération automatique de rapports",
            "paramètres": [
                "Type de rapport automatique",
                "Format par défaut (PDF/Excel)",
                "Heure de génération",
                "Période de rétention",
                "Inclusion de graphiques et alertes"
            ]
        },
        "Email": {
            "description": "Configuration complète des alertes par email",
            "paramètres": [
                "Serveur SMTP et port",
                "Authentification (utilisateur/mot de passe)",
                "Email d'expédition et de destination",
                "Test de configuration",
                "Envoi d'alertes de test"
            ]
        },
        "Système": {
            "description": "Actions de maintenance et informations système",
            "paramètres": [
                "Sauvegarde de la base de données",
                "Nettoyage du cache",
                "Réinitialisation des paramètres",
                "Informations système (version, statut)"
            ]
        }
    }
    
    for category, info in categories.items():
        print(f"\n🔧 {category}")
        print(f"   Description: {info['description']}")
        print(f"   Paramètres:")
        for param in info['paramètres']:
            print(f"     • {param}")

def main():
    """Fonction principale"""
    print("🚀 DÉMONSTRATION DE LA PAGE PARAMÈTRES")
    print("=" * 60)
    
    # Connexion
    cookies = login()
    if not cookies:
        return
    
    # Aperçu des paramètres actuels
    display_settings_overview(cookies)
    
    # Démonstration des catégories
    demonstrate_settings_categories()
    
    # Démonstration des fonctionnalités de la page
    demonstrate_page_features(cookies)
    
    # Démonstrations spécifiques
    demonstrate_network_settings(cookies)
    demonstrate_network_testing(cookies)
    demonstrate_alert_settings(cookies)
    demonstrate_email_configuration(cookies)
    demonstrate_test_alerts(cookies)
    demonstrate_report_settings(cookies)
    demonstrate_system_actions(cookies)
    
    print("\n" + "=" * 60)
    print("✅ DÉMONSTRATION TERMINÉE")
    print("\n🎯 Points clés de la page Paramètres:")
    print("   • Configuration complète du réseau de surveillance")
    print("   • Gestion des alertes et seuils")
    print("   • Configuration email pour notifications")
    print("   • Paramètres de génération de rapports")
    print("   • Actions de maintenance système")
    print("   • Tests et validation des configurations")
    print("   • Interface intuitive et organisée")
    print("   • Sauvegarde et restauration des paramètres")

if __name__ == "__main__":
    main() 