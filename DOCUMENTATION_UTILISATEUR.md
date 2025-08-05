# Documentation Utilisateur - Dashboard Central Danone

## Table des matières
1. [Introduction](#introduction)
2. [Tableau de bord principal](#tableau-de-bord-principal)
3. [Dashboard IA](#dashboard-ia)
4. [Alertes](#alertes)
5. [Rapports](#rapports)
6. [Paramètres](#paramètres)
7. [Monitoring avancé](#monitoring-avancé)
8. [IA avancée](#ia-avancée)

## Introduction

Le Dashboard Central Danone est une solution complète de supervision réseau intégrant l'intelligence artificielle pour la détection proactive d'anomalies et la maintenance prédictive.

### Accès à l'application
- **URL** : http://localhost:5000
- **Identifiants par défaut** :
  - Utilisateur : `admin`
  - Mot de passe : `admin123`

## Tableau de bord principal

### Métriques clés
- **Équipements surveillés** : Nombre total d'équipements dans le réseau
- **Équipements en ligne** : Équipements actuellement accessibles
- **Disponibilité** : Pourcentage de temps de fonctionnement du réseau
- **Score de santé** : Indicateur global de l'état du réseau (0-100%)

### Actions disponibles
- **Scanner le réseau** : Découverte automatique des équipements
- **Informations détaillées** : Accès aux détails techniques de chaque équipement

### Interprétation des scores
- **Score ≥ 80%** : État excellent
- **Score 60-80%** : Attention requise
- **Score < 60%** : Intervention immédiate nécessaire

## Dashboard IA

### Indicateurs IA
- **Score de santé moyen** : Moyenne des scores de santé de tous les équipements
- **Équipements critiques** : Équipements nécessitant une maintenance immédiate
- **Risque élevé** : Équipements avec probabilité de panne > 50%
- **Anomalies détectées** : Comportements anormaux identifiés par l'IA

### Équipements à risque élevé
Liste des équipements nécessitant une surveillance renforcée avec :
- Adresse IP et nom
- Score de santé actuel
- Probabilité de panne
- Dernière maintenance

### Anomalies détectées
Comportements anormaux identifiés par l'algorithme d'isolation forest :
- Type d'anomalie
- Équipement concerné
- Gravité
- Recommandations

## Alertes

### Types d'alertes
- **Équipements hors ligne** : Perte de connectivité
- **Risques critiques** : Détection de problèmes majeurs par l'IA
- **Anomalies de comportement** : Comportements anormaux détectés
- **Maintenance préventive** : Rappels de maintenance programmée

### Gestion des alertes
- **Marquer comme lue** : Indiquer qu'une alerte a été traitée
- **Supprimer** : Retirer une alerte résolue
- **Filtrer** : Afficher les alertes par type ou gravité

## Rapports

### Types de rapports
- **Journalier** : Résumé quotidien des activités
- **Hebdomadaire** : Analyse sur 7 jours
- **Mensuel** : Vue d'ensemble mensuelle

### Formats disponibles
- **PDF** : Rapport formaté pour impression et archivage
- **Excel** : Données structurées pour analyse approfondie

### Contenu des rapports
- Statistiques générales du réseau
- Liste complète des équipements
- Historique des scans effectués
- Graphiques de disponibilité
- Historique des alertes et incidents

## Paramètres

### Configuration réseau
- **Plage d'adresses** : Définir la plage réseau à surveiller
- **Fréquence de scan** : Intervalle entre les scans automatiques
- **Timeout de connexion** : Délai maximum pour la détection

### Configuration des alertes
- **Seuils de déclenchement** : Définir les conditions d'alerte
- **Notifications par email** : Configuration SMTP
- **Fréquence des alertes** : Éviter le spam d'alertes

### Configuration des rapports
- **Génération automatique** : Programmer les rapports
- **Format par défaut** : PDF ou Excel
- **Rétention** : Durée de conservation des rapports

### Configuration email
#### Gmail
- Serveur : `smtp.gmail.com`
- Port : `587`
- Authentification : Activer l'authentification à 2 facteurs
- Mot de passe : Utiliser un mot de passe d'application

#### Outlook
- Serveur : `smtp-mail.outlook.com`
- Port : `587`
- Authentification : Utiliser le mot de passe normal

## Monitoring avancé

### Services surveillés
- **HTTP/HTTPS** : Sites web et applications
- **FTP** : Transferts de fichiers
- **SSH** : Accès sécurisé
- **SMTP** : Envoi d'emails
- **DNS** : Résolution de noms
- **SNMP** : Monitoring réseau

### Découverte automatique
- **Scan de ports** : Identification des services actifs
- **Détection de type** : Classification automatique des équipements
- **Géolocalisation** : Position géographique des équipements

### Monitoring de bande passante
- **Utilisation réseau** : Trafic entrant/sortant
- **Historique** : Évolution de l'utilisation
- **Alertes** : Seuils de consommation

## IA avancée

### Prédictions de maintenance
- **Analyse prédictive** : Anticipation des pannes
- **Recommandations** : Actions préventives suggérées
- **Planification** : Optimisation des interventions

### Détection d'intrusions
- **Analyse comportementale** : Détection d'activités suspectes
- **Signatures** : Reconnaissance de patterns malveillants
- **Alertes en temps réel** : Notifications immédiates

### Optimisation automatique
- **Configuration réseau** : Ajustements automatiques
- **Performance** : Optimisation des paramètres
- **Économies** : Réduction des coûts opérationnels

### Analyse des tendances
- **Évolution temporelle** : Analyse sur le long terme
- **Prévisions** : Anticipation des besoins
- **Reporting** : Rapports d'analyse détaillés

### Chatbot IA
- **Assistance technique** : Réponses aux questions
- **Diagnostic** : Aide au dépannage
- **Documentation** : Accès aux informations

## Maintenance

### Sauvegarde
- **Base de données** : Sauvegarde automatique des données
- **Configuration** : Préservation des paramètres
- **Restauration** : Procédure de récupération

### Cache
- **Nettoyage** : Suppression des données temporaires
- **Performance** : Optimisation de la vitesse
- **Espace disque** : Gestion de l'espace de stockage

### Réinitialisation
- **Paramètres** : Retour aux valeurs par défaut
- **Base de données** : Remise à zéro complète
- **Attention** : Action irréversible

## Support technique

### Logs
- **Application** : Traces d'exécution
- **Erreurs** : Journal des incidents
- **Performance** : Métriques de fonctionnement

### Diagnostic
- **Tests de connectivité** : Vérification réseau
- **Tests de services** : Validation des fonctionnalités
- **Tests d'intégration** : Vérification complète

### Contact
Pour toute question ou problème technique, consultez les logs de l'application ou contactez l'équipe technique.

---

**Version** : 1.0  
**Date** : Août 2025  
**Central Danone - Dashboard de Supervision Réseau** 