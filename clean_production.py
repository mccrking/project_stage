#!/usr/bin/env python3
"""
Script de nettoyage pour passer en mode production Central Danone
Supprime toutes les données de démonstration et prépare la base pour la production
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Device, ScanHistory, Alert, AIModel

def clean_production_database():
    """Nettoie la base de données pour la production"""
    print("🧹 NETTOYAGE DE LA BASE DE DONNÉES CENTRAL DANONE")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Compter les données actuelles
            device_count = Device.query.count()
            scan_count = ScanHistory.query.count()
            alert_count = Alert.query.count()
            model_count = AIModel.query.count()
            
            print(f"📊 Données actuelles:")
            print(f"   - Équipements: {device_count}")
            print(f"   - Scans historiques: {scan_count}")
            print(f"   - Alertes: {alert_count}")
            print(f"   - Modèles IA: {model_count}")
            
            if device_count == 0:
                print("✅ Base de données déjà vide - prête pour la production")
                return
            
            # Demander confirmation
            print("\n⚠️  ATTENTION: Cette opération va supprimer TOUTES les données de démonstration")
            print("   Seuls les modèles IA entraînés seront conservés")
            
            response = input("\n❓ Continuer le nettoyage ? (oui/non): ").lower().strip()
            
            if response not in ['oui', 'o', 'yes', 'y']:
                print("❌ Nettoyage annulé")
                return
            
            print("\n🗑️  Suppression des données de démonstration...")
            
            # Supprimer les alertes
            Alert.query.delete()
            print("   ✅ Alertes supprimées")
            
            # Supprimer l'historique des scans
            ScanHistory.query.delete()
            print("   ✅ Historique des scans supprimé")
            
            # Supprimer les équipements de démonstration
            Device.query.delete()
            print("   ✅ Équipements supprimés")
            
            # Conserver les modèles IA
            print("   ✅ Modèles IA conservés")
            
            # Commit des changements
            db.session.commit()
            
            print("\n✅ NETTOYAGE TERMINÉ")
            print("=" * 60)
            print("🎯 La base de données est maintenant prête pour la production")
            print("📡 Lancez un scan réseau pour détecter vos vrais équipements")
            print("🧠 Les modèles IA s'entraîneront automatiquement avec les nouvelles données")
            
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage: {str(e)}")
            db.session.rollback()

def backup_demo_data():
    """Sauvegarde les données de démonstration avant nettoyage"""
    print("💾 SAUVEGARDE DES DONNÉES DE DÉMONSTRATION")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Créer un fichier de sauvegarde
            backup_file = f"backup_demo_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            
            # Exporter les données (format simple)
            devices = Device.query.all()
            scans = ScanHistory.query.all()
            alerts = Alert.query.all()
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write("-- Sauvegarde des données de démonstration Central Danone\n")
                f.write(f"-- Date: {datetime.now().isoformat()}\n\n")
                
                f.write(f"-- Équipements: {len(devices)}\n")
                for device in devices:
                    f.write(f"-- {device.ip} ({device.hostname})\n")
                
                f.write(f"\n-- Scans: {len(scans)}\n")
                f.write(f"-- Alertes: {len(alerts)}\n")
            
            print(f"✅ Sauvegarde créée: {backup_file}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {str(e)}")

def main():
    """Fonction principale"""
    print("🏭 CENTRAL DANONE - PASSAGE EN MODE PRODUCTION")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('app.py'):
        print("❌ Erreur: Ce script doit être exécuté depuis le répertoire du projet")
        return
    
    # Options
    print("Options disponibles:")
    print("1. Nettoyer la base de données (supprimer les données de démonstration)")
    print("2. Sauvegarder les données de démonstration")
    print("3. Nettoyer ET sauvegarder")
    print("4. Quitter")
    
    choice = input("\nChoisissez une option (1-4): ").strip()
    
    if choice == '1':
        clean_production_database()
    elif choice == '2':
        backup_demo_data()
    elif choice == '3':
        backup_demo_data()
        print()
        clean_production_database()
    elif choice == '4':
        print("👋 Au revoir!")
    else:
        print("❌ Option invalide")

if __name__ == '__main__':
    main() 