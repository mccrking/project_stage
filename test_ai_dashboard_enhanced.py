#!/usr/bin/env python3
"""
Test pour vérifier les nouvelles fonctionnalités de l'AI Dashboard
"""
import requests
import json
import time
from datetime import datetime

def test_enhanced_ai_dashboard():
    """Test des nouvelles fonctionnalités de l'AI Dashboard"""
    base_url = "http://localhost:5000"
    
    print("🧠 Test des Nouvelles Fonctionnalités AI Dashboard")
    print("=" * 60)
    
    # 1. Connexion
    print("1. Connexion...")
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data)
        if response.status_code == 200:
            print("✅ Connexion réussie")
        else:
            print(f"❌ Échec de la connexion: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # 2. Test API équipements à risque élevé
    print("\n2. Test API équipements à risque élevé...")
    try:
        response = session.get(f"{base_url}/api/ai/high-risk-devices")
        if response.status_code == 200:
            devices = response.json()
            print(f"✅ API équipements à risque fonctionnelle")
            print(f"   - Nombre d'équipements à risque: {len(devices)}")
            if devices:
                print(f"   - Premier équipement: {devices[0]['ip']} (risque: {devices[0]['failure_probability']:.1%})")
        else:
            print(f"❌ Erreur API équipements à risque: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API équipements à risque: {e}")
    
    # 3. Test API équipements avec anomalies
    print("\n3. Test API équipements avec anomalies...")
    try:
        response = session.get(f"{base_url}/api/ai/anomaly-devices")
        if response.status_code == 200:
            devices = response.json()
            print(f"✅ API équipements anomalies fonctionnelle")
            print(f"   - Nombre d'équipements avec anomalies: {len(devices)}")
            if devices:
                print(f"   - Premier équipement: {devices[0]['ip']} (score anomalie: {devices[0]['anomaly_score']:.3f})")
        else:
            print(f"❌ Erreur API équipements anomalies: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API équipements anomalies: {e}")
    
    # 4. Test API statistiques dashboard IA
    print("\n4. Test API statistiques dashboard IA...")
    try:
        response = session.get(f"{base_url}/api/ai/dashboard-stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ API statistiques dashboard IA fonctionnelle")
            print(f"   - Score de santé moyen: {stats['avg_health_score']}%")
            print(f"   - Équipements critiques: {stats['critical_devices']}")
            print(f"   - Équipements à risque élevé: {stats['high_risk_devices_count']}")
            print(f"   - Équipements avec anomalies: {stats['anomaly_devices_count']}")
        else:
            print(f"❌ Erreur API statistiques dashboard IA: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API statistiques dashboard IA: {e}")
    
    # 5. Test API recommandations IA
    print("\n5. Test API recommandations IA...")
    try:
        response = session.post(f"{base_url}/api/ai/recommendations")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                recommendations = data.get('recommendations', [])
                print(f"✅ API recommandations IA fonctionnelle")
                print(f"   - Nombre de recommandations: {len(recommendations)}")
                if recommendations:
                    print(f"   - Première recommandation: {recommendations[0]['message'][:50]}...")
                    print(f"   - Priorité: {recommendations[0]['priority']}")
            else:
                print(f"⚠️  API recommandations IA: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"❌ Erreur API recommandations: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API recommandations: {e}")
    
    # 6. Test de la page AI Dashboard avec nouvelles fonctionnalités
    print("\n6. Test page AI Dashboard améliorée...")
    try:
        response = session.get(f"{base_url}/ai-dashboard")
        if response.status_code == 200:
            content = response.text
            print("✅ Page AI Dashboard accessible")
            
            # Vérifier les nouvelles fonctionnalités
            if "refreshHighRiskDevices" in content:
                print("✅ Fonction rafraîchissement équipements à risque présente")
            else:
                print("⚠️  Fonction rafraîchissement équipements à risque manquante")
                
            if "refreshAnomalyDevices" in content:
                print("✅ Fonction rafraîchissement équipements anomalies présente")
            else:
                print("⚠️  Fonction rafraîchissement équipements anomalies manquante")
                
            if "generateAIRecommendations" in content:
                print("✅ Fonction génération recommandations présente")
            else:
                print("⚠️  Fonction génération recommandations manquante")
                
            if "deviceTypeChart" in content:
                print("✅ Graphiques Chart.js présents")
            else:
                print("⚠️  Graphiques Chart.js manquants")
                
            if "updateAIDashboard" in content:
                print("✅ Fonction mise à jour automatique présente")
            else:
                print("⚠️  Fonction mise à jour automatique manquante")
                
        else:
            print(f"❌ Erreur accès page: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur page AI Dashboard: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test des Nouvelles Fonctionnalités AI Dashboard terminé")
    return True

if __name__ == "__main__":
    test_enhanced_ai_dashboard() 