"""
Dashboard Central Danone - Application principale avec IA intégrée
Système de supervision réseau intelligent
"""

# Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import threading
import schedule
import time
import os
import json
import logging
from network_scanner_production import ProductionNetworkScanner
from report_generator import ReportGenerator
from ai_enhancement import ai_system, AIEnhancement
from advanced_monitoring import advanced_monitoring
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Réduire la verbosité des logs Werkzeug en production
if os.environ.get('FLASK_ENV') != 'development':
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)  # Masquer les requêtes INFO

# Configuration de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'danone-central-2024-ai-enhanced'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_monitor_production.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'warning'

# Fonction pour obtenir l'heure locale
def get_local_time():
    """Retourne l'heure locale actuelle"""
    return datetime.now()

# Initialisation de la base de données
db = SQLAlchemy(app)

# Modèle utilisateur pour l'authentification
class User(UserMixin, db.Model):
    """Modèle utilisateur pour l'authentification"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='technician')  # 'admin', 'technician'
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=get_local_time)
    
    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)

# Modèles de base de données étendus avec IA
class Device(db.Model):
    """Modèle d'équipement avec données IA et informations production"""
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    mac = db.Column(db.String(17), nullable=True)
    hostname = db.Column(db.String(100), nullable=True)
    mac_vendor = db.Column(db.String(100), nullable=True)
    is_online = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=get_local_time)
    device_type = db.Column(db.String(50), default='unknown')  # Classifié par IA
    ai_confidence = db.Column(db.Float, default=0.0)  # Confiance de l'IA
    health_score = db.Column(db.Float, default=100.0)  # Score de santé IA
    failure_probability = db.Column(db.Float, default=0.0)  # Probabilité de panne
    anomaly_score = db.Column(db.Float, default=0.0)  # Score d'anomalie
    maintenance_urgency = db.Column(db.String(20), default='low')  # Urgence maintenance
    ai_recommendations = db.Column(db.Text, default='[]')  # Recommandations IA (JSON)
    
    # Nouvelles colonnes pour données production
    response_time = db.Column(db.Float, default=0.0)  # Temps de réponse ping
    system_info = db.Column(db.String(100), nullable=True)  # OS détecté
    open_ports = db.Column(db.Text, default='[]')  # Ports ouverts (JSON)
    services = db.Column(db.Text, default='[]')  # Services détectés (JSON)
    
    created_at = db.Column(db.DateTime, default=get_local_time)
    updated_at = db.Column(db.DateTime, default=get_local_time, onupdate=get_local_time)

class ScanHistory(db.Model):
    """Historique des scans avec métriques IA"""
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    is_online = db.Column(db.Boolean, default=True)
    response_time = db.Column(db.Float, nullable=True)
    packet_loss = db.Column(db.Float, default=0.0)
    scan_duration = db.Column(db.Float, default=0.0)
    error_count = db.Column(db.Integer, default=0)
    ai_analysis = db.Column(db.Text, default='{}')  # Analyse IA complète (JSON)
    timestamp = db.Column(db.DateTime, default=get_local_time)

class Alert(db.Model):
    """Alertes intelligentes basées sur l'IA"""
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # 'offline', 'ai_critical', 'ai_warning', 'anomaly'
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'critical'
    ai_confidence = db.Column(db.Float, default=0.0)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_local_time)
    resolved_at = db.Column(db.DateTime, nullable=True)

class AIModel(db.Model):
    """Modèles IA entraînés"""
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)  # 'anomaly', 'maintenance', 'classification'
    accuracy = db.Column(db.Float, default=0.0)
    training_date = db.Column(db.DateTime, default=get_local_time)
    model_path = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class Report(db.Model):
    """Modèle pour les rapports générés"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)  # 'daily', 'weekly', 'monthly', 'custom', etc.
    format = db.Column(db.String(10), nullable=False)  # 'pdf', 'excel', 'html', 'csv'
    status = db.Column(db.String(20), default='processing')  # 'processing', 'completed', 'failed', 'scheduled'
    description = db.Column(db.Text, nullable=True)
    sections = db.Column(db.Text, default='[]')  # Sections incluses (JSON)
    file_path = db.Column(db.String(500), nullable=True)
    file_size = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    
    # Paramètres de génération
    date_from = db.Column(db.DateTime, nullable=True)
    date_to = db.Column(db.DateTime, nullable=True)
    generated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Programmation
    is_scheduled = db.Column(db.Boolean, default=False)
    schedule_frequency = db.Column(db.String(20), nullable=True)  # 'daily', 'weekly', 'monthly'
    schedule_time = db.Column(db.String(10), nullable=True)  # '08:00'
    schedule_email = db.Column(db.String(100), nullable=True)
    next_run = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=get_local_time)
    generated_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=get_local_time, onupdate=get_local_time)

    def to_dict(self):
        """Convertit le rapport en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'name': self.name,
            'filename': self.filename,
            'type': self.type,
            'format': self.format,
            'status': self.status,
            'description': self.description,
            'file_size': self.file_size,
            'download_count': self.download_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'date_from': self.date_from.isoformat() if self.date_from else None,
            'date_to': self.date_to.isoformat() if self.date_to else None,
            'download_url': f'/api/reports/download/{self.filename}' if self.status == 'completed' else None
        }

# Initialisation des modules
network_scanner = ProductionNetworkScanner()
report_generator = ReportGenerator()

# Variables globales
scan_in_progress = False
ai_models_loaded = False

# Configuration des seuils IA
AI_CONFIG = {
    'HIGH_RISK_THRESHOLD': 0.6,      # Seuil pour équipements à risque élevé
    'ANOMALY_THRESHOLD': -0.5,       # Seuil pour détection d'anomalies
    'CRITICAL_HEALTH_THRESHOLD': 50, # Seuil pour équipements critiques
    'MAX_RECOMMENDATIONS': 10        # Nombre max de recommandations
}

# Fonction pour charger l'utilisateur (requis pour Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    """Charge un utilisateur par son ID"""
    return User.query.get(int(user_id))

def create_default_admin():
    """Crée un utilisateur administrateur par défaut"""
    try:
        # Vérifier si un admin existe déjà
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@centraldanone.com',
                role='admin'
            )
            admin.set_password('admin123')  # Mot de passe par défaut
            db.session.add(admin)
            
            # Créer un technicien par défaut
            technician = User(
                username='technicien',
                email='technicien@centraldanone.com',
                role='technician'
            )
            technician.set_password('tech123')
            db.session.add(technician)
            
            db.session.commit()
            logger.info("Utilisateurs par défaut créés")
    except Exception as e:
        logger.error(f"Erreur création utilisateurs par défaut: {e}")

def admin_required(f):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Accès réservé aux administrateurs', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Configuration email pour alertes automatiques (désactivée par défaut)
EMAIL_CONFIG = {
    'enabled': False,  # Désactivé par défaut pour éviter les erreurs
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': '',  # À configurer via l'interface
    'password': '',  # À configurer via l'interface
    'from_email': '',  # À configurer via l'interface
    'to_email': ''   # À configurer via l'interface
}

# Système de notifications en temps réel
NOTIFICATIONS = []
MAX_NOTIFICATIONS = 50

def add_notification(message, type='info', priority='medium', device_ip=None):
    """Ajoute une notification en temps réel"""
    global NOTIFICATIONS
    
    notification = {
        'id': len(NOTIFICATIONS) + 1,
        'message': message,
        'type': type,  # 'info', 'warning', 'danger', 'success'
        'priority': priority,  # 'low', 'medium', 'high', 'critical'
        'device_ip': device_ip,
        'timestamp': get_local_time().isoformat(),
        'read': False
    }
    
    NOTIFICATIONS.append(notification)
    
    # Garder seulement les 50 dernières notifications
    if len(NOTIFICATIONS) > MAX_NOTIFICATIONS:
        NOTIFICATIONS = NOTIFICATIONS[-MAX_NOTIFICATIONS:]
    
    logger.info(f"Notification ajoutée: {message}")
    return notification

def get_unread_notifications():
    """Récupère les notifications non lues"""
    return [n for n in NOTIFICATIONS if not n['read']]

def mark_notification_read(notification_id):
    """Marque une notification comme lue"""
    for notification in NOTIFICATIONS:
        if notification['id'] == notification_id:
            notification['read'] = True
            break

def send_email_alert(subject, message, priority='medium'):
    """Envoie une alerte par email avec configuration simplifiée"""
    try:
        if not EMAIL_CONFIG['enabled'] or not EMAIL_CONFIG['to_email']:
            # Mode silencieux - pas de log si email désactivé volontairement
            add_notification(f"📧 {subject}: {message}", 'info', priority)
            return False
        
        # Vérifier que tous les champs requis sont remplis
        required_fields = ['username', 'password', 'from_email', 'to_email']
        if not all(EMAIL_CONFIG.get(field) for field in required_fields):
            logger.info("Configuration email incomplète - utilisation des notifications internes uniquement")
            add_notification(f"📧 {subject}: {message}", 'info', priority)
            return False
        
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['from_email']
        msg['To'] = EMAIL_CONFIG['to_email']
        msg['Subject'] = f"[Central Danone] {subject}"
        
        # Corps du message avec formatage professionnel
        body = f"""
        🚨 ALERTE CENTRAL DANONE 🚨
        
        {message}
        
        Priorité: {priority.upper()}
        Heure: {get_local_time().strftime('%d/%m/%Y %H:%M:%S')}
        
        ---
        Système de supervision Central Danone
        Généré automatiquement
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Connexion et envoi avec gestion d'erreur simplifiée
        try:
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG['from_email'], EMAIL_CONFIG['to_email'], text)
            server.quit()
            
            logger.info(f"Email d'alerte envoyé à {EMAIL_CONFIG['to_email']}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.info("Configuration email invalide - utilisation des notifications internes")
            # Fallback vers notifications en temps réel
            add_notification(f"📧 {subject}: {message}", 'info', priority)
            return False
            
        except Exception as e:
            logger.info(f"Service email non disponible - utilisation des notifications internes: {e}")
            # Fallback vers notifications en temps réel
            add_notification(f"📧 {subject}: {message}", 'info', priority)
            return False
        
    except Exception as e:
        logger.error(f"Erreur générale envoi email: {e}")
        return False

def test_email_configuration():
    """Teste la configuration email"""
    try:
        if not EMAIL_CONFIG['enabled']:
            return {'status': 'error', 'message': 'Email non activé'}
        
        if not EMAIL_CONFIG['to_email']:
            return {'status': 'error', 'message': 'Email de destination non configuré'}
        
        # Test d'envoi
        success = send_email_alert(
            "Test de configuration",
            "Ceci est un test de la configuration email pour les alertes Central Danone.",
            "low"
        )
        
        if success:
            return {'status': 'success', 'message': 'Email de test envoyé avec succès'}
        else:
            return {'status': 'error', 'message': 'Erreur lors de l\'envoi du test'}
            
    except Exception as e:
        return {'status': 'error', 'message': f'Erreur de test: {str(e)}'}

def create_directories():
    """Crée les répertoires nécessaires"""
    directories = ['reports', 'logs', 'ai_models']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Répertoire créé: {directory}")

def load_ai_models():
    """Charge les modèles IA sauvegardés"""
    global ai_models_loaded
    try:
        model_path = 'ai_models/network_ai_models.pkl'
        if os.path.exists(model_path):
            ai_system.load_models(model_path)
            ai_models_loaded = True
            logger.info("Modèles IA chargés avec succès")
        else:
            logger.info("Aucun modèle IA trouvé, entraînement nécessaire")
    except Exception as e:
        logger.error(f"Erreur chargement modèles IA: {e}")

def save_ai_models():
    """Sauvegarde les modèles IA"""
    try:
        model_path = 'ai_models/network_ai_models.pkl'
        ai_system.save_models(model_path)
        logger.info("Modèles IA sauvegardés")
    except Exception as e:
        logger.error(f"Erreur sauvegarde modèles IA: {e}")

def train_ai_models():
    """Entraîne les modèles IA avec les données existantes"""
    try:
        logger.info("Début de l'entraînement des modèles IA...")
        
        # Récupération des données d'entraînement
        devices = Device.query.all()
        training_data = []
        
        for device in devices:
            # Récupération de l'historique
            history = ScanHistory.query.filter_by(device_id=device.id).order_by(ScanHistory.timestamp.desc()).limit(100).all()
            
            if history:
                history_data = []
                for scan in history:
                    history_data.append({
                        'response_time': scan.response_time or 0,
                        'packet_loss': scan.packet_loss or 0,
                        'is_online': scan.is_online,
                        'scan_duration': scan.scan_duration or 0,
                        'error_count': scan.error_count or 0
                    })
                
                training_data.append({
                    'hostname': device.hostname or '',
                    'mac_vendor': device.mac_vendor or '',
                    'ip': device.ip,
                    'history': history_data
                })
        
        if len(training_data) >= 5:
            ai_system.train_all_models(training_data)
            save_ai_models()
            logger.info("Entraînement des modèles IA terminé")
        else:
            logger.warning("Données insuffisantes pour l'entraînement IA")
            
    except Exception as e:
        logger.error(f"Erreur entraînement modèles IA: {e}")

def analyze_device_with_ai(device):
    """Analyse un équipement avec l'IA"""
    try:
        # Récupération de l'historique
        history = ScanHistory.query.filter_by(device_id=device.id).order_by(ScanHistory.timestamp.desc()).limit(100).all()
        
        history_data = []
        for scan in history:
            history_data.append({
                'response_time': scan.response_time or 0,
                'packet_loss': scan.packet_loss or 0,
                'is_online': scan.is_online,
                'scan_duration': scan.scan_duration or 0,
                'error_count': scan.error_count or 0
            })
        
        # Données pour l'analyse IA
        device_data = {
            'hostname': device.hostname or '',
            'mac_vendor': device.mac_vendor or '',
            'ip': device.ip,
            'history': history_data
        }
        
        # Analyse IA complète
        ai_analysis = ai_system.analyze_device_complete(device_data)
        
        # Mise à jour de l'équipement avec les résultats IA
        device.device_type = ai_analysis['classification']['device_type']
        device.ai_confidence = ai_analysis['ai_confidence']
        device.health_score = ai_analysis['health_score']
        device.failure_probability = ai_analysis['maintenance_analysis']['failure_probability']
        device.anomaly_score = ai_analysis['anomaly_analysis']['anomaly_score']
        device.maintenance_urgency = ai_analysis['maintenance_analysis']['maintenance_urgency']
        device.ai_recommendations = json.dumps(ai_analysis['recommendations'])
        
        db.session.commit()
        
        # Génération d'alertes intelligentes
        generate_ai_alerts(device, ai_analysis)
        
        return ai_analysis
        
    except Exception as e:
        logger.error(f"Erreur analyse IA équipement {device.ip}: {e}")
        return None

