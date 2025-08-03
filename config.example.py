# Configuration du système de supervision Central Danone
# Copier ce fichier vers config.py et modifier selon vos besoins

# Configuration réseau
NETWORK_CONFIG = {
    'default_range': '192.168.1.0/24',  # Plage réseau par défaut
    'scan_interval': 60,                # Intervalle de scan en minutes
    'scan_timeout': 10,                 # Timeout de scan en secondes
    'max_retries': 2,                   # Nombre de tentatives
    'enable_auto_scan': True,           # Activer le scan automatique
}

# Configuration des alertes
ALERT_CONFIG = {
    'email': 'admin@centraldanone.com',  # Email pour les alertes
    'threshold': 85,                     # Seuil d'alerte en pourcentage
    'device_offline': True,              # Alerte appareil hors ligne
    'device_online': True,               # Alerte appareil de retour
    'low_uptime': True,                  # Alerte disponibilité faible
    'scan_failed': False,                # Alerte échec de scan
}

# Configuration des rapports
REPORT_CONFIG = {
    'auto_report': 'daily',              # Type de rapport automatique
    'default_format': 'pdf',             # Format par défaut
    'report_time': '08:00',              # Heure de génération
    'retention_days': 30,                # Rétention en jours
    'include_charts': True,              # Inclure les graphiques
    'include_alerts': True,              # Inclure l'historique des alertes
}

# Configuration de l'application
APP_CONFIG = {
    'debug': False,                      # Mode debug
    'host': '0.0.0.0',                  # Interface d'écoute
    'port': 5000,                       # Port d'écoute
    'secret_key': 'your-secret-key-here', # Clé secrète Flask
}

# Configuration de la base de données
DATABASE_CONFIG = {
    'uri': 'sqlite:///network_monitor.db',  # URI de la base de données
    'backup_enabled': True,                 # Activer les sauvegardes
    'backup_interval': 24,                  # Intervalle de sauvegarde en heures
}

# Configuration des logs
LOG_CONFIG = {
    'level': 'INFO',                     # Niveau de log
    'file': 'logs/network_monitor.log',  # Fichier de log
    'max_size': 10 * 1024 * 1024,        # Taille max du fichier (10MB)
    'backup_count': 5,                   # Nombre de fichiers de sauvegarde
}

# Types d'équipements détectés
DEVICE_TYPES = {
    'router': ['router', 'gateway', 'firewall'],
    'server': ['server', 'srv', 'dc', 'domain'],
    'printer': ['printer', 'print', 'hp', 'canon', 'epson'],
    'workstation': ['pc', 'workstation', 'desktop', 'laptop'],
    'switch': ['switch', 'sw', 'hub'],
    'camera': ['camera', 'cam', 'ipcam'],
    'phone': ['phone', 'voip', 'sip'],
    'automation': ['plc', 'automate', 'scada', 'hmi']
}

# Configuration de sécurité
SECURITY_CONFIG = {
    'enable_https': False,               # Activer HTTPS
    'ssl_cert': None,                    # Certificat SSL
    'ssl_key': None,                     # Clé SSL
    'allowed_hosts': ['localhost', '127.0.0.1'],  # Hôtes autorisés
}

# Configuration des performances
PERFORMANCE_CONFIG = {
    'max_concurrent_scans': 5,           # Nombre max de scans simultanés
    'scan_batch_size': 50,               # Taille des lots de scan
    'cache_timeout': 300,                # Timeout du cache en secondes
} 