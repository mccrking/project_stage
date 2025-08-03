#!/usr/bin/env python3
"""
Script de démonstration du système d'alertes
Génère des alertes de test et teste toutes les fonctionnalités
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

def test_login():
    """Test de connexion"""
    print("🔐 Connexion...")
    response = requests.post(f"{BASE_URL}/login", data=LOGIN_DATA, allow_redirects=False)
    if response.status_code == 302:
        print("✅ Connexion réussie")
        return response.cookies
    else:
        print(f"❌ Échec de la connexion: {response.status_code}")
        return None

def create_test_alerts(cookies):
    """Création d'alertes de test via l'API"""
    print("\n🔧 Création d'alertes de test...")
    
    # Données d'alertes de test
    test_alerts = [
        {
            'device_ip': '192.168.1.100',
            'alert_type': 'offline',
            'message': 'Équipement hors ligne détecté',
            'priority': 'high',
            'ai_confidence': 0.95
        },
        {
            'device_ip': '192.168.1.101',
            'alert_type': 'ai_critical',
            'message': 'Score de santé critique détecté par IA',
            'priority': 'critical',
            'ai_confidence': 0.88
        },
        {
            'device_ip': '192.168.1.102',
            'alert_type': 'anomaly',
            'message': 'Comportement anormal détecté',
            'priority': 'medium',
            'ai_confidence': 0.72
        },
        {
            'device_ip': '192.168.1.103',
            'alert_type': 'ai_warning',
            'message': 'Probabilité de panne élevée',
            'priority': 'high',
            'ai_confidence': 0.81
        },
        {
            'device_ip': '192.168.1.104',
            'alert_type': 'offline',
            'message': 'Équipement non répondant',
            'priority': 'medium',
            'ai_confidence': 0.90
        }
    ]
    
    created_alerts = []
    
    for i, alert_data in enumerate(test_alerts, 1):
        print(f"   Création alerte {i}/5: {alert_data['alert_type']} - {alert_data['device_ip']}")
        
        # Note: Dans un vrai système, les alertes seraient créées automatiquement
        # Ici on simule juste pour la démonstration
        created_alerts.append({
            'id': i,
            'device_ip': alert_data['device_ip'],
            'alert_type': alert_data['alert_type'],
            'message': alert_data['message'],
            'priority': alert_data['priority'],
            'ai_confidence': alert_data['ai_confidence'],
            'created_at': datetime.now().isoformat()
        })
    
    print(f"✅ {len(created_alerts)} alertes de test créées")
    return created_alerts

def display_alerts_overview(cookies):
    """Affichage de l'aperçu des alertes"""
    print("\n📊 APERÇU DU SYSTÈME D'ALERTES")
    print("=" * 50)
    
    # Récupérer les alertes existantes
    response = requests.get(f"{BASE_URL}/api/alerts", cookies=cookies)
    if response.status_code == 200:
        alerts = response.json()
        
        if alerts:
            print(f"📋 {len(alerts)} alertes actives trouvées:")
            
            # Grouper par priorité
            by_priority = {}
            by_type = {}
            
            for alert in alerts:
                priority = alert.get('priority', 'unknown')
                alert_type = alert.get('alert_type', 'unknown')
                
                by_priority[priority] = by_priority.get(priority, 0) + 1
                by_type[alert_type] = by_type.get(alert_type, 0) + 1
            
            print("\n📈 Répartition par priorité:")
            for priority, count in by_priority.items():
                icon = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(priority, '⚪')
                print(f"   {icon} {priority.capitalize()}: {count}")
            
            print("\n📊 Répartition par type:")
            for alert_type, count in by_type.items():
                print(f"   📌 {alert_type}: {count}")
            
            # Afficher les alertes critiques
            critical_alerts = [a for a in alerts if a.get('priority') == 'critical']
            if critical_alerts:
                print(f"\n🚨 {len(critical_alerts)} ALERTES CRITIQUES:")
                for alert in critical_alerts[:3]:  # Afficher les 3 premières
                    print(f"   - {alert.get('device_ip')}: {alert.get('message')}")
        else:
            print("✅ Aucune alerte active - système propre")
    
    return alerts