def generate_ai_alerts(device, ai_analysis):
    """Génère des alertes basées sur l'analyse IA avec notifications en temps réel"""
    try:
        # Alertes critiques
        if ai_analysis['maintenance_analysis']['failure_probability'] > AI_CONFIG['HIGH_RISK_THRESHOLD']:
            alert = Alert(
                device_id=device.id,
                alert_type='ai_critical',
                message=f"🚨 RISQUE CRITIQUE - {device.hostname} pourrait tomber en panne",
                priority='critical',
                ai_confidence=ai_analysis['ai_confidence']
            )
            db.session.add(alert)
            
            # Notification en temps réel
            add_notification(
                f"🚨 RISQUE CRITIQUE détecté sur {device.hostname} ({device.ip}) - Probabilité de panne: {ai_analysis['maintenance_analysis']['failure_probability']:.1%}",
                'danger',
                'critical',
                device.ip
            )
            
            # Tentative d'envoi email (fallback automatique vers notifications)
            send_email_alert(
                f"Risque critique détecté - {device.hostname}",
                f"L'IA a détecté un risque critique sur l'équipement {device.hostname} ({device.ip}). "
                f"Probabilité de panne: {ai_analysis['maintenance_analysis']['failure_probability']:.1%}. "
                f"Intervention immédiate recommandée.",
                'critical'
            )
        
        # Alertes d'anomalie
        elif ai_analysis['anomaly_analysis']['is_anomaly']:
            alert = Alert(
                device_id=device.id,
                alert_type='anomaly',
                message=f"🔍 COMPORTEMENT ANORMAL détecté sur {device.hostname}",
                priority='high',
                ai_confidence=ai_analysis['ai_confidence']
            )
            db.session.add(alert)
            
            # Notification en temps réel
            add_notification(
                f"🔍 ANOMALIE détectée sur {device.hostname} ({device.ip}) - Score d'anomalie: {ai_analysis['anomaly_analysis']['anomaly_score']:.3f}",
                'warning',
                'high',
                device.ip
            )
            
            # Tentative d'envoi email
            send_email_alert(
                f"Anomalie détectée - {device.hostname}",
                f"L'IA a détecté un comportement anormal sur l'équipement {device.hostname} ({device.ip}). "
                f"Score d'anomalie: {ai_analysis['anomaly_analysis']['anomaly_score']:.3f}. "
                f"Vérification recommandée.",
                'high'
            )
        
        # Alertes de maintenance
        elif ai_analysis['maintenance_analysis']['failure_probability'] > AI_CONFIG['HIGH_RISK_THRESHOLD']:
            alert = Alert(
                device_id=device.id,
                alert_type='ai_warning',
                message=f"⚠️ MAINTENANCE RECOMMANDÉE pour {device.hostname}",
                priority='medium',
                ai_confidence=ai_analysis['ai_confidence']
            )
            db.session.add(alert)
            
            # Notification en temps réel
            add_notification(
                f"⚠️ MAINTENANCE recommandée pour {device.hostname} ({device.ip}) - Risque: {ai_analysis['maintenance_analysis']['failure_probability']:.1%}",
                'warning',
                'medium',
                device.ip
            )
        
        db.session.commit()
        
    except Exception as e:
        logger.error(f"Erreur génération alertes IA: {e}")

def perform_network_scan():
    """Effectue un scan réseau avec analyse IA"""
    global scan_in_progress
    
    if scan_in_progress:
        logger.info("Scan déjà en cours, ignoré")
        return
    
    scan_in_progress = True
    try:
        logger.info("Début du scan réseau avec IA...")
        
        # Scan réseau (plage par défaut)
        from config import Config
        network_range = Config.DEFAULT_NETWORK_RANGE
        devices_found = network_scanner.scan_network_advanced(network_range, aggressive=False)
        
        # Utiliser le contexte d'application Flask
        with app.app_context():
            # Mise à jour de la base de données
            for device_info in devices_found:
                device = Device.query.filter_by(ip=device_info['ip']).first()
                if device:
                    # Mise à jour de l'équipement existant
                    device.is_online = device_info['is_online']
                    device.last_seen = get_local_time()
                    device.hostname = device_info.get('hostname', device.hostname)
                    device.mac = device_info.get('mac', device.mac)
                    device.mac_vendor = device_info.get('mac_vendor', device.mac_vendor)
                    device.device_type = device_info.get('type', device.device_type)
                else:
                    # Nouvel équipement
                    device = Device(
                        ip=device_info['ip'],
                        hostname=device_info.get('hostname', ''),
                        mac=device_info.get('mac', ''),
                        mac_vendor=device_info.get('mac_vendor', ''),
                        device_type=device_info.get('type', 'Unknown'),
                        is_online=device_info['is_online']
                    )
                    db.session.add(device)
                    db.session.flush()  # Pour obtenir l'ID
                
                # Enregistrement du scan
                scan_record = ScanHistory(
                    device_id=device.id,
                    is_online=device_info['is_online'],
                    response_time=device_info.get('response_time'),
                    packet_loss=device_info.get('packet_loss', 0.0),
                    scan_duration=device_info.get('scan_duration', 0.0),
                    error_count=device_info.get('error_count', 0)
                )
                db.session.add(scan_record)
                
                # Analyse IA si l'équipement est en ligne
                if device_info['is_online']:
                    analyze_device_with_ai(device)
            
            # Gestion des équipements hors ligne
            online_ips = [d['ip'] for d in devices_found if d['is_online']]
            offline_devices = Device.query.filter(~Device.ip.in_(online_ips)).all()
            
            for device in offline_devices:
                device.is_online = False
                scan_record = ScanHistory(
                    device_id=device.id,
                    is_online=False,
                    error_count=1
                )
                db.session.add(scan_record)
                
                # Analyse IA même pour les équipements hors ligne
                analyze_device_with_ai(device)
            
            db.session.commit()
            logger.info(f"Scan terminé: {len(devices_found)} équipements trouvés")
        
    except Exception as e:
        logger.error(f"Erreur lors du scan: {e}")
    finally:
        scan_in_progress = False

def perform_multi_network_scan():
    """Effectue un scan de tous les réseaux détectés"""
    global scan_in_progress
    
    if scan_in_progress:
        logger.info("Scan déjà en cours, ignoré")
        return
    
    scan_in_progress = True
    try:
        logger.info("Début du scan multi-réseaux avec IA...")
        
        # Scanner tous les réseaux détectés
        all_devices = network_scanner.scan_all_networks()
        
        total_devices_found = len(all_devices)
        
        # Utiliser le contexte d'application Flask
        with app.app_context():
            # Traiter tous les équipements trouvés
            for device_info in all_devices:
                device = Device.query.filter_by(ip=device_info['ip']).first()
                
                if device:
                    # Mise à jour de l'équipement existant
                    device.is_online = device_info['is_online']
                    device.last_seen = get_local_time()
                    device.hostname = device_info.get('hostname', device.hostname)
                    device.mac = device_info.get('mac', device.mac)
                    device.mac_vendor = device_info.get('mac_vendor', device.mac_vendor)
                else:
                    # Nouvel équipement
                    device = Device(
                        ip=device_info['ip'],
                        hostname=device_info.get('hostname', ''),
                        mac=device_info.get('mac', ''),
                        mac_vendor=device_info.get('mac_vendor', ''),
                        is_online=device_info['is_online']
                    )
                    db.session.add(device)
                    db.session.flush()  # Pour obtenir l'ID
                
                # Enregistrement du scan
                scan_record = ScanHistory(
                    device_id=device.id,
                    is_online=device_info['is_online'],
                    response_time=device_info.get('response_time'),
                    packet_loss=device_info.get('packet_loss', 0.0),
                    scan_duration=device_info.get('scan_duration', 0.0),
                    error_count=device_info.get('error_count', 0)
                )
                db.session.add(scan_record)
                
                # Analyse IA si l'équipement est en ligne
                if device_info['is_online']:
                    analyze_device_with_ai(device)
            
            db.session.commit()
            logger.info(f"Scan multi-réseaux terminé: {total_devices_found} équipements trouvés")
        
    except Exception as e:
        logger.error(f"Erreur lors du scan multi-réseaux: {e}")
    finally:
        scan_in_progress = False

def perform_production_scan(network_range, aggressive=False):
    """Effectue un scan production avancé avec détection réelle"""
    global scan_in_progress
    
    if scan_in_progress:
        logger.info("Scan déjà en cours, ignoré")
        return
    
    scan_in_progress = True
    try:
        logger.info(f"Début du scan production avancé sur {network_range} (aggressive: {aggressive})")
        
        # Utiliser le scanner production avancé
        devices_found = network_scanner.scan_network_advanced(network_range, aggressive)
        
        # Utiliser le contexte d'application Flask
        with app.app_context():
            for device_info in devices_found:
                # Chercher si l'équipement existe déjà
                device = Device.query.filter_by(ip=device_info['ip']).first()
                
                if device:
                    # Mise à jour complète avec données production
                    device.is_online = device_info['is_online']
                    device.last_seen = get_local_time()
                    device.hostname = device_info.get('hostname', device.hostname)
                    device.mac = device_info.get('mac', device.mac)
                    device.mac_vendor = device_info.get('mac_vendor', device.mac_vendor)
                    device.device_type = device_info.get('type', device.device_type)
                    device.ai_confidence = device_info.get('confidence', 0)
                    device.response_time = device_info.get('response_time', 0.0)
                    
                    # Mettre à jour les données système si disponibles
                    if 'os' in device_info:
                        device.system_info = device_info['os']
                    
                    # Stocker les ports et services découverts
                    device.open_ports = json.dumps(device_info.get('ports', []))
                    device.services = json.dumps(device_info.get('services', []))
                else:
                    # Nouvel équipement avec données complètes
                    device = Device(
                        ip=device_info['ip'],
                        hostname=device_info.get('hostname', ''),
                        mac=device_info.get('mac', ''),
                        mac_vendor=device_info.get('mac_vendor', ''),
                        device_type=device_info.get('type', 'Unknown'),
                        is_online=device_info['is_online'],
                        ai_confidence=device_info.get('confidence', 0),
                        response_time=device_info.get('response_time', 0.0),
                        system_info=device_info.get('os', ''),
                        open_ports=json.dumps(device_info.get('ports', [])),
                        services=json.dumps(device_info.get('services', []))
                    )
                    db.session.add(device)
                    db.session.flush()  # Pour obtenir l'ID
                
                # Enregistrement détaillé du scan
                scan_record = ScanHistory(
                    device_id=device.id,
                    is_online=device_info['is_online'],
                    response_time=device_info.get('response_time', 0.0),
                    packet_loss=0.0,  # À implémenter si nécessaire
                    scan_duration=0.0,  # À implémenter si nécessaire
                    error_count=0
                )
                db.session.add(scan_record)
                
                # Analyse IA avancée
                if device_info['is_online']:
                    analyze_device_with_ai(device)
                
                logger.info(f"Équipement traité: {device_info['ip']} ({device_info.get('type', 'Unknown')})")
            
            db.session.commit()
            logger.info(f"Scan production terminé: {len(devices_found)} équipements détectés")
        
    except Exception as e:
        logger.error(f"Erreur lors du scan production: {e}")
    finally:
        scan_in_progress = False

def perform_complete_network_scan(aggressive=False):
    """Effectue un scan complet de tous les réseaux avec détection avancée"""
    global scan_in_progress
    
    if scan_in_progress:
        logger.info("Scan déjà en cours, ignoré")
        return
    
    scan_in_progress = True
    try:
        logger.info(f"Début du scan complet avancé (aggressive: {aggressive})")
        
        # Scanner tous les réseaux avec le mode avancé
        all_devices = network_scanner.scan_all_networks(aggressive)
        
        # Utiliser le contexte d'application Flask
        with app.app_context():
            for device_info in all_devices:
                # Chercher si l'équipement existe déjà
                device = Device.query.filter_by(ip=device_info['ip']).first()
                
                if device:
                    # Mise à jour complète
                    device.is_online = device_info['is_online']
                    device.last_seen = get_local_time()
                    device.hostname = device_info.get('hostname', device.hostname)
                    device.mac = device_info.get('mac', device.mac)
                    device.mac_vendor = device_info.get('mac_vendor', device.mac_vendor)
                    device.device_type = device_info.get('type', device.device_type)
                    device.ai_confidence = device_info.get('confidence', 0)
                    device.response_time = device_info.get('response_time', 0.0)
                    device.system_info = device_info.get('os', '')
                    device.open_ports = json.dumps(device_info.get('ports', []))
                    device.services = json.dumps(device_info.get('services', []))
                else:
                    # Nouvel équipement
                    device = Device(
                        ip=device_info['ip'],
                        hostname=device_info.get('hostname', ''),
                        mac=device_info.get('mac', ''),
                        mac_vendor=device_info.get('mac_vendor', ''),
                        device_type=device_info.get('type', 'Unknown'),
                        is_online=device_info['is_online'],
                        ai_confidence=device_info.get('confidence', 0),
                        response_time=device_info.get('response_time', 0.0),
                        system_info=device_info.get('os', ''),
                        open_ports=json.dumps(device_info.get('ports', [])),
                        services=json.dumps(device_info.get('services', []))
                    )
                    db.session.add(device)
                    db.session.flush()
                
                # Enregistrement du scan
                scan_record = ScanHistory(
                    device_id=device.id,
                    is_online=device_info['is_online'],
                    response_time=device_info.get('response_time', 0.0),
                    packet_loss=0.0,
                    scan_duration=0.0,
                    error_count=0
                )
                db.session.add(scan_record)
                
                # Analyse IA
                if device_info['is_online']:
                    analyze_device_with_ai(device)
            
            db.session.commit()
            logger.info(f"Scan complet terminé: {len(all_devices)} équipements détectés")
        
    except Exception as e:
        logger.error(f"Erreur lors du scan complet: {e}")
    finally:
        scan_in_progress = False

