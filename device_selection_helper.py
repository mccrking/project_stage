#!/usr/bin/env python3
"""
Assistant de sélection d'équipements pour faciliter la configuration
Permet au technicien de sélectionner visuellement les équipements à surveiller
"""

import json
import time
from datetime import datetime
from network_scanner_production import ProductionNetworkScanner

class DeviceSelectionHelper:
    """Assistant pour faciliter la sélection des équipements à surveiller"""
    
    def __init__(self):
        self.scanner = ProductionNetworkScanner()
        self.discovered_devices = []
        self.selected_devices = []
        
    def auto_discover_with_classification(self):
        """Auto-découverte intelligente avec classification automatique"""
        print("🔍 Découverte automatique des équipements...")
        print("=" * 60)
        
        # Scanner tous les réseaux
        self.discovered_devices = self.scanner.scan_all_networks(aggressive=True)
        
        # Classifier par criticité et type
        classified_devices = self._classify_devices_by_importance()
        
        print(f"\n✅ {len(self.discovered_devices)} équipements découverts et classifiés")
        return classified_devices
    
    def _classify_devices_by_importance(self):
        """Classifie les équipements par ordre d'importance"""
        classification = {
            'critical': [],      # Serveurs, routeurs, automates
            'important': [],     # Switches, NAS, imprimantes importantes
            'monitoring': [],    # Caméras, capteurs
            'standard': []       # Postes de travail, autres
        }
        
        for device in self.discovered_devices:
            device_type = device.get('type', 'Unknown').lower()
            hostname = device.get('hostname', '').lower()
            ports = device.get('ports', [])
            
            # Classification intelligente
            if device_type in ['server', 'router', 'automation']:
                classification['critical'].append(device)
            elif device_type in ['switch', 'nas', 'printer'] and self._is_important_device(device):
                classification['important'].append(device)
            elif device_type in ['camera', 'phone']:
                classification['monitoring'].append(device)
            else:
                classification['standard'].append(device)
        
        return classification
    
    def _is_important_device(self, device):
        """Détermine si un équipement est important"""
        hostname = device.get('hostname', '').lower()
        ports = device.get('ports', [])
        
        # Indices d'importance
        important_keywords = ['prod', 'srv', 'main', 'principal', 'server', 'critical']
        important_ports = [80, 443, 22, 21, 139, 445]  # Services critiques
        
        # Vérifier hostname
        if any(keyword in hostname for keyword in important_keywords):
            return True
            
        # Vérifier ports critiques
        if len(set(ports) & set(important_ports)) >= 2:
            return True
            
        return False
    
    def generate_smart_suggestions(self):
        """Génère des suggestions intelligentes pour la surveillance"""
        classified = self.auto_discover_with_classification()
        
        suggestions = {
            'auto_select': [],  # Sélection automatique recommandée
            'review': [],       # À examiner par le technicien
            'optional': []      # Optionnels
        }
        
        # Auto-sélection des équipements critiques
        suggestions['auto_select'] = classified['critical'] + classified['important']
        
        # Révision pour les équipements de monitoring
        suggestions['review'] = classified['monitoring']
        
        # Optionnels pour les équipements standard
        suggestions['optional'] = classified['standard']
        
        return suggestions
    
    def create_configuration_template(self, selected_devices):
        """Crée un template de configuration prêt à utiliser"""
        template = {
            'monitoring_config': {
                'created_at': datetime.now().isoformat(),
                'total_devices': len(selected_devices),
                'networks_monitored': list(set([self._get_network_from_ip(d['ip']) for d in selected_devices])),
                'devices': []
            }
        }
        
        for device in selected_devices:
            device_config = {
                'ip': device['ip'],
                'hostname': device['hostname'],
                'type': device['type'],
                'priority': self._get_priority_level(device),
                'alert_config': {
                    'ping_monitoring': True,
                    'port_monitoring': len(device.get('ports', [])) > 0,
                    'response_time_threshold': self._get_threshold_by_type(device['type']),
                    'notification_level': self._get_notification_level(device)
                },
                'monitoring_ports': device.get('ports', [])[:5],  # Top 5 ports
                'scan_interval': self._get_scan_interval(device),
                'auto_configured': True
            }
            template['monitoring_config']['devices'].append(device_config)
        
        return template
    
    def _get_network_from_ip(self, ip):
        """Extrait le réseau d'une IP"""
        parts = ip.split('.')
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    
    def _get_priority_level(self, device):
        """Détermine le niveau de priorité"""
        device_type = device.get('type', 'Unknown').lower()
        
        priority_map = {
            'server': 'high',
            'router': 'high',
            'automation': 'critical',
            'switch': 'medium',
            'nas': 'medium',
            'printer': 'medium',
            'camera': 'low',
            'phone': 'low',
            'workstation': 'low'
        }
        
        return priority_map.get(device_type, 'low')
    
    def _get_threshold_by_type(self, device_type):
        """Seuil de temps de réponse par type d'équipement"""
        thresholds = {
            'server': 50,      # 50ms max pour serveurs
            'router': 30,      # 30ms max pour routeurs
            'automation': 20,  # 20ms max pour automates (critique)
            'switch': 40,      # 40ms max pour switches
            'nas': 100,        # 100ms max pour NAS
            'printer': 200,    # 200ms max pour imprimantes
            'camera': 300,     # 300ms max pour caméras
            'phone': 150,      # 150ms max pour téléphones IP
            'workstation': 500 # 500ms max pour postes
        }
        
        return thresholds.get(device_type.lower(), 200)
    
    def _get_notification_level(self, device):
        """Niveau de notification par importance"""
        priority = self._get_priority_level(device)
        
        notification_map = {
            'critical': 'immediate',    # Email + SMS immédiat
            'high': 'urgent',          # Email immédiat
            'medium': 'normal',        # Email groupé
            'low': 'summary'           # Rapport quotidien seulement
        }
        
        return notification_map.get(priority, 'normal')
    
    def _get_scan_interval(self, device):
        """Intervalle de scan selon la criticité"""
        priority = self._get_priority_level(device)
        
        interval_map = {
            'critical': 60,    # 1 minute
            'high': 300,       # 5 minutes
            'medium': 900,     # 15 minutes
            'low': 1800        # 30 minutes
        }
        
        return interval_map.get(priority, 900)
    
    def save_configuration(self, config, filename="monitoring_config.json"):
        """Sauvegarde la configuration"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration sauvegardée: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False
    
    def print_configuration_summary(self, config):
        """Affiche un résumé de la configuration"""
        devices = config['monitoring_config']['devices']
        
        print("\n" + "="*60)
        print("📋 RÉSUMÉ DE LA CONFIGURATION DE SURVEILLANCE")
        print("="*60)
        
        # Statistiques générales
        total = len(devices)
        by_priority = {}
        by_type = {}
        
        for device in devices:
            priority = device['alert_config']['notification_level']
            device_type = device['type']
            
            by_priority[priority] = by_priority.get(priority, 0) + 1
            by_type[device_type] = by_type.get(device_type, 0) + 1
        
        print(f"📊 Total d'équipements: {total}")
        print(f"🌐 Réseaux surveillés: {len(config['monitoring_config']['networks_monitored'])}")
        
        print(f"\n📈 Répartition par priorité:")
        for priority, count in sorted(by_priority.items()):
            print(f"  {priority.capitalize()}: {count} équipements")
        
        print(f"\n🔧 Répartition par type:")
        for device_type, count in sorted(by_type.items()):
            print(f"  {device_type}: {count}")
        
        # Top 5 équipements critiques
        critical_devices = [d for d in devices if d['priority'] in ['critical', 'high']][:5]
        
        if critical_devices:
            print(f"\n🚨 Top équipements critiques:")
            for device in critical_devices:
                print(f"  • {device['ip']:15} - {device['hostname'][:30]} ({device['type']})")
        
        print("="*60)

def interactive_device_selection():
    """Interface interactive pour la sélection d'équipements"""
    helper = DeviceSelectionHelper()
    
    print("🎯 ASSISTANT DE CONFIGURATION - SURVEILLANCE RÉSEAU")
    print("Facilite la sélection des équipements à surveiller")
    print("="*60)
    
    # 1. Auto-découverte
    suggestions = helper.generate_smart_suggestions()
    
    print(f"\n🤖 SUGGESTIONS INTELLIGENTES:")
    print(f"✅ Sélection automatique recommandée: {len(suggestions['auto_select'])} équipements")
    print(f"👀 À examiner: {len(suggestions['review'])} équipements") 
    print(f"🔧 Optionnels: {len(suggestions['optional'])} équipements")
    
    # 2. Afficher les équipements critiques auto-sélectionnés
    if suggestions['auto_select']:
        print(f"\n🚨 ÉQUIPEMENTS CRITIQUES (Sélection automatique recommandée):")
        for i, device in enumerate(suggestions['auto_select'], 1):
            print(f"  {i:2d}. {device['ip']:15} - {device['hostname']:25} [{device['type']}]")
    
    # 3. Générer la configuration
    all_selected = suggestions['auto_select']  # Pour demo, auto-sélectionner les critiques
    
    if all_selected:
        config = helper.create_configuration_template(all_selected)
        helper.print_configuration_summary(config)
        
        # Sauvegarder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"monitoring_config_{timestamp}.json"
        
        if helper.save_configuration(config, filename):
            print(f"\n✅ Configuration prête à utiliser!")
            print(f"📁 Fichier: {filename}")
            print(f"🚀 Importez ce fichier dans votre système de surveillance")
        
        return config
    
    else:
        print("⚠️ Aucun équipement critique détecté")
        return None

if __name__ == "__main__":
    config = interactive_device_selection()
