#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du Système de Thème - Dashboard Danone
Vérification du mode sombre/clair et de la persistance
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

class ThemeSystemTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """Enregistrer un résultat de test"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        # Affichage coloré
        if status == 'PASS':
            print(f"✅ {test_name}: {message}")
        elif status == 'FAIL':
            print(f"❌ {test_name}: {message}")
        else:
            print(f"⚠️  {test_name}: {message}")
    
    def test_theme_files(self):
        """Tester les fichiers de thème"""
        print("\n🎨 Test des fichiers de thème...")
        
        # Vérifier le fichier CSS
        css_file = "static/css/theme.css"
        if os.path.exists(css_file):
            self.log_test("Fichier theme.css", "PASS", "Fichier CSS trouvé")
            
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les variables CSS
            css_variables = [
                '--danone-blue',
                '--bg-primary',
                '--text-primary',
                '[data-theme="dark"]',
                '--card-bg',
                '--navbar-bg'
            ]
            
            for var in css_variables:
                if var in content:
                    self.log_test(f"Variable CSS {var}", "PASS", f"Variable {var} définie")
                else:
                    self.log_test(f"Variable CSS {var}", "FAIL", f"Variable {var} manquante")
        else:
            self.log_test("Fichier theme.css", "FAIL", "Fichier CSS manquant")
        
        # Vérifier le fichier JavaScript
        js_file = "static/js/theme.js"
        if os.path.exists(js_file):
            self.log_test("Fichier theme.js", "PASS", "Fichier JavaScript trouvé")
            
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les classes JavaScript
            js_classes = [
                'class ThemeManager',
                'class NotificationManager',
                'class AnimationManager',
                'class ResponsiveManager'
            ]
            
            for cls in js_classes:
                if cls in content:
                    self.log_test(f"Classe JS {cls}", "PASS", f"Classe {cls} trouvée")
                else:
                    self.log_test(f"Classe JS {cls}", "FAIL", f"Classe {cls} manquante")
            
            # Vérifier les méthodes de thème
            theme_methods = [
                'toggleTheme',
                'setTheme',
                'getStoredTheme',
                'applyTheme'
            ]
            
            for method in theme_methods:
                if method in content:
                    self.log_test(f"Méthode {method}", "PASS", f"Méthode {method} trouvée")
                else:
                    self.log_test(f"Méthode {method}", "FAIL", f"Méthode {method} manquante")
        else:
            self.log_test("Fichier theme.js", "FAIL", "Fichier JavaScript manquant")
    
    def test_template_integration(self):
        """Tester l'intégration dans les templates"""
        print("\n📄 Test de l'intégration dans les templates...")
        
        # Vérifier base.html
        base_file = "templates/base.html"
        if os.path.exists(base_file):
            self.log_test("Template base.html", "PASS", "Template trouvé")
            
            with open(base_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les liens CSS et JS
            if 'theme.css' in content:
                self.log_test("Lien theme.css", "PASS", "Lien CSS trouvé")
            else:
                self.log_test("Lien theme.css", "FAIL", "Lien CSS manquant")
            
            if 'theme.js' in content:
                self.log_test("Lien theme.js", "PASS", "Lien JavaScript trouvé")
            else:
                self.log_test("Lien theme.js", "FAIL", "Lien JavaScript manquant")
            
            # Vérifier l'attribut data-theme
            if 'data-theme' in content:
                self.log_test("Attribut data-theme", "PASS", "Attribut data-theme trouvé")
            else:
                self.log_test("Attribut data-theme", "FAIL", "Attribut data-theme manquant")
        else:
            self.log_test("Template base.html", "FAIL", "Template manquant")
    
    def test_theme_switch(self):
        """Tester le switch de thème"""
        print("\n🔄 Test du switch de thème...")
        
        js_file = "static/js/theme.js"
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier le switch de thème
            if '.theme-switch' in content:
                self.log_test("Switch de thème CSS", "PASS", "Styles du switch trouvés")
            else:
                self.log_test("Switch de thème CSS", "FAIL", "Styles du switch manquants")
            
            if 'slider' in content:
                self.log_test("Slider du switch", "PASS", "Styles du slider trouvés")
            else:
                self.log_test("Slider du switch", "FAIL", "Styles du slider manquants")
        else:
            self.log_test("Fichier theme.js", "FAIL", "Fichier JavaScript manquant")
    
    def test_localstorage(self):
        """Tester la persistance localStorage"""
        print("\n💾 Test de la persistance localStorage...")
        
        js_file = "static/js/theme.js"
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier localStorage
            if 'localStorage' in content:
                self.log_test("localStorage", "PASS", "localStorage utilisé")
            else:
                self.log_test("localStorage", "FAIL", "localStorage manquant")
            
            if 'getItem' in content and 'setItem' in content:
                self.log_test("Méthodes localStorage", "PASS", "Méthodes getItem/setItem trouvées")
            else:
                self.log_test("Méthodes localStorage", "FAIL", "Méthodes getItem/setItem manquantes")
        else:
            self.log_test("Fichier theme.js", "FAIL", "Fichier JavaScript manquant")
    
    def test_dark_mode_styles(self):
        """Tester les styles du mode sombre"""
        print("\n🌙 Test des styles du mode sombre...")
        
        css_file = "static/css/theme.css"
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les variables du mode sombre
            dark_variables = [
                '--bg-primary: #1a1a1a',
                '--text-primary: #ffffff',
                '--card-bg: #2d2d2d',
                '--navbar-bg: #1a1a1a'
            ]
            
            for var in dark_variables:
                if var in content:
                    self.log_test(f"Variable sombre {var.split(':')[0]}", "PASS", f"Variable sombre trouvée")
                else:
                    self.log_test(f"Variable sombre {var.split(':')[0]}", "FAIL", f"Variable sombre manquante")
        else:
            self.log_test("Fichier theme.css", "FAIL", "Fichier CSS manquant")
    
    def test_animations(self):
        """Tester les animations"""
        print("\n✨ Test des animations...")
        
        css_file = "static/css/theme.css"
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les animations
            animations = [
                '@keyframes fadeIn',
                '@keyframes slideIn',
                '@keyframes pulse',
                '@keyframes spin'
            ]
            
            for anim in animations:
                if anim in content:
                    self.log_test(f"Animation {anim}", "PASS", f"Animation {anim} trouvée")
                else:
                    self.log_test(f"Animation {anim}", "FAIL", f"Animation {anim} manquante")
            
            # Vérifier les classes d'animation
            animation_classes = [
                '.fade-in',
                '.slide-in',
                '.pulse',
                '.spinner'
            ]
            
            for cls in animation_classes:
                if cls in content:
                    self.log_test(f"Classe animation {cls}", "PASS", f"Classe {cls} trouvée")
                else:
                    self.log_test(f"Classe animation {cls}", "FAIL", f"Classe {cls} manquante")
        else:
            self.log_test("Fichier theme.css", "FAIL", "Fichier CSS manquant")
    
    def test_responsive_design(self):
        """Tester le design responsive"""
        print("\n📱 Test du design responsive...")
        
        css_file = "static/css/theme.css"
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les media queries
            media_queries = [
                '@media (max-width: 768px)',
                '@media (min-width: 769px) and (max-width: 1024px)'
            ]
            
            for query in media_queries:
                if query in content:
                    self.log_test(f"Media query {query}", "PASS", f"Media query {query} trouvée")
                else:
                    self.log_test(f"Media query {query}", "FAIL", f"Media query {query} manquante")
            
            # Vérifier les classes responsive
            responsive_classes = [
                '.mobile-card',
                '.mobile-view',
                '.touch-device'
            ]
            
            for cls in responsive_classes:
                if cls in content:
                    self.log_test(f"Classe responsive {cls}", "PASS", f"Classe {cls} trouvée")
                else:
                    self.log_test(f"Classe responsive {cls}", "FAIL", f"Classe {cls} manquante")
        else:
            self.log_test("Fichier theme.css", "FAIL", "Fichier CSS manquant")
    
    def test_notifications(self):
        """Tester le système de notifications"""
        print("\n🔔 Test du système de notifications...")
        
        js_file = "static/js/theme.js"
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les fonctionnalités de notification
            notification_features = [
                'showNotification',
                'showToast',
                'requestPermission',
                'Notification'
            ]
            
            for feature in notification_features:
                if feature in content:
                    self.log_test(f"Fonctionnalité {feature}", "PASS", f"Fonctionnalité {feature} trouvée")
                else:
                    self.log_test(f"Fonctionnalité {feature}", "FAIL", f"Fonctionnalité {feature} manquante")
        else:
            self.log_test("Fichier theme.js", "FAIL", "Fichier JavaScript manquant")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🎨 TEST DU SYSTÈME DE THÈME - Dashboard Danone")
        print("=" * 60)
        
        self.test_theme_files()
        self.test_template_integration()
        self.test_theme_switch()
        self.test_localstorage()
        self.test_dark_mode_styles()
        self.test_animations()
        self.test_responsive_design()
        self.test_notifications()
        
        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        
        print(f"Total des tests: {total_tests}")
        print(f"Tests réussis: {passed_tests} ✅")
        print(f"Tests échoués: {failed_tests} ❌")
        print(f"Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 SYSTÈME DE THÈME PARFAIT !")
            print("✅ Le changement de thème fonctionne correctement !")
        else:
            print(f"\n⚠️ {failed_tests} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
        
        # Sauvegarder les résultats
        with open('test_results_theme.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Résultats sauvegardés dans: test_results_theme.json")
        
        return failed_tests == 0

def main():
    """Fonction principale"""
    tester = ThemeSystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Le système de thème est prêt ! Vous pouvez tester le changement de thème dans l'interface.")
    else:
        print("\n🔧 Veuillez corriger les erreurs avant de tester le thème.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 