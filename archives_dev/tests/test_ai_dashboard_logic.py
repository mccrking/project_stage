#!/usr/bin/env python3
"""
Test de Cohérence Logique du Dashboard IA
Vérifie que toutes les logiques du dashboard IA sont cohérentes
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
LOGIN_DATA = {
    "username": "admin",
    "password": "admin123"
}

def test_login():
    """Test de connexion"""
    print("🔐 Test de connexion...")
    try:
        response = requests.post(f"{BASE_URL}/login", data=LOGIN_DATA, allow_redirects=False)
        if response.status_code == 302:  # Redirection après connexion réussie
            print("✅ Connexion réussie")
            return response.cookies
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def test_ai_dashboard_access(cookies):
    """Test d'accès au dashboard IA"""
    print("\n📊 Test d'accès au dashboard IA...")
    try:
        response = requests.get(f"{BASE_URL}/ai-dashboard", cookies=cookies)
        if response.status_code == 200:
            print("✅ Accès au dashboard IA réussi")
            return True
        else:
            print(f"❌ Échec d'accès: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur d'accès: {e}")
        return False

def test_ai_statistics_consistency(cookies):
    """Test de cohérence des statistiques IA"""
    print("\n📈 Test de cohérence des statistiques IA...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/dashboard-stats", cookies=cookies)
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Statistiques récupérées:")
            print(f"   - Score santé moyen: {stats.get('avg_health_score', 'N/A')}%")
            print(f"   - Équipements critiques: {stats.get('critical_devices', 'N/A')}")
            print(f"   - Risque élevé: {stats.get('high_risk_devices_count', 'N/A')}")
            print(f"   - Anomalies: {stats.get('anomaly_devices_count', 'N/A')}")
            
            # Vérifications de cohérence
            issues = []
            
            # Score de santé doit être entre 0 et 100
            if stats.get('avg_health_score', 0) < 0 or stats.get('avg_health_score', 0) > 100:
                issues.append("Score de santé moyen hors limites (0-100)")
            
            # Les compteurs doivent être >= 0
            if stats.get('critical_devices', -1) < 0:
                issues.append("Nombre d'équipements critiques négatif")
            if stats.get('high_risk_devices_count', -1) < 0:
                issues.append("Nombre d'équipements à risque négatif")
            if stats.get('anomaly_devices_count', -1) < 0:
                issues.append("Nombre d'anomalies négatif")
            
            if issues:
                print("⚠️  Problèmes de cohérence détectés:")
                for issue in issues:
                    print(f"   - {issue}")
                return False
            else:
                print("✅ Statistiques cohérentes")
                return True
        else:
            print(f"❌ Échec récupération statistiques: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")
        return False

def test_high_risk_devices_logic(cookies):
    """Test de la logique des équipements à risque élevé"""
    print("\n⚠️  Test de la logique des équipements à risque élevé...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/high-risk-devices", cookies=cookies)
        if response.status_code == 200:
            devices = response.json()
            print(f"📋 {len(devices)} équipements à risque élevé trouvés")
            
            # Vérifications de cohérence
            issues = []
            for device in devices:
                # Probabilité de panne doit être > 0.6 (seuil configuré)
                if device.get('failure_probability', 0) <= 0.6:
                    issues.append(f"Équipement {device.get('ip', 'N/A')}: probabilité de panne <= 0.6")
                
                # Score de santé doit être cohérent
                if device.get('health_score', 100) < 0 or device.get('health_score', 100) > 100:
                    issues.append(f"Équipement {device.get('ip', 'N/A')}: score de santé hors limites")
            
            if issues:
                print("⚠️  Problèmes de cohérence détectés:")
                for issue in issues:
                    print(f"   - {issue}")
                return False
            else:
                print("✅ Logique des équipements à risque cohérente")
                return True
        else:
            print(f"❌ Échec récupération équipements à risque: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur équipements à risque: {e}")
        return False

def test_anomaly_devices_logic(cookies):
    """Test de la logique des équipements avec anomalies"""
    print("\n🔍 Test de la logique des équipements avec anomalies...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/anomaly-devices", cookies=cookies)
        if response.status_code == 200:
            devices = response.json()
            print(f"📋 {len(devices)} équipements avec anomalies trouvés")
            
            # Vérifications de cohérence
            issues = []
            for device in devices:
                # Score d'anomalie doit être < -0.5 (seuil configuré)
                if device.get('anomaly_score', 0) >= -0.5:
                    issues.append(f"Équipement {device.get('ip', 'N/A')}: score d'anomalie >= -0.5")
                
                # Score de santé doit être cohérent
                if device.get('health_score', 100) < 0 or device.get('health_score', 100) > 100:
                    issues.append(f"Équipement {device.get('ip', 'N/A')}: score de santé hors limites")
            
            if issues:
                print("⚠️  Problèmes de cohérence détectés:")
                for issue in issues:
                    print(f"   - {issue}")
                return False
            else:
                print("✅ Logique des anomalies cohérente")
                return True
        else:
            print(f"❌ Échec récupération anomalies: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur anomalies: {e}")
        return False

