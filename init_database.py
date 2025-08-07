#!/usr/bin/env python3
"""
Script d'initialisation sécurisée de la base de données
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

print("🔧 Initialisation sécurisée de la base de données...")

# Configuration sécurisée
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key-for-init')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db = SQLAlchemy(app)

# Fonction pour obtenir l'heure locale
def get_local_time():
    return datetime.now()

# Modèles de base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_local_time)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    hostname = db.Column(db.String(100))
    device_type = db.Column(db.String(50), default='unknown')
    status = db.Column(db.String(20), default='unknown')
    last_seen = db.Column(db.DateTime, default=get_local_time)
    response_time = db.Column(db.Float, default=0.0)
    scan_duration = db.Column(db.Float, default=0.0)
    error_count = db.Column(db.Integer, default=0)

class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network_range = db.Column(db.String(20), nullable=False)
    devices_found = db.Column(db.Integer, default=0)
    scan_duration = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=get_local_time)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_local_time)
    resolved_at = db.Column(db.DateTime, nullable=True)

try:
    with app.app_context():
        # Supprimer les anciennes tables
        db.drop_all()
        print("🗑️ Anciennes tables supprimées")
        
        # Créer toutes les tables
        db.create_all()
        print("✅ Tables créées avec succès")
        
        # Créer un utilisateur admin par défaut
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            
            # Créer un utilisateur standard
            user = User(
                username='user',
                password_hash=generate_password_hash('user123'),
                is_admin=False
            )
            db.session.add(user)
            
            db.session.commit()
            print("✅ Utilisateurs par défaut créés:")
            print("   - Admin: admin / admin123")
            print("   - User:  user / user123")
        
        # Ajouter quelques données de démonstration
        demo_devices = [
            Device(ip_address='192.168.1.1', hostname='router-principal', device_type='router', status='online'),
            Device(ip_address='192.168.1.100', hostname='server-web', device_type='server', status='online'),
            Device(ip_address='192.168.1.200', hostname='imprimante-bureau', device_type='printer', status='offline'),
        ]
        
        for device in demo_devices:
            existing = Device.query.filter_by(ip_address=device.ip_address).first()
            if not existing:
                db.session.add(device)
        
        db.session.commit()
        print("✅ Données de démonstration ajoutées")
        
        print("🔐 Base de données initialisée avec succès!")
        print("🚀 Vous pouvez maintenant démarrer l'application")
        
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
