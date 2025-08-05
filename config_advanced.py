# ===== CONFIGURATION AVANCÉE - DASHBOARD DANONE =====

# Configuration des thèmes et interface utilisateur
UI_CONFIG = {
    'default_theme': 'light',
    'available_themes': ['light', 'dark'],
    'auto_detect_system_theme': True,
    'animation_duration': 300,  # ms
    'enable_animations': True,
    'enable_notifications': True,
    'notification_timeout': 5000,  # ms
    'mobile_breakpoint': 768,
    'tablet_breakpoint': 1024
}

# Configuration des notifications push
NOTIFICATION_CONFIG = {
    'enable_push_notifications': True,
    'enable_toast_notifications': True,
    'enable_sound_notifications': False,
    'notification_sound': '/static/sounds/notification.mp3',
    'max_notifications_display': 10,
    'notification_lifetime': 30000,  # ms
    'webhook_url': None,  # URL pour notifications externes
    'email_notifications': True
}

# Configuration du monitoring avancé
MONITORING_CONFIG = {
    'enable_service_monitoring': True,
    'enable_port_monitoring': True,
    'enable_bandwidth_monitoring': False,
    'enable_geolocation': False,
    'auto_discovery': True,
    'discovery_interval': 300,  # secondes
    
    # Services à surveiller
    'monitored_services': {
        'http': {'port': 80, 'timeout': 5},
        'https': {'port': 443, 'timeout': 5},
        'ftp': {'port': 21, 'timeout': 10},
        'ssh': {'port': 22, 'timeout': 10},
        'smtp': {'port': 25, 'timeout': 10},
        'dns': {'port': 53, 'timeout': 5},
        'snmp': {'port': 161, 'timeout': 10}
    },
    
    # Ports spécifiques à surveiller
    'monitored_ports': [
        80, 443, 22, 21, 25, 53, 161, 162,  # Services standards
        3389, 5900, 8080, 8443, 9000, 9090  # Services additionnels
    ],
    
    # Configuration SNMP
    'snmp_config': {
        'community': 'public',
        'version': 2,
        'timeout': 3,
        'retries': 3,
        'enabled': False
    }
}

# Configuration de l'IA avancée
AI_ADVANCED_CONFIG = {
    'enable_predictive_maintenance': True,
    'enable_intrusion_detection': True,
    'enable_auto_optimization': True,
    'enable_chatbot': True,
    'enable_trend_analysis': True,
    
    # Modèles de prédiction
    'prediction_models': {
        'failure_prediction': {
            'algorithm': 'random_forest',
            'confidence_threshold': 0.7,
            'training_interval': 24,  # heures
            'features': ['response_time', 'packet_loss', 'uptime', 'error_rate']
        },
        'anomaly_detection': {
            'algorithm': 'isolation_forest',
            'contamination': 0.1,
            'sensitivity': 0.8
        },
        'trend_analysis': {
            'algorithm': 'linear_regression',
            'forecast_period': 7,  # jours
            'min_data_points': 100
        }
    },
    
    # Chatbot IA
    'chatbot_config': {
        'model': 'gpt-3.5-turbo',
        'max_tokens': 150,
        'temperature': 0.7,
        'context_window': 10,
        'enable_learning': True
    }
}

# Configuration des rapports avancés
REPORTS_ADVANCED_CONFIG = {
    'enable_custom_dashboards': True,
    'enable_real_time_export': True,
    'enable_automated_reports': True,
    'enable_performance_comparison': True,
    
    # Formats d'export
    'export_formats': ['pdf', 'excel', 'csv', 'json', 'xml'],
    'chart_formats': ['png', 'svg', 'pdf'],
    
    # Rapports automatisés
    'automated_reports': {
        'daily': {
            'enabled': True,
            'time': '08:00',
            'recipients': [],
            'format': 'pdf',
            'include_charts': True
        },
        'weekly': {
            'enabled': True,
            'day': 'monday',
            'time': '09:00',
            'recipients': [],
            'format': 'excel',
            'include_charts': True
        },
        'monthly': {
            'enabled': True,
            'day': 1,
            'time': '10:00',
            'recipients': [],
            'format': 'pdf',
            'include_charts': True
        }
    }
}

# Configuration des intégrations
INTEGRATION_CONFIG = {
    'enable_rest_api': True,
    'enable_webhooks': True,
    'enable_snmp_integration': False,
    'enable_external_sync': False,
    'enable_cloud_backup': False,
    
    # API REST
    'api_config': {
        'version': 'v1',
        'rate_limit': 100,  # requêtes par minute
        'authentication': 'token',
        'cors_enabled': True,
        'documentation': True
    },
    
    # Webhooks
    'webhook_config': {
        'max_retries': 3,
        'timeout': 30,
        'signature_verification': True,
        'endpoints': {
            'device_status_change': None,
            'alert_triggered': None,
            'scan_completed': None,
            'report_generated': None
        }
    },
    
    # Synchronisation externe
    'sync_config': {
        'interval': 3600,  # secondes
        'batch_size': 100,
        'conflict_resolution': 'latest_wins',
        'external_systems': []
    }
}

