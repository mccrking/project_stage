#!/usr/bin/env python3
"""
Script de génération de données de démonstration pour Central Danone
Crée des équipements fictifs pour tester l'interface
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Device, ScanHistory, Alert

def create_demo_devices():
    """Crée des équipements de démonstration"""
    
    demo_devices = [
        # Serveurs
        {'ip': '192.168.1.10', 'hostname': 'DC-CENTRAL', 'type': 'Server', 'mac': '00:1B:44:11:3A:B7'},
        {'ip': '192.168.1.11', 'hostname': 'SRV-APPLI', 'type': 'Server', 'mac': '00:1B:44:11:3A:B8'},
        {'ip': '192.168.1.12', 'hostname': 'SRV-BACKUP', 'type': 'Server', 'mac': '00:1B:44:11:3A:B9'},
        
        # Routeurs et switches
        {'ip': '192.168.1.1', 'hostname': 'ROUTER-MAIN', 'type': 'Router', 'mac': '00:1B:44:11:3A:BA'},
        {'ip': '192.168.1.2', 'hostname': 'SW-CORE', 'type': 'Switch', 'mac': '00:1B:44:11:3A:BB'},
        {'ip': '192.168.1.3', 'hostname': 'SW-PROD', 'type': 'Switch', 'mac': '00:1B:44:11:3A:BC'},
        
        # Postes de travail
        {'ip': '192.168.1.20', 'hostname': 'PC-ADMIN', 'type': 'Workstation', 'mac': '00:1B:44:11:3A:BD'},
        {'ip': '192.168.1.21', 'hostname': 'PC-TECH1', 'type': 'Workstation', 'mac': '00:1B:44:11:3A:BE'},
        {'ip': '192.168.1.22', 'hostname': 'PC-TECH2', 'type': 'Workstation', 'mac': '00:1B:44:11:3A:BF'},
        {'ip': '192.168.1.23', 'hostname': 'PC-OP1', 'type': 'Workstation', 'mac': '00:1B:44:11:3A:C0'},
        {'ip': '192.168.1.24', 'hostname': 'PC-OP2', 'type': 'Workstation', 'mac': '00:1B:44:11:3A:C1'},
        
        # Imprimantes
        {'ip': '192.168.1.30', 'hostname': 'PRINT-ADMIN', 'type': 'Printer', 'mac': '00:1B:44:11:3A:C2'},
        {'ip': '192.168.1.31', 'hostname': 'PRINT-PROD', 'type': 'Printer', 'mac': '00:1B:44:11:3A:C3'},
        
        # Caméras
        {'ip': '192.168.1.40', 'hostname': 'CAM-ENTREE', 'type': 'Camera', 'mac': '00:1B:44:11:3A:C4'},
        {'ip': '192.168.1.41', 'hostname': 'CAM-PROD', 'type': 'Camera', 'mac': '00:1B:44:11:3A:C5'},
        
        # Automates
        {'ip': '192.168.1.50', 'hostname': 'PLC-LIGNE1', 'type': 'Automation', 'mac': '00:1B:44:11:3A:C6'},
        {'ip': '192.168.1.51', 'hostname': 'PLC-LIGNE2', 'type': 'Automation', 'mac': '00:1B:44:11:3A:C7'},
        {'ip': '192.168.1.52', 'hostname': 'HMI-PROD', 'type': 'Automation', 'mac': '00:1B:44:11:3A:C8'},
        
        # Équipements hors ligne (pour démonstration)
        {'ip': '192.168.1.60', 'hostname': 'PC-ANCIEN', 'type': 'Workstation', 'mac': '00:1B:44:11:3A:C9'},
        {'ip': '192.168.1.61', 'hostname': 'PRINT-BROKEN', 'type': 'Printer', 'mac': '00:1B:44:11:3A:CA'},
    ]
    
    print("🔧 Création des équipements de démonstration...")
    
    for device_data in demo_devices:
        # Déterminer le statut (la plupart en ligne, quelques-uns hors ligne)
        if device_data['ip'] in ['192.168.1.60', '192.168.1.61']:
            status = 'offline'
            last_seen = datetime.now() - timedelta(hours=random.randint(2, 24))
        else:
            status = 'online'
            last_seen = datetime.now() - timedelta(minutes=random.randint(1, 60))
        
        device = Device(
            ip_address=device_data['ip'],
            mac_address=device_data['mac'],
            hostname=device_data['hostname'],
            device_type=device_data['type'],
            status=status,
            last_seen=last_seen,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        
        db.session.add(device)
    
    db.session.commit()
    print(f"✅ {len(demo_devices)} équipements créés")

def create_demo_scan_history():
    """Crée un historique de scans de démonstration"""
    
    print("📊 Création de l'historique des scans...")
    
    # Créer des scans sur les 7 derniers jours
    for i in range(7):
        scan_date = datetime.now() - timedelta(days=i)
        
        # Statistiques variables
        total_devices = random.randint(18, 22)
        online_devices = random.randint(16, total_devices)
        offline_devices = total_devices - online_devices
        scan_duration = random.uniform(1.5, 4.0)
        
        scan = ScanHistory(
            scan_time=scan_date,
            total_devices=total_devices,
            online_devices=online_devices,
            offline_devices=offline_devices,
            scan_duration=scan_duration
        )
        
        db.session.add(scan)
    
    db.session.commit()
    print("✅ Historique des scans créé")

def create_demo_alerts():
    """Crée des alertes de démonstration"""
    
    print("🚨 Création des alertes de démonstration...")
    
    # Récupérer les équipements hors ligne
    offline_devices = Device.query.filter_by(status='offline').all()
    
    alert_messages = [
        "L'appareil {hostname} ({ip}) est hors ligne depuis plus de 2 heures",
        "Équipement {hostname} non joignable - vérification nécessaire",
        "Panne détectée sur {hostname} ({ip})",
        "L'automate {hostname} ne répond plus",
        "Imprimante {hostname} hors service"
    ]
    
    for device in offline_devices:
        # Créer 1-3 alertes par appareil hors ligne
        for i in range(random.randint(1, 3)):
            alert_time = datetime.now() - timedelta(hours=random.randint(1, 6))
            message = random.choice(alert_messages).format(
                hostname=device.hostname,
                ip=device.ip_address
            )
            
            alert = Alert(
                device_id=device.id,
                alert_type='device_offline',
                message=message,
                created_at=alert_time,
                is_read=random.choice([True, False])
            )
            
            db.session.add(alert)
    
    # Créer quelques alertes de retour en ligne
    online_devices = Device.query.filter_by(status='online').limit(3).all()
    for device in online_devices:
        alert_time = datetime.now() - timedelta(minutes=random.randint(10, 120))
        message = f"L'appareil {device.hostname} ({device.ip_address}) est de nouveau en ligne"
        
        alert = Alert(
            device_id=device.id,
            alert_type='device_online',
            message=message,
            created_at=alert_time,
            is_read=True
        )
        
        db.session.add(alert)
    
    db.session.commit()
    print("✅ Alertes de démonstration créées")

def main():
    """Fonction principale"""
    print("🏭 CENTRAL DANONE - GÉNÉRATION DE DONNÉES DE DÉMONSTRATION")
    print("=" * 60)
    
    with app.app_context():
        # Vérifier si la base de données existe
        try:
            db.create_all()
            print("✅ Base de données initialisée")
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
            return
        
        # Vérifier s'il y a déjà des données
        existing_devices = Device.query.count()
        if existing_devices > 0:
            print(f"⚠️ {existing_devices} équipements existent déjà dans la base")
            response = input("Voulez-vous supprimer les données existantes ? (y/N): ")
            if response.lower() == 'y':
                print("🗑️ Suppression des données existantes...")
                Device.query.delete()
                ScanHistory.query.delete()
                Alert.query.delete()
                db.session.commit()
                print("✅ Données supprimées")
            else:
                print("❌ Opération annulée")
                return
        
        # Créer les données de démonstration
        create_demo_devices()
        create_demo_scan_history()
        create_demo_alerts()
        
        print("\n🎉 Données de démonstration créées avec succès!")
        print("\n📋 Résumé:")
        print(f"   • {Device.query.count()} équipements")
        print(f"   • {ScanHistory.query.count()} scans historiques")
        print(f"   • {Alert.query.count()} alertes")
        print(f"   • {Device.query.filter_by(status='online').count()} équipements en ligne")
        print(f"   • {Device.query.filter_by(status='offline').count()} équipements hors ligne")
        
        print("\n🌐 Vous pouvez maintenant lancer l'application:")
        print("   python app.py")
        print("   Puis ouvrir http://localhost:5000 dans votre navigateur")

if __name__ == "__main__":
    main() 