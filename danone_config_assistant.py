#!/usr/bin/env python3
"""
Interface Interactive de Configuration - Version Danone
Permet au technicien de configurer facilement la surveillance réseau
"""

import json
import os
from datetime import datetime
from device_selection_helper import DeviceSelectionHelper

class DanoneDeviceConfiguration:
    """Interface de configuration spécialisée pour l'environnement Danone"""
    
    def __init__(self):
        self.helper = DeviceSelectionHelper()
        self.config_file = "danone_monitoring_config.json"
        
    def run_interactive_setup(self):
        """Lance la configuration interactive complète"""
        print("🏭 CONFIGURATION SURVEILLANCE RÉSEAU - DANONE")
        print("=" * 60)
        print("Cet assistant va vous aider à configurer la surveillance")
        print("de vos équipements réseau de manière simple et rapide.")
        print("=" * 60)
        
        # Étape 1: Découverte automatique
        print("\n🔍 ÉTAPE 1: DÉCOUVERTE AUTOMATIQUE")
        print("-" * 40)
        
        discovered_devices = self.helper.auto_discover_with_classification()
        total_devices = sum(len(devices) for devices in discovered_devices.values())
        
        if total_devices == 0:
            print("❌ Aucun équipement détecté. Vérifiez votre connexion réseau.")
            return None
        
        print(f"\n✅ {total_devices} équipements découverts!")
        
        # Étape 2: Affichage par catégories
        print("\n📊 ÉTAPE 2: CLASSIFICATION DES ÉQUIPEMENTS")
        print("-" * 40)
        
        self._display_discovered_devices(discovered_devices)
        
        # Étape 3: Sélection interactive
        print("\n🎯 ÉTAPE 3: SÉLECTION DES ÉQUIPEMENTS À SURVEILLER")
        print("-" * 40)
        
        selected_devices = self._interactive_device_selection(discovered_devices)
        
        if not selected_devices:
            print("⚠️ Aucun équipement sélectionné.")
            return None
        
        # Étape 4: Configuration des paramètres
        print(f"\n⚙️ ÉTAPE 4: CONFIGURATION DES PARAMÈTRES")
        print("-" * 40)
        
        config = self._configure_monitoring_settings(selected_devices)
        
        # Étape 5: Sauvegarde
        print(f"\n💾 ÉTAPE 5: SAUVEGARDE DE LA CONFIGURATION")
        print("-" * 40)
        
        if self._save_final_configuration(config):
            print(f"\n🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS!")
            print(f"📁 Fichier de configuration: {self.config_file}")
            print(f"🚀 La surveillance est maintenant configurée pour {len(selected_devices)} équipements")
            return config
        
        return None
    
    def _display_discovered_devices(self, classified_devices):
        """Affiche les équipements découverts par catégorie"""
        
        categories = {
            'critical': '🚨 ÉQUIPEMENTS CRITIQUES',
            'important': '⚡ ÉQUIPEMENTS IMPORTANTS', 
            'monitoring': '📹 ÉQUIPEMENTS DE SURVEILLANCE',
            'standard': '💻 ÉQUIPEMENTS STANDARD'
        }
        
        for category, title in categories.items():
            devices = classified_devices.get(category, [])
            if devices:
                print(f"\n{title} ({len(devices)} équipements):")
                for i, device in enumerate(devices, 1):
                    status = "🟢" if device.get('is_online') else "🔴"
                    print(f"  {i:2d}. {status} {device['ip']:15} - {device['hostname'][:30]} [{device['type']}]")
        
        # Résumé
        total = sum(len(devices) for devices in classified_devices.values())
        print(f"\n📊 RÉSUMÉ: {total} équipements découverts")
        for category, devices in classified_devices.items():
            if devices:
                print(f"  - {categories[category]}: {len(devices)}")
    
    def _interactive_device_selection(self, classified_devices):
        """Interface de sélection interactive"""
        
        selected_devices = []
        
        # Auto-sélection des équipements critiques et importants
        auto_select = classified_devices.get('critical', []) + classified_devices.get('important', [])
        
        if auto_select:
            print(f"\n✅ SÉLECTION AUTOMATIQUE:")
            print(f"Les {len(auto_select)} équipements critiques/importants seront surveillés automatiquement:")
            for device in auto_select:
                print(f"  • {device['ip']} - {device['hostname']} [{device['type']}]")
            selected_devices.extend(auto_select)
        
        # Sélection manuelle pour les autres catégories  
        other_devices = classified_devices.get('monitoring', []) + classified_devices.get('standard', [])
        
        if other_devices:
            print(f"\n❓ SÉLECTION MANUELLE ({len(other_devices)} équipements disponibles):")
            print("Souhaitez-vous surveiller d'autres équipements ? (o/n):", end=" ")
            
            try:
                choice = input().lower().strip()
                if choice in ['o', 'oui', 'y', 'yes']:
                    selected_additional = self._manual_device_selection(other_devices)
                    selected_devices.extend(selected_additional)
            except (EOFError, KeyboardInterrupt):
                print("\nSélection automatique uniquement.")
        
        return selected_devices
    
    def _manual_device_selection(self, devices):
        """Sélection manuelle d'équipements"""
        
        selected = []
        
        print(f"\nListe des équipements disponibles:")
        for i, device in enumerate(devices, 1):
            status = "🟢" if device.get('is_online') else "🔴"
            print(f"  {i:2d}. {status} {device['ip']:15} - {device['hostname'][:30]} [{device['type']}]")
        
        print(f"\nEntrez les numéros des équipements à surveiller (ex: 1,3,5) ou 'tous' pour tous:")
        print("Ou appuyez sur Entrée pour passer:", end=" ")
        
        try:
            choice = input().strip()
            
            if choice.lower() in ['tous', 'all', '*']:
                selected = devices.copy()
                print(f"✅ Tous les {len(devices)} équipements sélectionnés")
            
            elif choice:
                # Parse des numéros
                try:
                    numbers = [int(x.strip()) for x in choice.split(',')]
                    for num in numbers:
                        if 1 <= num <= len(devices):
                            selected.append(devices[num-1])
                    
                    print(f"✅ {len(selected)} équipements sélectionnés")
                    
                except ValueError:
                    print("⚠️ Format invalide. Aucune sélection.")
            
        except (EOFError, KeyboardInterrupt):
            print("\nAucune sélection manuelle.")
        
        return selected
    
    def _configure_monitoring_settings(self, selected_devices):
        """Configuration des paramètres de surveillance"""
        
        print(f"Configuration automatique des paramètres pour {len(selected_devices)} équipements...")
        
        # Génération de la configuration optimisée
        config = self.helper.create_configuration_template(selected_devices)
        
        # Configuration spécifique Danone
        config['danone_config'] = {
            'plant_name': 'Usine Danone',
            'configured_by': 'Technicien IT',
            'configuration_date': datetime.now().isoformat(),
            'environment': 'production',
            'email_notifications': True,
            'sms_notifications': False,
            'report_frequency': 'daily'
        }
        
        # Affichage du résumé
        self.helper.print_configuration_summary(config)
        
        return config
    
    def _save_final_configuration(self, config):
        """Sauvegarde la configuration finale"""
        
        try:
            # Sauvegarde principale
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Sauvegarde de backup avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backup_config_{timestamp}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration sauvegardée:")
            print(f"   📄 Principal: {self.config_file}")
            print(f"   💾 Backup: {backup_file}")
            
            # Génération du fichier résumé pour le technicien
            self._generate_summary_report(config)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def _generate_summary_report(self, config):
        """Génère un rapport résumé pour le technicien"""
        
        devices = config['monitoring_config']['devices']
        danone_config = config.get('danone_config', {})
        
        report = f"""
RAPPORT DE CONFIGURATION - SURVEILLANCE RÉSEAU DANONE
=====================================================
Date de configuration: {danone_config.get('configuration_date', 'N/A')}
Configuré par: {danone_config.get('configured_by', 'N/A')}
Environnement: {danone_config.get('environment', 'N/A')}

RÉSUMÉ DE LA SURVEILLANCE:
- Équipements surveillés: {len(devices)}
- Réseaux couverts: {len(config['monitoring_config']['networks_monitored'])}
- Notifications email: {'Activées' if danone_config.get('email_notifications') else 'Désactivées'}
- Fréquence des rapports: {danone_config.get('report_frequency', 'N/A')}

ÉQUIPEMENTS CONFIGURÉS:
"""
        
        for i, device in enumerate(devices, 1):
            report += f"""
{i:2d}. {device['ip']:15} - {device['hostname'][:30]}
    Type: {device['type']}
    Priorité: {device['priority']}
    Seuil de réponse: {device['alert_config']['response_time_threshold']}ms
    Intervalle de scan: {device['scan_interval']}s
    Ports surveillés: {', '.join(map(str, device['monitoring_ports'][:3]))}{'...' if len(device['monitoring_ports']) > 3 else ''}
"""
        
        report += f"""
PROCHAINES ÉTAPES:
1. Importez le fichier '{self.config_file}' dans votre système de surveillance
2. Configurez vos paramètres email dans l'interface web
3. Testez les notifications d'alerte
4. Planifiez la maintenance préventive

SUPPORT TECHNIQUE:
En cas de problème, consultez la documentation ou contactez l'équipe IT.
"""
        
        # Sauvegarder le rapport
        report_file = "rapport_configuration_danone.txt"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"   📋 Rapport: {report_file}")
        except Exception as e:
            print(f"⚠️ Erreur génération rapport: {e}")

def main():
    """Point d'entrée principal"""
    configurator = DanoneDeviceConfiguration()
    config = configurator.run_interactive_setup()
    
    if config:
        print(f"\n🎯 CONFIGURATION RÉUSSIE!")
        print(f"Votre système de surveillance est maintenant prêt à fonctionner.")
    else:
        print(f"\n⚠️ Configuration incomplète.")
        print(f"Relancez l'assistant si nécessaire.")

if __name__ == "__main__":
    main()
