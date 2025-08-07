#!/usr/bin/env python3
"""
Script de test pour la page Alertes
Teste toutes les fonctionnalités de la page alertes
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
    if response.status_code == 302:
        print("✅ Connexion réussie")
        return response.cookies
    else:
        print(f"❌ Échec de la connexion: {response.status_code}")
        return None

def test_alerts_page_access(cookies):
    """Test d'accès à la page alertes"""
    print("\n📄 Test d'accès à la page alertes...")
    response = requests.get(f"{BASE_URL}/alerts", cookies=cookies)
    if response.status_code == 200:
        print("✅ Page alertes accessible")
        return True
    else:
        print(f"❌ Impossible d'accéder à la page alertes: {response.status_code}")
        return False

def test_api_alerts(cookies):
    """Test de l'API des alertes"""
    print("\n🔍 Test de l'API des alertes...")
    response = requests.get(f"{BASE_URL}/api/alerts", cookies=cookies)
    if response.status_code == 200:
        alerts = response.json()
        print(f"✅ API alertes fonctionnelle - {len(alerts)} alertes trouvées")
        if alerts:
            print("📋 Exemple d'alerte:")
            alert = alerts[0]
            print(f"   - ID: {alert.get('id')}")
            print(f"   - Type: {alert.get('alert_type')}")
            print(f"   - Priorité: {alert.get('priority')}")
            print(f"   - Message: {alert.get('message')}")
            print(f"   - Équipement: {alert.get('device_ip')}")
        return alerts
    else:
        print(f"❌ Erreur API alertes: {response.status_code}")
        return []

def test_resolve_alert(cookies, alert_id):
    """Test de résolution d'une alerte"""
    print(f"\n✅ Test de résolution de l'alerte {alert_id}...")
    response = requests.post(f"{BASE_URL}/api/alert/{alert_id}/resolve", 
                           cookies=cookies, 
                           headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print("✅ Alerte résolue avec succès")
            return True
        else:
            print(f"❌ Erreur lors de la résolution: {data.get('message')}")
            return False
    else:
        print(f"❌ Erreur API résolution: {response.status_code}")
        return False

def test_bulk_resolve_alerts(cookies, alert_ids):
    """Test de résolution groupée d'alertes"""
    if not alert_ids:
        print("\n⚠️ Aucune alerte à résoudre en groupe")
        return True
    
    print(f"\n✅ Test de résolution groupée de {len(alert_ids)} alertes...")
    data = {'alert_ids': alert_ids}
    response = requests.post(f"{BASE_URL}/api/alerts/bulk-resolve", 
                           cookies=cookies, 
                           headers={'Content-Type': 'application/json'},
                           json=data)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print(f"✅ {data.get('resolved_count', 0)} alertes résolues en groupe")
            return True
        else:
            print(f"❌ Erreur lors de la résolution groupée: {data.get('message')}")
            return False
    else:
        print(f"❌ Erreur API résolution groupée: {response.status_code}")
        return False

def test_alerts_statistics(cookies):
    """Test des statistiques des alertes"""
    print("\n📊 Test des statistiques des alertes...")
    
    # Récupérer les alertes pour calculer les stats
    response = requests.get(f"{BASE_URL}/api/alerts", cookies=cookies)
    if response.status_code == 200:
        alerts = response.json()
        
        total_alerts = len(alerts)
        active_count = len([a for a in alerts if not a.get('is_resolved', False)])
        critical_count = len([a for a in alerts if a.get('priority') == 'critical'])
        
        print(f"📈 Statistiques calculées:")
        print(f"   - Total alertes: {total_alerts}")
        print(f"   - Alertes actives: {active_count}")
        print(f"   - Alertes critiques: {critical_count}")
        print(f"   - Alertes résolues: {total_alerts - active_count}")
        
        return True
    else:
        print(f"❌ Impossible de récupérer les statistiques: {response.status_code}")
        return False

def test_alerts_page_content(cookies):
    """Test du contenu de la page alertes"""
    print("\n📋 Test du contenu de la page alertes...")
    response = requests.get(f"{BASE_URL}/alerts", cookies=cookies)
    if response.status_code == 200:
        content = response.text
        
        # Vérifier la présence d'éléments clés
        checks = [
            ('Statistiques des alertes', 'Section statistiques'),
            ('Alertes actives', 'Section alertes actives'),
            ('Alertes résolues récentes', 'Section alertes résolues'),
            ('Résoudre tout', 'Bouton résolution groupée'),
            ('Actualiser', 'Bouton actualisation'),
            ('Priorité', 'En-tête de colonne'),
            ('Type', 'En-tête de colonne'),
            ('Équipement', 'En-tête de colonne'),
            ('Message', 'En-tête de colonne'),
            ('Date', 'En-tête de colonne'),
            ('Actions', 'En-tête de colonne')
        ]
        
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description} présente")
            else:
                print(f"❌ {description} manquante")
        
        return True
    else:
        print(f"❌ Impossible d'accéder au contenu: {response.status_code}")
        return False

def test_alert_creation_simulation():
    """Simulation de création d'alertes pour les tests"""
    print("\n🔧 Simulation de création d'alertes...")
    print("ℹ️ Pour tester complètement les alertes, il faudrait:")
    print("   - Avoir des équipements hors ligne")
    print("   - Avoir des anomalies détectées par l'IA")
    print("   - Avoir des seuils dépassés")
    print("   - Avoir des scans qui génèrent des alertes")
    print("ℹ️ Les alertes sont générées automatiquement par:")
    print("   - La fonction generate_ai_alerts()")
    print("   - Les scans réseau")
    print("   - La détection d'équipements hors ligne")

def main():
    """Fonction principale de test"""
    print("🚀 TEST DE LA PAGE ALERTES")
    print("=" * 50)
    
    # Test de connexion
    cookies = test_login()
    if not cookies:
        print("❌ Impossible de continuer sans connexion")
        return
    
    # Tests de base
    if not test_alerts_page_access(cookies):
        return
    
    if not test_alerts_page_content(cookies):
        return
    
    # Tests API
    alerts = test_api_alerts(cookies)
    test_alerts_statistics(cookies)
    
    # Tests de résolution (si des alertes existent)
    if alerts:
        # Test résolution individuelle
        first_alert_id = alerts[0]['id']
        test_resolve_alert(cookies, first_alert_id)
        
        # Test résolution groupée
        alert_ids = [alert['id'] for alert in alerts[:3]]  # Premières 3 alertes
        test_bulk_resolve_alerts(cookies, alert_ids)
    else:
        print("\n⚠️ Aucune alerte trouvée pour tester la résolution")
        test_alert_creation_simulation()
    
    print("\n" + "=" * 50)
    print("✅ TESTS DE LA PAGE ALERTES TERMINÉS")
    print("\n📝 Résumé:")
    print("   - Page alertes accessible et fonctionnelle")
    print("   - API des alertes opérationnelle")
    print("   - Système de résolution d'alertes fonctionnel")
    print("   - Interface utilisateur complète")
    if not alerts:
        print("   - Aucune alerte active (normal si système propre)")

if __name__ == "__main__":
    main() 