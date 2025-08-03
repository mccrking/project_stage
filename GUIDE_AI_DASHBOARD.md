# 🧠 Guide d'Utilisation - AI Dashboard Central Danone

## 📖 Introduction

L'AI Dashboard est la page centrale d'intelligence artificielle de la plateforme de supervision réseau Central Danone. Elle offre des analyses prédictives, une détection d'anomalies et des recommandations intelligentes pour optimiser la gestion de votre infrastructure réseau.

## 🚀 Accès à l'AI Dashboard

1. **Connexion** : Connectez-vous à l'application avec vos identifiants
2. **Navigation** : Cliquez sur "AI Dashboard" dans le menu principal
3. **URL directe** : `http://localhost:5000/ai-dashboard`

## 📊 Interface Principale

### En-tête du Dashboard
- **Titre** : "Intelligence Artificielle - Central Danone"
- **Statut des modèles IA** : Indique si les modèles sont entraînés ou en cours
- **Bouton "Entraîner IA"** : Lance l'entraînement des modèles IA

### Statistiques Globales (4 cartes)
1. **Score Santé Moyen** : Pourcentage de santé global du réseau
2. **Équipements Critiques** : Nombre d'équipements en état critique
3. **Risque Élevé** : Nombre d'équipements à risque de panne
4. **Anomalies Détectées** : Nombre d'équipements avec comportements anormaux

## 🔍 Fonctionnalités Principales

### 1. Équipements à Risque Élevé
**Localisation** : Section gauche de la page

**Fonctionnalités** :
- **Liste automatique** : Affiche les équipements avec un risque de panne > 60%
- **Bouton de rafraîchissement** : 🔄 Met à jour la liste en temps réel
- **Barre de progression** : Visualise le pourcentage de risque
- **Bouton d'analyse** : 🧠 Lance une analyse IA détaillée

**Utilisation** :
1. Consultez la liste des équipements à risque
2. Cliquez sur 🔄 pour actualiser les données
3. Cliquez sur 🧠 pour analyser un équipement spécifique

### 2. Comportements Anormaux
**Localisation** : Section droite de la page

**Fonctionnalités** :
- **Détection automatique** : Identifie les comportements anormaux
- **Score d'anomalie** : Indicateur numérique de l'anomalie
- **Bouton de rafraîchissement** : 🔄 Met à jour la liste
- **Bouton d'analyse** : 🔍 Analyse détaillée de l'anomalie

**Utilisation** :
1. Surveillez les équipements avec comportements anormaux
2. Cliquez sur 🔄 pour actualiser
3. Cliquez sur 🔍 pour analyser l'anomalie

### 3. Modèles IA
**Localisation** : Section inférieure gauche

**Informations affichées** :
- **Détection d'Anomalies** : Modèle Isolation Forest
- **Maintenance Prédictive** : Random Forest + Gradient Boosting
- **Classification Équipements** : Règles + Machine Learning

**Statut** : Tous les modèles sont marqués comme "Actifs"

### 4. Recommandations IA
**Localisation** : Section inférieure droite

**Fonctionnalités** :
- **Bouton "Générer"** : 🪄 Lance la génération de recommandations
- **Tri par priorité** : Critical, High, Medium, Low
- **Actions concrètes** : Recommandations d'interventions

**Utilisation** :
1. Cliquez sur "Générer" pour créer des recommandations
2. Consultez les recommandations par ordre de priorité
3. Suivez les actions suggérées

### 5. Graphiques Interactifs
**Localisation** : Section inférieure

**Types de graphiques** :
- **Graphique circulaire** : Distribution des types d'équipements
- **Graphique en barres** : Scores de santé par catégorie

**Fonctionnalités** :
- **Responsive** : S'adapte à la taille d'écran
- **Interactif** : Hover pour plus d'informations
- **Mise à jour automatique** : Données en temps réel

## 🔧 Analyse IA Détaillée

### Accès à l'Analyse
1. Cliquez sur le bouton 🧠 d'un équipement
2. Une fenêtre modale s'ouvre avec l'analyse complète

### Informations Affichées

#### Classification
- **Type d'équipement** : Classifié automatiquement par l'IA
- **Niveau de confiance** : Pourcentage de confiance de la classification

#### Maintenance Prédictive
- **Probabilité de panne** : Pourcentage de risque de défaillance
- **Niveau d'urgence** : Critical, High, Medium, Low

