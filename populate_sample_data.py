"""
Script pour populer la base de données avec des données d'exemple
"""

from app import app, db, User, Device, Alert, Report
from datetime import datetime, timedelta
import random
import os

def populate_sample_data():
    """Crée des données d'exemple pour tester la plateforme"""
    
    with app.app_context():
        print("🔄 Création des données d'exemple...")
        
        # Créer des utilisateurs d'exemple
        create_sample_users()
        
        # Créer des équipements d'exemple
        create_sample_devices()
        
        # Créer des alertes d'exemple
        create_sample_alerts()
        
        # Créer des rapports d'exemple
        create_sample_reports()
        
        print("✅ Données d'exemple créées avec succès!")

def create_sample_users():
    """Crée des utilisateurs d'exemple"""
    try:
        # Vérifier si les utilisateurs existent déjà
        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@centraldanone.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            tech = User(
                username='technicien',
                email='tech@centraldanone.com',
                role='technician'
            )
            tech.set_password('tech123')
            db.session.add(tech)
            
            db.session.commit()
            print("✅ Utilisateurs d'exemple créés")
        else:
            print("ℹ️ Utilisateurs déjà existants")
    except Exception as e:
        print(f"❌ Erreur création utilisateurs: {e}")

def create_sample_devices():
    """Crée des équipements d'exemple"""
    try:
        # Créer uniquement si moins de 3 dispositifs
        if Device.query.count() < 3:
            sample_devices = [
                {
                    'ip': '192.168.1.101',
                    'hostname': 'server-danone-web',
                    'device_type': 'server',
                    'mac_vendor': 'Dell',
                    'is_online': True,
                    'health_score': 94.2,
                    'response_time': 11.5
                },
                {
                    'ip': '192.168.1.102',
                    'hostname': 'switch-backup',
                    'device_type': 'switch',
                    'mac_vendor': 'Cisco',
                    'is_online': True,
                    'health_score': 87.9,
                    'response_time': 7.8
                }
            ]
            
            for device_data in sample_devices:
                # Vérifier si l'IP existe déjà
                existing = Device.query.filter_by(ip=device_data['ip']).first()
                if not existing:
                    device = Device(**device_data)
                    device.last_seen = datetime.now() - timedelta(minutes=random.randint(1, 60))
                    device.ai_confidence = random.uniform(0.7, 0.95)
                    device.failure_probability = random.uniform(0.01, 0.3)
                    device.anomaly_score = random.uniform(-1, 1)
                    device.maintenance_urgency = random.choice(['low', 'medium', 'high'])
                    
                    db.session.add(device)
            
            db.session.commit()
            print("✅ Équipements d'exemple créés")
        else:
            print("ℹ️ Équipements déjà existants")
    except Exception as e:
        print(f"❌ Erreur création équipements: {e}")
        db.session.rollback()

def create_sample_alerts():
    """Crée des alertes d'exemple"""
    try:
        if Alert.query.count() < 5:
            devices = Device.query.all()
            
            for i, device in enumerate(devices[:3]):
                # Vérifier si une alerte existe déjà pour ce device
                existing_alert = Alert.query.filter_by(device_id=device.id).first()
                if not existing_alert:
                    alert = Alert(
                        device_id=device.id,
                        alert_type=random.choice(['offline', 'high_latency', 'ai_warning', 'anomaly']),
                        message=f"Problème détecté sur {device.hostname}: {random.choice(['Latence élevée', 'Connexion instable', 'Anomalie détectée par IA'])}",
                        priority=random.choice(['low', 'medium', 'high']),
                        ai_confidence=random.uniform(0.6, 0.9),
                        created_at=datetime.now() - timedelta(hours=random.randint(1, 24))
                    )
                    db.session.add(alert)
            
            db.session.commit()
            print("✅ Alertes d'exemple créées")
        else:
            print("ℹ️ Alertes déjà existantes")
    except Exception as e:
        print(f"❌ Erreur création alertes: {e}")
        db.session.rollback()

def create_sample_reports():
    """Crée des rapports d'exemple"""
    try:
        if Report.query.count() == 0:
            admin_user = User.query.filter_by(role='admin').first()
            if not admin_user:
                print("❌ Aucun utilisateur admin trouvé")
                return
            
            sample_reports = [
                {
                    'name': 'Rapport Journalier - 05/08/2025',
                    'filename': 'rapport_daily_20250805_080000.pdf',
                    'type': 'daily',
                    'format': 'pdf',
                    'status': 'completed',
                    'description': 'Rapport automatique des activités réseau du jour',
                    'file_size': 2458369,  # ~2.4 MB
                    'download_count': 3,
                    'generated_by': admin_user.id,
                    'created_at': datetime.now() - timedelta(days=1),
                    'generated_at': datetime.now() - timedelta(days=1)
                },
                {
                    'name': 'Rapport Hebdomadaire - Semaine 31',
                    'filename': 'rapport_weekly_20250804_070000.xlsx',
                    'type': 'weekly',
                    'format': 'excel',
                    'status': 'completed',
                    'description': 'Analyse hebdomadaire des performances réseau',
                    'file_size': 1687493,  # ~1.6 MB
                    'download_count': 1,
                    'generated_by': admin_user.id,
                    'created_at': datetime.now() - timedelta(days=2),
                    'generated_at': datetime.now() - timedelta(days=2)
                },
                {
                    'name': 'Rapport Sécurité - Analyse IA',
                    'filename': 'rapport_security_20250806_120000.html',
                    'type': 'security',
                    'format': 'html',
                    'status': 'processing',
                    'description': 'Analyse de sécurité basée sur les algorithmes IA',
                    'file_size': 0,
                    'download_count': 0,
                    'generated_by': admin_user.id,
                    'created_at': datetime.now() - timedelta(hours=2)
                }
            ]
            
            for report_data in sample_reports:
                # Vérifier si le rapport existe déjà
                existing = Report.query.filter_by(filename=report_data['filename']).first()
                if not existing:
                    report = Report(**report_data)
                    if report.status == 'completed':
                        # Créer un fichier d'exemple
                        reports_dir = 'reports'
                        if not os.path.exists(reports_dir):
                            os.makedirs(reports_dir)
                        
                        file_path = os.path.join(reports_dir, report.filename)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(f"Rapport d'exemple: {report.name}\n")
                            f.write(f"Généré le: {report.created_at}\n")
                            f.write("Contenu du rapport...\n" * 100)  # Simuler du contenu
                        
                        report.file_path = file_path
                    
                    db.session.add(report)
            
            db.session.commit()
            print("✅ Rapports d'exemple créés")
        else:
            print("ℹ️ Rapports déjà existants")
    except Exception as e:
        print(f"❌ Erreur création rapports: {e}")
        db.session.rollback()

if __name__ == "__main__":
    populate_sample_data()
