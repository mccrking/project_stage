# Guide d'utilisation du système d'alertes

## 📋 Vue d'ensemble

Le système d'alertes de la plateforme de supervision réseau Danone est un module intelligent qui surveille en temps réel l'état des équipements et génère automatiquement des alertes basées sur l'IA pour maintenir la continuité opérationnelle.

## 🎯 Fonctionnalités principales

### 1. **Surveillance intelligente**
- Détection automatique d'équipements hors ligne
- Analyse IA pour détecter les anomalies
- Évaluation des scores de santé des équipements
- Prédiction des pannes avec probabilité

### 2. **Types d'alertes supportés**

| Type | Description | Priorité | Déclencheur |
|------|-------------|----------|-------------|
| `offline` | Équipement hors ligne | High/Critical | Ping échoué |
| `ai_critical` | Score de santé critique | Critical | IA détecte problème grave |
| `ai_warning` | Avertissement IA | Medium/High | IA détecte anomalie |
| `anomaly` | Comportement anormal | Medium | Détection d'anomalie |

### 3. **Niveaux de priorité**

| Priorité | Couleur | Description | Action requise |
|----------|---------|-------------|----------------|
| **Critical** | 🔴 Rouge | Action immédiate requise | Intervention urgente |
| **High** | 🟠 Orange | Action rapide nécessaire | Intervention rapide |
| **Medium** | 🟡 Jaune | Surveillance renforcée | Monitoring |
| **Low** | 🟢 Vert | Information | Aucune action |

## 🖥️ Interface utilisateur

### Page principale des alertes

#### **En-tête**
- **Titre** : "Alertes" avec icône de cloche
- **Boutons d'action** :
  - `Résoudre tout` : Résolution groupée des alertes sélectionnées
  - `Actualiser` : Rafraîchissement manuel de la page

#### **Statistiques des alertes**
- **Total alertes** : Nombre total d'alertes dans le système
- **Alertes actives** : Alertes non résolues
- **Critiques** : Alertes de priorité critique
- **Résolues** : Alertes déjà traitées

#### **Section "Alertes actives"**
Tableau avec les colonnes suivantes :
- ☑️ **Sélection** : Cases à cocher pour sélection multiple
- 🏷️ **Priorité** : Badge coloré selon le niveau
- 📌 **Type** : Type d'alerte (offline, ai_critical, etc.)
- 🖥️ **Équipement** : IP et hostname de l'équipement
- 💬 **Message** : Description détaillée de l'alerte
- 📅 **Date** : Date et heure de création
- ⚙️ **Actions** : Bouton de résolution individuelle

#### **Section "Alertes résolues récentes"**
Historique des 20 dernières alertes résolues avec :
- Priorité
- Type
- Équipement concerné
- Message
- Date de résolution

## 🔧 Utilisation pratique

### 1. **Accéder à la page alertes**
1. Connectez-vous à la plateforme
2. Cliquez sur "Alertes" dans le menu de navigation
3. La page se charge automatiquement avec les données en temps réel

### 2. **Consulter les alertes**
- Les alertes sont triées par date de création (plus récentes en premier)
- Les alertes critiques sont mises en évidence en rouge
- Utilisez les filtres visuels (badges de priorité) pour identifier rapidement les urgences

### 3. **Résoudre une alerte individuelle**
1. Localisez l'alerte dans le tableau
2. Cliquez sur le bouton ✅ dans la colonne "Actions"
3. L'alerte est automatiquement marquée comme résolue
4. La page se rafraîchit pour refléter le changement

### 4. **Résoudre plusieurs alertes**
1. Cochez les cases à côté des alertes à résoudre
2. Utilisez "Sélectionner tout" pour cocher toutes les alertes
3. Cliquez sur "Résoudre tout"
4. Toutes les alertes sélectionnées sont résolues en une fois

### 5. **Actualiser les données**
- Cliquez sur "Actualiser" pour forcer le rafraîchissement
- Les données se mettent à jour automatiquement toutes les 30 secondes

## 🤖 Intégration IA

### **Génération automatique d'alertes**
Les alertes sont générées automatiquement par :

1. **Scans réseau** :
   - Détection d'équipements hors ligne
   - Surveillance de la connectivité

2. **Analyse IA** :
   - Évaluation des scores de santé
   - Détection d'anomalies comportementales
   - Prédiction de pannes

3. **Seuils configurables** :
   - Seuils de santé critique
   - Seuils d'anomalie
   - Seuils de probabilité de panne

### **Confiance IA**
Chaque alerte inclut un score de confiance IA (0.0 à 1.0) qui indique la fiabilité de la détection.

## 📊 Statistiques et rapports

### **Métriques disponibles**
- Nombre total d'alertes
- Répartition par priorité
- Répartition par type
- Temps moyen de résolution
- Taux de résolution

### **Export et historique**
- Les alertes résolues sont conservées pour l'historique
- Intégration avec le système de rapports
- Possibilité d'export pour analyse

## ⚙️ Configuration avancée

### **Paramètres d'alerte**
Dans les paramètres système, vous pouvez configurer :
- Seuils de déclenchement des alertes
- Fréquence de surveillance
- Notifications par email
- Escalade automatique

### **Notifications**
- Alertes par email pour les priorités critiques
- Notifications en temps réel dans l'interface
- Intégration avec les systèmes de monitoring

## 🔍 Dépannage

### **Problèmes courants**

#### **Aucune alerte affichée**
- Vérifiez que les scans réseau sont actifs
- Contrôlez la configuration des seuils d'alerte
- Vérifiez la connectivité des équipements

#### **Alertes non mises à jour**
- Cliquez sur "Actualiser"
- Vérifiez la connexion à la base de données
- Contrôlez les logs système

#### **Erreur de résolution d'alerte**
- Vérifiez les permissions utilisateur
- Contrôlez la connectivité à la base de données
- Consultez les logs d'erreur

### **Logs et diagnostic**
- Les erreurs sont enregistrées dans les logs système
- Utilisez la console de développement pour le débogage
- Vérifiez la santé de la base de données

## 🚀 Bonnes pratiques

### **Gestion quotidienne**
1. **Vérification matinale** : Consultez les alertes critiques en priorité
2. **Résolution rapide** : Traitez les alertes high/critical dans les 30 minutes
3. **Documentation** : Notez les actions prises pour chaque résolution
4. **Analyse hebdomadaire** : Examinez les tendances d'alertes

### **Optimisation**
1. **Ajustement des seuils** : Adaptez les seuils selon l'environnement
2. **Maintenance préventive** : Utilisez les alertes IA pour anticiper les pannes
3. **Formation équipe** : Assurez-vous que tous les techniciens connaissent le système

### **Sécurité**
1. **Accès contrôlé** : Seuls les utilisateurs autorisés peuvent résoudre les alertes
2. **Audit trail** : Toutes les actions sont enregistrées
3. **Sauvegarde** : Les données d'alertes sont sauvegardées régulièrement

## 📞 Support

### **En cas de problème**
1. Consultez ce guide en premier
2. Vérifiez les logs système
3. Contactez l'équipe technique
4. Documentez le problème pour amélioration

### **Amélioration continue**
- Le système d'alertes évolue avec l'IA
- Les retours utilisateurs sont pris en compte
- Les nouvelles fonctionnalités sont régulièrement ajoutées

---

**Version** : 1.0  
**Dernière mise à jour** : 2024  
**Auteur** : Équipe technique Danone 