"""
Script de données de démonstration avec IA pour Central Danone
Génère des données réalistes pour tester toutes les fonctionnalités IA
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
import numpy as np

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Device, ScanHistory, Alert, AIModel
from ai_enhancement import ai_system

# Fonction pour obtenir l'heure locale
def get_local_time():
    """Retourne l'heure locale actuelle"""
    return datetime.now()

def create_demo_devices():
    """Crée des équipements de démonstration réalistes"""
    
    # Configuration des équipements Central Danone
    demo_devices = [
        # Serveurs
        {
            'ip': '192.168.1.10',
            'hostname': 'DC-CENTRAL',
            'mac': '00:1B:44:11:3A:B7',
            'mac_vendor': 'Dell Inc.',
            'device_type': 'server',
            'is_online': True
        },
        {
            'ip': '192.168.1.11',
            'hostname': 'SRV-EXCHANGE',
            'mac': '00:1B:44:11:3A:B8',
            'mac_vendor': 'Dell Inc.',
            'device_type': 'server',
            'is_online': True
        },
        {
            'ip': '192.168.1.12',
            'hostname': 'SRV-SQL',
            'mac': '00:1B:44:11:3A:B9',
            'mac_vendor': 'Dell Inc.',
            'device_type': 'server',
            'is_online': False  # Serveur en panne
        },
        
        # Routeurs et Switches
        {
            'ip': '192.168.1.1',
            'hostname': 'ROUTER-CORE',
            'mac': '00:1B:44:11:3A:C0',
            'mac_vendor': 'Cisco Systems',
            'device_type': 'router',
            'is_online': True
        },
        {
            'ip': '192.168.1.2',
            'hostname': 'SW-CORE-01',
            'mac': '00:1B:44:11:3A:C1',
            'mac_vendor': 'Cisco Systems',
            'device_type': 'router',
            'is_online': True
        },
        {
            'ip': '192.168.1.3',
            'hostname': 'SW-PRODUCTION',
            'mac': '00:1B:44:11:3A:C2',
            'mac_vendor': 'Cisco Systems',
            'device_type': 'router',
            'is_online': True
        },
        
        # PLCs et Automation
        {
            'ip': '192.168.1.20',
            'hostname': 'PLC-LIGNE1',
            'mac': '00:1B:44:11:3A:D0',
            'mac_vendor': 'Schneider Electric',
            'device_type': 'plc',
            'is_online': True
        },
        {
            'ip': '192.168.1.21',
            'hostname': 'PLC-LIGNE2',
            'mac': '00:1B:44:11:3A:D1',
            'mac_vendor': 'Schneider Electric',
            'device_type': 'plc',
            'is_online': True
        },
        {
            'ip': '192.168.1.22',
            'hostname': 'PLC-EMBALLAGE',
            'mac': '00:1B:44:11:3A:D2',
            'mac_vendor': 'Siemens AG',
            'device_type': 'plc',
            'is_online': False  # PLC en maintenance
        },
        
        # Imprimantes
        {
            'ip': '192.168.1.30',
            'hostname': 'PRINT-ADMIN',
            'mac': '00:1B:44:11:3A:E0',
            'mac_vendor': 'HP Inc.',
            'device_type': 'printer',
            'is_online': True
        },
        {
            'ip': '192.168.1.31',
            'hostname': 'PRINT-PROD',
            'mac': '00:1B:44:11:3A:E1',
            'mac_vendor': 'Canon Inc.',
            'device_type': 'printer',
            'is_online': True
        },
        
        # Postes de travail
        {
            'ip': '192.168.1.100',
            'hostname': 'PC-ADMIN',
            'mac': '00:1B:44:11:3A:F0',
            'mac_vendor': 'Microsoft Corporation',
            'device_type': 'workstation',
            'is_online': True
        },
        {
            'ip': '192.168.1.101',
            'hostname': 'PC-TECH',
            'mac': '00:1B:44:11:3A:F1',
            'mac_vendor': 'Microsoft Corporation',
            'device_type': 'workstation',
            'is_online': True
        },
        {
            'ip': '192.168.1.102',
            'hostname': 'PC-PROD',
            'mac': '00:1B:44:11:3A:F2',
            'mac_vendor': 'Microsoft Corporation',
            'device_type': 'workstation',
            'is_online': False  # PC éteint
        },
        
        # Caméras de surveillance
        {
            'ip': '192.168.1.200',
            'hostname': 'CAM-ENTREE',
            'mac': '00:1B:44:11:3A:G0',
            'mac_vendor': 'Axis Communications',
            'device_type': 'camera',
            'is_online': True
        },
        {
            'ip': '192.168.1.201',
            'hostname': 'CAM-PROD',
            'mac': '00:1B:44:11:3A:G1',
            'mac_vendor': 'Axis Communications',
            'device_type': 'camera',
            'is_online': True
        }
    ]
    
    devices_created = []
    
    for device_info in demo_devices:
        # Vérifier si l'équipement existe déjà
        existing_device = Device.query.filter_by(ip=device_info['ip']).first()
        
        if existing_device:
            # Mettre à jour l'équipement existant
            existing_device.hostname = device_info['hostname']
            existing_device.mac = device_info['mac']
            existing_device.mac_vendor = device_info['mac_vendor']
            existing_device.device_type = device_info['device_type']
            existing_device.is_online = device_info['is_online']
            existing_device.updated_at = get_local_time()
            devices_created.append(existing_device)
        else:
            # Créer un nouvel équipement
            device = Device(
                ip=device_info['ip'],
                hostname=device_info['hostname'],
                mac=device_info['mac'],
                mac_vendor=device_info['mac_vendor'],
                device_type=device_info['device_type'],
                is_online=device_info['is_online'],
                last_seen=get_local_time() if device_info['is_online'] else get_local_time() - timedelta(hours=2)
            )
            db.session.add(device)
            devices_created.append(device)
    
    db.session.commit()
    print(f"✅ {len(devices_created)} équipements de démonstration créés/mis à jour")
    return devices_created

