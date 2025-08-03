# Guide Utilisateur - Page Paramètres

## Vue d'ensemble

La page **Paramètres** est le centre de configuration de la plateforme de supervision réseau Central Danone. Elle permet de configurer tous les aspects du système, de la surveillance réseau aux alertes en passant par les rapports et la maintenance.

## Accès à la page

1. Connectez-vous à l'application avec vos identifiants
2. Cliquez sur **"Paramètres"** dans le menu de navigation
3. Vous accédez à l'interface de configuration complète

## Sections principales

### 1. Configuration réseau

**Objectif** : Configurer la surveillance et le scan des réseaux Central Danone.

#### Paramètres disponibles :

- **Plage réseau à scanner** : Format CIDR (ex: 192.168.1.0/24)
- **Intervalle de scan** : Fréquence des scans automatiques (15 min à 8h)
- **Timeout de scan** : Délai maximum par appareil (1-60 secondes)
- **Nombre de tentatives** : Tentatives en cas d'échec (1-5)
- **Scan automatique** : Activer/désactiver les scans automatiques

#### Informations réseau affichées :

- **Plage actuelle** : Réseau configuré et masque
- **Adresses** : Nombre d'adresses IP dans la plage
- **Statut du scan** : Actif/inactif et prochain scan
- **Performance** : Durée moyenne et dernier scan

#### Actions disponibles :

- **Sauvegarder** : Appliquer les nouveaux paramètres
- **Tester** : Vérifier la connectivité d'une plage réseau

### 2. Configuration des alertes

**Objectif** : Définir les seuils et types d'alertes pour la surveillance.

#### Paramètres disponibles :

- **Seuil d'alerte** : Pourcentage de disponibilité déclenchant une alerte (0-100%)
- **Email pour les alertes** : Adresse email de destination
- **Types d'alertes** :
  - Appareil hors ligne
  - Appareil de retour en ligne
  - Disponibilité faible
  - Échec de scan

#### Test des alertes :

- **Tester une alerte** : Générer une alerte de test
- **Tester l'email simple** : Vérifier l'envoi d'email
- **Dernières alertes** : Historique des alertes récentes

### 3. Configuration des rapports

**Objectif** : Configurer la génération automatique de rapports.

#### Paramètres disponibles :

- **Rapport automatique** : Type (Aucun, Journalier, Hebdomadaire, Mensuel)
- **Format par défaut** : PDF ou Excel
- **Heure de génération** : Heure de création automatique
- **Rétention** : Durée de conservation en jours (1-365)
- **Options** :
  - Inclure les graphiques
  - Inclure l'historique des alertes

#### Statistiques des rapports :

- **Ce mois** : Nombre de rapports générés
- **Taille moyenne** : Taille moyenne des fichiers
- **Prochain rapport** : Détails du prochain rapport programmé

### 4. Configuration des alertes par email

**Objectif** : Configurer l'envoi d'alertes par email avec SMTP.

#### Paramètres SMTP :

- **Activer les alertes par email** : Activer/désactiver
- **Serveur SMTP** : Adresse du serveur (ex: smtp.gmail.com)
- **Port SMTP** : Port de connexion (587 pour TLS, 465 pour SSL)
- **Nom d'utilisateur** : Compte email
- **Mot de passe** : Mot de passe ou mot de passe d'application
- **Email d'expédition** : Adresse d'envoi
- **Email de destination** : Adresse de réception

#### Actions disponibles :

- **Sauvegarder** : Enregistrer la configuration
- **Tester la configuration** : Vérifier la connexion SMTP
- **Envoyer une alerte de test** : Tester l'envoi d'email

#### Aide configuration :

- **Configuration Gmail** : Instructions pour Gmail
- **Configuration Outlook** : Instructions pour Outlook
- **Types d'alertes** : Liste des alertes envoyées par email

### 5. Paramètres système

**Objectif** : Actions de maintenance et informations système.

#### Informations système :

- **Version** : Version de l'application
- **Base de données** : Type de base utilisée
- **Dernière mise à jour** : Date de dernière mise à jour
- **Statut** : État opérationnel du système

