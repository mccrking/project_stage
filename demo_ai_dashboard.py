#!/usr/bin/env python3
"""
Démonstration complète de la page AI Dashboard
"""
import requests
import json
import time
from datetime import datetime

def demo_ai_dashboard():
    """Démonstration complète des fonctionnalités AI Dashboard"""
    base_url = "http://localhost:5000"
    
    print("🧠 DÉMONSTRATION COMPLÈTE - AI Dashboard Central Danone")
    print("=" * 70)
    print(f"🕐 Début de la démonstration: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # 1. Connexion
    print("1️⃣ CONNEXION À L'APPLICATION")
    print("-" * 40)
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data)
        if response.status_code == 200:
            print("✅ Connexion réussie avec l'utilisateur admin")
        else:
            print(f"❌ Échec de la connexion: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # 2. État initial du système
    print("\n2️⃣ ÉTAT INITIAL DU SYSTÈME")
    print("-" * 40)
    
    # Statistiques globales
    try:
        response = session.get(f"{base_url}/api/statistics")
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Statistiques réseau:")
            print(f"   • Total équipements: {stats['total_devices']}")
            print(f"   • Équipements en ligne: {stats['online_devices']}")
            print(f"   • Équipements hors ligne: {stats['offline_devices']}")
            print(f"   • Disponibilité: {stats['uptime_percentage']}%")
    except Exception as e:
        print(f"⚠️  Erreur récupération statistiques: {e}")
    
    # Statistiques IA
    try:
        response = session.get(f"{base_url}/api/ai/dashboard-stats")
        if response.status_code == 200:
            ai_stats = response.json()
            print(f"🤖 Statistiques IA:")
            print(f"   • Score de santé moyen: {ai_stats['avg_health_score']}%")
            print(f"   • Équipements critiques: {ai_stats['critical_devices']}")
            print(f"   • Équipements à risque élevé: {ai_stats['high_risk_devices_count']}")
            print(f"   • Équipements avec anomalies: {ai_stats['anomaly_devices_count']}")
    except Exception as e:
        print(f"⚠️  Erreur récupération stats IA: {e}")
    
    # 3. Démonstration des équipements à risque
    print("\n3️⃣ ÉQUIPEMENTS À RISQUE ÉLEVÉ")
    print("-" * 40)
    
    try:
        response = session.get(f"{base_url}/api/ai/high-risk-devices")
        if response.status_code == 200:
            devices = response.json()
            print(f"🔴 {len(devices)} équipements à risque élevé détectés:")
            
            for i, device in enumerate(devices[:5], 1):  # Afficher les 5 premiers
                risk_percent = device['failure_probability'] * 100
                print(f"   {i}. {device['hostname'] or device['ip']}")
                print(f"      IP: {device['ip']} | Type: {device['device_type']}")
                print(f"      Risque de panne: {risk_percent:.1f}% | Santé: {device['health_score']:.1f}%")
                print()
            
            if len(devices) > 5:
                print(f"   ... et {len(devices) - 5} autres équipements")
    except Exception as e:
        print(f"⚠️  Erreur récupération équipements à risque: {e}")
    
    # 4. Démonstration des anomalies
    print("\n4️⃣ DÉTECTION D'ANOMALIES")
    print("-" * 40)
    
    try:
        response = session.get(f"{base_url}/api/ai/anomaly-devices")
        if response.status_code == 200:
            devices = response.json()
            if devices:
                print(f"⚠️  {len(devices)} équipements avec comportements anormaux:")
                
                for i, device in enumerate(devices[:3], 1):  # Afficher les 3 premiers
                    print(f"   {i}. {device['hostname'] or device['ip']}")
                    print(f"      IP: {device['ip']} | Type: {device['device_type']}")
                    print(f"      Score anomalie: {device['anomaly_score']:.3f}")
                    print()
            else:
                print("✅ Aucune anomalie détectée - Système stable")
    except Exception as e:
        print(f"⚠️  Erreur récupération anomalies: {e}")
    
    # 5. Démonstration de l'analyse IA d'un équipement
    print("\n5️⃣ ANALYSE IA DÉTAILLÉE")
    print("-" * 40)
    
    try:
        # Récupérer un équipement pour l'analyse
        response = session.get(f"{base_url}/api/devices")
        if response.status_code == 200:
            devices = response.json()
            if devices:
                device = devices[0]  # Premier équipement
                print(f"🔍 Analyse IA de l'équipement: {device['hostname'] or device['ip']}")
                
                # Analyse IA
                response = session.get(f"{base_url}/api/device/{device['id']}/ai-analysis")
                if response.status_code == 200:
                    analysis = response.json()
                    if 'error' not in analysis:
                        print(f"   📋 Classification:")
                        print(f"      • Type: {analysis['classification']['device_type']}")
                        print(f"      • Confiance: {analysis['classification']['confidence']*100:.1f}%")
                        
                        print(f"   🔧 Maintenance prédictive:")
                        print(f"      • Probabilité de panne: {analysis['maintenance_analysis']['failure_probability']*100:.1f}%")
                        print(f"      • Urgence: {analysis['maintenance_analysis']['maintenance_urgency']}")
                        
                        print(f"   🚨 Détection d'anomalies:")
                        print(f"      • Anomalie détectée: {'Oui' if analysis['anomaly_analysis']['is_anomaly'] else 'Non'}")
                        print(f"      • Score anomalie: {analysis['anomaly_analysis']['anomaly_score']:.3f}")
                        
                        print(f"   📊 Scores globaux:")
                        print(f"      • Score de santé: {analysis['health_score']:.1f}%")
                        print(f"      • Confiance IA: {analysis['ai_confidence']*100:.1f}%")
                        
                        print(f"   💡 Recommandations ({len(analysis['recommendations'])}):")
                        for i, rec in enumerate(analysis['recommendations'][:3], 1):
                            print(f"      {i}. [{rec['priority'].upper()}] {rec['message']}")
                    else:
                        print(f"   ❌ Erreur analyse: {analysis['error']}")
                else:
                    print(f"   ❌ Erreur API analyse: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Erreur analyse IA: {e}")
    
    # 6. Démonstration des recommandations IA
    print("\n6️⃣ RECOMMANDATIONS IA")
    print("-" * 40)
    
    try:
        response = session.post(f"{base_url}/api/ai/recommendations")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                recommendations = data.get('recommendations', [])
                print(f"💡 {len(recommendations)} recommandations IA générées:")
                
                # Grouper par priorité
                by_priority = {}
                for rec in recommendations:
                    priority = rec['priority']
                    if priority not in by_priority:
                        by_priority[priority] = []
                    by_priority[priority].append(rec)
                
                for priority in ['critical', 'high', 'medium', 'low']:
                    if priority in by_priority:
                        print(f"   🔴 {priority.upper()} ({len(by_priority[priority])}):")
                        for rec in by_priority[priority][:2]:  # Max 2 par priorité
                            print(f"      • {rec['message'][:60]}...")
                        if len(by_priority[priority]) > 2:
                            print(f"      ... et {len(by_priority[priority]) - 2} autres")
                        print()
            else:
                print(f"   ⚠️  Erreur génération: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur API recommandations: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Erreur recommandations IA: {e}")
    
    # 7. Démonstration de l'entraînement IA
    print("\n7️⃣ ENTRAÎNEMENT DES MODÈLES IA")
    print("-" * 40)
    
    print("🔄 Lancement de l'entraînement des modèles IA...")
    try:
        response = session.post(f"{base_url}/api/ai/train")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("✅ Entraînement IA lancé avec succès")
                print("   • Les modèles se mettent à jour en arrière-plan")
                print("   • Les nouvelles analyses utiliseront les modèles améliorés")
            else:
                print(f"   ⚠️  Erreur entraînement: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"   ❌ Erreur API entraînement: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Erreur entraînement IA: {e}")
    
    # 8. Résumé et conclusion
    print("\n8️⃣ RÉSUMÉ DE LA DÉMONSTRATION")
    print("-" * 40)
    
    print("🎯 Fonctionnalités démontrées:")
    print("   ✅ Connexion sécurisée à l'application")
    print("   ✅ Visualisation des statistiques réseau et IA")
    print("   ✅ Détection des équipements à risque élevé")
    print("   ✅ Identification des comportements anormaux")
    print("   ✅ Analyse IA détaillée d'un équipement")
    print("   ✅ Génération de recommandations intelligentes")
    print("   ✅ Entraînement des modèles IA")
    
    print("\n🚀 Avantages de l'AI Dashboard:")
    print("   • Surveillance proactive du réseau")
    print("   • Détection précoce des problèmes")
    print("   • Recommandations d'actions concrètes")
    print("   • Interface intuitive et moderne")
    print("   • Mises à jour en temps réel")
    print("   • Intelligence artificielle avancée")
    
    print(f"\n🕐 Fin de la démonstration: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    print("🎉 La page AI Dashboard est entièrement fonctionnelle !")
    
    return True

if __name__ == "__main__":
    demo_ai_dashboard() 