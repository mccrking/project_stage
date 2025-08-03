#!/usr/bin/env python3
"""
Script pour vérifier les données dans la base de données
"""

import sqlite3
from datetime import datetime

def check_database():
    """Vérifie les données dans la base de données"""
    print("🗄️ VÉRIFICATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('network_monitor.db')
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables trouvées: {[table[0] for table in tables]}")
        print()
        
        # Vérifier les équipements
        cursor.execute("SELECT COUNT(*) FROM device")
        device_count = cursor.fetchone()[0]
        print(f"📱 Nombre d'équipements: {device_count}")
        
        if device_count > 0:
            print("\n📊 ÉQUIPEMENTS DÉTECTÉS:")
            print("-" * 40)
            
            cursor.execute("""
                SELECT ip, hostname, device_type, is_online, last_seen, 
                       health_score, failure_probability, anomaly_score
                FROM device 
                ORDER BY last_seen DESC
            """)
            
            devices = cursor.fetchall()
            
            for i, device in enumerate(devices, 1):
                ip, hostname, device_type, is_online, last_seen, health_score, failure_prob, anomaly_score = device
                status = "🟢 En ligne" if is_online else "🔴 Hors ligne"
                
                print(f"{i}. {hostname or 'N/A'} ({ip})")
                print(f"   Type: {device_type}")
                print(f"   Statut: {status}")
                print(f"   Dernière vue: {last_seen}")
                print(f"   Score santé: {health_score:.1f}%")
                print(f"   Risque panne: {failure_prob*100:.1f}%")
                print(f"   Score anomalie: {anomaly_score:.3f}")
                print()
        
        # Vérifier l'historique des scans
        cursor.execute("SELECT COUNT(*) FROM scan_history")
        scan_count = cursor.fetchone()[0]
        print(f"📈 Nombre de scans historiques: {scan_count}")
        
        if scan_count > 0:
            print("\n📊 DERNIERS SCANS:")
            print("-" * 40)
            
            cursor.execute("""
                SELECT sh.timestamp, sh.is_online, d.ip, d.hostname
                FROM scan_history sh
                JOIN device d ON sh.device_id = d.id
                ORDER BY sh.timestamp DESC
                LIMIT 10
            """)
            
            scans = cursor.fetchall()
            for scan in scans:
                timestamp, is_online, ip, hostname = scan
                status = "🟢" if is_online else "🔴"
                print(f"{status} {timestamp} - {hostname or ip}")
        
        # Vérifier les alertes
        cursor.execute("SELECT COUNT(*) FROM alert")
        alert_count = cursor.fetchone()[0]
        print(f"\n🚨 Nombre d'alertes: {alert_count}")
        
        if alert_count > 0:
            print("\n🚨 DERNIÈRES ALERTES:")
            print("-" * 40)
            
            cursor.execute("""
                SELECT a.message, a.priority, a.created_at, d.ip
                FROM alert a
                JOIN device d ON a.device_id = d.id
                ORDER BY a.created_at DESC
                LIMIT 5
            """)
            
            alerts = cursor.fetchall()
            for alert in alerts:
                message, priority, created_at, ip = alert
                print(f"⚠️ {created_at} - {ip}: {message}")
        
        # Vérifier les modèles IA
        cursor.execute("SELECT COUNT(*) FROM ai_model")
        model_count = cursor.fetchone()[0]
        print(f"\n🧠 Nombre de modèles IA: {model_count}")
        
        conn.close()
        
        print("\n" + "=" * 50)
        if device_count > 0:
            print("✅ Des équipements ont été détectés !")
            print("🌐 Vérifiez le dashboard: http://localhost:5000")
        else:
            print("⚠️ Aucun équipement détecté")
            print("📡 Lancez un scan réseau pour détecter vos appareils")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == '__main__':
    check_database() 