#### Détection d'Anomalies
- **Anomalie détectée** : Oui/Non
- **Score d'anomalie** : Valeur numérique de l'anomalie

#### Scores Globaux
- **Score de santé** : État général de l'équipement
- **Confiance IA** : Fiabilité de l'analyse

#### Recommandations
- **Messages** : Conseils d'actions
- **Priorités** : Niveau d'urgence des actions
- **Actions suggérées** : Interventions recommandées

## ⚙️ Entraînement des Modèles IA

### Lancement de l'Entraînement
1. Cliquez sur le bouton "Entraîner IA" dans l'en-tête
2. Le bouton affiche un spinner pendant l'entraînement
3. Une notification confirme le succès
4. La page se recharge automatiquement après 3 secondes

### Processus d'Entraînement
- **Données utilisées** : Historique des scans et métriques
- **Modèles mis à jour** : Classification, Anomalies, Maintenance
- **Amélioration continue** : Les modèles s'améliorent avec plus de données

## 🔄 Mises à Jour Automatiques

### Fréquence
- **Statistiques** : Mise à jour toutes les 30 secondes
- **Graphiques** : Actualisation automatique
- **Indicateurs** : Temps réel

### Fonctionnalités
- **Pas de rechargement** : Mises à jour silencieuses
- **Indicateurs visuels** : Changements de couleurs selon les seuils
- **Notifications** : Alertes en cas de changement critique

## 🎯 Bonnes Pratiques

### Surveillance Quotidienne
1. **Vérifiez les statistiques** : Score de santé et équipements critiques
2. **Consultez les risques** : Équipements à risque élevé
3. **Analysez les anomalies** : Comportements anormaux
4. **Générez des recommandations** : Conseils d'actions

### Actions Préventives
1. **Analysez les équipements à risque** : Cliquez sur 🧠
2. **Suivez les recommandations** : Actions prioritaires
3. **Entraînez régulièrement** : Améliorez les modèles IA
4. **Surveillez les tendances** : Graphiques et métriques

### Maintenance
1. **Rafraîchissez les données** : Boutons 🔄
2. **Vérifiez les modèles** : Statut "Actifs"
3. **Entraînez les modèles** : Amélioration continue
4. **Consultez les logs** : Traçabilité des actions

## 🚨 Alertes et Notifications

### Types d'Alertes
- **Équipements critiques** : Santé < 50%
- **Risque élevé** : Probabilité de panne > 60%
- **Anomalies** : Comportements anormaux détectés
- **Entraînement** : Statut des modèles IA

### Actions Recommandées
- **Critical** : Intervention immédiate requise
- **High** : Action préventive recommandée
- **Medium** : Surveillance renforcée
- **Low** : Maintenance planifiée

## 📱 Interface Responsive

### Adaptation Écran
- **Desktop** : Affichage complet avec tous les éléments
- **Tablet** : Réorganisation automatique des sections
- **Mobile** : Interface optimisée pour petits écrans

### Navigation
- **Menu** : Accessible sur tous les appareils
- **Graphiques** : Redimensionnement automatique
- **Modales** : Adaptation à la taille d'écran

## 🔍 Dépannage

### Problèmes Courants

#### Page ne se charge pas
- Vérifiez la connexion à l'application
- Rechargez la page (F5)
- Vérifiez les logs d'erreur

#### Données non mises à jour
- Cliquez sur les boutons de rafraîchissement 🔄
- Vérifiez la connexion réseau
- Attendez la mise à jour automatique (30s)

#### Analyse IA échoue
- Vérifiez que les modèles sont entraînés
- Lancez un entraînement des modèles
- Consultez les logs d'erreur

#### Graphiques non affichés
- Vérifiez la connexion internet (Chart.js)
- Rechargez la page
- Vérifiez la console du navigateur

### Support Technique
- **Logs** : Consultez les fichiers de log
- **API** : Testez les endpoints directement
- **Documentation** : Référez-vous à ce guide

## 🎉 Conclusion

L'AI Dashboard offre une solution complète d'intelligence artificielle pour la supervision réseau. En suivant ce guide, vous pourrez exploiter pleinement toutes les fonctionnalités pour optimiser la gestion de votre infrastructure Central Danone.

**Rappel** : L'IA s'améliore avec l'utilisation. Plus vous utilisez le système, plus les analyses et recommandations deviennent précises ! 