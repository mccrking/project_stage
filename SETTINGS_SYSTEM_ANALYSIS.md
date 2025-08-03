# Analyse Technique - Page Paramètres

## Vue d'ensemble technique

La page **Paramètres** est l'interface centrale de configuration de la plateforme de supervision réseau Central Danone. Elle offre une gestion complète de tous les aspects du système via une interface web intuitive et des APIs REST robustes.

## Architecture backend

### Modèles de données

#### Configuration réseau
```python
# Paramètres stockés dans config.py
DEFAULT_NETWORK_RANGE = "192.168.1.0/24"
SCAN_INTERVAL = 300  # secondes
SCAN_TIMEOUT = 30    # secondes
MAX_CONCURRENT_SCANS = 3
PRODUCTION_NETWORKS = [
    '192.168.1.0/24',    # Réseau principal usine
    '192.168.2.0/24',    # Réseau production
    '192.168.10.0/24',   # Réseau administration
    '192.168.20.0/24',   # Réseau PLC/automation
    '192.168.30.0/24',   # Réseau sécurité
    '10.0.0.0/24',       # Réseau étendu
    '172.16.0.0/24',     # Réseau backup
]
```

#### Configuration email
```python
# Configuration SMTP stockée en mémoire
EMAIL_CONFIG = {
    'enabled': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': '',
    'password': '',
    'from_email': '',
    'to_email': ''
}
```

### Routes API disponibles

#### 1. Gestion des paramètres généraux
```python
@app.route('/api/settings')
@login_required
def api_settings():
    """Récupération des paramètres actuels"""
    
@app.route('/api/settings', methods=['POST'])
@login_required
def api_update_settings():
    """Mise à jour des paramètres réseau"""
    
@app.route('/api/settings/save', methods=['POST'])
@login_required
def api_save_settings():
    """Sauvegarde générale des paramètres"""
```

#### 2. Gestion des réseaux
```python
@app.route('/api/settings/networks', methods=['GET'])
@login_required
def api_get_networks():
    """Récupération des réseaux configurés"""
    
@app.route('/api/settings/test-network', methods=['POST'])
@login_required
def api_test_network():
    """Test de connectivité réseau"""
```

#### 3. Configuration email
```python
@app.route('/api/settings/email', methods=['GET'])
@login_required
def api_get_email_settings():
    """Récupération de la config email"""
    
@app.route('/api/settings/email', methods=['POST'])
@login_required
def api_save_email_settings():
    """Sauvegarde de la config email"""
    
@app.route('/api/settings/email/test', methods=['POST'])
@login_required
def api_test_email():
    """Test de la configuration email"""
    
@app.route('/api/settings/email/alert', methods=['POST'])
@login_required
def api_send_test_alert():
    """Envoi d'alerte de test"""
    
@app.route('/api/settings/alert-email', methods=['POST'])
@login_required
def api_save_alert_email():
    """Sauvegarde email d'alerte simple"""
```

### Fonctionnalités implémentées

#### 1. Configuration réseau
- **Plage réseau** : Support du format CIDR
- **Intervalle de scan** : 15 min à 8h configurable
- **Timeout** : 1-60 secondes par appareil
- **Tentatives** : 1-5 tentatives en cas d'échec
- **Scan automatique** : Activation/désactivation
- **Test réseau** : Validation de connectivité

#### 2. Configuration des alertes
- **Seuil d'alerte** : 0-100% configurable
- **Types d'alertes** : 4 types configurables
- **Email simple** : Configuration rapide
- **Test d'alertes** : Génération d'alertes de test

#### 3. Configuration des rapports
- **Types** : Aucun, Journalier, Hebdomadaire, Mensuel
- **Formats** : PDF et Excel
- **Heure** : Configuration de l'heure de génération
- **Rétention** : 1-365 jours
- **Options** : Graphiques et alertes inclus

#### 4. Configuration email SMTP
- **Serveurs** : Support Gmail, Outlook, serveurs personnalisés
- **Ports** : 587 (TLS) et 465 (SSL)
- **Authentification** : Utilisateur/mot de passe
- **Test** : Validation de configuration
- **Alertes** : Envoi d'alertes de test

#### 5. Actions système
- **Sauvegarde** : Base de données
- **Cache** : Nettoyage du cache
- **Réinitialisation** : Paramètres par défaut
- **Informations** : Version et statut

## Interface utilisateur

### Structure HTML