# Configuration des performances
PERFORMANCE_CONFIG = {
    'enable_redis_cache': False,
    'enable_database_optimization': True,
    'enable_parallel_scanning': True,
    'enable_load_balancing': False,
    'enable_performance_monitoring': True,
    
    # Cache Redis
    'redis_config': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,
        'ttl': 3600,  # secondes
        'max_memory': '256mb'
    },
    
    # Optimisation base de données
    'database_config': {
        'connection_pool_size': 10,
        'query_timeout': 30,
        'enable_indexing': True,
        'vacuum_interval': 24,  # heures
        'backup_interval': 24   # heures
    },
    
    # Scan parallèle
    'parallel_scan_config': {
        'max_workers': 10,
        'chunk_size': 50,
        'timeout_per_host': 5,
        'retry_failed': True
    }
}

# Configuration des fonctionnalités métier
BUSINESS_CONFIG = {
    'enable_ticket_management': False,
    'enable_approval_workflow': False,
    'enable_maintenance_scheduling': False,
    'enable_vendor_management': False,
    'enable_compliance': False,
    
    # Gestion des tickets
    'ticket_config': {
        'auto_assignment': True,
        'escalation_rules': True,
        'sla_targets': {
            'critical': 1,    # heure
            'high': 4,        # heures
            'medium': 24,     # heures
            'low': 72         # heures
        }
    },
    
    # Workflow d'approbation
    'approval_config': {
        'require_approval_for': ['network_changes', 'security_updates'],
        'approvers': [],
        'auto_approve_low_risk': True,
        'approval_timeout': 24  # heures
    },
    
    # Planification des maintenances
    'maintenance_config': {
        'enable_scheduling': True,
        'maintenance_windows': [],
        'notification_advance': 24,  # heures
        'auto_reschedule_on_conflict': True
    },
    
    # Conformité
    'compliance_config': {
        'gdpr_enabled': False,
        'data_retention_days': 365,
        'audit_logging': True,
        'data_encryption': False
    }
}

# Configuration des couleurs Danone
DANONE_COLORS = {
    'primary_blue': '#0066CC',
    'light_blue': '#4A90E2',
    'dark_blue': '#004499',
    'green': '#00A651',
    'orange': '#FF6B35',
    'red': '#E74C3C',
    'yellow': '#F39C12',
    'gray': '#95A5A6',
    'light_gray': '#ECF0F1',
    'dark_gray': '#2C3E50'
}

# Configuration des alertes avancées
ALERT_ADVANCED_CONFIG = {
    'enable_smart_alerts': True,
    'enable_alert_correlation': True,
    'enable_alert_escalation': True,
    'enable_alert_suppression': True,
    
    # Alertes intelligentes
    'smart_alerts': {
        'learning_enabled': True,
        'false_positive_reduction': True,
        'context_aware': True,
        'adaptive_thresholds': True
    },
    
    # Corrélation d'alertes
    'correlation_config': {
        'time_window': 300,  # secondes
        'similarity_threshold': 0.8,
        'max_correlated_alerts': 5
    },
    
    # Escalade d'alertes
    'escalation_config': {
        'levels': [
            {'level': 1, 'timeout': 300, 'action': 'email'},
            {'level': 2, 'timeout': 900, 'action': 'sms'},
            {'level': 3, 'timeout': 1800, 'action': 'phone'}
        ]
    }
}

# Configuration de sécurité avancée
SECURITY_ADVANCED_CONFIG = {
    'enable_advanced_auth': False,
    'enable_audit_logging': True,
    'enable_session_management': True,
    'enable_rate_limiting': True,
    
    # Authentification avancée
    'auth_config': {
        'mfa_enabled': False,
        'mfa_methods': ['sms', 'email', 'totp'],
        'session_timeout': 3600,  # secondes
        'max_failed_attempts': 5,
        'lockout_duration': 900   # secondes
    },
    
    # Audit logging
    'audit_config': {
        'log_all_actions': True,
        'retention_days': 365,
        'encrypt_logs': False,
        'export_logs': False
    }
}

# Configuration de développement
DEV_CONFIG = {
    'debug_mode': False,
    'enable_hot_reload': True,
    'enable_auto_backup': True,
    'enable_performance_profiling': False,
    
    # Hot reload
    'hot_reload_config': {
        'watch_directories': ['templates', 'static', 'app.py'],
        'exclude_patterns': ['*.pyc', '__pycache__', '*.log'],
        'reload_delay': 1  # secondes
    },
    
    # Auto backup
    'backup_config': {
        'interval': 3600,  # secondes
        'max_backups': 10,
        'backup_database': True,
        'backup_config_files': True,
        'backup_models': True
    }
} 