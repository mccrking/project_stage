#!/usr/bin/env python3
"""
Gestionnaire de paramètres pour la plateforme de supervision réseau Central Danone
Permet de sauvegarder et charger les paramètres depuis un fichier JSON
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SettingsManager:
    """Gestionnaire de paramètres avec persistance JSON"""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings = self._load_default_settings()
        self._load_settings()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """Charger les paramètres par défaut"""
        return {
            # Configuration réseau
            'network_range': '192.168.1.0/24',
            'scan_interval': 300,  # 5 minutes
            'scan_timeout': 10,
            'max_retries': 2,
            'enable_auto_scan': True,
            
            # Configuration des alertes
            'alert_threshold': 85,
            'alert_device_offline': True,
            'alert_device_online': True,
            'alert_low_uptime': True,
            'alert_scan_failed': False,
            'alert_email': '',
            
            # Configuration des rapports
            'auto_report': 'daily',
            'report_format': 'pdf',
            'report_time': '08:00',
            'report_retention': 30,
            'include_charts': True,
            'include_alerts': True,
            
            # Configuration email SMTP
            'email_enabled': False,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email_username': '',
            'email_password': '',
            'from_email': '',
            'to_email': '',
            
            # Métadonnées
            'last_updated': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    
    def _load_settings(self) -> None:
        """Charger les paramètres depuis le fichier JSON"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # Fusionner avec les paramètres par défaut
                    self.settings.update(saved_settings)
                    logger.info(f"Paramètres chargés depuis {self.settings_file}")
            else:
                logger.info("Fichier de paramètres non trouvé, utilisation des valeurs par défaut")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des paramètres: {e}")
    
    def save_settings(self) -> bool:
        """Sauvegarder les paramètres dans le fichier JSON"""
        try:
            # Mettre à jour la date de modification
            self.settings['last_updated'] = datetime.now().isoformat()
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Paramètres sauvegardés dans {self.settings_file}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des paramètres: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Récupérer un paramètre"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Définir un paramètre"""
        try:
            self.settings[key] = value
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la définition du paramètre {key}: {e}")
            return False
    
    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Mettre à jour plusieurs paramètres"""
        try:
            self.settings.update(new_settings)
            return self.save_settings()
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des paramètres: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Récupérer tous les paramètres"""
        return self.settings.copy()
    
    def reset_to_defaults(self) -> bool:
        """Réinitialiser aux valeurs par défaut"""
        try:
            self.settings = self._load_default_settings()
            return self.save_settings()
        except Exception as e:
            logger.error(f"Erreur lors de la réinitialisation: {e}")
            return False
    
    def get_network_settings(self) -> Dict[str, Any]:
        """Récupérer les paramètres réseau"""
        return {
            'network_range': self.get_setting('network_range'),
            'scan_interval': self.get_setting('scan_interval'),
            'scan_timeout': self.get_setting('scan_timeout'),
            'max_retries': self.get_setting('max_retries'),
            'enable_auto_scan': self.get_setting('enable_auto_scan')
        }
    
    def get_alert_settings(self) -> Dict[str, Any]:
        """Récupérer les paramètres d'alertes"""
        return {
            'alert_threshold': self.get_setting('alert_threshold'),
            'alert_device_offline': self.get_setting('alert_device_offline'),
            'alert_device_online': self.get_setting('alert_device_online'),
            'alert_low_uptime': self.get_setting('alert_low_uptime'),
            'alert_scan_failed': self.get_setting('alert_scan_failed'),
            'alert_email': self.get_setting('alert_email')
        }
    
    def get_report_settings(self) -> Dict[str, Any]:
        """Récupérer les paramètres de rapports"""
        return {
            'auto_report': self.get_setting('auto_report'),
            'report_format': self.get_setting('report_format'),
            'report_time': self.get_setting('report_time'),
            'report_retention': self.get_setting('report_retention'),
            'include_charts': self.get_setting('include_charts'),
            'include_alerts': self.get_setting('include_alerts')
        }
    
    def get_email_settings(self) -> Dict[str, Any]:
        """Récupérer les paramètres email"""
        return {
            'enabled': self.get_setting('email_enabled'),
            'smtp_server': self.get_setting('smtp_server'),
            'smtp_port': self.get_setting('smtp_port'),
            'username': self.get_setting('email_username'),
            'from_email': self.get_setting('from_email'),
            'to_email': self.get_setting('to_email')
        }
    
    def backup_settings(self, backup_file: str = None) -> bool:
        """Créer une sauvegarde des paramètres"""
        try:
            if backup_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"settings_backup_{timestamp}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Sauvegarde créée: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def restore_settings(self, backup_file: str) -> bool:
        """Restaurer les paramètres depuis une sauvegarde"""
        try:
            if not os.path.exists(backup_file):
                logger.error(f"Fichier de sauvegarde non trouvé: {backup_file}")
                return False
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_settings = json.load(f)
            
            self.settings.update(backup_settings)
            return self.save_settings()
        except Exception as e:
            logger.error(f"Erreur lors de la restauration: {e}")
            return False

# Instance globale du gestionnaire de paramètres
settings_manager = SettingsManager()

def get_settings_manager() -> SettingsManager:
    """Récupérer l'instance globale du gestionnaire de paramètres"""
    return settings_manager 