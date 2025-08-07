#!/usr/bin/env python3
"""
Script de test pour la page Paramètres
Teste toutes les fonctionnalités de la page paramètres
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

def test_settings_page_access(cookies):
    """Test d'accès à la page paramètres"""
    print("\n⚙️ Test d'accès à la page paramètres...")
    response = requests.get(f"{BASE_URL}/settings", cookies=cookies)
    if response.status_code == 200:
        print("✅ Page paramètres accessible")
        return True
    else:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")
        return False

def test_api_settings(cookies):
    """Test de l'API des paramètres"""
    print("\n📋 Test de l'API paramètres...")
    response = requests.get(f"{BASE_URL}/api/settings", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Paramètres récupérés:")
        print(f"   - Plage réseau: {data.get('network_range', 'N/A')}")
        print(f"   - Intervalle scan: {data.get('scan_interval', 'N/A')}s")
        print(f"   - Timeout scan: {data.get('scan_timeout', 'N/A')}s")
        print(f"   - Réseaux production: {len(data.get('production_networks', []))}")
        return data
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return None

def test_api_networks(cookies):
    """Test de l'API des réseaux"""
    print("\n🌐 Test de l'API réseaux...")
    response = requests.get(f"{BASE_URL}/api/settings/networks", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            networks = data.get('networks', [])
            production_networks = data.get('production_networks', [])
            print(f"✅ Réseaux découverts: {len(networks)}")
            print(f"✅ Réseaux production: {len(production_networks)}")
            return data
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return None
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return None

def test_save_network_settings(cookies):
    """Test de sauvegarde des paramètres réseau"""
    print("\n💾 Test de sauvegarde paramètres réseau...")
    
    settings = {
        'network_range': '192.168.1.0/24',
        'scan_interval': 300,
        'scan_timeout': 10,
        'max_retries': 2,
        'enable_auto_scan': True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/settings",
        json=settings,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Paramètres réseau sauvegardés avec succès")
            return True
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_save_settings(cookies):
    """Test de sauvegarde générale des paramètres"""
    print("\n💾 Test de sauvegarde générale...")
    
    settings = {
        'network_range': '192.168.2.0/24',
        'scan_interval': 600,
        'alert_threshold': 85,
        'auto_report': 'daily',
        'report_format': 'pdf'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/settings/save",
        json=settings,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Paramètres sauvegardés avec succès")
            return True
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_network_scan(cookies):
    """Test de scan réseau"""
    print("\n🔍 Test de scan réseau...")
    
    test_data = {
        'network_range': '192.168.1.0/24'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/settings/test-network",
        json=test_data,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            devices_found = data.get('devices_found', 0)
            print(f"✅ Test réseau réussi: {devices_found} appareils trouvés")
            return True
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_email_settings_get(cookies):
    """Test de récupération des paramètres email"""
    print("\n📧 Test de récupération config email...")
    response = requests.get(f"{BASE_URL}/api/settings/email", cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        if 'error' not in data:
            print("✅ Configuration email récupérée:")
            print(f"   - Activé: {data.get('enabled', False)}")
            print(f"   - Serveur: {data.get('smtp_server', 'N/A')}")
            print(f"   - Port: {data.get('smtp_port', 'N/A')}")
            print(f"   - Email destination: {data.get('to_email', 'N/A')}")
            return data
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return None
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return None

def test_email_settings_save(cookies):
    """Test de sauvegarde des paramètres email"""
    print("\n💾 Test de sauvegarde config email...")
    
    email_settings = {
        'enabled': True,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'test@example.com',
        'password': 'test_password',
        'from_email': 'supervision@centraldanone.com',
        'to_email': 'admin@centraldanone.com'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/settings/email",
        json=email_settings,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Configuration email sauvegardée avec succès")
            return True
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_email_test(cookies):
    """Test de test email"""
    print("\n🧪 Test de test email...")
    
    response = requests.post(
        f"{BASE_URL}/api/settings/email/test",
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Test email réussi")
            return True
        else:
            print(f"❌ Erreur test email: {data.get('message', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_send_test_alert(cookies):
    """Test d'envoi d'alerte de test"""
    print("\n🚨 Test d'envoi alerte de test...")
    
    alert_data = {
        'subject': 'Test d\'alerte Central Danone',
        'message': 'Ceci est un test d\'alerte pour vérifier la configuration email.',
        'priority': 'medium'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/settings/email/alert",
        json=alert_data,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Alerte de test envoyée avec succès")
            return True
        else:
            print(f"❌ Erreur envoi alerte: {data.get('message', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_save_alert_email(cookies):
    """Test de sauvegarde email d'alerte simple"""
    print("\n💾 Test de sauvegarde email alerte simple...")
    
    alert_email_data = {
        'alert_email': 'mehdi.chmiti2000@gmail.com'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/settings/alert-email",
        json=alert_email_data,
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Email d'alerte simple sauvegardé avec succès")
            return True
        else:
            print(f"❌ Erreur API: {data.get('error', 'Erreur inconnue')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

def test_settings_page_content(cookies):
    """Test du contenu de la page paramètres"""
    print("\n🔍 Test du contenu de la page...")
    response = requests.get(f"{BASE_URL}/settings", cookies=cookies)
    
    if response.status_code == 200:
        content = response.text
        
        # Vérifier les éléments clés
        checks = [
            ("Configuration réseau", "Configuration réseau" in content),
            ("Plage réseau", "Plage réseau à scanner" in content),
            ("Intervalle de scan", "Intervalle de scan" in content),
            ("Configuration des alertes", "Configuration des alertes" in content),
            ("Seuil d'alerte", "Seuil d'alerte" in content),
            ("Types d'alertes", "Types d'alertes" in content),
            ("Configuration des rapports", "Configuration des rapports" in content),
            ("Rapport automatique", "Rapport automatique" in content),
            ("Configuration email", "Configuration des alertes par email" in content),
            ("Serveur SMTP", "Serveur SMTP" in content),
            ("Paramètres système", "Paramètres système" in content),
            ("Sauvegarde base de données", "Sauvegarde de la base de données" in content),
            ("Test des alertes", "Test des alertes" in content),
            ("Test configuration", "Tester la configuration" in content),
            ("Aide configuration", "Aide configuration email" in content),
            ("Formulaires", "Sauvegarder les paramètres" in content),
            ("Boutons d'action", "Tester une alerte" in content),
            ("Informations réseau", "Informations réseau" in content),
            ("Statistiques", "Statistiques des rapports" in content),
            ("Actions système", "Actions système" in content)
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

def test_settings_workflow(cookies):
    """Test du workflow complet des paramètres"""
    print("\n🔄 Test du workflow complet...")
    
    # 1. Récupérer les paramètres actuels
    current_settings = test_api_settings(cookies)
    if not current_settings:
        return False
    
    # 2. Sauvegarder de nouveaux paramètres réseau
    if not test_save_network_settings(cookies):
        return False
    
    # 3. Tester un scan réseau
    if not test_network_scan(cookies):
        return False
    
    # 4. Configurer et tester l'email
    if not test_email_settings_save(cookies):
        return False
    
    # 5. Tester l'envoi d'email
    if not test_email_test(cookies):
        return False
    
    # 6. Envoyer une alerte de test
    if not test_send_test_alert(cookies):
        return False
    
    print("✅ Workflow complet réussi")
    return True

def main():
    """Fonction principale"""
    print("🚀 Test de la page Paramètres")
    print("=" * 50)
    
    # Connexion
    cookies = test_login()
    if not cookies:
        return
    
    # Tests de base
    if not test_settings_page_access(cookies):
        return
    
    if not test_settings_page_content(cookies):
        return
    
    # Tests des APIs
    settings = test_api_settings(cookies)
    networks = test_api_networks(cookies)
    
    # Tests de sauvegarde
    test_save_network_settings(cookies)
    test_save_settings(cookies)
    
    # Tests réseau
    test_network_scan(cookies)
    
    # Tests email
    email_settings = test_email_settings_get(cookies)
    test_email_settings_save(cookies)
    test_email_test(cookies)
    test_send_test_alert(cookies)
    test_save_alert_email(cookies)
    
    # Test du workflow complet
    test_settings_workflow(cookies)
    
    print("\n" + "=" * 50)
    print("✅ Tests de la page Paramètres terminés")
    if settings:
        print(f"📊 Paramètres réseau: {settings.get('network_range', 'N/A')}")
    if networks:
        print(f"🌐 Réseaux production: {len(networks.get('production_networks', []))}")
    if email_settings:
        print(f"📧 Email configuré: {email_settings.get('to_email', 'N/A')}")

if __name__ == "__main__":
    main() 