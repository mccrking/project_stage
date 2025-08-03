#!/usr/bin/env python3
"""
Script de validation de l'installation Central Danone
Vérifie que tous les composants sont en place
"""

import os
import sys
import importlib

def check_python_version():
    """Vérifie la version de Python"""
    print("🐍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Version 3.8+ requise")
        return False

def check_required_files():
    """Vérifie la présence des fichiers requis"""
    print("\n📁 Vérification des fichiers requis...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/login.html',
        'templates/change_password.html',
        'templates/dashboard.html',
        'templates/base.html',
        'templates/alerts.html',
        'templates/reports.html',
        'templates/settings.html',
        'start_production_auth.bat',
        'test_auth.py',
        'README_AUTH.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MANQUANT")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_directories():
    """Vérifie la présence des répertoires"""
    print("\n📂 Vérification des répertoires...")
    
    directories = ['templates', 'static', 'reports', 'logs', 'ai_models']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"⚠️ {directory}/ - Création automatique...")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ {directory}/ - Créé")
            except Exception as e:
                print(f"❌ Erreur création {directory}/: {e}")
    
    return True

def check_flask_login():
    """Vérifie que Flask-Login est dans requirements.txt"""
    print("\n🔐 Vérification Flask-Login...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            if 'Flask-Login' in content:
                print("✅ Flask-Login dans requirements.txt")
                return True
            else:
                print("❌ Flask-Login manquant dans requirements.txt")
                return False
    except Exception as e:
        print(f"❌ Erreur lecture requirements.txt: {e}")
        return False

def check_authentication_routes():
    """Vérifie que les routes d'authentification sont présentes"""
    print("\n🛣️ Vérification des routes d'authentification...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_routes = [
            '@app.route(\'/login\'',
            '@app.route(\'/logout\'',
            '@app.route(\'/change-password\'',
            '@login_required',
            'Flask-Login',
            'UserMixin'
        ]
        
        missing_routes = []
        for route in required_routes:
            if route in content:
                print(f"✅ {route}")
            else:
                print(f"❌ {route} - MANQUANT")
                missing_routes.append(route)
        
        return len(missing_routes) == 0
        
    except Exception as e:
        print(f"❌ Erreur lecture app.py: {e}")
        return False

def check_user_model():
    """Vérifie que le modèle User est défini"""
    print("\n👤 Vérification du modèle User...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'class User(UserMixin, db.Model):' in content:
            print("✅ Modèle User défini")
            return True
        else:
            print("❌ Modèle User manquant")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification modèle User: {e}")
        return False

def check_default_users():
    """Vérifie que les utilisateurs par défaut sont créés"""
    print("\n👥 Vérification des utilisateurs par défaut...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'create_default_admin()' in content and 'admin123' in content and 'tech123' in content:
            print("✅ Utilisateurs par défaut configurés")
            return True
        else:
            print("❌ Utilisateurs par défaut manquants")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification utilisateurs: {e}")
        return False

def check_protected_routes():
    """Vérifie que les routes sont protégées"""
    print("\n🔒 Vérification de la protection des routes...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Compter les routes protégées
        protected_count = content.count('@login_required')
        total_routes = content.count('@app.route')
        
        print(f"✅ {protected_count} routes protégées sur {total_routes} routes totales")
        
        if protected_count >= 10:  # Au moins 10 routes protégées
            print("✅ Protection des routes suffisante")
            return True
        else:
            print("⚠️ Protection des routes insuffisante")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification protection: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🔍 VALIDATION DE L'INSTALLATION CENTRAL DANONE")
    print("=" * 50)
    
    # Tests
    tests = [
        check_python_version,
        check_required_files,
        check_directories,
        check_flask_login,
        check_authentication_routes,
        check_user_model,
        check_default_users,
        check_protected_routes
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests réussis: {passed}/{total}")
    print(f"Taux de réussite: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 VALIDATION RÉUSSIE !")
        print("✅ L'installation est complète et prête")
        print("✅ Le système d'authentification est configuré")
        print("✅ Toutes les fonctionnalités sont en place")
        print("\n🚀 Pour démarrer l'application:")
        print("   start_production_auth.bat")
        print("\n🔑 Identifiants par défaut:")
        print("   Admin: admin / admin123")
        print("   Technicien: technicien / tech123")
    else:
        print("\n⚠️ VALIDATION INCOMPLÈTE")
        print("🔧 Certains composants nécessitent une attention")
        print("📖 Consultez le README_AUTH.md pour plus d'informations")

if __name__ == "__main__":
    main() 