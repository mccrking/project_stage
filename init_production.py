#!/usr/bin/env python3
"""
Script d'initialisation pour plateforme de production
Base de données avec support des détections avancées
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

print("🚀 INITIALISATION PLATEFORME PRODUCTION")
print("=" * 50)

# Configuration sécurisée
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key-for-init')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_monitor_production.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db = SQLAlchemy(app)

def get_local_time():
    return datetime.now()

# Modèles complets pour production
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='technician')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=get_local_time)

class Device(db.Model):
    """Modèle d'équipement production avec détection avancée"""
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    mac = db.Column(db.String(17), nullable=True)
    hostname = db.Column(db.String(100), nullable=True)
    mac_vendor = db.Column(db.String(100), nullable=True)
    is_online = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=get_local_time)
    device_type = db.Column(db.String(50), default='unknown')
    ai_confidence = db.Column(db.Float, default=0.0)
    health_score = db.Column(db.Float, default=100.0)
    failure_probability = db.Column(db.Float, default=0.0)
    anomaly_score = db.Column(db.Float, default=0.0)
    maintenance_urgency = db.Column(db.String(20), default='low')
    ai_recommendations = db.Column(db.Text, default='[]')
    
    # Colonnes production avancées
    response_time = db.Column(db.Float, default=0.0)
    system_info = db.Column(db.String(100), nullable=True)
    open_ports = db.Column(db.Text, default='[]')
    services = db.Column(db.Text, default='[]')
    
    created_at = db.Column(db.DateTime, default=get_local_time)
    updated_at = db.Column(db.DateTime, default=get_local_time, onupdate=get_local_time)

class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    is_online = db.Column(db.Boolean, nullable=False)
    response_time = db.Column(db.Float, default=0.0)
    packet_loss = db.Column(db.Float, default=0.0)
    scan_duration = db.Column(db.Float, default=0.0)
    error_count = db.Column(db.Integer, default=0)
    ai_analysis = db.Column(db.Text, default='{}')
    timestamp = db.Column(db.DateTime, default=get_local_time)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')
    ai_confidence = db.Column(db.Float, default=0.0)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_local_time)
    resolved_at = db.Column(db.DateTime, nullable=True)

class AIModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)
    accuracy = db.Column(db.Float, default=0.0)
    training_date = db.Column(db.DateTime, default=get_local_time)
    model_path = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

try:
    with app.app_context():
        # Supprimer et recréer toutes les tables
        print("🗑️ Suppression des anciennes tables...")
        db.drop_all()
        
        print("🔧 Création des nouvelles tables...")
        db.create_all()
        print("✅ Tables créées avec succès")
        
        # Créer utilisateurs par défaut
        print("👥 Création des utilisateurs...")
        
        # Administrateur
        admin = User(
            username='admin',
            email='admin@danone.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        
        # Technicien
        tech = User(
            username='technicien',
            email='tech@danone.com',
            password_hash=generate_password_hash('tech123'),
            role='technician'
        )
        db.session.add(tech)
        
        # Utilisateur de démonstration
        demo = User(
            username='demo',
            email='demo@danone.com',
            password_hash=generate_password_hash('demo123'),
            role='technician'
        )
        db.session.add(demo)
        
        db.session.commit()
        
        print("✅ Utilisateurs créés:")
        print("   - admin@danone.com / admin123 (Administrateur)")
        print("   - tech@danone.com / tech123 (Technicien)")
        print("   - demo@danone.com / demo123 (Démonstration)")
        
        # Créer répertoires nécessaires
        print("📁 Création des répertoires...")
        directories = ['reports', 'logs', 'ai_models', 'static/uploads']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"   ✅ {directory}/")
        
        print("\n🎯 PLATEFORME PRODUCTION INITIALISÉE")
        print("=" * 50)
        print("✅ Base de données: network_monitor_production.db")
        print("✅ Tables: 6 tables créées")
        print("✅ Utilisateurs: 3 comptes actifs")
        print("✅ Répertoires: Créés et prêts")
        
        print("\n🚀 POUR DÉMARRER:")
        print("1. python app.py")
        print("2. Accéder: http://localhost:5000")
        print("3. Login avec un des comptes ci-dessus")
        
        print("\n🔍 FONCTIONNALITÉS PRODUCTION:")
        print("✅ Détection automatique des réseaux")
        print("✅ Scan avancé avec Nmap")
        print("✅ Identification des équipements (type, OS, ports)")
        print("✅ Analyse temps réel")
        print("✅ Intelligence artificielle intégrée")
        print("✅ Alertes et notifications")
        print("✅ Génération de rapports")
        
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
