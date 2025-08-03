#!/usr/bin/env python3
"""
Script de test pour le système de supervision Central Danone
Vérifie que toutes les dépendances et composants fonctionnent correctement
"""

import sys
import os
import importlib
import subprocess
from datetime import datetime

def print_header(title):
    """Affiche un en-tête de test"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def print_warning(message):
    """Affiche un message d'avertissement"""
    print(f"⚠️ {message}")

def print_info(message):
    """Affiche un message d'information"""
    print(f"ℹ️ {message}")

def test_python_version():
    """Teste la version de Python"""
    print_header("TEST DE LA VERSION PYTHON")
    
    version = sys.version_info
    print_info(f"Version Python détectée: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Version Python compatible (3.8+)")
        return True
    else:
        print_error("Version Python incompatible. Requis: 3.8+")
        return False

def test_dependencies():
    """Teste les dépendances Python"""
    print_header("TEST DES DÉPENDANCES PYTHON")
    
    dependencies = [
        'flask',
        'flask_sqlalchemy', 
        'nmap',
        'schedule',
        'fpdf2',
        'openpyxl',
        'python_dotenv'
    ]
    
    all_ok = True
    
    for dep in dependencies:
        try:
            importlib.import_module(dep.replace('-', '_'))
            print_success(f"Module {dep} disponible")
        except ImportError:
            print_error(f"Module {dep} manquant")
            all_ok = False
    
    return all_ok

def test_nmap():
    """Teste l'installation de Nmap"""
    print_header("TEST DE NMAP")
    
    try:
        result = subprocess.run(['nmap', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_success(f"Nmap installé: {version_line}")
            return True
        else:
            print_error("Nmap installé mais ne répond pas correctement")
            return False
    except FileNotFoundError:
        print_warning("Nmap non trouvé - le mode fallback sera utilisé")
        return False
    except subprocess.TimeoutExpired:
        print_error("Timeout lors du test de Nmap")
        return False

def test_directories():
    """Teste la création des dossiers nécessaires"""
    print_header("TEST DES DOSSIERS")
    
    directories = ['reports', 'logs', 'templates', 'static']
    all_ok = True
    
    for directory in directories:
        if os.path.exists(directory):
            print_success(f"Dossier {directory} existe")
        else:
            try:
                os.makedirs(directory, exist_ok=True)
                print_success(f"Dossier {directory} créé")
            except Exception as e:
                print_error(f"Impossible de créer le dossier {directory}: {e}")
                all_ok = False
    
    return all_ok

def test_modules():
    """Teste les modules de l'application"""
    print_header("TEST DES MODULES DE L'APPLICATION")
    
    modules = ['network_scanner', 'report_generator']
    all_ok = True
    
    for module in modules:
        try:
            importlib.import_module(module)
            print_success(f"Module {module} importé avec succès")
        except ImportError as e:
            print_error(f"Erreur d'import du module {module}: {e}")
            all_ok = False
    
    return all_ok

def test_network_scanner():
    """Teste le scanner réseau"""
    print_header("TEST DU SCANNER RÉSEAU")
    
    try:
        from network_scanner import NetworkScanner
        scanner = NetworkScanner()
        
        # Test de validation de plage réseau
        test_ranges = ['192.168.1.0/24', '10.0.0.0/8', '172.16.0.0/12']
        for range_test in test_ranges:
            if scanner.validate_network_range(range_test):
                print_success(f"Plage réseau valide: {range_test}")
            else:
                print_error(f"Plage réseau invalide: {range_test}")
        
        # Test d'analyse réseau
        network_info = scanner.get_network_info('192.168.1.0/24')
        if network_info:
            print_success(f"Analyse réseau: {network_info['network']} - {network_info['usable_addresses']} adresses")
        else:
            print_error("Échec de l'analyse réseau")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors du test du scanner: {e}")
        return False

def test_report_generator():
    """Teste le générateur de rapports"""
    print_header("TEST DU GÉNÉRATEUR DE RAPPORTS")
    
    try:
        from report_generator import ReportGenerator
        generator = ReportGenerator()
        
        # Test de données d'exemple
        test_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'devices': [
                {
                    'ip': '192.168.1.1',
                    'hostname': 'router-test',
                    'status': 'online',
                    'last_seen': '2024-12-01 10:00:00'
                }
            ],
            'statistics': {
                'total_devices': 1,
                'online_devices': 1,
                'offline_devices': 0
            }
        }
        
        # Test de génération PDF
        try:
            generator.generate_pdf_report(test_data, 'test_report.pdf')
            if os.path.exists('reports/test_report.pdf'):
                print_success("Génération PDF réussie")
                os.remove('reports/test_report.pdf')  # Nettoyer
            else:
                print_error("Fichier PDF non créé")
        except Exception as e:
            print_error(f"Erreur génération PDF: {e}")
        
        # Test de génération Excel
        try:
            generator.generate_excel_report(test_data, 'test_report.xlsx')
            if os.path.exists('reports/test_report.xlsx'):
                print_success("Génération Excel réussie")
                os.remove('reports/test_report.xlsx')  # Nettoyer
            else:
                print_error("Fichier Excel non créé")
        except Exception as e:
            print_error(f"Erreur génération Excel: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors du test du générateur: {e}")
        return False

def test_flask_app():
    """Teste l'application Flask"""
    print_header("TEST DE L'APPLICATION FLASK")
    
    try:
        # Test d'import de l'app
        from app import app
        
        # Test de création de contexte
        with app.app_context():
            from app import db
            print_success("Contexte Flask créé avec succès")
            
            # Test de création de base de données
            try:
                db.create_all()
                print_success("Base de données créée avec succès")
            except Exception as e:
                print_error(f"Erreur création base de données: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors du test Flask: {e}")
        return False

def test_network_connectivity():
    """Teste la connectivité réseau"""
    print_header("TEST DE CONNECTIVITÉ RÉSEAU")
    
    try:
        import socket
        
        # Test de résolution DNS
        try:
            socket.gethostbyname('localhost')
            print_success("Résolution DNS locale fonctionnelle")
        except Exception as e:
            print_error(f"Erreur résolution DNS: {e}")
        
        # Test de ping local
        try:
            result = subprocess.run(['ping', '-n', '1', '127.0.0.1'] if os.name == 'nt' else ['ping', '-c', '1', '127.0.0.1'],
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print_success("Ping local fonctionnel")
            else:
                print_warning("Ping local échoué")
        except Exception as e:
            print_warning(f"Test ping non disponible: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur test connectivité: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🏭 CENTRAL DANONE - TEST DU SYSTÈME DE SUPERVISION")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Version Python", test_python_version),
        ("Dépendances Python", test_dependencies),
        ("Nmap", test_nmap),
        ("Dossiers", test_directories),
        ("Modules application", test_modules),
        ("Scanner réseau", test_network_scanner),
        ("Générateur de rapports", test_report_generator),
        ("Application Flask", test_flask_app),
        ("Connectivité réseau", test_network_connectivity)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print_header("RÉSUMÉ DES TESTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print_success("🎉 Tous les tests sont passés! Le système est prêt.")
        print_info("Vous pouvez maintenant lancer l'application avec: python app.py")
        return 0
    else:
        print_error("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 