#### 1. Configuration réseau
```html
<!-- Formulaire de configuration réseau -->
<form id="network-settings-form">
    <input type="text" id="network-range" value="192.168.1.0/24">
    <select id="scan-interval">
        <option value="15">15 minutes</option>
        <option value="30">30 minutes</option>
        <option value="60" selected>1 heure</option>
        <!-- ... autres options -->
    </select>
    <input type="number" id="scan-timeout" value="10">
    <input type="number" id="max-retries" value="2">
    <input type="checkbox" id="enable-auto-scan" checked>
    <button type="submit">Sauvegarder</button>
</form>

<!-- Informations réseau -->
<div class="card">
    <h6>Plage actuelle</h6>
    <p><strong>Réseau:</strong> <span id="current-network">192.168.1.0/24</span></p>
    <p><strong>Masque:</strong> <span id="current-mask">255.255.255.0</span></p>
    <p><strong>Adresses:</strong> <span id="current-addresses">254</span></p>
    
    <h6>Statut du scan</h6>
    <span class="badge bg-success" id="scan-status">Actif</span>
    <small>Prochain scan dans <span id="next-scan">45 min</span></small>
    
    <h6>Performance</h6>
    <p><strong>Durée moyenne:</strong> <span id="avg-duration">2.3s</span></p>
    <p><strong>Dernier scan:</strong> <span id="last-scan-time">Il y a 15 min</span></p>
</div>
```

#### 2. Configuration des alertes
```html
<!-- Formulaire de configuration des alertes -->
<form id="alert-settings-form">
    <input type="number" id="alert-threshold" value="85">
    <input type="email" id="alert-email" placeholder="email@example.com">
    
    <div class="form-check">
        <input type="checkbox" id="alert-device-offline" checked>
        <label>Appareil hors ligne</label>
    </div>
    <div class="form-check">
        <input type="checkbox" id="alert-device-online" checked>
        <label>Appareil de retour en ligne</label>
    </div>
    <div class="form-check">
        <input type="checkbox" id="alert-low-uptime" checked>
        <label>Disponibilité faible</label>
    </div>
    <div class="form-check">
        <input type="checkbox" id="alert-scan-failed">
        <label>Échec de scan</label>
    </div>
    
    <button type="submit">Sauvegarder</button>
</form>

<!-- Test des alertes -->
<div class="card">
    <button id="btn-test-alert">Tester une alerte</button>
    <button id="btn-test-email">Tester l'email simple</button>
    
    <div class="alert alert-info">
        <h6>Dernières alertes</h6>
        <small>
            <div>• Appareil 192.168.1.100 hors ligne (il y a 2h)</div>
            <div>• Disponibilité à 87% (il y a 1h)</div>
            <div>• Appareil 192.168.1.50 de retour (il y a 30min)</div>
        </small>
    </div>
</div>
```

#### 3. Configuration des rapports
```html
<!-- Formulaire de configuration des rapports -->
<form id="report-settings-form">
    <select id="auto-report">
        <option value="none">Aucun</option>
        <option value="daily" selected>Journalier</option>
        <option value="weekly">Hebdomadaire</option>
        <option value="monthly">Mensuel</option>
    </select>
    
    <select id="report-format">
        <option value="pdf" selected>PDF</option>
        <option value="excel">Excel</option>
    </select>
    
    <input type="time" id="report-time" value="08:00">
    <input type="number" id="report-retention" value="30">
    
    <div class="form-check">
        <input type="checkbox" id="include-charts" checked>
        <label>Inclure les graphiques</label>
    </div>
    <div class="form-check">
        <input type="checkbox" id="include-alerts" checked>
        <label>Inclure l'historique des alertes</label>
    </div>
    
    <button type="submit">Sauvegarder</button>
</form>

<!-- Statistiques des rapports -->
<div class="card">
    <div class="row text-center">
        <div class="col-6">
            <div class="stat-number text-primary">12</div>
            <div class="stat-label">Ce mois</div>
        </div>
        <div class="col-6">
            <div class="stat-number text-success">2.3 MB</div>
            <div class="stat-label">Taille moyenne</div>
        </div>
    </div>
    
    <h6>Prochain rapport</h6>
    <p>
        <strong>Type:</strong> Journalier<br>
        <strong>Format:</strong> PDF<br>
        <strong>Heure:</strong> 08:00 (demain)<br>
        <strong>Statut:</strong> <span class="badge bg-success">Programmé</span>
    </p>
</div>
```

