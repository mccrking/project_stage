#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Phase 1 - Interface Utilisateur et UX
Dashboard Danone - Améliorations
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

class Phase1UITester:
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
    
    def test_theme_system(self):
        """Tester le système de thèmes"""
        print("\n🎨 Test du système de thèmes...")
        
        try:
            # Vérifier que les fichiers CSS et JS existent
            css_file = "static/css/theme.css"
            js_file = "static/js/theme.js"
            
            if os.path.exists(css_file):
                self.log_test("Fichier CSS thème", "PASS", "Fichier theme.css trouvé")
            else:
                self.log_test("Fichier CSS thème", "FAIL", "Fichier theme.css manquant")
            
            if os.path.exists(js_file):
                self.log_test("Fichier JS thème", "PASS", "Fichier theme.js trouvé")
            else:
                self.log_test("Fichier JS thème", "FAIL", "Fichier theme.js manquant")
            
            # Vérifier le contenu du fichier CSS
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                
            if '--danone-blue' in css_content:
                self.log_test("Variables CSS Danone", "PASS", "Variables de couleurs Danone définies")
            else:
                self.log_test("Variables CSS Danone", "FAIL", "Variables de couleurs Danone manquantes")
            
            if '[data-theme="dark"]' in css_content:
                self.log_test("Mode sombre CSS", "PASS", "Styles mode sombre définis")
            else:
                self.log_test("Mode sombre CSS", "FAIL", "Styles mode sombre manquants")
            
            # Vérifier le contenu du fichier JS
            with open(js_file, 'r', encoding='utf-8') as f:
                js_content = f.read()
                
            if 'class ThemeManager' in js_content:
                self.log_test("Classe ThemeManager", "PASS", "Classe ThemeManager trouvée")
            else:
                self.log_test("Classe ThemeManager", "FAIL", "Classe ThemeManager manquante")
            
            if 'localStorage.setItem' in js_content:
                self.log_test("Persistance thème", "PASS", "Persistance localStorage implémentée")
            else:
                self.log_test("Persistance thème", "FAIL", "Persistance localStorage manquante")
                
        except Exception as e:
            self.log_test("Système de thèmes", "FAIL", f"Erreur: {str(e)}")
    
    def test_notification_system(self):
        """Tester le système de notifications"""
        print("\n🔔 Test du système de notifications...")
        
        try:
            js_file = "static/js/theme.js"
            
            with open(js_file, 'r', encoding='utf-8') as f:
                js_content = f.read()
                
            if 'class NotificationManager' in js_content:
                self.log_test("Classe NotificationManager", "PASS", "Classe NotificationManager trouvée")
            else:
                self.log_test("Classe NotificationManager", "FAIL", "Classe NotificationManager manquante")
            
            if 'Notification.requestPermission' in js_content:
                self.log_test("Permissions notifications", "PASS", "Demande de permissions implémentée")
            else:
                self.log_test("Permissions notifications", "FAIL", "Demande de permissions manquante")
            
            if 'showToastNotification' in js_content:
                self.log_test("Notifications toast", "PASS", "Notifications toast implémentées")
            else:
                self.log_test("Notifications toast", "FAIL", "Notifications toast manquantes")
                
        except Exception as e:
            self.log_test("Système de notifications", "FAIL", f"Erreur: {str(e)}")
    
    def test_animation_system(self):
        """Tester le système d'animations"""
        print("\n✨ Test du système d'animations...")
        
        try:
            css_file = "static/css/theme.css"
            
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                
            if '@keyframes fadeIn' in css_content:
                self.log_test("Animation fadeIn", "PASS", "Animation fadeIn définie")
            else:
                self.log_test("Animation fadeIn", "FAIL", "Animation fadeIn manquante")
            
            if '@keyframes slideIn' in css_content:
                self.log_test("Animation slideIn", "PASS", "Animation slideIn définie")
            else:
                self.log_test("Animation slideIn", "FAIL", "Animation slideIn manquante")
            
            if '@keyframes pulse' in css_content:
                self.log_test("Animation pulse", "PASS", "Animation pulse définie")
            else:
                self.log_test("Animation pulse", "FAIL", "Animation pulse manquante")
            
            if 'transition:' in css_content:
                self.log_test("Transitions CSS", "PASS", "Transitions CSS définies")
            else:
                self.log_test("Transitions CSS", "FAIL", "Transitions CSS manquantes")
                
        except Exception as e:
            self.log_test("Système d'animations", "FAIL", f"Erreur: {str(e)}")
    
    def test_responsive_design(self):
        """Tester le design responsive"""
        print("\n📱 Test du design responsive...")
        
        try:
            css_file = "static/css/theme.css"
            
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                
            if '@media (max-width: 768px)' in css_content:
                self.log_test("Media queries mobile", "PASS", "Media queries mobile définies")
            else:
                self.log_test("Media queries mobile", "FAIL", "Media queries mobile manquantes")
            
            if 'mobile-card' in css_content:
                self.log_test("Classes mobile", "PASS", "Classes CSS mobile définies")
            else:
                self.log_test("Classes mobile", "FAIL", "Classes CSS mobile manquantes")
            
            if 'touch-device' in css_content:
                self.log_test("Support tactile", "PASS", "Support tactile implémenté")
            else:
                self.log_test("Support tactile", "FAIL", "Support tactile manquant")
                
        except Exception as e:
            self.log_test("Design responsive", "FAIL", f"Erreur: {str(e)}")
    
    def test_template_integration(self):
        """Tester l'intégration dans les templates"""
        print("\n🔗 Test de l'intégration dans les templates...")
        
        try:
            base_template = "templates/base.html"
            
            with open(base_template, 'r', encoding='utf-8') as f:
                template_content = f.read()
                
            if 'theme.css' in template_content:
                self.log_test("Lien CSS thème", "PASS", "Lien vers theme.css dans le template")
            else:
                self.log_test("Lien CSS thème", "FAIL", "Lien vers theme.css manquant")
            
            if 'theme.js' in template_content:
                self.log_test("Lien JS thème", "PASS", "Lien vers theme.js dans le template")
            else:
                self.log_test("Lien JS thème", "FAIL", "Lien vers theme.js manquant")
            
            if 'theme-color' in template_content:
                self.log_test("Meta theme-color", "PASS", "Meta theme-color définie")
            else:
                self.log_test("Meta theme-color", "FAIL", "Meta theme-color manquante")
                
        except Exception as e:
            self.log_test("Intégration templates", "FAIL", f"Erreur: {str(e)}")
    
    def test_logo_and_assets(self):
        """Tester les assets (logo, etc.)"""
        print("\n🖼️ Test des assets...")
        
        try:
            logo_file = "static/img/danone-logo.svg"
            
            if os.path.exists(logo_file):
                self.log_test("Logo Danone", "PASS", "Logo SVG Danone trouvé")
                
                with open(logo_file, 'r', encoding='utf-8') as f:
                    logo_content = f.read()
                    
                if 'DANONE' in logo_content:
                    self.log_test("Contenu logo", "PASS", "Logo contient le texte DANONE")
                else:
                    self.log_test("Contenu logo", "FAIL", "Logo ne contient pas DANONE")
            else:
                self.log_test("Logo Danone", "FAIL", "Logo SVG Danone manquant")
            
            # Vérifier la structure des dossiers
            static_dirs = ['static/css', 'static/js', 'static/img']
            for dir_path in static_dirs:
                if os.path.exists(dir_path):
                    self.log_test(f"Dossier {dir_path}", "PASS", f"Dossier {dir_path} trouvé")
                else:
                    self.log_test(f"Dossier {dir_path}", "FAIL", f"Dossier {dir_path} manquant")
                    
        except Exception as e:
            self.log_test("Assets", "FAIL", f"Erreur: {str(e)}")
    
    def test_configuration_files(self):
        """Tester les fichiers de configuration"""
        print("\n⚙️ Test des fichiers de configuration...")
        
        try:
            config_file = "config_advanced.py"
            
            if os.path.exists(config_file):
                self.log_test("Fichier config avancée", "PASS", "Fichier config_advanced.py trouvé")
                
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_content = f.read()
                    
                if 'UI_CONFIG' in config_content:
                    self.log_test("Configuration UI", "PASS", "Configuration UI définie")
                else:
                    self.log_test("Configuration UI", "FAIL", "Configuration UI manquante")
                
                if 'NOTIFICATION_CONFIG' in config_content:
                    self.log_test("Configuration notifications", "PASS", "Configuration notifications définie")
                else:
                    self.log_test("Configuration notifications", "FAIL", "Configuration notifications manquante")
                
                if 'DANONE_COLORS' in config_content:
                    self.log_test("Couleurs Danone", "PASS", "Palette de couleurs Danone définie")
                else:
                    self.log_test("Couleurs Danone", "FAIL", "Palette de couleurs Danone manquante")
            else:
                self.log_test("Fichier config avancée", "FAIL", "Fichier config_advanced.py manquant")
                
        except Exception as e:
            self.log_test("Configuration", "FAIL", f"Erreur: {str(e)}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 PHASE 1 - Test des améliorations Interface Utilisateur et UX")
        print("=" * 70)
        
        self.test_theme_system()
        self.test_notification_system()
        self.test_animation_system()
        self.test_responsive_design()
        self.test_template_integration()
        self.test_logo_and_assets()
        self.test_configuration_files()
        
        # Résumé
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        
        print(f"Total des tests: {total_tests}")
        print(f"Tests réussis: {passed_tests} ✅")
        print(f"Tests échoués: {failed_tests} ❌")
        print(f"Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
            print("✅ La Phase 1 (Interface Utilisateur et UX) est prête !")
        else:
            print(f"\n⚠️ {failed_tests} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
        
        # Sauvegarder les résultats
        with open('test_results_phase1.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Résultats sauvegardés dans: test_results_phase1.json")
        
        return failed_tests == 0

def main():
    """Fonction principale"""
    tester = Phase1UITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Prêt pour la Phase 2 : Fonctionnalités Avancées de Monitoring")
    else:
        print("\n🔧 Veuillez corriger les erreurs avant de passer à la phase suivante")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 