def create_demo_scan_history(devices):
    """Crée un historique de scans réaliste avec métriques IA"""
    
    print("📊 Création de l'historique des scans...")
    
    # Supprimer l'historique existant
    ScanHistory.query.delete()
    
    # Générer des données sur les 30 derniers jours
    end_date = get_local_time()
    start_date = end_date - timedelta(days=30)
    
    scan_records = []
    
    for device in devices:
        # Déterminer le comportement de l'équipement
        if device.device_type == 'server':
            # Serveurs : généralement stables, mais peuvent avoir des problèmes
            base_response_time = random.uniform(5, 15)
            base_uptime = 0.98 if device.is_online else 0.0
        elif device.device_type == 'plc':
            # PLCs : très stables en production
            base_response_time = random.uniform(2, 8)
            base_uptime = 0.99 if device.is_online else 0.0
        elif device.device_type == 'router':
            # Routeurs : très stables
            base_response_time = random.uniform(1, 5)
            base_uptime = 0.995 if device.is_online else 0.0
        elif device.device_type == 'printer':
            # Imprimantes : moins critiques
            base_response_time = random.uniform(10, 30)
            base_uptime = 0.95 if device.is_online else 0.0
        elif device.device_type == 'workstation':
            # PCs : peuvent être éteints
            base_response_time = random.uniform(8, 20)
            base_uptime = 0.90 if device.is_online else 0.0
        else:
            # Autres équipements
            base_response_time = random.uniform(5, 15)
            base_uptime = 0.95 if device.is_online else 0.0
        
        # Générer des scans toutes les heures
        current_date = start_date
        while current_date <= end_date:
            # Ajouter de la variabilité
            response_time_variation = random.uniform(0.8, 1.2)
            response_time = base_response_time * response_time_variation
            
            # Simuler des pannes temporaires
            is_online = device.is_online
            if random.random() > base_uptime:
                is_online = False
            
            # Métriques supplémentaires
            packet_loss = random.uniform(0, 0.05) if is_online else random.uniform(0.8, 1.0)
            scan_duration = random.uniform(0.5, 2.0)
            error_count = 0 if is_online else random.randint(1, 3)
            
            # Créer l'enregistrement de scan
            scan_record = ScanHistory(
                device_id=device.id,
                is_online=is_online,
                response_time=response_time if is_online else None,
                packet_loss=packet_loss,
                scan_duration=scan_duration,
                error_count=error_count,
                timestamp=current_date
            )
            scan_records.append(scan_record)
            
            current_date += timedelta(hours=1)
    
    # Ajouter les enregistrements par batch pour éviter les problèmes de mémoire
    batch_size = 1000
    for i in range(0, len(scan_records), batch_size):
        batch = scan_records[i:i + batch_size]
        db.session.add_all(batch)
        db.session.commit()
        print(f"   📈 {len(batch)} enregistrements de scan ajoutés...")
    
    print(f"✅ {len(scan_records)} enregistrements d'historique créés")