#### 4. Configuration email
```html
<!-- Formulaire de configuration email -->
<form id="email-settings-form">
    <div class="form-check">
        <input type="checkbox" id="email-enabled">
        <label>Activer les alertes par email</label>
    </div>
    
    <input type="text" id="smtp-server" value="smtp.gmail.com">
    <input type="number" id="smtp-port" value="587">
    <input type="email" id="email-username" placeholder="votre.email@gmail.com">
    <input type="password" id="email-password" placeholder="Mot de passe">
    <input type="email" id="from-email" placeholder="supervision@centraldanone.com">
    <input type="email" id="to-email" placeholder="admin@centraldanone.com" required>
    
    <button type="submit">Sauvegarder</button>
    <button type="button" id="btn-test-email-config">Tester la configuration</button>
    <button type="button" id="btn-send-test-alert">Envoyer une alerte de test</button>
</form>

<!-- Aide configuration -->
<div class="card">
    <h6>Configuration Gmail</h6>
    <ul>
        <li>Serveur: smtp.gmail.com</li>
        <li>Port: 587</li>
        <li>Activer l'authentification à 2 facteurs</li>
        <li>Générer un mot de passe d'application</li>
    </ul>
    
    <h6>Configuration Outlook</h6>
    <ul>
        <li>Serveur: smtp-mail.outlook.com</li>
        <li>Port: 587</li>
        <li>Utiliser votre mot de passe normal</li>
    </ul>
    
    <div class="alert alert-info">
        <h6>Types d'alertes</h6>
        <small>
            • Appareils hors ligne<br>
            • Risques critiques détectés par IA<br>
            • Anomalies de comportement<br>
            • Rapports quotidiens
        </small>
    </div>
</div>
```

#### 5. Paramètres système
```html
<!-- Informations système -->
<div class="card">
    <div class="row">
        <div class="col-md-6">
            <h6>Informations système</h6>
            <table class="table table-sm">
                <tr><td>Version:</td><td>1.0.0</td></tr>
                <tr><td>Base de données:</td><td>SQLite</td></tr>
                <tr><td>Dernière mise à jour:</td><td>2024-12-01</td></tr>
                <tr><td>Statut:</td><td><span class="badge bg-success">Opérationnel</span></td></tr>
            </table>
        </div>
        
        <div class="col-md-6">
            <h6>Actions système</h6>
            <div class="d-grid gap-2">
                <button id="btn-backup">Sauvegarde de la base de données</button>
                <button id="btn-clear-cache">Vider le cache</button>
                <button id="btn-reset-settings">Réinitialiser les paramètres</button>
            </div>
        </div>
    </div>
</div>
```

### JavaScript et interactions

#### 1. Chargement des paramètres
```javascript
function loadSettings() {
    // Charger les paramètres réseau
    fetch('/api/settings')
        .then(response => response.json())
        .then(settings => {
            document.getElementById('network-range').value = settings.network_range || '192.168.1.0/24';
            document.getElementById('scan-interval').value = settings.scan_interval || 60;
            updateNetworkInfo(settings.network_range || '192.168.1.0/24');
        })
        .catch(error => {
            console.error('Erreur lors du chargement des paramètres:', error);
        });
    
    // Charger la configuration email
    fetch('/api/settings/email')
        .then(response => response.json())
        .then(emailSettings => {
            document.getElementById('email-enabled').checked = emailSettings.enabled || false;
            document.getElementById('smtp-server').value = emailSettings.smtp_server || 'smtp.gmail.com';
            document.getElementById('smtp-port').value = emailSettings.smtp_port || 587;
            document.getElementById('email-username').value = emailSettings.username || '';
            document.getElementById('from-email').value = emailSettings.from_email || '';
            document.getElementById('to-email').value = emailSettings.to_email || '';
            
            // Synchroniser avec l'email simple
            if (emailSettings.to_email) {
                document.getElementById('alert-email').value = emailSettings.to_email;
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement de la config email:', error);
        });
}
```

#### 2. Sauvegarde des paramètres réseau
```javascript
function saveNetworkSettings() {
    const settings = {
        network_range: document.getElementById('network-range').value,
        scan_interval: parseInt(document.getElementById('scan-interval').value),
        scan_timeout: parseInt(document.getElementById('scan-timeout').value),
        max_retries: parseInt(document.getElementById('max-retries').value),
        enable_auto_scan: document.getElementById('enable-auto-scan').checked
    };
    
    fetch('/api/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', 'Paramètres réseau sauvegardés avec succès');
            updateNetworkInfo(settings.network_range);
        } else {
            showAlert('danger', data.message);
        }
    })
    .catch(error => {
        showAlert('danger', 'Erreur lors de la sauvegarde: ' + error.message);
    });
}
```

#### 3. Test de configuration email
```javascript
function testEmailConfiguration() {
    const button = document.getElementById('btn-test-email-config');
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Test en cours...';
    button.disabled = true;
    
    fetch('/api/settings/email/test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showAlert('success', 'Configuration email testée avec succès ! Vérifiez votre boîte mail.');
        } else {
            showAlert('danger', data.message || 'Erreur lors du test');
        }
    })
    .catch(error => {
        showAlert('danger', 'Erreur lors du test: ' + error.message);
    })
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    });
}
```