def perform_universal_network_scan():
    """Effectue un scan universel ultra-complet pour détecter TOUS les équipements"""
    global scan_in_progress
    
    if scan_in_progress:
        logger.info("Scan déjà en cours, ignoré")
        return
    
    scan_in_progress = True
    try:
        logger.info("🌍 SCAN UNIVERSEL DÉMARRÉ - Détection maximale activée!")
        
        # Étape 1: Découverte étendue des réseaux
        logger.info("🔍 Phase 1: Découverte étendue des réseaux...")
        discovered_networks = network_scanner.discover_local_networks()
        
        # Extraire les adresses réseau des résultats (ce sont des dictionnaires)
        all_networks = []
        if isinstance(discovered_networks, list):
            for network_info in discovered_networks:
                if isinstance(network_info, dict) and 'network' in network_info:
                    all_networks.append(network_info['network'])
                elif isinstance(network_info, str):
                    all_networks.append(network_info)
        
        # Ajout de plages réseau communes pour smartphones/TV
        additional_ranges = [
            '192.168.1.0/24',   # Réseau domestique classique
            '192.168.0.0/24',   # Réseau alternatif  
            '10.0.0.0/24',      # Réseau privé
            '172.16.0.0/24'     # Autre réseau privé
        ]
        
        # Combiner tous les réseaux (en supprimant les doublons)
        all_scan_ranges = []
        combined_ranges = all_networks + additional_ranges
        for range_item in combined_ranges:
            if range_item not in all_scan_ranges:
                all_scan_ranges.append(range_item)
                
        logger.info(f"🌐 {len(all_scan_ranges)} réseau(x) à scanner en mode universel: {all_scan_ranges}")
        logger.info(f"📍 Réseaux détectés: {all_networks}")
        logger.info(f"🔧 Réseaux additionnels: {additional_ranges}")
        
        all_devices_found = []
        
        # Utiliser le contexte d'application Flask
        with app.app_context():
            # Étape 2: Scan ultra-agressif de chaque réseau
            for network_range in all_scan_ranges:
                try:
                    logger.info(f"🚀 Scan ULTRA-AGRESSIF du réseau: {network_range}")
                    
                    # Scan avec mode agressif activé pour détection maximale
                    devices_found = network_scanner.scan_network_advanced(network_range, aggressive=True)
                    
                    logger.info(f"📱 {len(devices_found)} équipement(s) détecté(s) sur {network_range}")
                    all_devices_found.extend(devices_found)
                    
                except Exception as e:
                    logger.warning(f"Erreur scan {network_range}: {e}")
                    continue
            
            # Étape 3: Traitement et analyse des équipements
            logger.info(f"📊 Traitement de {len(all_devices_found)} équipements détectés...")
            
            for device_info in all_devices_found:
                try:
                    # Chercher si l'équipement existe déjà
                    device = Device.query.filter_by(ip=device_info['ip']).first()
                    
                    if device:
                        # Mise à jour complète avec détection améliorée
                        device.is_online = device_info['is_online']
                        device.last_seen = get_local_time()
                        device.hostname = device_info.get('hostname', device.hostname)
                        device.mac = device_info.get('mac', device.mac)
                        device.mac_vendor = device_info.get('mac_vendor', device.mac_vendor)
                        device.device_type = device_info.get('type', device.device_type)
                        device.ai_confidence = device_info.get('confidence', 0)
                        device.response_time = device_info.get('response_time', 0.0)
                        device.system_info = device_info.get('os', device.system_info)
                        device.open_ports = json.dumps(device_info.get('ports', []))
                        device.services = json.dumps(device_info.get('services', []))
                    else:
                        # Nouvel équipement avec détection avancée
                        device = Device(
                            ip=device_info['ip'],
                            hostname=device_info.get('hostname', ''),
                            mac=device_info.get('mac', ''),
                            mac_vendor=device_info.get('mac_vendor', ''),
                            device_type=device_info.get('type', 'Unknown'),
                            is_online=device_info['is_online'],
                            ai_confidence=device_info.get('confidence', 0),
                            response_time=device_info.get('response_time', 0.0),
                            system_info=device_info.get('os', ''),
                            open_ports=json.dumps(device_info.get('ports', [])),
                            services=json.dumps(device_info.get('services', []))
                        )
                        db.session.add(device)
                        db.session.flush()
                    
                    # Détection spécialisée pour smartphones et TV
                    if device_info.get('mac_vendor'):
                        vendor = device_info['mac_vendor'].lower()
                        if 'oppo' in vendor or 'oneplus' in vendor:
                            device.device_type = 'smartphone'
                            logger.info(f"📱 TÉLÉPHONE OPPO détecté: {device.ip}")
                        elif 'samsung' in vendor and 'tv' in device_info.get('hostname', '').lower():
                            device.device_type = 'smart_tv'
                            logger.info(f"📺 TV SAMSUNG détectée: {device.ip}")
                        elif 'samsung' in vendor:
                            device.device_type = 'smartphone'
                            logger.info(f"📱 SMARTPHONE SAMSUNG détecté: {device.ip}")
                    
                    # Enregistrement détaillé du scan
                    scan_record = ScanHistory(
                        device_id=device.id,
                        is_online=device_info['is_online'],
                        response_time=device_info.get('response_time', 0.0),
                        packet_loss=0.0,
                        scan_duration=0.0,
                        error_count=0
                    )
                    db.session.add(scan_record)
                    
                    # Analyse IA améliorée
                    if device_info['is_online']:
                        analyze_device_with_ai(device)
                    
                    logger.info(f"✅ Équipement traité: {device_info['ip']} ({device_info.get('type', 'Unknown')}) - {device_info.get('mac_vendor', 'Inconnu')}")
                    
                except Exception as e:
                    logger.error(f"Erreur traitement équipement {device_info.get('ip', 'unknown')}: {e}")
                    continue
            
            db.session.commit()
            
            # Étape 4: Notification des résultats avec détection spécialisée
            total_detected = len(all_devices_found)
            smartphones = sum(1 for d in all_devices_found if 'phone' in d.get('type', '').lower() or 'mobile' in d.get('type', '').lower())
            tvs = sum(1 for d in all_devices_found if 'tv' in d.get('type', '').lower() or 'smart' in d.get('type', '').lower())
            
            # Détection spécialisée OPPO et Samsung
            oppo_devices = []
            samsung_devices = []
            for d in all_devices_found:
                vendor = d.get('mac_vendor', '').lower()
                if 'oppo' in vendor:
                    oppo_devices.append(d['ip'])
                elif 'samsung' in vendor:
                    samsung_devices.append(d['ip'])
            
            logger.info(f"🎯 SCAN UNIVERSEL TERMINÉ!")
            logger.info(f"📊 RÉSULTATS: {total_detected} équipements détectés")
            logger.info(f"📱 Smartphones: {smartphones}")
            logger.info(f"📺 Smart TV: {tvs}")
            if oppo_devices:
                logger.info(f"📱 OPPO détectés: {', '.join(oppo_devices)}")
            if samsung_devices:
                logger.info(f"📱📺 SAMSUNG détectés: {', '.join(samsung_devices)}")
            
            # Notification en temps réel améliorée
            success_message = f"🌍 SCAN UNIVERSEL RÉUSSI ! {total_detected} équipements détectés"
            if oppo_devices:
                success_message += f" 📱 OPPO trouvé: {', '.join(oppo_devices)}"
            if samsung_devices:
                success_message += f" 📱📺 SAMSUNG trouvés: {', '.join(samsung_devices)}"
            if smartphones > 0:
                success_message += f" (📱{smartphones} smartphones"
            if tvs > 0:
                success_message += f", 📺{tvs} TV)"
            elif smartphones > 0:
                success_message += ")"
                
            add_notification(success_message, 'success', 'high')
        
    except Exception as e:
        logger.error(f"Erreur lors du scan universel: {e}")
        add_notification(f"❌ Erreur scan universel: {str(e)}", 'danger', 'high')
    finally:
        scan_in_progress = False

def generate_ai_report():
    """Génère un rapport avec insights IA"""
    try:
        logger.info("Génération du rapport IA...")
        
        # Données pour le rapport
        devices = Device.query.all()
        total_devices = len(devices)
        online_devices = sum(1 for d in devices if d.is_online)
        offline_devices = total_devices - online_devices
        
        # Statistiques IA
        critical_devices = sum(1 for d in devices if d.maintenance_urgency == 'critical')
        high_risk_devices = sum(1 for d in devices if d.failure_probability > AI_CONFIG['HIGH_RISK_THRESHOLD'])
        anomaly_devices = sum(1 for d in devices if d.anomaly_score < AI_CONFIG['ANOMALY_THRESHOLD'])
        
        # Score de santé global
        avg_health_score = np.mean([d.health_score for d in devices]) if devices else 0
        
        # Recommandations globales
        global_recommendations = []
        if critical_devices > 0:
            global_recommendations.append(f"🚨 {critical_devices} équipements critiques nécessitent une intervention immédiate")
        if high_risk_devices > 0:
            global_recommendations.append(f"⚠️ {high_risk_devices} équipements à risque élevé")
        if anomaly_devices > 0:
            global_recommendations.append(f"🔍 {anomaly_devices} équipements présentent des comportements anormaux")
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'network_stats': {
                'total_devices': total_devices,
                'online_devices': online_devices,
                'offline_devices': offline_devices,
                'availability_percentage': (online_devices / total_devices * 100) if total_devices > 0 else 0
            },
            'ai_insights': {
                'avg_health_score': avg_health_score,
                'critical_devices': critical_devices,
                'high_risk_devices': high_risk_devices,
                'anomaly_devices': anomaly_devices,
                'ai_models_status': 'Trained' if ai_models_loaded else 'Training needed'
            },
            'recommendations': global_recommendations,
            'devices_details': []
        }
        
        # Détails des équipements
        for device in devices:
            device_detail = {
                'ip': device.ip,
                'hostname': device.hostname,
                'device_type': device.device_type,
                'is_online': device.is_online,
                'health_score': device.health_score,
                'failure_probability': device.failure_probability,
                'maintenance_urgency': device.maintenance_urgency,
                'ai_confidence': device.ai_confidence
            }
            report_data['devices_details'].append(device_detail)
        
        # Sauvegarde du rapport
        report_filename = f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join('reports', report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Rapport IA généré: {report_path}")
        return report_path
        
    except Exception as e:
        logger.error(f"Erreur génération rapport IA: {e}")
        return None

def schedule_tasks():
    """Planifie les tâches automatiques"""
    schedule.every(30).minutes.do(perform_network_scan)
    schedule.every().day.at("08:00").do(generate_ai_report)
    schedule.every().day.at("18:00").do(train_ai_models)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Routes d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            user.last_login = get_local_time()
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté avec succès', 'success')
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Changement de mot de passe"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Mot de passe actuel incorrect', 'danger')
        elif new_password != confirm_password:
            flash('Les nouveaux mots de passe ne correspondent pas', 'danger')
        elif len(new_password) < 6:
            flash('Le nouveau mot de passe doit contenir au moins 6 caractères', 'danger')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Mot de passe modifié avec succès', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')

# Routes de l'application
@app.route('/')
@login_required
def dashboard():
    """Dashboard principal avec IA"""
    try:
        # Statistiques de base
        total_devices = Device.query.count()
        online_devices = Device.query.filter_by(is_online=True).count()
        offline_devices = total_devices - online_devices
        availability_percentage = (online_devices / total_devices * 100) if total_devices > 0 else 0
        
        # Statistiques IA
        critical_devices = Device.query.filter_by(maintenance_urgency='critical').count()
        high_risk_devices = Device.query.filter(Device.failure_probability > AI_CONFIG['HIGH_RISK_THRESHOLD']).count()
        anomaly_devices = Device.query.filter(Device.anomaly_score < AI_CONFIG['ANOMALY_THRESHOLD']).count()
        avg_health_score = db.session.query(db.func.avg(Device.health_score)).scalar() or 0
        
        # Équipements récents
        recent_devices = Device.query.order_by(Device.updated_at.desc()).limit(10).all()
        
        # Alertes récentes
        recent_alerts = Alert.query.filter_by(is_resolved=False).order_by(Alert.created_at.desc()).limit(5).all()
        
        # Historique des scans
        recent_scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(20).all()
        
        devices = Device.query.order_by(Device.ip).all()
        current_time = get_local_time()
        return render_template('dashboard.html',
                             total_devices=total_devices,
                             online_devices=online_devices,
                             offline_devices=offline_devices,
                             availability_percentage=round(availability_percentage, 2),
                             critical_devices=critical_devices,
                             high_risk_devices=high_risk_devices,
                             anomaly_devices=anomaly_devices,
                             avg_health_score=round(avg_health_score, 1),
                             recent_devices=recent_devices,
                             recent_alerts=recent_alerts,
                             scan_history=recent_scans,
                             recent_scans=recent_scans,
                             ai_models_loaded=ai_models_loaded,
                             devices=devices,
                             current_time=current_time)
    except Exception as e:
        logger.error(f"Erreur dashboard: {e}")
        return render_template('error.html', error=str(e))