def test_chart_data_consistency(cookies):
    """Test de cohérence des données des graphiques"""
    print("\n📊 Test de cohérence des données des graphiques...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/chart-data", cookies=cookies)
        if response.status_code == 200:
            chart_data = response.json()
            
            # Vérification des types d'équipements
            device_types = chart_data.get('device_types', {})
            if 'labels' in device_types and 'data' in device_types:
                print(f"📈 Types d'équipements: {len(device_types['labels'])} catégories")
                
                # Vérifier que les données correspondent aux labels
                if len(device_types['labels']) != len(device_types['data']):
                    print("⚠️  Nombre de labels et données incohérent pour les types d'équipements")
                    return False
            
            # Vérification des scores de santé
            health_scores = chart_data.get('health_scores', {})
            if 'labels' in health_scores and 'data' in health_scores:
                print(f"📈 Scores de santé: {len(health_scores['labels'])} catégories")
                
                # Vérifier que les données correspondent aux labels
                if len(health_scores['labels']) != len(health_scores['data']):
                    print("⚠️  Nombre de labels et données incohérent pour les scores de santé")
                    return False
                
                # Vérifier que la somme des équipements est cohérente
                total_devices = sum(health_scores['data'])
                print(f"📊 Total équipements dans le graphique: {total_devices}")
            
            print("✅ Données des graphiques cohérentes")
            return True
        else:
            print(f"❌ Échec récupération données graphiques: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur données graphiques: {e}")
        return False

def test_ai_recommendations_logic(cookies):
    """Test de la logique des recommandations IA"""
    print("\n💡 Test de la logique des recommandations IA...")
    try:
        response = requests.post(f"{BASE_URL}/api/ai/recommendations", cookies=cookies)
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                recommendations = result.get('recommendations', [])
                print(f"💡 {len(recommendations)} recommandations générées")
                
                # Vérifications de cohérence
                issues = []
                for rec in recommendations:
                    # Vérifier les champs requis
                    required_fields = ['device_ip', 'message', 'priority', 'actions']
                    for field in required_fields:
                        if field not in rec:
                            issues.append(f"Recommandation manque le champ: {field}")
                    
                    # Vérifier la priorité
                    valid_priorities = ['critical', 'high', 'medium', 'low']
                    if rec.get('priority') not in valid_priorities:
                        issues.append(f"Priorité invalide: {rec.get('priority')}")
                
                if issues:
                    print("⚠️  Problèmes de cohérence détectés:")
                    for issue in issues:
                        print(f"   - {issue}")
                    return False
                else:
                    print("✅ Logique des recommandations cohérente")
                    return True
            else:
                print(f"❌ Échec génération recommandations: {result.get('message', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Échec requête recommandations: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur recommandations: {e}")
        return False

def test_ai_analysis_consistency(cookies):
    """Test de cohérence de l'analyse IA"""
    print("\n🧠 Test de cohérence de l'analyse IA...")
    try:
        # Récupérer un équipement pour test
        response = requests.get(f"{BASE_URL}/api/devices", cookies=cookies)
        if response.status_code == 200:
            devices = response.json()
            if devices:
                test_device = devices[0]
                device_id = test_device.get('id')
                
                # Analyser l'équipement
                analysis_response = requests.get(f"{BASE_URL}/api/device/{device_id}/ai-analysis", cookies=cookies)
                if analysis_response.status_code == 200:
                    analysis = analysis_response.json()
                    
                    # Vérifications de cohérence
                    issues = []
                    
                    # Score de santé doit être entre 0 et 100
                    health_score = analysis.get('health_score', 0)
                    if health_score < 0 or health_score > 100:
                        issues.append(f"Score de santé hors limites: {health_score}")
                    
                    # Confiance IA doit être entre 0 et 1
                    ai_confidence = analysis.get('ai_confidence', 0)
                    if ai_confidence < 0 or ai_confidence > 1:
                        issues.append(f"Confiance IA hors limites: {ai_confidence}")
                    
                    # Probabilité de panne doit être entre 0 et 1
                    failure_prob = analysis.get('maintenance_analysis', {}).get('failure_probability', 0)
                    if failure_prob < 0 or failure_prob > 1:
                        issues.append(f"Probabilité de panne hors limites: {failure_prob}")
                    
                    if issues:
                        print("⚠️  Problèmes de cohérence détectés:")
                        for issue in issues:
                            print(f"   - {issue}")
                        return False
                    else:
                        print("✅ Analyse IA cohérente")
                        return True
                else:
                    print(f"❌ Échec analyse IA: {analysis_response.status_code}")
                    return False
            else:
                print("⚠️  Aucun équipement disponible pour test")
                return True
        else:
            print(f"❌ Échec récupération équipements: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur analyse IA: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🔍 TEST DE COHÉRENCE LOGIQUE DU DASHBOARD IA")
    print("=" * 50)
    
    # Test de connexion
    cookies = test_login()
    if not cookies:
        print("\n❌ Impossible de continuer sans connexion")
        return
    
    print(f"🍪 Cookies de session: {cookies}")
    
    # Tests de cohérence
    tests = [
        test_ai_dashboard_access,
        test_ai_statistics_consistency,
        test_high_risk_devices_logic,
        test_anomaly_devices_logic,
        test_chart_data_consistency,
        test_ai_recommendations_logic,
        test_ai_analysis_consistency
    ]
    
    results = []
    for test in tests:
        try:
            result = test(cookies)
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DES TESTS DE COHÉRENCE")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS DE COHÉRENCE SONT PASSÉS!")
        print("✅ Le dashboard IA est logiquement cohérent")
    else:
        print(f"\n⚠️  {total - passed} PROBLÈME(S) DE COHÉRENCE DÉTECTÉ(S)")
        print("🔧 Des corrections sont nécessaires")
    
    print(f"\n📅 Test effectué le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 