#### 4. Envoi d'alerte de test
```javascript
function sendTestAlert() {
    const button = document.getElementById('btn-send-test-alert');
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Envoi...';
    button.disabled = true;
    
    const testData = {
        subject: 'Test d\'alerte Central Danone',
        message: 'Ceci est un test d\'alerte pour vérifier la configuration email du système de supervision Central Danone.',
        priority: 'medium'
    };
    
    fetch('/api/settings/email/alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showAlert('success', 'Alerte de test envoyée ! Vérifiez votre boîte mail.');
        } else {
            showAlert('danger', data.message || 'Erreur lors de l\'envoi');
        }
    })
    .catch(error => {
        showAlert('danger', 'Erreur lors de l\'envoi: ' + error.message);
    })
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    });
}
```

#### 5. Mise à jour des informations réseau
```javascript
function updateNetworkInfo(networkRange) {
    // Simuler l'analyse de la plage réseau
    const parts = networkRange.split('/');
    const ip = parts[0];
    const cidr = parseInt(parts[1]);
    
    document.getElementById('current-network').textContent = networkRange;
    document.getElementById('current-mask').textContent = calculateSubnetMask(cidr);
    document.getElementById('current-addresses').textContent = Math.pow(2, 32 - cidr) - 2;
}

function calculateSubnetMask(cidr) {
    const mask = (0xffffffff >> (32 - cidr)) << (32 - cidr);
    return [
        (mask >> 24) & 0xff,
        (mask >> 16) & 0xff,
        (mask >> 8) & 0xff,
        mask & 0xff
    ].join('.');
}

// Mise à jour du temps jusqu'au prochain scan
function updateNextScan() {
    const interval = parseInt(document.getElementById('scan-interval').value);
    const nextScan = new Date(Date.now() + interval * 60 * 1000);
    const minutes = Math.floor((nextScan - Date.now()) / (1000 * 60));
    
    if (minutes > 60) {
        const hours = Math.floor(minutes / 60);
        const remainingMinutes = minutes % 60;
        document.getElementById('next-scan').textContent = `${hours}h ${remainingMinutes}min`;
    } else {
        document.getElementById('next-scan').textContent = `${minutes} min`;
    }
}

// Mettre à jour toutes les minutes
setInterval(updateNextScan, 60000);
updateNextScan();
```

## Sécurité et authentification

### Protection des routes
- **Authentification requise** : Toutes les routes sont protégées par `@login_required`
- **Validation des données** : Validation côté serveur de tous les paramètres
- **Logs de sécurité** : Journalisation des modifications de paramètres

### Gestion des mots de passe
- **Chiffrement** : Mots de passe SMTP stockés en mémoire uniquement
- **Validation** : Test de configuration avant sauvegarde
- **Sécurité** : Recommandations pour mots de passe d'application

## Performance et optimisation

### Chargement des paramètres
- **Cache** : Paramètres chargés une fois au démarrage
- **Mise à jour** : Actualisation en temps réel des informations
- **Optimisation** : Requêtes API optimisées

### Interface utilisateur
- **Responsive** : Design adaptatif pour tous les écrans
- **Feedback** : Retours visuels pour toutes les actions
- **Validation** : Validation côté client et serveur

## Tests et validation

### Tests automatisés
- **API** : Tests de toutes les routes API
- **Interface** : Tests des formulaires et interactions
- **Intégration** : Tests de workflow complet

### Validation des données
- **Formats** : Validation des formats CIDR, email, etc.
- **Plages** : Validation des valeurs numériques
- **Cohérence** : Vérification de la cohérence des paramètres

## Métriques et monitoring

### Métriques collectées
- **Performance** : Durée des scans, temps de réponse
- **Utilisation** : Fréquence des modifications de paramètres
- **Erreurs** : Taux d'échec des tests et configurations

### Monitoring
- **Statut** : État opérationnel du système
- **Alertes** : Surveillance des échecs de configuration
- **Logs** : Journalisation détaillée des actions

## Évolutivité

### Extensibilité
- **Nouveaux paramètres** : Architecture modulaire pour ajouter des paramètres
- **Nouvelles sections** : Structure flexible pour de nouvelles catégories
- **APIs** : Interface REST extensible

### Maintenance
- **Sauvegarde** : Système de sauvegarde automatique
- **Restauration** : Procédures de restauration des paramètres
- **Migration** : Gestion des versions de configuration

---

*Cette analyse technique couvre l'architecture complète de la page Paramètres. Le système est conçu pour être robuste, sécurisé et facilement extensible.* 