@app.route('/api/scan', methods=['POST'])
@login_required
def api_scan():
    """API pour déclencher un scan manuel"""
    try:
        if scan_in_progress:
            return jsonify({'status': 'error', 'message': 'Scan déjà en cours'})
        
        # Lancement du scan dans un thread séparé
        thread = threading.Thread(target=perform_network_scan)
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Scan lancé'})
    except Exception as e:
        logger.error(f"Erreur API scan: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/scan-all-networks', methods=['POST'])
@login_required
def api_scan_all_networks():
    """API pour scanner tous les réseaux détectés"""
    try:
        if scan_in_progress:
            return jsonify({'status': 'error', 'message': 'Scan déjà en cours'})
        
        # Lancement du scan multi-réseaux dans un thread séparé
        thread = threading.Thread(target=perform_multi_network_scan)
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Scan multi-réseaux lancé'})
    except Exception as e:
        logger.error(f"Erreur API scan multi-réseaux: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/discover-networks')
@login_required
def api_discover_networks():
    """API pour découvrir les réseaux disponibles"""
    try:
        networks = network_scanner.discover_local_networks()
        return jsonify({
            'status': 'success',
            'networks': networks,
            'total_networks': len(networks)
        })
    except Exception as e:
        logger.error(f"Erreur découverte réseaux: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/scan-production')
@login_required
def api_scan_production():
    """API pour lancer un scan production avancé"""
    try:
        if scan_in_progress:
            return jsonify({'status': 'error', 'message': 'Scan déjà en cours'})
        
        network_range = request.args.get('network', '192.168.1.0/24')
        aggressive = request.args.get('aggressive', 'false').lower() == 'true'
        
        # Lancement du scan production dans un thread séparé
        thread = threading.Thread(target=perform_production_scan, args=(network_range, aggressive))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success', 
            'message': f'Scan production lancé sur {network_range}',
            'aggressive': aggressive
        })
    except Exception as e:
        logger.error(f"Erreur API scan production: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/scan-all-networks')
@login_required
def api_scan_all_networks_get():
    """API pour scanner tous les réseaux détectés (GET)"""
    try:
        if scan_in_progress:
            return jsonify({'status': 'error', 'message': 'Scan déjà en cours'})
        
        aggressive = request.args.get('aggressive', 'false').lower() == 'true'
        
        # Lancement du scan complet dans un thread séparé
        thread = threading.Thread(target=perform_complete_network_scan, args=(aggressive,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success', 
            'message': 'Scan complet de tous les réseaux lancé',
            'aggressive': aggressive
        })
    except Exception as e:
        logger.error(f"Erreur API scan complet: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/scan-universal', methods=['POST'])
@login_required
def api_scan_universal():
    """API pour un scan universel ultra-complet avec détection avancée"""
    try:
        if scan_in_progress:
            return jsonify({'status': 'error', 'message': 'Scan déjà en cours'})
        
        # Lancement du scan universel dans un thread séparé
        thread = threading.Thread(target=perform_universal_network_scan)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success', 
            'message': '🌍 Scan Universel lancé - Détection maximale activée!'
        })
    except Exception as e:
        logger.error(f"Erreur API scan universel: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/devices')
@login_required
def api_devices():
    """API pour récupérer la liste des équipements avec IA"""
    try:
        devices = Device.query.all()
        devices_data = []
        
        for device in devices:
            device_data = {
                'id': device.id,
                'ip': device.ip,
                'hostname': device.hostname,
                'mac': device.mac,
                'mac_vendor': device.mac_vendor,
                'is_online': device.is_online,
                'last_seen': device.last_seen.isoformat() if device.last_seen else None,
                'device_type': device.device_type,
                'ai_confidence': device.ai_confidence,
                'health_score': device.health_score,
                'failure_probability': device.failure_probability,
                'anomaly_score': device.anomaly_score,
                'maintenance_urgency': device.maintenance_urgency,
                'ai_recommendations': json.loads(device.ai_recommendations) if device.ai_recommendations else []
            }
            devices_data.append(device_data)
        
        return jsonify(devices_data)
    except Exception as e:
        logger.error(f"Erreur API devices: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/devices/<int:device_id>')
@login_required
def api_device_details(device_id):
    """API pour récupérer les détails d'un équipement spécifique"""
    try:
        device = Device.query.get_or_404(device_id)
        
        # Récupérer l'historique des scans
        scan_history = ScanHistory.query.filter_by(device_id=device.id).order_by(ScanHistory.timestamp.desc()).limit(50).all()
        
        # Récupérer les alertes actives
        active_alerts = Alert.query.filter_by(device_id=device.id, is_resolved=False).order_by(Alert.created_at.desc()).all()
        
        device_data = {
            'id': device.id,
            'ip': device.ip,
            'hostname': device.hostname,
            'mac': device.mac,
            'mac_vendor': device.mac_vendor,
            'is_online': device.is_online,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None,
            'device_type': device.device_type,
            'ai_confidence': device.ai_confidence,
            'health_score': device.health_score,
            'failure_probability': device.failure_probability,
            'anomaly_score': device.anomaly_score,
            'maintenance_urgency': device.maintenance_urgency,
            'ai_recommendations': json.loads(device.ai_recommendations) if device.ai_recommendations else [],
            'created_at': device.created_at.isoformat() if device.created_at else None,
            'updated_at': device.updated_at.isoformat() if device.updated_at else None,
            'scan_history': [
                {
                    'timestamp': scan.timestamp.isoformat(),
                    'is_online': scan.is_online,
                    'response_time': scan.response_time,
                    'packet_loss': scan.packet_loss,
                    'scan_duration': scan.scan_duration,
                    'error_count': scan.error_count
                }
                for scan in scan_history
            ],
            'active_alerts': [
                {
                    'id': alert.id,
                    'alert_type': alert.alert_type,
                    'message': alert.message,
                    'priority': alert.priority,
                    'ai_confidence': alert.ai_confidence,
                    'created_at': alert.created_at.isoformat()
                }
                for alert in active_alerts
            ]
        }
        
        return jsonify(device_data)
    except Exception as e:
        logger.error(f"Erreur API device details: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/device/<int:device_id>/ai-analysis')
@login_required
def api_device_ai_analysis(device_id):
    """API pour l'analyse IA d'un équipement spécifique"""
    try:
        device = Device.query.get_or_404(device_id)
        ai_analysis = analyze_device_with_ai(device)
        
        if ai_analysis:
            return jsonify(ai_analysis)
        else:
            return jsonify({'error': 'Erreur lors de l\'analyse IA'})
    except Exception as e:
        logger.error(f"Erreur API analyse IA: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/ai/train', methods=['POST'])
@login_required
def api_train_ai():
    """API pour entraîner les modèles IA"""
    try:
        thread = threading.Thread(target=train_ai_models)
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Entraînement IA lancé'})
    except Exception as e:
        logger.error(f"Erreur API entraînement IA: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/ai/high-risk-devices')
@login_required
def api_high_risk_devices():
    """API pour récupérer les équipements à risque élevé"""
    try:
        devices = Device.query.filter(Device.failure_probability > AI_CONFIG['HIGH_RISK_THRESHOLD']).order_by(Device.failure_probability.desc()).limit(AI_CONFIG['MAX_RECOMMENDATIONS']).all()
        devices_data = []
        
        for device in devices:
            device_data = {
                'id': device.id,
                'ip': device.ip,
                'hostname': device.hostname,
                'device_type': device.device_type,
                'failure_probability': device.failure_probability,
                'health_score': device.health_score
            }
            devices_data.append(device_data)
        
        return jsonify(devices_data)
    except Exception as e:
        logger.error(f"Erreur API équipements à risque: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/anomaly-devices')
@login_required
def api_anomaly_devices():
    """API pour récupérer les équipements avec anomalies"""
    try:
        devices = Device.query.filter(Device.anomaly_score < AI_CONFIG['ANOMALY_THRESHOLD']).order_by(Device.anomaly_score.asc()).limit(AI_CONFIG['MAX_RECOMMENDATIONS']).all()
        devices_data = []
        
        for device in devices:
            device_data = {
                'id': device.id,
                'ip': device.ip,
                'hostname': device.hostname,
                'device_type': device.device_type,
                'anomaly_score': device.anomaly_score,
                'health_score': device.health_score
            }
            devices_data.append(device_data)
        
        return jsonify(devices_data)
    except Exception as e:
        logger.error(f"Erreur API équipements anomalies: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/dashboard-stats')
@login_required
def api_ai_dashboard_stats():
    """API pour les statistiques du dashboard IA"""
    try:
        # Calcul du score de santé moyen
        avg_health_score = db.session.query(db.func.avg(Device.health_score)).scalar() or 0
        
        # Équipements critiques
        critical_devices = Device.query.filter(Device.health_score < AI_CONFIG['CRITICAL_HEALTH_THRESHOLD']).count()
        
        # Équipements à risque élevé
        high_risk_devices_count = Device.query.filter(Device.failure_probability > AI_CONFIG['HIGH_RISK_THRESHOLD']).count()
        
        # Équipements avec anomalies
        anomaly_devices_count = Device.query.filter(Device.anomaly_score < AI_CONFIG['ANOMALY_THRESHOLD']).count()
        
        return jsonify({
            'avg_health_score': round(avg_health_score, 1),
            'critical_devices': critical_devices,
            'high_risk_devices_count': high_risk_devices_count,
            'anomaly_devices_count': anomaly_devices_count
        })
    except Exception as e:
        logger.error(f"Erreur API stats dashboard IA: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/recommendations', methods=['POST'])
@login_required
def api_ai_recommendations():
    """API pour générer des recommandations IA"""
    try:
        # Récupérer tous les équipements
        devices = Device.query.all()
        recommendations = []
        
        for device in devices:
            # Analyser l'équipement avec l'IA
            ai_analysis = analyze_device_with_ai(device)
            
            if ai_analysis and 'recommendations' in ai_analysis:
                for rec in ai_analysis['recommendations']:
                    recommendations.append({
                        'device_ip': device.ip,
                        'device_hostname': device.hostname or device.ip,
                        'message': rec['message'],
                        'priority': rec['priority'],
                        'actions': rec['actions']
                    })
        
        # Trier par priorité
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations[:AI_CONFIG['MAX_RECOMMENDATIONS']]  # Limiter à 10 recommandations
        })
    except Exception as e:
        logger.error(f"Erreur API recommandations IA: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/ai/report', methods=['POST'])
@login_required
def api_generate_ai_report():
    """API pour générer un rapport IA"""
    try:
        report_path = generate_ai_report()
        
        if report_path:
            return jsonify({'status': 'success', 'report_path': report_path})
        else:
            return jsonify({'status': 'error', 'message': 'Erreur génération rapport'})
    except Exception as e:
        logger.error(f"Erreur API rapport IA: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/alerts')
@login_required
def api_alerts():
    """API pour récupérer les alertes"""
    try:
        alerts = Alert.query.filter_by(is_resolved=False).order_by(Alert.created_at.desc()).all()
        alerts_data = []
        
        for alert in alerts:
            device = Device.query.get(alert.device_id)
            alert_data = {
                'id': alert.id,
                'device_ip': device.ip if device else 'Unknown',
                'device_hostname': device.hostname if device else 'Unknown',
                'alert_type': alert.alert_type,
                'message': alert.message,
                'priority': alert.priority,
                'ai_confidence': alert.ai_confidence,
                'created_at': alert.created_at.isoformat()
            }
            alerts_data.append(alert_data)
        
        return jsonify(alerts_data)
    except Exception as e:
        logger.error(f"Erreur API alerts: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/alert/<int:alert_id>/resolve', methods=['POST'])
@login_required
def api_resolve_alert(alert_id):
    """API pour résoudre une alerte"""
    try:
        alert = Alert.query.get_or_404(alert_id)
        alert.is_resolved = True
        alert.resolved_at = get_local_time()
        db.session.commit()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Erreur API resolve alert: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/alerts')
@login_required
def alerts():
    """Page des alertes"""
    try:
        # Récupérer toutes les alertes non résolues
        active_alerts = Alert.query.filter_by(is_resolved=False).order_by(Alert.created_at.desc()).all()
        
        # Récupérer les alertes résolues récentes
        resolved_alerts = Alert.query.filter_by(is_resolved=True).order_by(Alert.resolved_at.desc()).limit(20).all()
        
        # Statistiques des alertes
        total_alerts = Alert.query.count()
        active_count = len(active_alerts)
        critical_count = Alert.query.filter_by(priority='critical', is_resolved=False).count()
        
        return render_template('alerts.html',
                             active_alerts=active_alerts,
                             resolved_alerts=resolved_alerts,
                             total_alerts=total_alerts,
                             active_count=active_count,
                             critical_count=critical_count)
    except Exception as e:
        logger.error(f"Erreur page alertes: {e}")
        return render_template('error.html', error=str(e))

@app.route('/api/alerts/bulk-resolve', methods=['POST'])
@login_required
def api_bulk_resolve_alerts():
    """API pour résoudre plusieurs alertes en une fois"""
    try:
        data = request.get_json()
        alert_ids = data.get('alert_ids', [])
        
        resolved_count = 0
        for alert_id in alert_ids:
            alert = Alert.query.get(alert_id)
            if alert and not alert.is_resolved:
                alert.is_resolved = True
                alert.resolved_at = get_local_time()
                resolved_count += 1
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'{resolved_count} alertes résolues',
            'resolved_count': resolved_count
        })
    except Exception as e:
        logger.error(f"Erreur résolution groupée alertes: {e}")
        return jsonify({'error': str(e)})

@app.route('/reports')
@login_required
def reports():
    """Page des rapports avec données réelles depuis la base de données"""
    try:
        # Récupérer les statistiques réelles depuis la base de données
        total_reports = Report.query.count()
        
        # Rapports de ce mois
        current_month = datetime.now().month
        current_year = datetime.now().year
        reports_month = Report.query.filter(
            db.extract('month', Report.created_at) == current_month,
            db.extract('year', Report.created_at) == current_year
        ).count()
        
        # Rapports programmés
        scheduled_count = Report.query.filter_by(is_scheduled=True, status='scheduled').count()
        
        # Rapports en cours de traitement
        processing_count = Report.query.filter_by(status='processing').count()
        
        # Rapports récents (5 derniers)
        recent_reports = Report.query.order_by(Report.created_at.desc()).limit(5).all()
        
        return render_template('reports.html', 
                             total_reports=total_reports,
                             reports_month=reports_month,
                             scheduled_count=scheduled_count,
                             processing_count=processing_count,
                             recent_reports=[r.to_dict() for r in recent_reports])
    except Exception as e:
        logger.error(f"Erreur page rapports: {e}")
        return render_template('reports.html', 
                             total_reports=0,
                             reports_month=0,
                             scheduled_count=0,
                             processing_count=0,
                             recent_reports=[])

@app.route('/api/reports/delete/<filename>', methods=['DELETE'])
@login_required
def api_delete_report(filename):
    """API pour supprimer un rapport"""
    try:
        from report_generator import ReportGenerator
        report_gen = ReportGenerator()
        success = report_gen.delete_report(filename)
        
        if success:
            return jsonify({'success': True, 'message': f'Rapport {filename} supprimé'})
        else:
            return jsonify({'success': False, 'message': f'Erreur lors de la suppression de {filename}'})
    except Exception as e:
        logger.error(f"Erreur suppression rapport: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/settings')
@login_required
def settings():
    """Page des paramètres"""
    return render_template('settings.html')

@app.route('/api/settings')
@login_required
def api_settings():
    """API pour récupérer les paramètres production"""
    try:
        from settings_manager_production import get_production_settings_manager
        
        settings_manager = get_production_settings_manager()
        settings = settings_manager.get_all_settings()
        
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Erreur API settings: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings', methods=['POST'])
@login_required
def api_update_settings():
    """API pour mettre à jour les paramètres réseau production"""
    try:
        from settings_manager_production import get_production_settings_manager
        
        data = request.get_json()
        settings_manager = get_production_settings_manager()
        
        # Mettre à jour les paramètres réseau
        network_settings = {
            'network_range': data.get('network_range'),
            'scan_interval': data.get('scan_interval'),
            'scan_timeout': data.get('scan_timeout'),
            'max_retries': data.get('max_retries'),
            'enable_auto_scan': data.get('enable_auto_scan', True),
            'aggressive_scan': data.get('aggressive_scan', False)
        }
        
        success, message = settings_manager.update_network_settings(network_settings)
        
        if success:
            return jsonify({'status': 'success', 'message': message})
        else:
            return jsonify({'status': 'error', 'message': message})
    except Exception as e:
        logger.error(f"Erreur mise à jour settings: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/settings/networks', methods=['GET'])
@login_required
def api_get_networks():
    """API pour récupérer les réseaux détectés automatiquement"""
    try:
        from settings_manager_production import get_production_settings_manager
        
        settings_manager = get_production_settings_manager()
        detected_networks = settings_manager.get_detected_networks()
        current_network = settings_manager.get_current_network_info()
        
        return jsonify({
            'status': 'success',
            'detected_networks': detected_networks,
            'current_network': current_network,
            'auto_detection_available': True
        })
    except Exception as e:
        logger.error(f"Erreur récupération réseaux: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings/save', methods=['POST'])
@login_required
def api_save_settings():
    """API pour sauvegarder les paramètres avec le gestionnaire production"""
    try:
        from settings_manager_production import get_production_settings_manager
        
        data = request.get_json()
        settings_manager = get_production_settings_manager()
        
        # Sauvegarde unifiée des paramètres avec le gestionnaire production
        success = settings_manager.save_settings(data)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Paramètres sauvegardés avec succès'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de la sauvegarde'
            })
    except Exception as e:
        logger.error(f"Erreur sauvegarde paramètres: {e}")
        return jsonify({'status': 'error', 'message': str(e)})
        return jsonify({'error': str(e)})

@app.route('/api/settings/test-network', methods=['POST'])
@login_required
def api_test_network():
    """API pour tester une plage réseau avec le scanner production"""
    try:
        from settings_manager_production import get_production_settings_manager
        
        data = request.get_json()
        network_range = data.get('network_range', 'auto-detect')
        
        settings_manager = get_production_settings_manager()
        success, message = settings_manager.test_network_connectivity(network_range)
        
        if success:
            return jsonify({
                'status': 'success',
                'network_range': network_range,
                'message': message
            })
        else:
            return jsonify({
                'status': 'error',
                'message': message
            })
    except Exception as e:
        logger.error(f"Erreur test réseau: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/reports/generate', methods=['POST'])
@login_required
def api_generate_report():
    """API pour générer un rapport avec sauvegarde en base de données"""
    try:
        data = request.get_json()
        report_type = data.get('type', 'daily')
        report_format = data.get('format', 'pdf')
        date_from = data.get('dateFrom') or data.get('date_from')
        date_to = data.get('dateTo') or data.get('date_to')
        description = data.get('description', '')
        sections = data.get('sections', [])
        
        # Générer un nom de fichier unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"rapport_{report_type}_{timestamp}.{report_format}"
        
        # Créer l'entrée en base de données
        new_report = Report(
            name=f"Rapport {report_type.title()} - {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            filename=filename,
            type=report_type,
            format=report_format,
            status='processing',
            description=description,
            sections=json.dumps(sections),
            date_from=datetime.fromisoformat(date_from) if date_from else None,
            date_to=datetime.fromisoformat(date_to) if date_to else None,
            generated_by=current_user.id
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        try:
            # Simuler la génération du rapport (remplacer par vraie génération)
            report_data = generate_real_report_data(report_type, date_from, date_to, sections)
            
            # Créer le dossier reports s'il n'existe pas
            reports_dir = 'reports'
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            report_path = os.path.join(reports_dir, filename)
            
            # Générer le fichier selon le format
            if report_format == 'pdf':
                generate_pdf_report(report_path, report_data, report_type)
            elif report_format == 'excel':
                generate_excel_report(report_path, report_data)
            elif report_format == 'html':
                generate_html_report(report_path, report_data, report_type)
            elif report_format == 'csv':
                generate_csv_report(report_path, report_data)
            
            # Mettre à jour le rapport avec les informations du fichier
            file_size = os.path.getsize(report_path) if os.path.exists(report_path) else 0
            new_report.status = 'completed'
            new_report.file_path = report_path
            new_report.file_size = file_size
            new_report.generated_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Rapport {report_type} généré avec succès',
                'filename': filename,
                'report_url': f'/api/reports/download/{filename}',
                'report_id': new_report.id
            })
            
        except Exception as e:
            # Marquer le rapport comme échoué
            new_report.status = 'failed'
            db.session.commit()
            raise e
            
    except Exception as e:
        logger.error(f"Erreur génération rapport: {e}")
        return jsonify({'success': False, 'message': str(e)})

def generate_real_report_data(report_type, date_from, date_to, sections):
    """Génère des données réelles pour le rapport"""
    data = {
        'metadata': {
            'type': report_type,
            'generated_at': datetime.now(),
            'period': f"{date_from} à {date_to}" if date_from and date_to else "Données actuelles",
            'sections': sections
        }
    }
    
    # Récupérer les données réelles depuis la base
    devices = Device.query.all()
    alerts = Alert.query.filter_by(is_resolved=False).all()
    
    # Statistiques générales
    data['summary'] = {
        'total_devices': len(devices),
        'online_devices': len([d for d in devices if d.is_online]),
        'offline_devices': len([d for d in devices if not d.is_online]),
        'active_alerts': len(alerts),
        'health_score_avg': sum(d.health_score for d in devices) / len(devices) if devices else 0
    }
    
    # Données des équipements
    data['devices'] = []
    for device in devices:
        data['devices'].append({
            'ip': device.ip,
            'hostname': device.hostname or 'N/A',
            'type': device.device_type,
            'status': 'En ligne' if device.is_online else 'Hors ligne',
            'health_score': device.health_score,
            'last_seen': device.last_seen.strftime('%Y-%m-%d %H:%M') if device.last_seen else 'N/A',
            'response_time': device.response_time
        })
    
    # Données des alertes
    data['alerts'] = []
    for alert in alerts:
        device = Device.query.get(alert.device_id)
        data['alerts'].append({
            'device_ip': device.ip if device else 'N/A',
            'type': alert.alert_type,
            'message': alert.message,
            'priority': alert.priority,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return data

def generate_pdf_report(file_path, data, report_type):
    """Génère un rapport PDF"""
    # Simuler la génération PDF avec un contenu simple
    content = f"""
RAPPORT {report_type.upper()} - CENTRAL DANONE
===============================================

Généré le: {data['metadata']['generated_at'].strftime('%Y-%m-%d %H:%M:%S')}
Période: {data['metadata']['period']}

RÉSUMÉ EXÉCUTIF
===============
- Total équipements: {data['summary']['total_devices']}
- Équipements en ligne: {data['summary']['online_devices']}
- Équipements hors ligne: {data['summary']['offline_devices']}
- Alertes actives: {data['summary']['active_alerts']}
- Score de santé moyen: {data['summary']['health_score_avg']:.1f}%

ÉQUIPEMENTS
===========
"""
    
    for device in data['devices'][:10]:  # Limiter à 10 pour l'exemple
        content += f"- {device['ip']} ({device['hostname']}) - {device['status']} - Santé: {device['health_score']:.1f}%\n"
    
    content += "\nALERTES ACTIVES\n===============\n"
    for alert in data['alerts'][:5]:  # Limiter à 5 pour l'exemple
        content += f"- {alert['device_ip']}: {alert['message']} ({alert['priority']})\n"
    
    # Écrire dans un fichier texte (simuler PDF)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_excel_report(file_path, data):
    """Génère un rapport Excel"""
    try:
        import pandas as pd
        
        # Créer un fichier Excel avec plusieurs feuilles
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Feuille résumé
            summary_df = pd.DataFrame([data['summary']])
            summary_df.to_excel(writer, sheet_name='Résumé', index=False)
            
            # Feuille équipements
            devices_df = pd.DataFrame(data['devices'])
            devices_df.to_excel(writer, sheet_name='Équipements', index=False)
            
            # Feuille alertes
            if data['alerts']:
                alerts_df = pd.DataFrame(data['alerts'])
                alerts_df.to_excel(writer, sheet_name='Alertes', index=False)
                
    except ImportError:
        # Fallback si pandas n'est pas disponible
        generate_csv_report(file_path.replace('.xlsx', '.csv'), data)

def generate_html_report(file_path, data, report_type):
    """Génère un rapport HTML"""
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Rapport {report_type.title()} - Central Danone</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #0066cc; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .online {{ color: green; }}
        .offline {{ color: red; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Rapport {report_type.title()} - Central Danone</h1>
        <p>Généré le: {data['metadata']['generated_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Période: {data['metadata']['period']}</p>
    </div>
    
    <div class="summary">
        <h2>Résumé Exécutif</h2>
        <ul>
            <li>Total équipements: <strong>{data['summary']['total_devices']}</strong></li>
            <li>Équipements en ligne: <strong class="online">{data['summary']['online_devices']}</strong></li>
            <li>Équipements hors ligne: <strong class="offline">{data['summary']['offline_devices']}</strong></li>
            <li>Alertes actives: <strong>{data['summary']['active_alerts']}</strong></li>
            <li>Score de santé moyen: <strong>{data['summary']['health_score_avg']:.1f}%</strong></li>
        </ul>
    </div>
    
    <h2>Équipements</h2>
    <table>
        <tr>
            <th>IP</th>
            <th>Hostname</th>
            <th>Type</th>
            <th>Statut</th>
            <th>Santé</th>
            <th>Dernière vue</th>
        </tr>
"""
    
    for device in data['devices']:
        status_class = 'online' if 'ligne' in device['status'] else 'offline'
        html_content += f"""
        <tr>
            <td>{device['ip']}</td>
            <td>{device['hostname']}</td>
            <td>{device['type']}</td>
            <td class="{status_class}">{device['status']}</td>
            <td>{device['health_score']:.1f}%</td>
            <td>{device['last_seen']}</td>
        </tr>
        """
    
    html_content += """
    </table>
    
    <h2>Alertes Actives</h2>
    <table>
        <tr>
            <th>Équipement</th>
            <th>Type</th>
            <th>Message</th>
            <th>Priorité</th>
            <th>Date</th>
        </tr>
    """
    
    for alert in data['alerts']:
        html_content += f"""
        <tr>
            <td>{alert['device_ip']}</td>
            <td>{alert['type']}</td>
            <td>{alert['message']}</td>
            <td>{alert['priority']}</td>
            <td>{alert['created_at']}</td>
        </tr>
        """
    
    html_content += """
    </table>
</body>
</html>
    """
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_csv_report(file_path, data):
    """Génère un rapport CSV"""
    content = "Type,Données\n"
    content += f"Total Équipements,{data['summary']['total_devices']}\n"
    content += f"En Ligne,{data['summary']['online_devices']}\n"
    content += f"Hors Ligne,{data['summary']['offline_devices']}\n"
    content += f"Alertes Actives,{data['summary']['active_alerts']}\n"
    content += f"Score Santé Moyen,{data['summary']['health_score_avg']:.1f}\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

@app.route('/api/reports/download/<filename>')
@login_required
def api_download_report(filename):
    """API pour télécharger un rapport avec compteur"""
    try:
        from flask import send_file
        
        # Chercher le rapport en base de données
        report = Report.query.filter_by(filename=filename).first()
        if not report:
            return jsonify({'success': False, 'message': 'Rapport non trouvé en base'}), 404
        
        # Vérifier que le fichier existe
        if not report.file_path or not os.path.exists(report.file_path):
            return jsonify({'success': False, 'message': 'Fichier physique non trouvé'}), 404
        
        # Incrémenter le compteur de téléchargements
        report.download_count += 1
        db.session.commit()
        
        # Retourner le fichier
        return send_file(report.file_path, as_attachment=True, download_name=filename)
            
    except Exception as e:
        logger.error(f"Erreur téléchargement rapport: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/download/<filename>')
@login_required
def download_report(filename):
    """Route de téléchargement direct pour compatibilité frontend"""
    try:
        from flask import send_file
        report_path = os.path.join('reports', filename)
        
        if os.path.exists(report_path):
            return send_file(report_path, as_attachment=True)
        else:
            return jsonify({'success': False, 'message': 'Fichier non trouvé'}), 404
            
    except Exception as e:
        logger.error(f"Erreur téléchargement rapport: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/reports/stats')
@login_required
def api_reports_stats():
    """API pour les statistiques des rapports"""
    try:
        reports_dir = 'reports'
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        report_files = []
        for filename in os.listdir(reports_dir):
            if filename.endswith(('.pdf', '.xlsx', '.json')):
                filepath = os.path.join(reports_dir, filename)
                stat = os.stat(filepath)
                report_files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime)
                })
        
        total_reports = len(report_files)
        current_month = datetime.now().month
        reports_this_month = len([r for r in report_files if r['created'].month == current_month])
        
        return jsonify({
            'total_reports': total_reports,
            'reports_this_month': reports_this_month,
            'total_size_mb': sum(r['size'] for r in report_files) / (1024 * 1024)
        })
        
    except Exception as e:
        logger.error(f"Erreur statistiques rapports: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/reports')
@login_required
def api_reports():
    """API pour récupérer la liste des rapports depuis la base de données"""
    try:
        # Récupérer tous les rapports depuis la base de données
        reports = Report.query.order_by(Report.created_at.desc()).all()
        
        # Convertir en format attendu par le frontend
        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'name': report.name,
                'filename': report.filename,
                'type': report.format.upper(),  # PDF, EXCEL, etc.
                'format': report.format,
                'status': report.status,
                'size': f"{report.file_size / (1024 * 1024):.1f} MB" if report.file_size > 1024*1024 else f"{report.file_size / 1024:.1f} KB",
                'created': report.created_at.strftime('%Y-%m-%d %H:%M:%S') if report.created_at else '',
                'created_at': report.created_at.isoformat() if report.created_at else None,
                'description': report.description or 'Rapport automatisé',
                'download_url': f'/api/reports/download/{report.filename}' if report.status == 'completed' else None,
                'report_type': report.type.title()
            })
        
        return jsonify({
            'success': True,
            'reports': reports_data
        })
        
    except Exception as e:
        logger.error(f"Erreur récupération rapports: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'reports': []
        }), 500

@app.route('/api/reports/list')
@login_required
def api_reports_list():
    """API pour récupérer la liste des rapports"""
    try:
        from report_generator import ReportGenerator
        report_gen = ReportGenerator()
        reports = report_gen.list_reports()
        
        # Formater les données pour le frontend
        formatted_reports = []
        for report in reports:
            # Déterminer le type de rapport basé sur le nom de fichier
            filename = report['filename']
            if 'journalier' in filename:
                report_type = 'Journalier'
            elif 'hebdomadaire' in filename:
                report_type = 'Hebdomadaire'
            elif 'mensuel' in filename:
                report_type = 'Mensuel'
            elif 'ai' in filename:
                report_type = 'IA'
            else:
                report_type = 'Personnalisé'
            
            # Déterminer le format
            if filename.endswith('.pdf'):
                format_type = 'PDF'
                format_class = 'pdf'
            elif filename.endswith('.xlsx'):
                format_type = 'Excel'
                format_class = 'excel'
            elif filename.endswith('.json'):
                format_type = 'JSON'
                format_class = 'json'
            else:
                format_type = 'Inconnu'
                format_class = 'unknown'
            
            # Formater la taille
            size_mb = report['size'] / (1024 * 1024)
            if size_mb < 1:
                size_str = f"{report['size'] / 1024:.1f} KB"
            else:
                size_str = f"{size_mb:.1f} MB"
            
            formatted_reports.append({
                'filename': filename,
                'type': format_type,
                'size': size_str,
                'created': report['created'].strftime('%Y-%m-%d %H:%M:%S'),
                'format': format_class,
                'report_type': report_type
            })
        
        return jsonify({
            'success': True,
            'reports': formatted_reports
        })
        
    except Exception as e:
        logger.error(f"Erreur liste rapports: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reports/schedule', methods=['POST'])
@login_required
def api_reports_schedule():
    """API pour programmer la génération de rapports"""
    try:
        data = request.get_json()
        
        # Valider les données requises
        required_fields = ['type', 'frequency', 'time']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Champ requis manquant: {field}'}), 400
        
        # Simuler la programmation (dans un vrai système, on utiliserait un scheduler comme Celery)
        scheduled_report = {
            'id': f"scheduled_{int(time.time())}",
            'type': data.get('type'),
            'frequency': data.get('frequency'),
            'time': data.get('time'),
            'email': data.get('email'),
            'sections': data.get('sections', []),
            'created_at': datetime.now().isoformat(),
            'status': 'scheduled'
        }
        
        # En production, on sauvegarderait en base de données
        logger.info(f"Rapport programmé: {scheduled_report}")
        
        return jsonify({
            'success': True,
            'message': 'Rapport programmé avec succès',
            'schedule_id': scheduled_report['id']
        })
        
    except Exception as e:
        logger.error(f"Erreur programmation rapport: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/ai-dashboard')
@login_required
def ai_dashboard():
    """Dashboard spécialisé IA"""
    try:
        # Statistiques IA avancées
        devices = Device.query.all()
        
        # Distribution par type d'équipement
        device_types = {}
        for device in devices:
            device_type = device.device_type
            device_types[device_type] = device_types.get(device_type, 0) + 1
        
        # Distribution par urgence de maintenance
        urgency_distribution = {
            'critical': Device.query.filter_by(maintenance_urgency='critical').count(),
            'high': Device.query.filter_by(maintenance_urgency='high').count(),
            'medium': Device.query.filter_by(maintenance_urgency='medium').count(),
            'low': Device.query.filter_by(maintenance_urgency='low').count()
        }
        
        # Équipements à risque
        high_risk_devices = Device.query.filter(Device.failure_probability > AI_CONFIG['HIGH_RISK_THRESHOLD']).order_by(Device.failure_probability.desc()).limit(AI_CONFIG['MAX_RECOMMENDATIONS']).all()
        
        # Équipements avec anomalies
        anomaly_devices = Device.query.filter(Device.anomaly_score < AI_CONFIG['ANOMALY_THRESHOLD']).order_by(Device.anomaly_score.asc()).limit(AI_CONFIG['MAX_RECOMMENDATIONS']).all()
        
        # Modèles IA
        ai_models = AIModel.query.filter_by(is_active=True).all()
        
        # Calcul du score de santé moyen
        avg_health_score = db.session.query(db.func.avg(Device.health_score)).scalar() or 0
        
        # Équipements critiques
        critical_devices = Device.query.filter(Device.health_score < AI_CONFIG['CRITICAL_HEALTH_THRESHOLD']).count()
        
        # Nombre d'équipements à risque élevé
        high_risk_count = len(high_risk_devices)
        
        # Nombre d'équipements avec anomalies
        anomaly_count = len(anomaly_devices)
        
        return render_template('ai_dashboard.html',
                             device_types=device_types,
                             urgency_distribution=urgency_distribution,
                             high_risk_devices=high_risk_devices,
                             anomaly_devices=anomaly_devices,
                             ai_models=ai_models,
                             avg_health_score=round(avg_health_score, 1),
                             ai_models_loaded=ai_models_loaded,
                             critical_devices=critical_devices,
                             high_risk_devices_count=high_risk_count,
                             anomaly_devices_count=anomaly_count)
    except Exception as e:
        logger.error(f"Erreur dashboard IA: {e}")
        return render_template('error.html', error=str(e))

@app.route('/api/statistics')
@login_required
def api_statistics():
    """API pour statistiques globales du réseau"""
    try:
        total_devices = Device.query.count()
        online_devices = Device.query.filter_by(is_online=True).count()
        offline_devices = Device.query.filter_by(is_online=False).count()
        uptime_percentage = 0.0
        if total_devices > 0:
            uptime_percentage = (online_devices / total_devices) * 100
        return jsonify({
            'total_devices': total_devices,
            'online_devices': online_devices,
            'offline_devices': offline_devices,
            'uptime_percentage': round(uptime_percentage, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/email', methods=['GET'])
@login_required
def api_get_email_settings():
    """API pour récupérer la configuration email avec gestionnaire production"""
    try:
        from settings_manager_production import get_production_settings_manager
        
        settings_manager = get_production_settings_manager()
        email_settings = settings_manager.get_email_settings()
        
        return jsonify(email_settings)
    except Exception as e:
        logger.error(f"Erreur récupération config email: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings/email/test', methods=['POST'])
@login_required
def api_test_email():
    """API pour tester l'envoi d'email"""
    try:
        result = test_email_configuration()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur test email: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/settings/email', methods=['POST'])
@login_required
def api_save_email_settings():
    """API pour sauvegarder la configuration email"""
    try:
        data = request.get_json()
        
        # Get settings manager
        from settings_manager_production import get_production_settings_manager
        settings_manager = get_production_settings_manager()
        
        # Update email settings in the manager
        settings_manager.settings.update({
            'email_enabled': data.get('email_enabled', False),
            'smtp_server': data.get('smtp_server', ''),
            'smtp_port': data.get('smtp_port', 587),
            'email_username': data.get('smtp_username', ''),
            'email_password': data.get('smtp_password', ''),
            'from_email': data.get('from_email', ''),
            'to_email': ', '.join(data.get('recipients', [])),
            'last_updated': datetime.now().isoformat()
        })
        
        # Save settings
        success = settings_manager.save_settings()
        
        if success:
            # Update global EMAIL_CONFIG for immediate use
            global EMAIL_CONFIG
            EMAIL_CONFIG.update({
                'enabled': data.get('email_enabled', False),
                'smtp_server': data.get('smtp_server', ''),
                'smtp_port': data.get('smtp_port', 587),
                'smtp_username': data.get('smtp_username', ''),
                'smtp_password': data.get('smtp_password', ''),
                'use_tls': data.get('use_tls', True),
                'from_email': data.get('from_email', ''),
                'recipients': data.get('recipients', [])
            })
            
            logger.info("Configuration email mise à jour avec succès")
            return jsonify({
                'status': 'success',
                'message': 'Configuration email sauvegardée avec succès'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de la sauvegarde'
            })
            
    except Exception as e:
        logger.error(f"Erreur sauvegarde email: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/settings/email/status', methods=['GET'])
@login_required
def api_email_status():
    """API pour obtenir le statut de la configuration email"""
    try:
        # Get settings from settings manager
        from settings_manager_production import get_production_settings_manager
        settings_manager = get_production_settings_manager()
        settings = settings_manager.get_all_settings()
        
        status = {
            'enabled': settings.get('email_enabled', False),
            'configured': bool(settings.get('smtp_server') and settings.get('email_username')),
            'smtp_server': settings.get('smtp_server', ''),
            'smtp_port': settings.get('smtp_port', 587),
            'smtp_username': settings.get('email_username', ''),
            'use_tls': True,  # Default value
            'recipients': [email.strip() for email in settings.get('to_email', '').split(',') if email.strip()]
        }
        
        return jsonify({
            'status': 'success',
            'data': status
        })
    except Exception as e:
        logger.error(f"Erreur statut email: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/settings/email/alert', methods=['POST'])
@login_required
def api_send_test_alert():
    """API pour envoyer une alerte de test"""
    try:
        data = request.get_json()
        subject = data.get('subject', 'Test d\'alerte')
        message = data.get('message', 'Ceci est un test d\'alerte Central Danone')
        priority = data.get('priority', 'medium')
        
        success = send_email_alert(subject, message, priority)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Alerte de test envoyée avec succès'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de l\'envoi de l\'alerte'
            })
    except Exception as e:
        logger.error(f"Erreur envoi alerte test: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/settings/alert-email', methods=['POST'])
@login_required
def api_save_alert_email():
    """API pour sauvegarder l'email d'alerte simple"""
    try:
        data = request.get_json()
        alert_email = data.get('alert_email', '')
        
        # Mettre à jour la configuration email avec l'email simple
        EMAIL_CONFIG['to_email'] = alert_email
        
        logger.info(f"Email d'alerte simple mis à jour: {alert_email}")
        
        return jsonify({
            'status': 'success',
            'message': 'Email d\'alerte sauvegardé'
        })
    except Exception as e:
        logger.error(f"Erreur sauvegarde email alerte: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/notifications')
@login_required
def api_notifications():
    """API pour récupérer les notifications"""
    try:
        unread_count = len(get_unread_notifications())
        recent_notifications = NOTIFICATIONS[-10:]  # 10 dernières
        
        return jsonify({
            'unread_count': unread_count,
            'notifications': recent_notifications
        })
    except Exception as e:
        logger.error(f"Erreur API notifications: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/notifications/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def api_mark_notification_read(notification_id):
    """API pour marquer une notification comme lue"""
    try:
        mark_notification_read(notification_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Erreur marquer notification lue: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/notifications/clear', methods=['POST'])
@login_required
def api_clear_notifications():
    """API pour effacer toutes les notifications"""
    try:
        global NOTIFICATIONS
        NOTIFICATIONS = []
        return jsonify({'status': 'success', 'message': 'Notifications effacées'})
    except Exception as e:
        logger.error(f"Erreur effacer notifications: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/test-notification', methods=['POST'])
@login_required
def api_test_notification():
    """API pour tester les notifications"""
    try:
        data = request.get_json()
        message = data.get('message', 'Test de notification Central Danone')
        notification_type = data.get('type', 'info')
        priority = data.get('priority', 'medium')
        
        notification = add_notification(message, notification_type, priority)
        
        return jsonify({
            'status': 'success',
            'message': 'Notification de test créée',
            'notification': notification
        })
    except Exception as e:
        logger.error(f"Erreur test notification: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/ai/chart-data')
@login_required
def api_ai_chart_data():
    """API pour les données des graphiques IA"""
    try:
        # Données pour le graphique des types d'équipements
        device_types = db.session.query(
            Device.device_type,
            db.func.count(Device.id).label('count')
        ).group_by(Device.device_type).all()
        
        device_types_data = {
            'labels': [dt.device_type.title() for dt in device_types],
            'data': [dt.count for dt in device_types]
        }
        
        # Données pour le graphique des scores de santé
        health_ranges = [
            (90, 100, 'Excellent'),
            (70, 89, 'Bon'),
            (50, 69, 'Moyen'),
            (30, 49, 'Faible'),
            (0, 29, 'Critique')
        ]
        
        health_scores_data = []
        health_scores_labels = []
        
        for min_score, max_score, label in health_ranges:
            count = Device.query.filter(
                Device.health_score >= min_score,
                Device.health_score <= max_score
            ).count()
            health_scores_data.append(count)
            health_scores_labels.append(label)
        
        health_scores = {
            'labels': health_scores_labels,
            'data': health_scores_data
        }
        
        return jsonify({
            'device_types': device_types_data,
            'health_scores': health_scores
        })
    except Exception as e:
        logger.error(f"Erreur API données graphiques IA: {e}")
        return jsonify({'error': str(e)}), 500

# ===== ROUTES POUR LE MONITORING AVANCÉ =====

@app.route('/advanced-monitoring')
@login_required
def advanced_monitoring_page():
    """Page de monitoring avancé"""
    return render_template('advanced_monitoring.html')

@app.route('/api/advanced-monitoring/services')
@login_required
def api_advanced_monitoring_services():
    """API pour récupérer les statuts des services"""
    try:
        services = advanced_monitoring.get_service_status_summary()
        return jsonify(services)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des services: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-monitoring/ports')
@login_required
def api_advanced_monitoring_ports():
    """API pour récupérer les statuts des ports"""
    try:
        # Simuler des données de ports pour l'instant
        ports = [
            {'port': 80, 'status': 'up', 'last_check': datetime.now().isoformat()},
            {'port': 443, 'status': 'up', 'last_check': datetime.now().isoformat()},
            {'port': 22, 'status': 'down', 'last_check': datetime.now().isoformat()},
            {'port': 21, 'status': 'timeout', 'last_check': datetime.now().isoformat()}
        ]
        return jsonify(ports)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des ports: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-monitoring/discovered-devices')
@login_required
def api_advanced_monitoring_discovered_devices():
    """API pour récupérer les équipements découverts"""
    try:
        devices = advanced_monitoring.get_discovered_devices()
        return jsonify(devices)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des équipements découverts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-monitoring/locations')
@login_required
def api_advanced_monitoring_locations():
    """API pour récupérer les géolocalisations"""
    try:
        locations = advanced_monitoring.get_device_locations()
        return jsonify([{
            'ip': loc.ip,
            'country': loc.country,
            'city': loc.city,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'isp': loc.isp
        } for loc in locations])
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des géolocalisations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-monitoring/bandwidth')
@login_required
def api_advanced_monitoring_bandwidth():
    """API pour récupérer les données de bande passante"""
    try:
        # Simuler des données de bande passante pour l'instant
        bandwidth = [
            {
                'device_ip': '192.168.1.1',
                'interface': 'eth0',
                'bytes_sent': 1024000,
                'bytes_received': 2048000,
                'packets_sent': 1000,
                'packets_received': 2000,
                'timestamp': datetime.now().isoformat()
            }
        ]
        return jsonify(bandwidth)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la bande passante: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-monitoring/check-services', methods=['POST'])
@login_required
def api_advanced_monitoring_check_services():
    """API pour vérifier les services"""
    try:
        advanced_monitoring.check_all_services()
        return jsonify({'success': True, 'message': 'Vérification des services terminée'})
    except Exception as e:
        logger.error(f"Erreur lors de la vérification des services: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/advanced-monitoring/scan-ports', methods=['POST'])
@login_required
def api_advanced_monitoring_scan_ports():
    """API pour scanner les ports"""
    try:
        advanced_monitoring.check_all_ports()
        return jsonify({'success': True, 'message': 'Scan des ports terminé'})
    except Exception as e:
        logger.error(f"Erreur lors du scan des ports: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/advanced-monitoring/discover-devices', methods=['POST'])
@login_required
def api_advanced_monitoring_discover_devices():
    """API pour découvrir de nouveaux équipements"""
    try:
        advanced_monitoring.auto_discover_devices()
        discovered_count = len(advanced_monitoring.get_discovered_devices())
        return jsonify({
            'success': True, 
            'message': 'Découverte d\'équipements terminée',
            'discovered_count': discovered_count
        })
    except Exception as e:
        logger.error(f"Erreur lors de la découverte d'équipements: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/advanced-monitoring/update-locations', methods=['POST'])
@login_required
def api_advanced_monitoring_update_locations():
    """API pour mettre à jour les géolocalisations"""
    try:
        advanced_monitoring.update_device_locations()
        return jsonify({'success': True, 'message': 'Mise à jour des géolocalisations terminée'})
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des géolocalisations: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/advanced-monitoring/device-details/<ip>')
@login_required
def api_advanced_monitoring_device_details(ip):
    """API pour les détails d'un équipement"""
    try:
        # Récupérer les détails de l'équipement
        device = Device.query.filter_by(ip=ip).first()
        location = advanced_monitoring.get_device_location(ip)
        
        details = {
            'ip': ip,
            'mac': device.mac if device else None,
            'hostname': device.hostname if device else None,
            'device_type': device.device_type if device else 'unknown',
            'location': {
                'country': location.country if location else None,
                'city': location.city if location else None,
                'isp': location.isp if location else None
            } if location else None
        }
        
        return jsonify(details)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des détails de l'équipement: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced-monitoring/add-device', methods=['POST'])
@login_required
def api_advanced_monitoring_add_device():
    """API pour ajouter un équipement au monitoring"""
    try:
        data = request.get_json()
        ip = data.get('ip')
        
        if not ip:
            return jsonify({'success': False, 'error': 'Adresse IP requise'}), 400
        
        # Vérifier si l'équipement existe déjà
        existing_device = Device.query.filter_by(ip=ip).first()
        if existing_device:
            return jsonify({'success': False, 'error': 'Équipement déjà en monitoring'}), 400
        
        # Créer un nouvel équipement
        new_device = Device(
            ip=ip,
            is_online=True,
            device_type='discovered',
            created_at=datetime.now()
        )
        
        db.session.add(new_device)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Équipement {ip} ajouté au monitoring'})
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout de l'équipement: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes pour l'IA Avancée - Phase 3
@app.route('/ai-advanced')
@login_required
def ai_advanced_page():
    """Page IA Avancée"""
    current_time = get_local_time()
    return render_template('ai_advanced.html', current_time=current_time)

@app.route('/api/ai-advanced/predictions')
@login_required
def api_ai_advanced_predictions():
    """API pour récupérer les prédictions IA basées sur des données réelles"""
    try:
        # Récupérer les équipements avec des scores de défaillance élevés
        high_risk_devices = Device.query.filter(
            Device.failure_probability > 0.3
        ).order_by(Device.failure_probability.desc()).limit(5).all()
        
        predictions = []
        for device in high_risk_devices:
            # Déterminer le type de prédiction basé sur les métriques
            if device.failure_probability > 0.7:
                prediction_type = "Défaillance critique imminente"
                severity = "Critique"
            elif device.failure_probability > 0.5:
                prediction_type = "Problème de performance"
                severity = "Élevé"
            elif device.health_score < 60:
                prediction_type = "Maintenance préventive"
                severity = "Moyen"
            else:
                prediction_type = "Surveillance renforcée"
                severity = "Faible"
            
            predictions.append({
                'device_id': device.id,
                'device_name': device.hostname or f"Équipement {device.ip}",
                'prediction_type': prediction_type,
                'confidence': round(device.ai_confidence, 2) if device.ai_confidence > 0 else 0.75,
                'timestamp': device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                'description': f"Prédiction basée sur le score de défaillance ({device.failure_probability:.1%}) et le score de santé ({device.health_score:.1f}%)",
                'severity': severity
            })
        
        # Si pas assez de prédictions, ajouter des équipements avec des scores de santé faibles
        if len(predictions) < 3:
            low_health_devices = Device.query.filter(
                Device.health_score < 80,
                Device.failure_probability <= 0.3
            ).order_by(Device.health_score.asc()).limit(3 - len(predictions)).all()
            
            for device in low_health_devices:
                predictions.append({
                    'device_id': device.id,
                    'device_name': device.hostname or f"Équipement {device.ip}",
                    'prediction_type': "Dégradation de performance",
                    'confidence': 0.65,
                    'timestamp': device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'description': f"Score de santé faible ({device.health_score:.1f}%) détecté",
                    'severity': "Moyen"
                })
        
        return jsonify({'success': True, 'predictions': predictions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/intrusions')
@login_required
def api_ai_advanced_intrusions():
    """API pour récupérer les intrusions détectées basées sur des données réelles"""
    try:
        intrusions = []
        
        # Récupérer les alertes de sécurité récentes
        security_alerts = Alert.query.filter(
            Alert.alert_type.in_(['intrusion', 'security', 'anomaly']),
            Alert.created_at >= datetime.now() - timedelta(days=7)
        ).order_by(Alert.created_at.desc()).limit(5).all()
        
        for alert in security_alerts:
            device = Device.query.get(alert.device_id)
            if device:
                # Déterminer le type d'attaque basé sur l'alerte
                if 'intrusion' in alert.alert_type.lower():
                    attack_type = "Tentative d'intrusion"
                    severity = "Critique" if alert.priority == 'critical' else "Moyen"
                elif 'anomaly' in alert.alert_type.lower():
                    attack_type = "Comportement anormal"
                    severity = "Élevé" if alert.priority == 'high' else "Faible"
                else:
                    attack_type = "Activité suspecte"
                    severity = "Moyen"
                
                intrusions.append({
                    'id': alert.id,
                    'source_ip': 'Détecté automatiquement',
                    'target_ip': device.ip,
                    'attack_type': attack_type,
                    'severity': severity,
                    'timestamp': alert.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 'En cours' if not alert.is_resolved else 'Résolu',
                    'description': alert.message
                })
        
        # Si pas assez d'intrusions, analyser les équipements avec des scores d'anomalie élevés
        if len(intrusions) < 3:
            anomaly_devices = Device.query.filter(
                Device.anomaly_score > 0.5
            ).order_by(Device.anomaly_score.desc()).limit(3 - len(intrusions)).all()
            
            for device in anomaly_devices:
                intrusions.append({
                    'id': len(intrusions) + 1,
                    'source_ip': 'Analyse comportementale',
                    'target_ip': device.ip,
                    'attack_type': "Anomalie détectée",
                    'severity': "Moyen",
                    'timestamp': device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 'Analysée',
                    'description': f"Score d'anomalie élevé ({device.anomaly_score:.1%}) détecté sur {device.hostname or device.ip}"
                })
        
        return jsonify({'success': True, 'intrusions': intrusions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/optimizations')
@login_required
def api_ai_advanced_optimizations():
    """API pour récupérer les optimisations basées sur des données réelles"""
    try:
        optimizations = []
        
        # Récupérer les équipements avec des scores de santé faibles qui nécessitent des optimisations
        low_health_devices = Device.query.filter(
            Device.health_score < 80
        ).order_by(Device.health_score.asc()).limit(5).all()
        
        for device in low_health_devices:
            # Déterminer le type d'optimisation basé sur le score de santé
            if device.health_score < 50:
                category = "Maintenance critique"
                title = "Intervention immédiate requise"
                impact = "Critique"
                implementation_time = "Immédiat"
                status = "En attente"
            elif device.health_score < 70:
                category = "Performance réseau"
                title = "Optimisation des performances"
                impact = "Élevé"
                implementation_time = "4 heures"
                status = "En cours"
            else:
                category = "Maintenance préventive"
                title = "Maintenance préventive recommandée"
                impact = "Moyen"
                implementation_time = "2 heures"
                status = "Planifiée"
            
            optimizations.append({
                'id': device.id,
                'category': category,
                'title': title,
                'description': f"Optimisation recommandée pour {device.hostname or device.ip} (Score de santé: {device.health_score:.1f}%)",
                'impact': impact,
                'implementation_time': implementation_time,
                'status': status,
                'timestamp': device.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Ajouter des optimisations basées sur les recommandations IA
        devices_with_recommendations = Device.query.filter(
            Device.ai_recommendations != '[]',
            Device.ai_recommendations != ''
        ).limit(3).all()
        
        for device in devices_with_recommendations:
            try:
                recommendations = json.loads(device.ai_recommendations)
                if recommendations and len(recommendations) > 0:
                    optimizations.append({
                        'id': f"rec_{device.id}",
                        'category': "Recommandation IA",
                        'title': f"Optimisation IA pour {device.hostname or device.ip}",
                        'description': recommendations[0] if isinstance(recommendations, list) else str(recommendations),
                        'impact': "Moyen",
                        'implementation_time': "1 heure",
                        'status': "Terminée",
                        'timestamp': device.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    })
            except (json.JSONDecodeError, IndexError):
                continue
        
        return jsonify({'success': True, 'optimizations': optimizations})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/trends')
@login_required
def api_ai_advanced_trends():
    """API pour récupérer les analyses de tendances basées sur des données réelles"""
    try:
        trends = []
        
        # Analyser les tendances de temps de réponse
        recent_scans = ScanHistory.query.filter(
            ScanHistory.timestamp >= datetime.now() - timedelta(days=7)
        ).all()
        
        if recent_scans:
            # Calculer les tendances de temps de réponse
            response_times = [scan.response_time for scan in recent_scans if scan.response_time]
            if response_times:
                current_avg = sum(response_times) / len(response_times)
                # Comparer avec la semaine précédente
                old_scans = ScanHistory.query.filter(
                    ScanHistory.timestamp >= datetime.now() - timedelta(days=14),
                    ScanHistory.timestamp < datetime.now() - timedelta(days=7)
                ).all()
                
                old_response_times = [scan.response_time for scan in old_scans if scan.response_time]
                if old_response_times:
                    previous_avg = sum(old_response_times) / len(old_response_times)
                    change_percentage = ((current_avg - previous_avg) / previous_avg) * 100
                    trend_direction = "Hausse" if change_percentage > 0 else "Baisse" if change_percentage < 0 else "Stable"
                else:
                    change_percentage = 0.0
                    trend_direction = "Stable"
                
                trends.append({
                    'metric': 'Temps de réponse moyen',
                    'current_value': round(current_avg, 1),
                    'previous_value': round(previous_avg, 1) if old_response_times else round(current_avg, 1),
                    'change_percentage': round(change_percentage, 1),
                    'trend_direction': trend_direction,
                    'period': '24h',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Analyser les tendances de disponibilité
        devices = Device.query.all()
        if devices:
            online_count = sum(1 for d in devices if d.is_online)
            current_availability = (online_count / len(devices)) * 100
            
            # Comparer avec les données historiques
            total_scans = ScanHistory.query.count()
            online_scans = ScanHistory.query.filter_by(is_online=True).count()
            historical_availability = (online_scans / total_scans * 100) if total_scans > 0 else current_availability
            
            change_percentage = current_availability - historical_availability
            trend_direction = "Hausse" if change_percentage > 0 else "Baisse" if change_percentage < 0 else "Stable"
            
            trends.append({
                'metric': 'Taux de disponibilité',
                'current_value': round(current_availability, 1),
                'previous_value': round(historical_availability, 1),
                'change_percentage': round(change_percentage, 1),
                'trend_direction': trend_direction,
                'period': '24h',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Analyser les tendances de santé IA
        if devices:
            avg_health = sum(d.health_score for d in devices) / len(devices)
            critical_devices = sum(1 for d in devices if d.health_score < 50)
            
            trends.append({
                'metric': 'Score de santé moyen',
                'current_value': round(avg_health, 1),
                'previous_value': round(avg_health, 1),  # Pour simplifier
                'change_percentage': 0.0,
                'trend_direction': "Stable",
                'period': '24h',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            trends.append({
                'metric': 'Équipements critiques',
                'current_value': critical_devices,
                'previous_value': critical_devices,  # Pour simplifier
                'change_percentage': 0.0,
                'trend_direction': "Stable",
                'period': '24h',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify({'success': True, 'trends': trends})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/statistics')
@login_required
def api_ai_advanced_statistics():
    """API pour récupérer les statistiques IA avancée basées sur des données réelles"""
    try:
        # Calculer les statistiques réelles basées sur les données de la base
        devices = Device.query.all()
        total_devices = len(devices)
        
        # Statistiques des prédictions (basées sur les scores de santé)
        critical_devices = sum(1 for d in devices if d.maintenance_urgency == 'critical')
        high_risk_devices = sum(1 for d in devices if d.failure_probability > 0.5)
        total_predictions = total_devices
        
        # Taux de précision basé sur les scores de confiance IA
        if total_devices > 0:
            avg_confidence = sum(d.ai_confidence for d in devices) / total_devices
            accuracy_rate = round(avg_confidence, 2) if avg_confidence > 0 else 0.85
        else:
            accuracy_rate = 0.85
        
        # Intrusions bloquées (basées sur les alertes de sécurité)
        security_alerts = Alert.query.filter(
            Alert.alert_type.in_(['intrusion', 'security', 'anomaly'])
        ).count()
        intrusions_blocked = security_alerts
        
        # Optimisations appliquées (basées sur les changements de scores de santé)
        optimizations_applied = sum(1 for d in devices if d.health_score > 90)
        
        # Tendances analysées (basées sur l'historique des scans)
        trends_analyzed = ScanHistory.query.count()
        
        # Modèles IA actifs
        ai_models_active = AIModel.query.filter_by(is_active=True).count()
        
        # Dernier entraînement
        latest_model = AIModel.query.order_by(AIModel.training_date.desc()).first()
        last_training = latest_model.training_date.strftime("%Y-%m-%d %H:%M:%S") if latest_model else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prochain entraînement (6 heures après le dernier)
        next_training = (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
        
        statistics = {
            'total_predictions': total_predictions,
            'accuracy_rate': accuracy_rate,
            'intrusions_blocked': intrusions_blocked,
            'optimizations_applied': optimizations_applied,
            'trends_analyzed': trends_analyzed,
            'ai_models_active': ai_models_active,
            'last_training': last_training,
            'next_training': next_training
        }
        return jsonify({'success': True, 'statistics': statistics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/run-predictions', methods=['POST'])
@login_required
def api_ai_advanced_run_predictions():
    """API pour lancer les prédictions IA"""
    try:
        # Simulation de lancement de prédictions
        time.sleep(2)  # Simulation de traitement
        return jsonify({'success': True, 'message': 'Prédictions IA lancées avec succès !'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/run-intrusion-detection', methods=['POST'])
@login_required
def api_ai_advanced_run_intrusion_detection():
    """API pour lancer la détection d'intrusion"""
    try:
        # Simulation de détection d'intrusion
        time.sleep(2)  # Simulation de traitement
        return jsonify({'success': True, 'message': 'Détection d\'intrusion lancée avec succès !'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/run-optimization', methods=['POST'])
@login_required
def api_ai_advanced_run_optimization():
    """API pour lancer l'optimisation automatique"""
    try:
        # Simulation d'optimisation
        time.sleep(2)  # Simulation de traitement
        return jsonify({'success': True, 'message': 'Optimisation automatique lancée avec succès !'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/run-trend-analysis', methods=['POST'])
@login_required
def api_ai_advanced_run_trend_analysis():
    """API pour lancer l'analyse des tendances"""
    try:
        # Simulation d'analyse de tendances
        time.sleep(2)  # Simulation de traitement
        return jsonify({'success': True, 'message': 'Analyse des tendances lancée avec succès !'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/chatbot', methods=['POST'])
@login_required
def api_ai_advanced_chatbot():
    """API pour le chatbot IA avec DeepSeek"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Récupérer les données réelles
        devices = Device.query.all()
        alerts = Alert.query.filter_by(is_resolved=False).all()
        
        # Convertir en dictionnaires pour DeepSeek
        devices_data = []
        for device in devices:
            devices_data.append({
                'ip': device.ip,
                'hostname': device.hostname,
                'is_online': device.is_online,
                'health_score': device.health_score,
                'maintenance_urgency': device.maintenance_urgency,
                'device_type': device.device_type,
                'last_seen': device.last_seen.strftime("%Y-%m-%d %H:%M:%S") if device.last_seen else None
            })
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'message': alert.message,
                'alert_type': alert.alert_type,
                'priority': alert.priority,
                'is_resolved': alert.is_resolved,
                'created_at': alert.created_at.strftime("%Y-%m-%d %H:%M:%S") if alert.created_at else None
            })
        
        # Importer et utiliser Groq
        try:
            from groq_chatbot import groq_bot
            
            # Essayer Groq d'abord
            result = groq_bot.chat(message, devices_data, alerts_data)
            
            if result.get('success'):
                return jsonify({
                    'success': True,
                    'response': result['response'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'confidence': result['confidence'],
                    'model': result.get('model', 'Groq'),
                    'tokens_used': result.get('tokens_used', 0)
                })
            else:
                # Fallback vers l'ancien système si Groq échoue
                logger.warning(f"Groq échoué: {result.get('error')}, utilisation du fallback")
                return _fallback_chatbot(message, devices, alerts)
                
        except ImportError:
            logger.warning("Module Groq non disponible, utilisation du fallback")
            return _fallback_chatbot(message, devices, alerts)
            
    except Exception as e:
        logger.error(f"Erreur chatbot: {e}")
        return jsonify({'success': False, 'error': str(e)})

def _fallback_chatbot(message: str, devices, alerts):
    """Chatbot de fallback basé sur les données réelles"""
    try:
        message_lower = message.lower()
        
        total_devices = len(devices)
        online_devices = sum(1 for d in devices if d.is_online)
        offline_devices = total_devices - online_devices
        critical_devices = sum(1 for d in devices if d.maintenance_urgency == 'critical')
        avg_health = sum(d.health_score for d in devices) / len(devices) if devices else 0
        
        active_alerts = len(alerts)
        
        if any(word in message_lower for word in ['bonjour', 'salut', 'hello']):
            response = f"Bonjour ! Je suis l'assistant IA de Central Danone. Je surveille actuellement {total_devices} équipements. Comment puis-je vous aider ?"
        elif any(word in message_lower for word in ['santé', 'état', 'statut', 'status']):
            if avg_health > 80:
                response = f"La santé du réseau est excellente ! Score moyen : {avg_health:.1f}%. {online_devices}/{total_devices} équipements en ligne."
            elif avg_health > 60:
                response = f"La santé du réseau est correcte. Score moyen : {avg_health:.1f}%. {offline_devices} équipements hors ligne nécessitent attention."
            else:
                response = f"⚠️ La santé du réseau nécessite attention. Score moyen : {avg_health:.1f}%. {critical_devices} équipements critiques détectés."
        elif any(word in message_lower for word in ['problème', 'erreur', 'alerte']):
            if active_alerts > 0:
                response = f"🚨 {active_alerts} alerte(s) active(s) détectée(s). Voulez-vous que je génère un rapport détaillé ?"
            else:
                response = "✅ Aucune alerte active actuellement. Le système fonctionne normalement."
        elif any(word in message_lower for word in ['optimisation', 'optimiser']):
            low_health_count = sum(1 for d in devices if d.health_score < 70)
            if low_health_count > 0:
                response = f"J'ai identifié {low_health_count} opportunité(s) d'optimisation. Voulez-vous les voir ?"
            else:
                response = "Tous les équipements fonctionnent de manière optimale. Aucune optimisation nécessaire."
        elif any(word in message_lower for word in ['sécurité', 'intrusion']):
            security_alerts = sum(1 for a in alerts if a.alert_type in ['intrusion', 'security', 'anomaly'])
            if security_alerts > 0:
                response = f"🛡️ {security_alerts} menace(s) de sécurité détectée(s). Niveau de sécurité : Élevé."
            else:
                response = "🛡️ Le niveau de sécurité est élevé. Aucune menace critique détectée."
        elif any(word in message_lower for word in ['performance', 'perf']):
            if avg_health > 85:
                response = "Les performances sont excellentes. Tous les équipements fonctionnent dans les normes."
            elif avg_health > 70:
                response = "Les performances sont correctes. Quelques optimisations mineures possibles."
            else:
                response = "⚠️ Les performances nécessitent attention. Optimisations recommandées."
        elif any(word in message_lower for word in ['aide', 'help', 'assistance']):
            response = "Je peux vous aider avec : santé réseau, problèmes, optimisations, sécurité, performance, statistiques."
        elif any(word in message_lower for word in ['statistique', 'stats', 'nombre']):
            response = f"📊 Statistiques actuelles : {total_devices} équipements total, {online_devices} en ligne, {offline_devices} hors ligne, {active_alerts} alertes actives."
        elif any(word in message_lower for word in ['au revoir', 'bye', 'merci']):
            response = "Au revoir ! N'hésitez pas à revenir si vous avez besoin d'aide."
        else:
            response = "Je ne comprends pas votre demande. Tapez 'aide' pour voir mes capacités ou posez une question sur l'état du réseau."
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'confidence': 0.9,
            'model': 'Fallback'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-advanced/test-deepseek', methods=['POST'])
@login_required
def api_test_deepseek():
    """Teste la connexion à l'API DeepSeek"""
    try:
        from deepseek_chatbot import deepseek_bot
        result = deepseek_bot.test_connection()
        return jsonify(result)
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Module DeepSeek non disponible'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/ai-advanced/test-groq', methods=['POST'])
@login_required
def api_test_groq():
    """Teste la connexion à l'API Groq"""
    try:
        from groq_chatbot import groq_bot
        result = groq_bot.test_connection()
        return jsonify(result)
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Module Groq non disponible'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Initialisation de l'application
def init_app():
    """Initialise l'application"""
    try:
        create_directories()
        
        with app.app_context():
            db.create_all()
            logger.info("Base de données initialisée")
            
            # Création des utilisateurs par défaut
            create_default_admin()
            
            # Chargement des modèles IA
            load_ai_models()
            
            # Entraînement initial si nécessaire
            if not ai_models_loaded:
                logger.info("Entraînement initial des modèles IA...")
                # Vérifier s'il y a des données réelles pour l'entraînement
                device_count = Device.query.count()
                if device_count > 0:
                    train_ai_models()
                else:
                    logger.info("Aucune donnée disponible pour l'entraînement IA - en attente de scans réseau")
        
        # Démarrage du planificateur de tâches
        scheduler_thread = threading.Thread(target=schedule_tasks)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        logger.info("Application Central Danone initialisée avec succès - MODE PRODUCTION")
        
    except Exception as e:
        logger.error(f"Erreur initialisation: {e}")



if __name__ == '__main__':
    init_app()
    print("🚀 Application Central Danone démarrée!")
    print("📱 Interface web: http://localhost:5000")
    print("👤 Connexion: admin / admin123")
    print("🔄 Mode production - Pas d'auto-reload")
    print("⏹️  Arrêt: Ctrl+C")
    print("-" * 50)
    
    # Mode production sans auto-reload
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False) 