#### Actions système :

- **Sauvegarde de la base de données** : Créer une sauvegarde
- **Vider le cache** : Nettoyer le cache système
- **Réinitialiser les paramètres** : Retour aux valeurs par défaut

## Utilisation pratique

### Configuration initiale

1. **Configurer le réseau** :
   - Définir la plage réseau à surveiller
   - Ajuster l'intervalle de scan selon vos besoins
   - Tester la connectivité

2. **Configurer les alertes** :
   - Définir le seuil de disponibilité critique
   - Activer les types d'alertes nécessaires
   - Configurer l'email de destination

3. **Configurer les rapports** :
   - Choisir le type de rapport automatique
   - Définir l'heure de génération
   - Configurer la rétention

4. **Configurer l'email** (optionnel) :
   - Configurer le serveur SMTP
   - Tester la configuration
   - Envoyer une alerte de test

### Maintenance régulière

1. **Vérifier les paramètres** :
   - Contrôler les seuils d'alerte
   - Vérifier la configuration email
   - Examiner les statistiques

2. **Tests périodiques** :
   - Tester les alertes
   - Vérifier l'envoi d'emails
   - Contrôler la génération de rapports

3. **Sauvegarde** :
   - Créer des sauvegardes régulières
   - Vider le cache si nécessaire

## Bonnes pratiques

### Configuration réseau

- **Plage réseau** : Utilisez des plages CIDR appropriées
- **Intervalle de scan** : Équilibrez entre réactivité et charge réseau
- **Timeout** : Adaptez selon la latence de votre réseau
- **Test** : Testez toujours une nouvelle configuration

### Alertes

- **Seuils** : Définissez des seuils réalistes (85-95%)
- **Types** : Activez seulement les alertes nécessaires
- **Email** : Utilisez une adresse email dédiée

### Rapports

- **Fréquence** : Adaptez selon vos besoins de reporting
- **Format** : PDF pour présentation, Excel pour analyse
- **Rétention** : Conservez selon vos obligations légales

### Email

- **Sécurité** : Utilisez des mots de passe d'application pour Gmail
- **Test** : Testez toujours la configuration avant mise en production
- **Monitoring** : Surveillez les échecs d'envoi

## Dépannage

### Problèmes courants

1. **Scan réseau échoue** :
   - Vérifiez la plage réseau
   - Contrôlez les permissions réseau
   - Ajustez le timeout

2. **Alertes non reçues** :
   - Vérifiez la configuration email
   - Testez la connexion SMTP
   - Contrôlez les seuils d'alerte

3. **Rapports non générés** :
   - Vérifiez la configuration automatique
   - Contrôlez les permissions de fichiers
   - Examinez les logs

### Actions de récupération

1. **Réinitialiser les paramètres** :
   - Utilisez avec précaution
   - Sauvegardez avant réinitialisation
   - Reconfigurez étape par étape

2. **Sauvegarde/restauration** :
   - Créez des sauvegardes régulières
   - Testez la restauration
   - Documentez les configurations

## Sécurité

### Recommandations

- **Mots de passe** : Utilisez des mots de passe forts
- **Accès** : Limitez l'accès aux paramètres aux administrateurs
- **Sauvegarde** : Chiffrez les sauvegardes sensibles
- **Audit** : Surveillez les modifications de paramètres

### Configuration sécurisée

- **SMTP** : Utilisez TLS/SSL
- **Authentification** : Activez l'authentification à 2 facteurs
- **Permissions** : Restreignez les accès réseau
- **Logs** : Activez la journalisation des actions

## Support

### Ressources

- **Documentation** : Consultez la documentation technique
- **Logs** : Examinez les logs pour diagnostiquer les problèmes
- **Tests** : Utilisez les fonctions de test intégrées
- **Sauvegarde** : Gardez des sauvegardes de configuration

### Contact

Pour toute question ou problème :
- Consultez la documentation
- Vérifiez les logs système
- Contactez l'équipe technique

---

*Ce guide couvre les fonctionnalités principales de la page Paramètres. Pour des informations techniques détaillées, consultez la documentation développeur.* 