def create_demo_ai_analysis(devices):
    """Applique l'analyse IA aux équipements de démonstration"""
    
    print("🧠 Application de l'analyse IA...")
    
    for device in devices:
        # Récupérer l'historique de l'équipement
        history = ScanHistory.query.filter_by(device_id=device.id).order_by(ScanHistory.timestamp.desc()).limit(100).all()
        
        if history:
            # Préparer les données pour l'analyse IA
            history_data = []
            for scan in history:
                history_data.append({
                    'response_time': scan.response_time or 0,
                    'packet_loss': scan.packet_loss or 0,
                    'is_online': scan.is_online,
                    'scan_duration': scan.scan_duration or 0,
                    'error_count': scan.error_count or 0
                })
            
            # Données pour l'analyse IA
            device_data = {
                'hostname': device.hostname or '',
                'mac_vendor': device.mac_vendor or '',
                'ip': device.ip,
                'history': history_data
            }
            
            # Analyse IA
            ai_analysis = ai_system.analyze_device_complete(device_data)
            
            # Mettre à jour l'équipement avec les résultats IA
            device.device_type = ai_analysis['classification']['device_type']
            device.ai_confidence = ai_analysis['ai_confidence']
            device.health_score = ai_analysis['health_score']
            device.failure_probability = ai_analysis['maintenance_analysis']['failure_probability']
            device.anomaly_score = ai_analysis['anomaly_analysis']['anomaly_score']
            device.maintenance_urgency = ai_analysis['maintenance_analysis']['maintenance_urgency']
            device.ai_recommendations = json.dumps(ai_analysis['recommendations'])
            
            print(f"   🧠 {device.hostname}: Score santé {ai_analysis['health_score']:.1f}%, Risque {ai_analysis['maintenance_analysis']['failure_probability']*100:.1f}%")
    
    db.session.commit()
    print("✅ Analyse IA appliquée à tous les équipements")

def create_demo_alerts(devices):
    """Crée des alertes basées sur l'analyse IA"""
    
    print("🚨 Création des alertes IA...")
    
    # Supprimer les alertes existantes
    Alert.query.delete()
    
    alerts_created = []
    
    for device in devices:
        # Alertes basées sur le statut en ligne
        if not device.is_online:
            alert = Alert(
                device_id=device.id,
                alert_type='offline',
                message=f"🚨 Équipement {device.hostname} ({device.ip}) hors ligne",
                priority='high',
                ai_confidence=0.9
            )
            alerts_created.append(alert)
        
        # Alertes basées sur l'analyse IA
        if device.failure_probability > 0.8:
            alert = Alert(
                device_id=device.id,
                alert_type='ai_critical',
                message=f"🚨 RISQUE CRITIQUE - {device.hostname} pourrait tomber en panne (Probabilité: {device.failure_probability*100:.1f}%)",
                priority='critical',
                ai_confidence=device.ai_confidence
            )
            alerts_created.append(alert)
        elif device.failure_probability > 0.6:
            alert = Alert(
                device_id=device.id,
                alert_type='ai_warning',
                message=f"⚠️ MAINTENANCE RECOMMANDÉE - {device.hostname} présente un risque élevé (Probabilité: {device.failure_probability*100:.1f}%)",
                priority='medium',
                ai_confidence=device.ai_confidence
            )
            alerts_created.append(alert)
        
        # Alertes d'anomalie
        if device.anomaly_score < -0.5:
            alert = Alert(
                device_id=device.id,
                alert_type='anomaly',
                message=f"🔍 COMPORTEMENT ANORMAL détecté sur {device.hostname} (Score: {device.anomaly_score:.3f})",
                priority='high',
                ai_confidence=device.ai_confidence
            )
            alerts_created.append(alert)
    
    # Ajouter quelques alertes résolues pour l'historique
    for i in range(5):
        device = random.choice(devices)
        alert = Alert(
            device_id=device.id,
            alert_type='offline',
            message=f"Équipement {device.hostname} était hors ligne (RÉSOLU)",
            priority='medium',
            ai_confidence=0.8,
            is_resolved=True,
            resolved_at=get_local_time() - timedelta(hours=random.randint(1, 24))
        )
        alerts_created.append(alert)
    
    db.session.add_all(alerts_created)
    db.session.commit()
    
    print(f"✅ {len(alerts_created)} alertes créées")

