#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des tableaux avec le système de thème
"""

import os
import json
from datetime import datetime

class TableThemeTester:
    def __init__(self):
        self.results = []
        self.test_count = 0
        self.passed_count = 0
        
    def log_test(self, test_name, status, message):
        self.test_count += 1
        if status == "PASS":
            self.passed_count += 1
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
        
        self.results.append({
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_table_styles(self):
        """Test des styles de tableaux dans theme.css"""
        print("\n🎨 Test des styles de tableaux...")
        
        try:
            with open("static/css/theme.css", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Test des styles table-hover
            if ".table-hover tbody tr:hover" in content:
                self.log_test("Table hover", "PASS", "Style table-hover trouvé")
            else:
                self.log_test("Table hover", "FAIL", "Style table-hover manquant")
            
            if ".table-hover tbody tr" in content:
                self.log_test("Table hover base", "PASS", "Style table-hover base trouvé")
            else:
                self.log_test("Table hover base", "FAIL", "Style table-hover base manquant")
            
            # Test des badges dans les tableaux
            if ".table .badge.bg-success" in content:
                self.log_test("Badge success", "PASS", "Style badge success trouvé")
            else:
                self.log_test("Badge success", "FAIL", "Style badge success manquant")
            
            if ".table .badge.bg-danger" in content:
                self.log_test("Badge danger", "PASS", "Style badge danger trouvé")
            else:
                self.log_test("Badge danger", "FAIL", "Style badge danger manquant")
            
            # Test des textes dans les tableaux
            if ".table .text-success" in content:
                self.log_test("Texte success", "PASS", "Style texte success trouvé")
            else:
                self.log_test("Texte success", "FAIL", "Style texte success manquant")
            
            if ".table .text-danger" in content:
                self.log_test("Texte danger", "PASS", "Style texte danger trouvé")
            else:
                self.log_test("Texte danger", "FAIL", "Style texte danger manquant")
            
            # Test des boutons dans les tableaux
            if ".table .btn-outline-primary" in content:
                self.log_test("Bouton primary", "PASS", "Style bouton primary trouvé")
            else:
                self.log_test("Bouton primary", "FAIL", "Style bouton primary manquant")
            
            if ".table .btn-outline-info" in content:
                self.log_test("Bouton info", "PASS", "Style bouton info trouvé")
            else:
                self.log_test("Bouton info", "FAIL", "Style bouton info manquant")
                
        except FileNotFoundError:
            self.log_test("Fichier theme.css", "FAIL", "Fichier theme.css non trouvé")
        except Exception as e:
            self.log_test("Lecture theme.css", "FAIL", f"Erreur: {str(e)}")
    
    def test_table_templates(self):
        """Test des tableaux dans les templates"""
        print("\n📄 Test des tableaux dans les templates...")
        
        templates_to_check = [
            "templates/dashboard.html",
            "templates/alerts.html", 
            "templates/reports.html",
            "templates/advanced_monitoring.html"
        ]
        
        for template in templates_to_check:
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                template_name = os.path.basename(template)
                
                if "table-hover" in content:
                    self.log_test(f"Table hover dans {template_name}", "PASS", "Classe table-hover trouvée")
                else:
                    self.log_test(f"Table hover dans {template_name}", "FAIL", "Classe table-hover manquante")
                
                if "badge bg-" in content:
                    self.log_test(f"Badges dans {template_name}", "PASS", "Badges trouvés")
                else:
                    self.log_test(f"Badges dans {template_name}", "FAIL", "Badges manquants")
                
                if "btn-outline-" in content:
                    self.log_test(f"Boutons dans {template_name}", "PASS", "Boutons outline trouvés")
                else:
                    self.log_test(f"Boutons dans {template_name}", "FAIL", "Boutons outline manquants")
                    
            except FileNotFoundError:
                self.log_test(f"Template {template}", "FAIL", f"Fichier {template} non trouvé")
            except Exception as e:
                self.log_test(f"Lecture {template}", "FAIL", f"Erreur: {str(e)}")
    
    def test_variables_css(self):
        """Test des variables CSS pour les tableaux"""
        print("\n🎨 Test des variables CSS...")
        
        try:
            with open("static/css/theme.css", 'r', encoding='utf-8') as f:
                content = f.read()
            
            variables_to_check = [
                "--card-bg",
                "--text-primary", 
                "--bg-tertiary",
                "--danone-green",
                "--danone-red",
                "--danone-blue",
                "--danone-light-blue",
                "--text-muted"
            ]
            
            for var in variables_to_check:
                if var in content:
                    self.log_test(f"Variable {var}", "PASS", f"Variable {var} définie")
                else:
                    self.log_test(f"Variable {var}", "FAIL", f"Variable {var} manquante")
                    
        except Exception as e:
            self.log_test("Variables CSS", "FAIL", f"Erreur: {str(e)}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🎨 TEST DES TABLEAUX AVEC LE SYSTÈME DE THÈME")
        print("=" * 60)
        
        self.test_table_styles()
        self.test_table_templates()
        self.test_variables_css()
        
        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        print(f"Total des tests: {self.test_count}")
        print(f"Tests réussis: {self.passed_count} ✅")
        print(f"Tests échoués: {self.test_count - self.passed_count} ❌")
        print(f"Taux de réussite: {(self.passed_count / self.test_count * 100):.1f}%")
        
        if self.passed_count == self.test_count:
            print("\n🎉 TOUS LES TABLEAUX S'ADAPTENT AU THÈME !")
            print("✅ Les tableaux changent maintenant de couleur en mode sombre !")
        else:
            print("\n⚠️ Certains tests ont échoué. Vérifiez les corrections.")
        
        # Sauvegarder les résultats
        with open("test_results_table_theme.json", 'w', encoding='utf-8') as f:
            json.dump({
                "test_date": datetime.now().isoformat(),
                "total_tests": self.test_count,
                "passed_tests": self.passed_count,
                "failed_tests": self.test_count - self.passed_count,
                "success_rate": (self.passed_count / self.test_count * 100) if self.test_count > 0 else 0,
                "results": self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Résultats sauvegardés dans: test_results_table_theme.json")

if __name__ == "__main__":
    tester = TableThemeTester()
    tester.run_all_tests() 