# Guide d'utilisation du système de génération de rapports

## 📋 Vue d'ensemble

Le système de génération de rapports de la plateforme de supervision réseau Central Danone permet de créer des rapports détaillés sur l'état et les performances du réseau industriel. Ces rapports sont essentiels pour la maintenance préventive, l'audit et la conformité.

## 🎯 Fonctionnalités principales

### Types de rapports disponibles

1. **Rapport journalier** - Synthèse quotidienne de l'état du réseau
2. **Rapport hebdomadaire** - Analyse complète de la semaine
3. **Rapport mensuel** - Synthèse mensuelle avec tendances
4. **Rapport personnalisé** - Période et contenu personnalisables

### Formats supportés

- **PDF** - Format professionnel pour l'archivage et la présentation
- **Excel** - Format tabulaire pour l'analyse et les calculs

## 🚀 Utilisation de l'interface web

### Accès à la page des rapports

1. Connectez-vous à l'application avec vos identifiants
2. Cliquez sur "Rapports" dans le menu de navigation
3. Vous accédez à l'interface de gestion des rapports

### Génération d'un nouveau rapport

#### Étape 1 : Configuration du rapport

1. **Type de rapport** : Sélectionnez le type souhaité
   - `Journalier` : Pour une vue quotidienne
   - `Hebdomadaire` : Pour une analyse de la semaine
   - `Mensuel` : Pour une synthèse mensuelle
   - `Personnalisé` : Pour une période spécifique

2. **Format** : Choisissez le format de sortie
   - `PDF` : Format professionnel
   - `Excel` : Format tabulaire

3. **Période** : Définissez la période d'analyse
   - `Date de début` : Première date à inclure
   - `Date de fin` : Dernière date à inclure

4. **Description** : Ajoutez une description optionnelle du rapport

#### Étape 2 : Génération

1. Cliquez sur "Générer le rapport"
2. Le système traite les données et génère le fichier
3. Le téléchargement démarre automatiquement
4. Le rapport est ajouté à la liste des rapports disponibles

### Gestion des rapports existants

#### Liste des rapports

La page affiche tous les rapports disponibles avec :
- **Nom du fichier** : Identifiant unique du rapport
- **Type** : Format du fichier (PDF/Excel)
- **Taille** : Taille du fichier en MB/KB
- **Date de création** : Quand le rapport a été généré
- **Actions** : Boutons pour télécharger, aperçu, supprimer

#### Filtrage des rapports

Utilisez les boutons de filtre pour afficher :
- **Tous** : Tous les rapports
- **PDF** : Seulement les rapports PDF
- **Excel** : Seulement les rapports Excel

#### Actions sur les rapports

- **Télécharger** : Télécharger le fichier
- **Aperçu** : Voir un aperçu du contenu
- **Supprimer** : Supprimer le rapport (avec confirmation)

### Statistiques des rapports

La page affiche des statistiques en temps réel :
- **Total rapports** : Nombre total de rapports
- **Ce mois** : Rapports générés ce mois-ci
- **Types de rapports** : Répartition par type (journalier, hebdomadaire, mensuel)

## 📊 Contenu des rapports

### Rapport PDF

#### En-tête
- Logo et titre Central Danone
- Date de génération
- Type de rapport

#### Statistiques générales
- Total des équipements surveillés
- Équipements en ligne/hors ligne
- Taux de disponibilité
- Nombre de scans effectués

#### Liste des équipements
- Adresse IP
- Nom d'hôte
- Statut (en ligne/hors ligne)
- Dernière vue
- Score de santé (si disponible)

#### Pied de page
- Informations de contact
- Généré automatiquement

### Rapport Excel

#### Feuille "Statistiques"
- Métriques clés du réseau
- Calculs de disponibilité
- Tendances temporelles

#### Feuille "Appareils"
- Liste complète des équipements
- Données détaillées par appareil
- Codes couleur selon le statut

#### Feuille "Résumé"
- Synthèse exécutive
- Évaluation de la santé du réseau
- Recommandations

