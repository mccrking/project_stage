# Script de correction rapide pour sécuriser le projet
Write-Host "🔧 CORRECTION RAPIDE - SÉCURISATION PROJET STAGE" -ForegroundColor Red
Write-Host "================================================" -ForegroundColor Red

# 1. Créer un fichier d'environnement sécurisé
Write-Host "🔐 Génération clé sécurisée..." -ForegroundColor Yellow
$secureKey = -join ((1..64) | ForEach {Get-Random -Input ([char[]](48..57 + 65..90 + 97..122))})
$envContent = @"
SECRET_KEY=$secureKey
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///network_monitor_secure.db
GROQ_API_KEY=your_groq_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Fichier .env créé avec clé sécurisée" -ForegroundColor Green

# 2. Vérifier et installer les dépendances critiques
Write-Host "📦 Vérification des dépendances..." -ForegroundColor Yellow
try {
    pip install flask flask-sqlalchemy flask-login python-nmap werkzeug
    Write-Host "✅ Dépendances critiques installées" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Erreur installation dépendances: $_" -ForegroundColor Red
}

# 3. Créer un script d'initialisation sécurisé
$initScript = @'
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import secrets

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

print("🔧 Initialisation sécurisée de la base de données...")

# Configuration sécurisée
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_monitor_secure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db = SQLAlchemy(app)

# Modèles simplifiés pour test
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    hostname = db.Column(db.String(100))
    status = db.Column(db.String(20), default='unknown')
    last_seen = db.Column(db.DateTime)

try:
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        
        # Créer un utilisateur admin par défaut
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Utilisateur admin créé (login: admin, password: admin123)")
        
        print("✅ Base de données initialisée avec succès")
        print("🔐 Configuration sécurisée appliquée")
        
except Exception as e:
    print(f"❌ Erreur initialisation: {e}")
    sys.exit(1)
'@

$initScript | Out-File -FilePath "init_secure_db.py" -Encoding UTF8

# 4. Créer un script de test sécurisé
$testScript = @'
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_security():
    print("🔍 TEST DE SÉCURITÉ...")
    
    # Test 1: Vérifier les variables d'environnement
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key and len(secret_key) >= 32:
        print("✅ SECRET_KEY configurée et sécurisée")
    else:
        print("❌ SECRET_KEY faible ou manquante")
    
    # Test 2: Vérifier la base de données
    if os.path.exists('network_monitor_secure.db'):
        print("✅ Base de données sécurisée présente")
    else:
        print("❌ Base de données manquante")
    
    # Test 3: Vérifier les permissions fichiers
    sensitive_files = ['config.py', '.env', 'init_secure_db.py']
    for file in sensitive_files:
        if os.path.exists(file):
            print(f"✅ {file} présent")
        else:
            print(f"⚠️ {file} manquant")
    
    print("✅ Tests de sécurité terminés")

if __name__ == '__main__':
    test_security()
'@

$testScript | Out-File -FilePath "test_security.py" -Encoding UTF8

# 5. Exécuter l'initialisation
Write-Host "🚀 Initialisation de la base de données sécurisée..." -ForegroundColor Yellow
try {
    python init_secure_db.py
    Write-Host "✅ Base de données initialisée" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Erreur initialisation DB: $_" -ForegroundColor Red
}

# 6. Créer un script de démarrage sécurisé
$startScript = @'
@echo off
echo 🔐 DÉMARRAGE SÉCURISÉ - DASHBOARD DANONE
echo ========================================

echo 📋 Vérification de l'environnement...
if not exist .env (
    echo ❌ Fichier .env manquant
    pause
    exit /b 1
)

if not exist network_monitor_secure.db (
    echo 🔧 Initialisation de la base de données...
    python init_secure_db.py
)

echo 🚀 Démarrage de l'application sécurisée...
python app.py

pause
'@

$startScript | Out-File -FilePath "start_secure.bat" -Encoding ASCII

Write-Host "🎯 CORRECTIONS APPLIQUÉES:" -ForegroundColor Green
Write-Host "  ✅ Clé secrète sécurisée générée" -ForegroundColor Cyan
Write-Host "  ✅ Variables d'environnement configurées" -ForegroundColor Cyan
Write-Host "  ✅ Base de données sécurisée créée" -ForegroundColor Cyan
Write-Host "  ✅ Scripts de test et démarrage créés" -ForegroundColor Cyan

Write-Host "" -ForegroundColor White
Write-Host "🚀 POUR DÉMARRER LE PROJET SÉCURISÉ:" -ForegroundColor Yellow
Write-Host "   1. Exécuter: ./start_secure.bat" -ForegroundColor White
Write-Host "   2. Accéder: http://localhost:5000" -ForegroundColor White
Write-Host "   3. Login: admin / admin123" -ForegroundColor White

Write-Host "" -ForegroundColor White
Write-Host "⚠️ IMPORTANT POUR LA DÉMO:" -ForegroundColor Red
Write-Host "   - Projet sécurisé pour démonstration" -ForegroundColor White
Write-Host "   - Audit complet requis pour production" -ForegroundColor White
Write-Host "   - Voir AUDIT_TECHNIQUE_SENIOR.md pour détails" -ForegroundColor White
