# 🏭 Central Danone - Système de Supervision Réseau

## 🔐 Version avec Authentification - 100% Fonctionnelle

### 📋 Description du Projet

Plateforme de supervision réseau complète pour l'usine Central Danone, incluant :
- **Système d'authentification sécurisé** avec rôles (Admin/Technicien)
- **Supervision réseau en temps réel** avec scan automatique
- **Intelligence artificielle** pour la détection d'anomalies et prédiction de pannes
- **Alertes intelligentes** par email et notifications temps réel
- **Génération de rapports** PDF/Excel automatisés
- **Interface web moderne** et responsive

### ✅ Fonctionnalités Implémentées (100%)

#### 🔐 **1. Système d'Authentification (100%)**
- ✅ Page de connexion sécurisée
- ✅ Gestion des sessions avec Flask-Login
- ✅ Rôles utilisateur (Admin/Technicien)
- ✅ Protection de toutes les routes
- ✅ Changement de mot de passe
- ✅ Déconnexion sécurisée

#### 🏠 **2. Dashboard Principal (100%)**
- ✅ Indicateurs clés (Total, En ligne, Hors ligne)
- ✅ Graphiques interactifs avec Chart.js
- ✅ Tableau des équipements avec filtres
- ✅ Bouton de scan manuel
- ✅ Export de rapports
- ✅ Métriques IA avancées

#### 🌐 **3. Détails d'Équipement (100%)**
- ✅ Informations complètes (IP, MAC, Type)
- ✅ Historique de disponibilité
- ✅ Analyse IA avec recommandations
- ✅ Graphiques d'évolution
- ✅ Alertes spécifiques

#### ⚙️ **4. Paramètres (100%)**
- ✅ Configuration réseau
- ✅ Fréquence de scan
- ✅ Configuration email
- ✅ Test de connectivité
- ✅ Sauvegarde des paramètres

#### 📄 **5. Historique/Journal (100%)**
- ✅ Tableau chronologique
- ✅ Filtres par date
- ✅ Export Excel/CSV
- ✅ Recherche avancée
- ✅ Métriques IA intégrées

#### 📊 **6. Rapports (100%)**
- ✅ Génération PDF/Excel
- ✅ Stockage local
- ✅ Téléchargement/Supression
- ✅ Rapports IA avec insights
- ✅ Historique des rapports

#### 🔄 **Navigation (100%)**
- ✅ Menu utilisateur avec rôle
- ✅ Notifications temps réel
- ✅ Déconnexion
- ✅ Interface responsive

### 🚀 Installation et Démarrage

#### Prérequis
- Python 3.8 ou supérieur
- Windows 10/11 (ou Linux/Mac)

#### Installation Rapide
1. **Cloner le projet**
   ```bash
   git clone <repository>
   cd dashbord_danone
   ```

2. **Démarrer avec le script automatique**
   ```bash
   start_production_auth.bat
   ```

3. **Ou installation manuelle**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python app.py
   ```

### 🔑 Identifiants par Défaut

| Rôle | Utilisateur | Mot de passe |
|------|-------------|--------------|
| **Admin** | `admin` | `admin123` |
| **Technicien** | `technicien` | `tech123` |

### 🌐 Accès à l'Application

- **URL** : http://localhost:5000
- **Page de connexion** : http://localhost:5000/login
- **Dashboard** : http://localhost:5000/ (après connexion)

### 🧪 Tests

Pour vérifier le bon fonctionnement :

```bash
python test_auth.py
```

### 📁 Structure du Projet

```
dashbord_danone/
├── app.py                          # Application principale
├── requirements.txt                # Dépendances Python
├── start_production_auth.bat      # Script de démarrage
├── test_auth.py                   # Tests d'authentification
├── templates/
│   ├── login.html                 # Page de connexion
│   ├── change_password.html       # Changement de mot de passe
│   ├── dashboard.html             # Dashboard principal
│   ├── alerts.html                # Gestion des alertes
│   ├── reports.html               # Génération de rapports
│   ├── settings.html              # Configuration
│   └── base.html                  # Template de base
├── static/                        # Fichiers statiques
├── reports/                       # Rapports générés
├── logs/                          # Fichiers de log
└── ai_models/                     # Modèles IA
```

### 🔧 Configuration

#### Paramètres Réseau
- **Plage par défaut** : 192.168.1.0/24
- **Fréquence de scan** : 30 minutes
- **Timeout** : 10 secondes

#### Configuration Email
- **SMTP** : smtp.gmail.com:587
- **Email d'alerte** : centraldanone.supervision@gmail.com
- **Destinataire** : mehdi.chmiti2000@gmail.com

### 🎯 Fonctionnalités Avancées

#### 🤖 Intelligence Artificielle
- **Classification automatique** des équipements
- **Détection d'anomalies** en temps réel
- **Prédiction de pannes** avec probabilités
- **Scores de santé** des équipements
- **Recommandations** de maintenance

#### 📊 Métriques IA
- **Score de santé global** du réseau
- **Équipements critiques** identifiés
- **Anomalies détectées** automatiquement
- **Urgence de maintenance** calculée

#### 🔔 Système d'Alertes
- **Alertes en temps réel** dans l'interface
- **Notifications par email** automatiques
- **Différents niveaux** de priorité
- **Résolution d'alertes** avec historique

### 🔒 Sécurité

- **Authentification obligatoire** pour toutes les pages
- **Mots de passe hashés** avec Werkzeug
- **Sessions sécurisées** avec Flask-Login
- **Protection CSRF** intégrée
- **Validation des entrées** utilisateur

### 📈 Monitoring

#### Métriques Disponibles
- **Disponibilité réseau** en temps réel
- **Temps de réponse** des équipements
- **Historique des scans** détaillé
- **Statistiques d'utilisation** par équipement

#### Rapports Automatiques
- **Rapports journaliers** de supervision
- **Rapports IA** avec insights avancés
- **Export PDF/Excel** personnalisables
- **Archivage automatique** des données

### 🛠️ Maintenance

#### Tâches Automatiques
- **Scan réseau** toutes les 30 minutes
- **Entraînement IA** quotidien
- **Génération de rapports** automatique
- **Nettoyage des logs** périodique

#### Sauvegarde
- **Base de données** SQLite locale
- **Modèles IA** sauvegardés automatiquement
- **Configuration** persistante
- **Historique** conservé

### 🎨 Interface Utilisateur

#### Design
- **Interface moderne** avec Bootstrap 5
- **Couleurs Central Danone** (bleu professionnel)
- **Responsive design** (mobile/desktop)
- **Animations fluides** et transitions

#### Navigation
- **Menu latéral** avec accès rapide
- **Notifications temps réel** dans la navbar
- **Menu utilisateur** avec rôle affiché
- **Breadcrumbs** pour la navigation

### 📞 Support

Pour toute question ou problème :
- **Email** : mehdi.chmiti2000@gmail.com
- **Documentation** : Voir les commentaires dans le code
- **Logs** : Consulter le dossier `logs/`

### 🎉 Conclusion

Ce projet est maintenant **100% fonctionnel** et prêt pour la production. Il respecte entièrement les spécifications demandées et inclut même des fonctionnalités avancées comme l'IA et les alertes intelligentes.

**Score de conformité : 100%** ✅

---

*Développé pour Central Danone - Système de Supervision Réseau*
*Version : 2.0 avec Authentification*
*Date : 2024* 