def create_demo_ai_models():
    """Crée des enregistrements de modèles IA"""
    
    print("🤖 Création des enregistrements de modèles IA...")
    
    # Supprimer les modèles existants
    AIModel.query.delete()
    
    ai_models = [
        {
            'model_name': 'Anomaly Detection - Isolation Forest',
            'model_type': 'anomaly',
            'accuracy': 0.92,
            'model_path': 'ai_models/anomaly_detector.pkl'
        },
        {
            'model_name': 'Predictive Maintenance - Random Forest',
            'model_type': 'maintenance',
            'accuracy': 0.88,
            'model_path': 'ai_models/maintenance_predictor.pkl'
        },
        {
            'model_name': 'Device Classification - Rule-based + ML',
            'model_type': 'classification',
            'accuracy': 0.95,
            'model_path': 'ai_models/device_classifier.pkl'
        }
    ]
    
    for model_info in ai_models:
        model = AIModel(
            model_name=model_info['model_name'],
            model_type=model_info['model_type'],
            accuracy=model_info['accuracy'],
            model_path=model_info['model_path'],
            training_date=get_local_time() - timedelta(days=random.randint(1, 7)),
            is_active=True
        )
        db.session.add(model)
    
    db.session.commit()
    print("✅ Modèles IA enregistrés")

def main():
    """Fonction principale pour créer toutes les données de démonstration"""
    
    print("🚀 Création des données de démonstration Central Danone avec IA...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Créer les équipements
            devices = create_demo_devices()
            
            # Créer l'historique des scans
            create_demo_scan_history(devices)
            
            # Entraîner les modèles IA
            print("🧠 Entraînement des modèles IA...")
            training_data = []
            for device in devices:
                history = ScanHistory.query.filter_by(device_id=device.id).order_by(ScanHistory.timestamp.desc()).limit(100).all()
                if history:
                    history_data = []
                    for scan in history:
                        history_data.append({
                            'response_time': scan.response_time or 0,
                            'packet_loss': scan.packet_loss or 0,
                            'is_online': scan.is_online,
                            'scan_duration': scan.scan_duration or 0,
                            'error_count': scan.error_count or 0
                        })
                    
                    training_data.append({
                        'hostname': device.hostname or '',
                        'mac_vendor': device.mac_vendor or '',
                        'ip': device.ip,
                        'history': history_data
                    })
            
            if len(training_data) >= 5:
                ai_system.train_all_models(training_data)
                print("✅ Modèles IA entraînés avec succès")
            else:
                print("⚠️ Données insuffisantes pour l'entraînement IA")
            
            # Appliquer l'analyse IA
            create_demo_ai_analysis(devices)
            
            # Créer les alertes
            create_demo_alerts(devices)
            
            # Créer les enregistrements de modèles IA
            create_demo_ai_models()
            
            # Statistiques finales
            total_devices = Device.query.count()
            online_devices = Device.query.filter_by(is_online=True).count()
            total_alerts = Alert.query.filter_by(is_resolved=False).count()
            avg_health_score = db.session.query(db.func.avg(Device.health_score)).scalar() or 0
            
            print("\n" + "=" * 60)
            print("📊 STATISTIQUES FINALES:")
            print(f"   • Équipements totaux: {total_devices}")
            print(f"   • Équipements en ligne: {online_devices}")
            print(f"   • Alertes actives: {total_alerts}")
            print(f"   • Score santé moyen: {avg_health_score:.1f}%")
            print(f"   • Modèles IA: 3 entraînés")
            print("=" * 60)
            print("✅ Données de démonstration créées avec succès!")
            print("\n🌐 Accédez au dashboard: http://localhost:5000")
            print("🧠 Dashboard IA: http://localhost:5000/ai-dashboard")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des données: {e}")
            db.session.rollback()

if __name__ == '__main__':
    main() 