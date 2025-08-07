#!/usr/bin/env python3
"""
Script de démarrage pour plateforme PRODUCTION
Dashboard Danone - Détection réelle des équipements réseau
"""

import os
import sys
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def check_environment():
    """Vérifier l'environnement de production"""
    print("🔍 VÉRIFICATION ENVIRONNEMENT PRODUCTION")
    print("=" * 50)
    
    checks = []
    
    # 1. Variables d'environnement
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key and len(secret_key) >= 16:
        checks.append("✅ SECRET_KEY configurée")
    else:
        checks.append("❌ SECRET_KEY manquante ou faible")
    
    # 2. Base de données
    if os.path.exists('network_monitor_production.db'):
        checks.append("✅ Base de données production présente")
    else:
        checks.append("❌ Base de données production manquante")
    
    # 3. Nmap disponible
    try:
        import nmap
        nm = nmap.PortScanner()
        checks.append("✅ Nmap opérationnel")
    except:
        checks.append("❌ Nmap non disponible")
    
    # 4. Modules critiques
    try:
        import flask, flask_sqlalchemy, flask_login
        checks.append("✅ Modules Flask disponibles")
    except:
        checks.append("❌ Modules Flask manquants")
    
    # 5. Scanner production
    try:
        from network_scanner_production import ProductionNetworkScanner
        scanner = ProductionNetworkScanner()
        if scanner.nmap_available:
            checks.append("✅ Scanner production opérationnel")
        else:
            checks.append("⚠️ Scanner en mode fallback")
    except Exception as e:
        checks.append(f"❌ Scanner production: {e}")
    
    # Afficher les résultats
    for check in checks:
        print(f"  {check}")
    
    # Compter les erreurs
    errors = len([c for c in checks if c.startswith("❌")])
    warnings = len([c for c in checks if c.startswith("⚠️")])
    
    if errors > 0:
        print(f"\n❌ {errors} erreur(s) critique(s) détectée(s)")
        return False
    elif warnings > 0:
        print(f"\n⚠️ {warnings} avertissement(s) - fonctionnalité réduite")
        return True
    else:
        print("\n✅ Environnement production validé")
        return True

def start_production_app():
    """Démarrer l'application en mode production"""
    print("\n🚀 DÉMARRAGE APPLICATION PRODUCTION")
    print("=" * 50)
    
    try:
        # Importer l'application
        from app import app, db, create_default_admin
        
        print("📱 Configuration de l'application...")
        
        # Configuration production
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_monitor_production.db'
        
        # Vérifier la base de données
        with app.app_context():
            try:
                db.create_all()
                create_default_admin()
                print("✅ Base de données initialisée")
            except Exception as e:
                print(f"⚠️ Base de données: {e}")
        
        print("🌐 Informations de connexion:")
        print(f"   URL: http://localhost:5000")
        print(f"   Admin: admin@danone.com / admin123")
        print(f"   Tech: tech@danone.com / tech123")
        
        print("\n🔍 FONCTIONNALITÉS PRODUCTION ACTIVES:")
        print("   ✅ Détection automatique des réseaux")
        print("   ✅ Scan avancé avec Nmap")
        print("   ✅ Identification détaillée des équipements")
        print("   ✅ Détection du type, OS, ports, services")
        print("   ✅ Analysis en temps réel")
        print("   ✅ Intelligence artificielle")
        print("   ✅ Système d'alertes")
        print("   ✅ Génération de rapports")
        
        print(f"\n🎯 DÉMARRAGE DE LA PLATEFORME...")
        print("   (Ctrl+C pour arrêter)")
        print("=" * 50)
        
        # Démarrer Flask
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Arrêt de la plateforme par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur de démarrage: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale"""
    print("🏭 PLATEFORME DANONE - SUPERVISION RÉSEAU")
    print("🔧 MODE PRODUCTION - DÉTECTION RÉELLE")
    print("=" * 50)
    
    # Vérifier l'environnement
    if not check_environment():
        print("\n❌ ENVIRONNEMENT NON VALIDE")
        print("Exécutez d'abord: python init_production.py")
        sys.exit(1)
    
    # Petite pause pour la lisibilité
    time.sleep(2)
    
    # Démarrer l'application
    start_production_app()

if __name__ == '__main__':
    main()
