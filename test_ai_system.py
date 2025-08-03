"""
Test complet du système Central Danone avec IA
Vérifie l'installation et le fonctionnement de toutes les fonctionnalités IA
"""

import os
import sys
import importlib
import subprocess
from datetime import datetime

def test_python_version():
    """Test de la version Python"""
    print("🐍 Test de la version Python...")
    version = sys.version_info
    print(f"   Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("   ✅ Version Python compatible")
        return True
    else:
        print("   ❌ Version Python incompatible (requis: Python 3.8+)")
        return False

def test_python_dependencies():
    """Test des dépendances Python"""
    print("\n📦 Test des dépendances Python...")
    
    required_packages = [
        'flask', 'sqlalchemy', 'numpy', 'pandas', 'sklearn', 
        'joblib', 'matplotlib', 'seaborn', 'plotly', 'torch',
        'transformers', 'scipy', 'schedule', 'fpdf2', 'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MANQUANT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   ⚠️ {len(missing_packages)} packages manquants")
        print("   Exécutez: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ Toutes les dépendances sont installées")
        return True

def test_nmap_installation():
    """Test de l'installation de Nmap"""
    print("\n🔍 Test de l'installation Nmap...")
    
    try:
        result = subprocess.run(['nmap', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ Nmap installé et fonctionnel")
            return True
        else:
            print("   ❌ Nmap installé mais non fonctionnel")
            return False
    except FileNotFoundError:
        print("   ⚠️ Nmap non trouvé - le mode fallback sera utilisé")
        return True  # Pas critique car il y a un fallback
    except Exception as e:
        print(f"   ❌ Erreur lors du test Nmap: {e}")
        return False

def test_directory_structure():
    """Test de la structure des répertoires"""
    print("\n📁 Test de la structure des répertoires...")
    
    required_dirs = ['templates', 'reports', 'logs', 'ai_models']
    missing_dirs = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"   ✅ {directory}/")
        else:
            print(f"   ❌ {directory}/ - MANQUANT")
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"\n   Création des répertoires manquants...")
        for directory in missing_dirs:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ {directory}/ créé")
    
    return True

def test_application_modules():
    """Test des modules de l'application"""
    print("\n🔧 Test des modules de l'application...")
    
    modules = [
        'app', 'network_scanner', 'report_generator', 'ai_enhancement'
    ]
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}.py")
        except ImportError as e:
            print(f"   ❌ {module}.py - ERREUR: {e}")
            return False
    
    return True

def test_ai_system():
    """Test du système IA"""
    print("\n🧠 Test du système IA...")
    
    try:
        from ai_enhancement import ai_system
        
        # Test de la classification d'équipements
        classification = ai_system.device_classifier.classify_device(
            'SRV-TEST', 'Dell Inc.', '192.168.1.100'
        )
        print(f"   ✅ Classification d'équipements: {classification['device_type']}")
        
        # Test de la détection d'anomalies
        anomaly_detector = ai_system.anomaly_detector
        print(f"   ✅ Détecteur d'anomalies initialisé")
        
        # Test de la maintenance prédictive
        maintenance_predictor = ai_system.maintenance_predictor
        print(f"   ✅ Prédicteur de maintenance initialisé")
        
        # Test des recommandations
        recommendation_system = ai_system.recommendation_system
        print(f"   ✅ Système de recommandations initialisé")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur système IA: {e}")
        return False

def test_database_connection():
    """Test de la connexion à la base de données"""
    print("\n🗄️ Test de la base de données...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Test de connexion
            db.engine.execute("SELECT 1")
            print("   ✅ Connexion à la base de données")
            
            # Test de création des tables
            db.create_all()
            print("   ✅ Tables créées/mises à jour")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
        return False

def test_flask_application():
    """Test de l'application Flask"""
    print("\n🌐 Test de l'application Flask...")
    
    try:
        from app import app
        
        # Test de création de l'application
        with app.test_client() as client:
            # Test de la route principale
            response = client.get('/')
            if response.status_code == 200:
                print("   ✅ Application Flask fonctionnelle")
                return True
            else:
                print(f"   ❌ Erreur route principale: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Erreur application Flask: {e}")
        return False

def test_network_scanner():
    """Test du scanner réseau"""
    print("\n📡 Test du scanner réseau...")
    
    try:
        from network_scanner import NetworkScanner
        
        scanner = NetworkScanner()
        
        # Test de validation d'adresse IP
        is_valid = scanner.is_valid_ip_range("192.168.1.0/24")
        if is_valid:
            print("   ✅ Validation d'adresse IP")
        else:
            print("   ❌ Erreur validation d'adresse IP")
            return False
        
        # Test de scan local (localhost)
        print("   🔍 Test de scan local...")
        devices = scanner.scan_network("127.0.0.1/32")
        print(f"   ✅ Scan local terminé: {len(devices)} équipements trouvés")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur scanner réseau: {e}")
        return False

def test_report_generator():
    """Test du générateur de rapports"""
    print("\n📊 Test du générateur de rapports...")
    
    try:
        from report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        # Test de données de rapport
        test_data = {
            'timestamp': datetime.now().isoformat(),
            'network_stats': {
                'total_devices': 10,
                'online_devices': 8,
                'offline_devices': 2,
                'availability_percentage': 80.0
            },
            'ai_insights': {
                'avg_health_score': 85.0,
                'critical_devices': 1,
                'high_risk_devices': 2,
                'anomaly_devices': 0
            },
            'recommendations': ['Test recommendation'],
            'devices_details': []
        }
        
        # Test de génération de rapport JSON
        report_path = generator.generate_ai_report(test_data)
        if report_path and os.path.exists(report_path):
            print("   ✅ Génération de rapport IA")
            os.remove(report_path)  # Nettoyer
        else:
            print("   ❌ Erreur génération rapport")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur générateur de rapports: {e}")
        return False

def test_demo_data():
    """Test de création des données de démonstration"""
    print("\n🎭 Test des données de démonstration...")
    
    try:
        # Importer le script de démo
        import demo_data_ai
        
        # Test de création d'équipements
        devices = demo_data_ai.create_demo_devices()
        if devices:
            print(f"   ✅ {len(devices)} équipements de démonstration créés")
        else:
            print("   ❌ Erreur création équipements")
            return False
        
        # Test de création d'historique
        demo_data_ai.create_demo_scan_history(devices)
        print("   ✅ Historique de scans créé")
        
        # Test d'analyse IA
        demo_data_ai.create_demo_ai_analysis(devices)
        print("   ✅ Analyse IA appliquée")
        
        # Test de création d'alertes
        demo_data_ai.create_demo_alerts(devices)
        print("   ✅ Alertes créées")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur données de démonstration: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST COMPLET DU SYSTÈME CENTRAL DANONE AVEC IA")
    print("=" * 60)
    
    tests = [
        ("Version Python", test_python_version),
        ("Dépendances Python", test_python_dependencies),
        ("Installation Nmap", test_nmap_installation),
        ("Structure répertoires", test_directory_structure),
        ("Modules application", test_application_modules),
        ("Système IA", test_ai_system),
        ("Base de données", test_database_connection),
        ("Application Flask", test_flask_application),
        ("Scanner réseau", test_network_scanner),
        ("Générateur rapports", test_report_generator),
        ("Données démo", test_demo_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("\n🚀 Le système est prêt à être utilisé:")
        print("   • Dashboard principal: http://localhost:5000")
        print("   • Dashboard IA: http://localhost:5000/ai-dashboard")
        print("   • Rapports: http://localhost:5000/reports")
        print("\n💡 Pour démarrer l'application:")
        print("   python app.py")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n🔧 Actions recommandées:")
        print("   1. Vérifiez l'installation des dépendances")
        print("   2. Installez Nmap si nécessaire")
        print("   3. Vérifiez les permissions des répertoires")
        print("   4. Relancez les tests après correction")
    
    print("=" * 60)

if __name__ == '__main__':
    main() 