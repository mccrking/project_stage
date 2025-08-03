"""
Dashboard Central Danone - Application principale avec IA intégrée
Système de supervision réseau intelligent
"""

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
from network_scanner import NetworkScanner
from report_generator import ReportGenerator
from ai_enhancement import ai_system, AIEnhancement
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'danone-central-2024-ai-enhanced'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_monitor.db'
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
    """Modèle d'équipement avec données IA"""
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

# Initialisation des modules
network_scanner = NetworkScanner()
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

# Configuration email simplifiée pour alertes automatiques
EMAIL_CONFIG = {
    'enabled': True,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'centraldanone.supervision@gmail.com',  # Email dédié Central Danone
    'password': 'supervision2024',  # Mot de passe simple
    'from_email': 'centraldanone.supervision@gmail.com',
    'to_email': 'mehdi.chmiti2000@gmail.com'  # Email de Mehdi
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
            logger.info("Email non configuré ou désactivé")
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
            logger.warning("Erreur d'authentification email - Utilisation du mode notification")
            # Fallback vers notifications en temps réel
            add_notification(f"⚠️ Alerte: {subject} - {message}", 'warning', priority)
            return False
            
        except Exception as e:
            logger.error(f"Erreur envoi email: {e}")
            # Fallback vers notifications en temps réel
            add_notification(f"⚠️ Alerte: {subject} - {message}", 'warning', priority)
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
        devices_found = network_scanner.scan_network(network_range)
        
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
        all_results = network_scanner.scan_all_networks()
        
        total_devices_found = 0
        
        # Traiter les résultats de chaque réseau
        for network_range, result in all_results.items():
            if 'error' in result:
                logger.warning(f"Erreur scan {network_range}: {result['error']}")
                continue
                
            devices_found = result['devices']
            total_devices_found += len(devices_found)
            
            logger.info(f"Réseau {network_range}: {len(devices_found)} équipements trouvés")
            
            # Mise à jour de la base de données pour ce réseau
            for device_info in devices_found:
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
        logger.info(f"Scan multi-réseaux terminé: {total_devices_found} équipements trouvés sur {len(all_results)} réseaux")
        
    except Exception as e:
        logger.error(f"Erreur lors du scan multi-réseaux: {e}")
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
        networks = network_scanner.discover_networks()
        return jsonify({
            'status': 'success',
            'networks': networks,
            'total_networks': len(networks)
        })
    except Exception as e:
        logger.error(f"Erreur découverte réseaux: {e}")
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
    """Page des rapports"""
    try:
        # Liste des rapports disponibles
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
        
        report_files.sort(key=lambda x: x['created'], reverse=True)
        
        return render_template('reports.html', reports=report_files)
    except Exception as e:
        logger.error(f"Erreur page rapports: {e}")
        return render_template('error.html', error=str(e))

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
    """API pour récupérer les paramètres"""
    try:
        from settings_manager import get_settings_manager
        from config import Config
        
        settings_manager = get_settings_manager()
        settings = settings_manager.get_all_settings()
        
        # Ajouter les paramètres de configuration système
        settings.update({
            'production_networks': Config.PRODUCTION_NETWORKS,
            'ai_training_interval': Config.AI_TRAINING_INTERVAL,
            'max_concurrent_scans': Config.MAX_CONCURRENT_SCANS
        })
        
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Erreur API settings: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings', methods=['POST'])
@login_required
def api_update_settings():
    """API pour mettre à jour les paramètres réseau"""
    try:
        from settings_manager import get_settings_manager
        
        data = request.get_json()
        settings_manager = get_settings_manager()
        
        # Mettre à jour les paramètres réseau
        network_settings = {
            'network_range': data.get('network_range'),
            'scan_interval': data.get('scan_interval'),
            'scan_timeout': data.get('scan_timeout'),
            'max_retries': data.get('max_retries'),
            'enable_auto_scan': data.get('enable_auto_scan')
        }
        
        success = settings_manager.update_settings(network_settings)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Paramètres réseau mis à jour'})
        else:
            return jsonify({'status': 'error', 'message': 'Erreur lors de la sauvegarde'})
    except Exception as e:
        logger.error(f"Erreur mise à jour settings: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings/networks', methods=['GET'])
@login_required
def api_get_networks():
    """API pour récupérer les réseaux configurés"""
    try:
        from config import Config
        networks = network_scanner.discover_networks()
        
        return jsonify({
            'status': 'success',
            'networks': networks,
            'production_networks': Config.PRODUCTION_NETWORKS,
            'default_network': Config.DEFAULT_NETWORK_RANGE
        })
    except Exception as e:
        logger.error(f"Erreur récupération réseaux: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings/save', methods=['POST'])
@login_required
def api_save_settings():
    """API pour sauvegarder les paramètres généraux"""
    try:
        from settings_manager import get_settings_manager
        
        data = request.get_json()
        settings_manager = get_settings_manager()
        
        # Déterminer le type de paramètres à sauvegarder
        if 'alert_threshold' in data:
            # Paramètres d'alertes
            alert_settings = {
                'alert_threshold': data.get('alert_threshold'),
                'alert_device_offline': data.get('alert_device_offline'),
                'alert_device_online': data.get('alert_device_online'),
                'alert_low_uptime': data.get('alert_low_uptime'),
                'alert_scan_failed': data.get('alert_scan_failed')
            }
            success = settings_manager.update_settings(alert_settings)
            message = 'Paramètres d\'alertes sauvegardés'
        elif 'auto_report' in data:
            # Paramètres de rapports
            report_settings = {
                'auto_report': data.get('auto_report'),
                'report_format': data.get('report_format'),
                'report_time': data.get('report_time'),
                'report_retention': data.get('report_retention'),
                'include_charts': data.get('include_charts'),
                'include_alerts': data.get('include_alerts')
            }
            success = settings_manager.update_settings(report_settings)
            message = 'Paramètres de rapports sauvegardés'
        else:
            # Paramètres généraux
            success = settings_manager.update_settings(data)
            message = 'Paramètres sauvegardés'
        
        if success:
            return jsonify({
                'status': 'success',
                'message': message
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de la sauvegarde'
            })
    except Exception as e:
        logger.error(f"Erreur sauvegarde paramètres: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings/test-network', methods=['POST'])
@login_required
def api_test_network():
    """API pour tester une plage réseau"""
    try:
        data = request.get_json()
        network_range = data.get('network_range', '192.168.1.0/24')
        
        # Test rapide du réseau
        devices_found = network_scanner.scan_network(network_range)
        
        return jsonify({
            'status': 'success',
            'network_range': network_range,
            'devices_found': len(devices_found),
            'devices': devices_found[:5]  # Limiter à 5 pour l'aperçu
        })
    except Exception as e:
        logger.error(f"Erreur test réseau: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/reports/generate', methods=['POST'])
@login_required
def api_generate_report():
    """API pour générer un rapport"""
    try:
        from report_generator import ReportGenerator
        
        data = request.get_json()
        report_type = data.get('type', 'daily')
        report_format = data.get('format', 'pdf')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        description = data.get('description', '')
        
        # Générer le rapport selon le type
        if report_type == 'ai':
            report_path = generate_ai_report()
        else:
            # Utiliser le générateur de rapports standard
            report_gen = ReportGenerator()
            report_path = report_gen.generate_report(
                report_type=report_type,
                format=report_format,
                date_from=date_from,
                date_to=date_to,
                description=description
            )
        
        if report_path:
            filename = os.path.basename(report_path)
            return jsonify({
                'success': True, 
                'message': f'Rapport {report_type} généré avec succès',
                'filename': filename,
                'report_path': report_path
            })
        else:
            return jsonify({'success': False, 'message': 'Erreur lors de la génération du rapport'})
            
    except Exception as e:
        logger.error(f"Erreur génération rapport: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/reports/download/<filename>')
@login_required
def api_download_report(filename):
    """API pour télécharger un rapport"""
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
    """API pour récupérer la configuration email"""
    try:
        from settings_manager import get_settings_manager
        
        settings_manager = get_settings_manager()
        email_settings = settings_manager.get_email_settings()
        
        return jsonify(email_settings)
    except Exception as e:
        logger.error(f"Erreur récupération config email: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/settings/email', methods=['POST'])
@login_required
def api_save_email_settings():
    """API pour sauvegarder la configuration email"""
    try:
        data = request.get_json()
        
        # Mise à jour de la configuration
        EMAIL_CONFIG['enabled'] = data.get('enabled', False)
        EMAIL_CONFIG['smtp_server'] = data.get('smtp_server', 'smtp.gmail.com')
        EMAIL_CONFIG['smtp_port'] = data.get('smtp_port', 587)
        EMAIL_CONFIG['username'] = data.get('username', '')
        EMAIL_CONFIG['password'] = data.get('password', '')
        EMAIL_CONFIG['from_email'] = data.get('from_email', '')
        EMAIL_CONFIG['to_email'] = data.get('to_email', '')
        
        logger.info(f"Configuration email mise à jour: {EMAIL_CONFIG['to_email']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Configuration email sauvegardée'
        })
    except Exception as e:
        logger.error(f"Erreur sauvegarde config email: {e}")
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
            
            # Entraînement initial si nécessaire (seulement si pas de données de démonstration)
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
    print("🔄 Mode debug activé - Auto-reload à chaque modification")
    print("⏹️  Arrêt: Ctrl+C")
    print("-" * 50)
    
    # Mode debug avec auto-reload
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True) 