## 🔧 Utilisation avancée

### Rapports personnalisés

Pour des besoins spécifiques :

1. Sélectionnez "Rapport personnalisé"
2. Définissez la période exacte souhaitée
3. Ajoutez une description détaillée
4. Choisissez le format approprié

### Automatisation

Les rapports peuvent être générés automatiquement :
- **Rapports journaliers** : Génération automatique quotidienne
- **Rapports hebdomadaires** : Génération automatique le lundi
- **Rapports mensuels** : Génération automatique le premier du mois

### Intégration avec l'IA

Les rapports incluent automatiquement :
- **Analyses IA** : Scores de santé et prédictions
- **Détection d'anomalies** : Comportements anormaux identifiés
- **Recommandations** : Suggestions de maintenance

## 📁 Organisation des fichiers

### Structure des dossiers

```
reports/
├── rapport_journalier_20241201.pdf
├── rapport_hebdomadaire_20241124.xlsx
├── rapport_mensuel_20241101.pdf
└── rapport_personnalise_20241201.xlsx
```

### Convention de nommage

- `rapport_[type]_[date].{format}`
- Date au format YYYYMMDD
- Format : pdf, xlsx, json

## 🛠️ Dépannage

### Problèmes courants

#### Erreur de génération
- **Cause** : Données insuffisantes ou erreur système
- **Solution** : Vérifiez la période sélectionnée et réessayez

#### Fichier corrompu
- **Cause** : Interruption pendant la génération
- **Solution** : Régénérez le rapport

#### Téléchargement échoué
- **Cause** : Problème de réseau ou de navigateur
- **Solution** : Vérifiez votre connexion et réessayez

### Logs et diagnostics

Les erreurs sont enregistrées dans :
- **Logs applicatifs** : `logs/app.log`
- **Console du navigateur** : F12 → Console

## 📈 Bonnes pratiques

### Génération de rapports

1. **Planifiez la génération** : Évitez les heures de pointe
2. **Vérifiez les données** : Assurez-vous que les données sont complètes
3. **Utilisez des descriptions** : Facilitez l'identification des rapports
4. **Archivez régulièrement** : Sauvegardez les rapports importants

### Gestion des fichiers

1. **Organisez par période** : Créez des dossiers par mois/trimestre
2. **Nommez clairement** : Utilisez des noms descriptifs
3. **Vérifiez l'intégrité** : Testez l'ouverture des fichiers
4. **Sauvegardez** : Gardez des copies de sécurité

### Utilisation des statistiques

1. **Surveillez les tendances** : Analysez l'évolution des métriques
2. **Identifiez les anomalies** : Utilisez les rapports pour détecter les problèmes
3. **Planifiez la maintenance** : Basez-vous sur les données pour la maintenance
4. **Partagez les insights** : Communiquez les résultats aux équipes

## 🔐 Sécurité et permissions

### Accès aux rapports

- **Authentification requise** : Seuls les utilisateurs connectés peuvent accéder
- **Permissions par rôle** : Les administrateurs ont accès complet
- **Audit trail** : Toutes les actions sont enregistrées

### Protection des données

- **Chiffrement** : Les données sensibles sont protégées
- **Accès limité** : Seuls les utilisateurs autorisés peuvent télécharger
- **Suppression sécurisée** : Les fichiers supprimés sont irrécupérables

## 📞 Support et assistance

### En cas de problème

1. **Vérifiez la documentation** : Consultez ce guide
2. **Testez avec les scripts** : Utilisez `test_reports_system.py`
3. **Contactez l'équipe IT** : Pour les problèmes techniques
4. **Consultez les logs** : Pour les diagnostics avancés

### Ressources supplémentaires

- **Script de test** : `test_reports_system.py`
- **Script de démonstration** : `demo_reports_system.py`
- **Documentation technique** : Code source et commentaires
- **Interface web** : Guide interactif dans l'application

---

*Ce guide couvre toutes les fonctionnalités du système de génération de rapports. Pour des questions spécifiques, contactez l'équipe de développement.* 