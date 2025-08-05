#!/usr/bin/env python3
"""
Script de nettoyage pour l'environnement de production
Supprime toutes les données de démonstration et prépare l'environnement pour des données réelles
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Device, ScanHistory, Alert, AIModel

def clean_database():
    """Nettoie la base de données de toutes les données de démonstration"""
    print("🧹 NETTOYAGE DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Supprimer toutes les données
            print("🗑️ Suppression des données de démonstration...")
            
            # Supprimer dans l'ordre pour respecter les contraintes de clés étrangères
            ScanHistory.query.delete()
            print("   ✅ Historique des scans supprimé")
            
            Alert.query.delete()
            print("   ✅ Alertes supprimées")
            
            Device.query.delete()
            print("   ✅ Équipements supprimés")
            
            AIModel.query.delete()
            print("   ✅ Modèles IA supprimés")
            
            # Valider les changements
            db.session.commit()
            print("✅ Base de données nettoyée avec succès")
            
            # Vérifier que la base est vide
            device_count = Device.query.count()
            scan_count = ScanHistory.query.count()
            alert_count = Alert.query.count()
            
            print(f"\n📊 État de la base de données :")
            print(f"   • Équipements : {device_count}")
            print(f"   • Scans : {scan_count}")
            print(f"   • Alertes : {alert_count}")
            
            if device_count == 0 and scan_count == 0 and alert_count == 0:
                print("✅ Base de données prête pour la production")
                print("\n🚀 Vous pouvez maintenant :")
                print("   1. Démarrer l'application : python app.py")
                print("   2. Effectuer un scan réseau pour détecter les vrais équipements")
                print("   3. Les données seront collectées dynamiquement")
            else:
                print("⚠️ Certaines données persistent encore")
                
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage : {e}")
            db.session.rollback()

def verify_production_ready():
    """Vérifie que l'environnement est prêt pour la production"""
    print("\n🔍 VÉRIFICATION DE L'ENVIRONNEMENT DE PRODUCTION")
    print("=" * 50)
    
    # Vérifier les fichiers de configuration
    config_files = ['config.py', 'network_scanner.py', 'ai_enhancement.py']
    for file in config_files:
        if os.path.exists(file):
            print(f"✅ {file} présent")
        else:
            print(f"❌ {file} manquant")
    
    # Vérifier les répertoires nécessaires
    directories = ['reports', 'logs', 'ai_models', 'static', 'templates']
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ Répertoire {directory}/ présent")
        else:
            print(f"❌ Répertoire {directory}/ manquant")
    
    # Vérifier les dépendances
    try:
        import flask
        import sqlalchemy
        import nmap
        import sklearn
        print("✅ Toutes les dépendances Python sont installées")
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e}")

if __name__ == "__main__":
    print("🚀 PRÉPARATION DE L'ENVIRONNEMENT DE PRODUCTION")
    print("=" * 60)
    print("Ce script va nettoyer la base de données et préparer")
    print("l'environnement pour des données réelles de production.")
    print()
    
    response = input("Continuer ? (y/N) : ")
    if response.lower() in ['y', 'yes', 'oui']:
        clean_database()
        verify_production_ready()
        print("\n🎉 Environnement de production prêt !")
    else:
        print("❌ Opération annulée") 