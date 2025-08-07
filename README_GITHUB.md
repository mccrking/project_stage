# 🏢 Central Danone - Plateforme de Supervision Réseau

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 **Vue d'ensemble**

Plateforme complète de supervision et monitoring réseau développée pour **Central Danone**. Solution professionnelle intégrant scanner réseau intelligent, intelligence artificielle pour l'analyse prédictive, et interface web moderne avec thèmes adaptatifs.

## ✨ **Fonctionnalités Principales**

### 🔍 **Scanner Réseau Universel**
- **Détection automatique** : OPPO phones, Samsung TV, équipements réseau
- **Multi-réseaux** : 192.168.32.0/24, 192.168.121.0/24, 192.168.0.0/24
- **Scan en temps réel** : Monitoring continu des dispositifs
- **Base de données** : Historique complet des équipements

### 🤖 **Intelligence Artificielle Intégrée**
- **Analyse prédictive** : Détection d'anomalies réseau
- **Classification automatique** : Catégorisation des équipements
- **Maintenance prédictive** : Alertes et recommandations
- **Chatbot IA** : Assistant Groq/DeepSeek intégré

### 🎨 **Interface Moderne**
- **Thèmes adaptatifs** : Mode clair/sombre avec transition fluide
- **Dashboard temps réel** : Visualisation des données réseau
- **Responsive design** : Compatible mobile/desktop
- **Notifications email** : Alertes automatiques configurables

## 🚀 **Installation & Démarrage**

### **Prérequis**
```bash
Python 3.8+
nmap
pip install -r requirements.txt
```

### **Installation**
```bash
git clone https://github.com/mccrking/project_stage.git
cd project_stage
pip install -r requirements.txt
```

### **Configuration**
```bash
# Configuration production
python init_production.py

# Démarrage serveur
python start_production_real.py
```

### **Démarrage rapide**
```bash
# Mode développement
start_dev.bat

# Mode production
start_production.bat

# Avec IA Groq
start_with_groq.bat
```

## 📁 **Structure du Projet**

```
dashbord_danone/
├── app.py                          # Application Flask principale
├── network_scanner_production.py   # Scanner réseau production
├── config_groq.py                 # Configuration IA Groq
├── templates/                      # Templates HTML
│   ├── base.html                   # Template de base avec thèmes
│   ├── dashboard.html              # Dashboard principal
│   └── ai_dashboard.html           # Interface IA
├── static/                         # Assets statiques
│   ├── css/theme.css              # Système de thèmes
│   └── js/theme.js                # Gestion thèmes JS
├── archives_dev/                   # Archives développement
└── docs/                          # Documentation complète
```

## 🔧 **Configuration**

### **Variables d'environnement**
```bash
# Base de données
DATABASE_URL=sqlite:///network_monitor.db

# IA Groq (optionnel)
GROQ_API_KEY=your_groq_api_key

# Email (optionnel)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## 📊 **Fonctionnalités Avancées**

### **Scanner Réseau**
- **Détection spécialisée** pour équipements Danone
- **Scan par plages** : Configuration multi-réseaux
- **Historique** : Suivi temporel des équipements
- **Export** : Rapports PDF/Excel

### **IA & Analytics**
- **Machine Learning** : Patterns de comportement réseau
- **Prédictions** : Maintenance prédictive
- **Alertes intelligentes** : Anomalies automatiques
- **Chatbot** : Assistant IA conversationnel

## 👥 **Équipe de Développement**

**Réalisé par :**
- **Mehdi Chmiti** - Développeur Principal
- **Ismail Haddaoui** - Développeur Full-Stack

## 📄 **Licence**

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 **Support**

Pour toute question ou support technique :
- 📧 Email : support@danone-network.com
- 📋 Issues : [GitHub Issues](https://github.com/mccrking/project_stage/issues)

---

### 🏆 **Plateforme Production Ready - Central Danone 2024**
