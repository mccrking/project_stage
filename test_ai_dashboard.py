#!/usr/bin/env python3
"""
Test pour vérifier le fonctionnement de la page AI Dashboard
"""
import requests
import json
import time
from datetime import datetime

def test_ai_dashboard():
    """Test complet de la page AI Dashboard"""
    base_url = "http://localhost:5000"
    
    print("🧠 Test de la page AI Dashboard")
    print("=" * 50)
    
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
    
    # 2. Test de la page AI Dashboard
    print("\n2. Test de la page AI Dashboard...")
    try:
        response = session.get(f"{base_url}/ai-dashboard")
        if response.status_code == 200:
            print("✅ Page AI Dashboard accessible")
            
            # Vérifier le contenu
            if "Intelligence Artificielle" in response.text:
                print("✅ Contenu IA détecté")
            else:
                print("⚠️  Contenu IA non trouvé")
                
            if "Score Santé Moyen" in response.text:
                print("✅ Statistiques IA présentes")
            else:
                print("⚠️  Statistiques IA manquantes")
                
        else:
            print(f"❌ Erreur accès page: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur page AI Dashboard: {e}")
        return False
    
    # 3. Test API entraînement IA
    print("\n3. Test API entraînement IA...")
    try:
        response = session.post(f"{base_url}/api/ai/train")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("✅ API entraînement IA fonctionnelle")
            else:
                print(f"⚠️  API entraînement IA: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"❌ Erreur API entraînement: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API entraînement: {e}")
    
    # 4. Test API analyse IA d'un équipement
    print("\n4. Test API analyse IA équipement...")
    try:
        # Récupérer la liste des équipements
        response = session.get(f"{base_url}/api/devices")
        if response.status_code == 200:
            devices = response.json()
            if devices:
                device_id = devices[0]['id']
                print(f"   Test avec l'équipement ID: {device_id}")
                
                # Test analyse IA
                response = session.get(f"{base_url}/api/device/{device_id}/ai-analysis")
                if response.status_code == 200:
                    analysis = response.json()
                    if 'error' not in analysis:
                        print("✅ API analyse IA fonctionnelle")
                        print(f"   - Type d'équipement: {analysis.get('classification', {}).get('device_type', 'N/A')}")
                        print(f"   - Score de santé: {analysis.get('health_score', 'N/A')}")
                        print(f"   - Probabilité de panne: {analysis.get('maintenance_analysis', {}).get('failure_probability', 'N/A')}")
                    else:
                        print(f"⚠️  Erreur analyse IA: {analysis['error']}")
                else:
                    print(f"❌ Erreur API analyse: {response.status_code}")
            else:
                print("⚠️  Aucun équipement trouvé pour le test")
        else:
            print(f"❌ Erreur récupération équipements: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur test analyse IA: {e}")
    
    # 5. Test API statistiques
    print("\n5. Test API statistiques...")
    try:
        response = session.get(f"{base_url}/api/statistics")
        if response.status_code == 200:
            stats = response.json()
            print("✅ API statistiques fonctionnelle")
            print(f"   - Total équipements: {stats.get('total_devices', 'N/A')}")
            print(f"   - Équipements en ligne: {stats.get('online_devices', 'N/A')}")
            print(f"   - Pourcentage disponibilité: {stats.get('uptime_percentage', 'N/A')}%")
        else:
            print(f"❌ Erreur API statistiques: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API statistiques: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test AI Dashboard terminé")
    return True

if __name__ == "__main__":
    test_ai_dashboard() 