# 🏭 Dashboard - Plateforme de Supervision Réseau

## 📋 Description

Plateforme de supervision réseau développée pour industrie, permettant la surveillance en temps réel des équipements réseau dans un environnement industriel. Cette application offre une interface web moderne et intuitive pour les techniciens et administrateurs réseau.

## ✨ Fonctionnalités Principales

### 🔐 Authentification Sécurisée
- Système de connexion avec gestion des rôles
- Protection des routes avec Flask-Login
- Gestion des sessions sécurisées

### 📊 Dashboard en Temps Réel
- Affichage en temps réel de l'état du réseau
- Statistiques dynamiques (équipements en ligne/hors ligne)
- Tableau interactif des équipements avec filtres
- Actions rapides (info, ping, scan)

### 🤖 Intelligence Artificielle
- Analyse prédictive des équipements
- Détection d'anomalies automatique
- Recommandations intelligentes
- Scores de santé des équipements

### ⚠️ Système d'Alertes
- Alertes en temps réel
- Notifications par email
- Gestion des alertes (résolution, historique)
- Seuils configurables

### 📄 Génération de Rapports
- Rapports PDF et Excel automatisés
- Historique des rapports
- Export de données
- Rapports personnalisables

### ⚙️ Paramètres Configurables
- Configuration du réseau à scanner
- Paramètres d'alertes
- Configuration email
- Persistance des paramètres

## 🛠️ Technologies Utilisées

### Backend
- **Flask** - Framework web Python
- **Flask-Login** - Gestion de l'authentification
- **SQLAlchemy** - ORM pour la base de données
- **Python-nmap** - Scanner réseau
- **Scikit-learn** - Intelligence artificielle
- **Schedule** - Planification des tâches

### Frontend
- **Bootstrap 5** - Framework CSS responsive
- **Chart.js** - Visualisation de données
- **JavaScript** - Interactivité côté client
- **AJAX** - Requêtes asynchrones

### Base de Données
- **SQLite** - Base de données légère

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- pip
- Accès réseau pour les scans

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/mccrking/project_stage.git
cd project_stage
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configuration initiale**
```bash
# Copier le fichier de configuration
cp config.example.py config.py

# Éditer config.py avec vos paramètres
```

6. **Lancer l'application**
```bash
python app.py
```

### Accès par défaut
- **URL** : http://localhost:5000
- **Utilisateur** : admin
- **Mot de passe** : admin123


## 🔧 Configuration

### Paramètres Réseau
- **Sous-réseau** : Définir la plage IP à scanner
- **Fréquence de scan** : Intervalle entre les scans
- **Ports** : Ports spécifiques à surveiller

### Paramètres Email
- **SMTP Server** : Serveur SMTP pour les alertes
- **Email d'alerte** : Adresse de destination
- **Authentification** : Identifiants SMTP

### Paramètres IA
- **Seuils de risque** : Configuration des alertes IA
- **Modèles** : Sauvegarde et chargement des modèles

## 📊 Utilisation

### Dashboard Principal
1. Se connecter avec vos identifiants
2. Visualiser l'état global du réseau
3. Utiliser les filtres pour rechercher des équipements
4. Cliquer sur "Info" pour les détails d'un équipement

### Intelligence Artificielle
1. Accéder à la page "IA Dashboard"
2. Visualiser les analyses prédictives
3. Consulter les recommandations
4. Entraîner de nouveaux modèles

### Gestion des Alertes
1. Consulter les alertes actives
2. Résoudre les incidents
3. Configurer les seuils d'alerte

### Rapports
1. Générer des rapports automatiques
2. Télécharger les rapports existants
3. Configurer les formats d'export

## 🔒 Sécurité

- Authentification obligatoire pour toutes les pages
- Protection CSRF sur les formulaires
- Validation des entrées utilisateur
- Logs de sécurité
- Sessions sécurisées

## 📈 Monitoring et Maintenance

### Logs
- Logs d'application dans `logs/`
- Logs de sécurité
- Logs de performance

### Sauvegarde
- Base de données sauvegardée automatiquement
- Rapports conservés dans `reports/`
- Modèles IA sauvegardés dans `ai_models/`


## 👥 Auteurs
- **Supervision** - Équipe IT 

---

**Version** : 1.0.0  
**Dernière mise à jour** : ******
**Statut** : Production Ready ✅ 