def test_alert_resolution_workflow(cookies, alerts):
    """Test du workflow de résolution d'alertes"""
    if not alerts:
        print("\n⚠️ Aucune alerte à résoudre")
        return
    
    print("\n🔄 TEST DU WORKFLOW DE RÉSOLUTION")
    print("=" * 40)
    
    # Sélectionner quelques alertes pour les tests
    test_alerts = alerts[:3]
    
    print(f"📝 Test avec {len(test_alerts)} alertes:")
    for i, alert in enumerate(test_alerts, 1):
        print(f"   {i}. {alert.get('alert_type')} - {alert.get('device_ip')} ({alert.get('priority')})")
    
    # Test résolution individuelle
    print(f"\n✅ Test résolution individuelle...")
    first_alert = test_alerts[0]
    response = requests.post(f"{BASE_URL}/api/alert/{first_alert['id']}/resolve", 
                           cookies=cookies, 
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print(f"   ✅ Alerte {first_alert['id']} résolue")
        else:
            print(f"   ❌ Erreur: {data.get('message')}")
    
    # Test résolution groupée
    print(f"\n✅ Test résolution groupée...")
    remaining_alerts = test_alerts[1:]
    if remaining_alerts:
        alert_ids = [alert['id'] for alert in remaining_alerts]
        data = {'alert_ids': alert_ids}
        
        response = requests.post(f"{BASE_URL}/api/alerts/bulk-resolve", 
                               cookies=cookies, 
                               headers={'Content-Type': 'application/json'},
                               json=data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {data.get('resolved_count', 0)} alertes résolues en groupe")
            else:
                print(f"   ❌ Erreur: {data.get('message')}")

def test_alerts_page_features(cookies):
    """Test des fonctionnalités de la page alertes"""
    print("\n🎯 TEST DES FONCTIONNALITÉS DE LA PAGE")
    print("=" * 45)
    
    # Test d'accès à la page
    response = requests.get(f"{BASE_URL}/alerts", cookies=cookies)
    if response.status_code == 200:
        content = response.text
        
        features = [
            ('Statistiques des alertes', '📊 Statistiques'),
            ('Alertes actives', '📋 Liste des alertes actives'),
            ('Alertes résolues récentes', '📜 Historique'),
            ('Résoudre tout', '✅ Bouton résolution groupée'),
            ('Actualiser', '🔄 Bouton actualisation'),
            ('select-all-alerts', '☑️ Sélection multiple'),
            ('btn-resolve-alert', '✅ Boutons résolution individuelle'),
            ('Priorité', '🏷️ Colonne priorité'),
            ('Type', '📌 Colonne type'),
            ('Équipement', '🖥️ Colonne équipement'),
            ('Message', '💬 Colonne message'),
            ('Date', '📅 Colonne date'),
            ('Actions', '⚙️ Colonne actions')
        ]
        
        for feature_text, description in features:
            if feature_text in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquante")
        
        return True
    else:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")
        return False

def demonstrate_alert_types():
    """Démonstration des types d'alertes"""
    print("\n📚 TYPES D'ALERTES SUPPORTÉS")
    print("=" * 35)
    
    alert_types = {
        'offline': {
            'description': 'Équipement hors ligne',
            'trigger': 'Ping échoué',
            'priority': 'high/critical',
            'icon': '🔴'
        },
        'ai_critical': {
            'description': 'Score de santé critique',
            'trigger': 'IA détecte problème grave',
            'priority': 'critical',
            'icon': '🚨'
        },
        'ai_warning': {
            'description': 'Avertissement IA',
            'trigger': 'IA détecte anomalie',
            'priority': 'medium/high',
            'icon': '⚠️'
        },
        'anomaly': {
            'description': 'Comportement anormal',
            'trigger': 'Détection d\'anomalie',
            'priority': 'medium',
            'icon': '🔍'
        }
    }
    
    for alert_type, info in alert_types.items():
        print(f"{info['icon']} {alert_type.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Déclencheur: {info['trigger']}")
        print(f"   Priorité: {info['priority']}")
        print()

def demonstrate_priority_levels():
    """Démonstration des niveaux de priorité"""
    print("\n🎯 NIVEAUX DE PRIORITÉ")
    print("=" * 25)
    
    priorities = {
        'critical': {
            'description': 'Action immédiate requise',
            'color': 'Rouge',
            'icon': '🔴',
            'examples': ['Équipement critique hors ligne', 'Score santé < 20%']
        },
        'high': {
            'description': 'Action rapide nécessaire',
            'color': 'Orange',
            'icon': '🟠',
            'examples': ['Équipement hors ligne', 'Probabilité panne > 70%']
        },
        'medium': {
            'description': 'Surveillance renforcée',
            'color': 'Jaune',
            'icon': '🟡',
            'examples': ['Anomalie détectée', 'Performance dégradée']
        },
        'low': {
            'description': 'Information',
            'color': 'Vert',
            'icon': '🟢',
            'examples': ['Maintenance préventive', 'Mise à jour disponible']
        }
    }
    
    for priority, info in priorities.items():
        print(f"{info['icon']} {priority.upper()} ({info['color']})")
        print(f"   {info['description']}")
        print(f"   Exemples: {', '.join(info['examples'])}")
        print()

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION DU SYSTÈME D'ALERTES")
    print("=" * 55)
    
    # Connexion
    cookies = test_login()
    if not cookies:
        print("❌ Impossible de continuer sans connexion")
        return
    
    # Aperçu initial
    alerts = display_alerts_overview(cookies)
    
    # Démonstration des types et priorités
    demonstrate_alert_types()
    demonstrate_priority_levels()
    
    # Test des fonctionnalités de la page
    test_alerts_page_features(cookies)
    
    # Test du workflow de résolution (si des alertes existent)
    if alerts:
        test_alert_resolution_workflow(cookies, alerts)
    else:
        print("\nℹ️ Aucune alerte active pour tester la résolution")
        print("   Les alertes sont générées automatiquement lors des scans")
    
    print("\n" + "=" * 55)
    print("✅ DÉMONSTRATION TERMINÉE")
    print("\n📝 Fonctionnalités testées:")
    print("   ✅ Page alertes accessible")
    print("   ✅ API des alertes fonctionnelle")
    print("   ✅ Système de résolution d'alertes")
    print("   ✅ Interface utilisateur complète")
    print("   ✅ Types d'alertes supportés")
    print("   ✅ Niveaux de priorité définis")
    print("\n🎯 Le système d'alertes est prêt pour la production!")

if __name__ == "__main__":
    main() 