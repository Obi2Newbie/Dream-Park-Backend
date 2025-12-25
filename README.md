# DreamPark - Partie 4: Interface Graphique Complète

## Description

Partie 4 du projet DreamPark - Système de gestion intelligent de parking avec interface graphique complète basée sur le modèle MVC (Model-View-Controller). Cette application fournit une interface utilisateur intuitive pour gérer toutes les opérations du parking, incluant les entrées/sorties de véhicules, les services pour abonnés, et l'administration.


## Architecture

### Model (DreamParkModel)
- Gestion de la base de données SQLite
- Logique métier du parking
- Création et vérification des tables
- Gestion des transactions

### Controller (DreamParkController)
- Logique de contrôle entre le modèle et la vue
- Traitement des événements utilisateur
- Mise à jour de l'affichage

### View (DreamParkView)
- Interface graphique complète avec Tkinter
- Onglets multiples pour différentes fonctionnalités
- Affichage en temps réel des statistiques

## Fonctionnalités Principales

### 1. Onglet Accueil
- Panneaux d'affichage extérieurs pour les 2 accès (Nord et Sud)
- Affichage dynamique du nombre de places disponibles par accès
- Statistiques en temps réel:
  - Taux d'occupation
  - Véhicules présents
  - Total clients
  - Services actifs
- Code couleur selon la disponibilité (vert/orange/rouge)

### 2. Onglet Accès Entrée
- Simulation de caméra pour capture d'immatriculation
- Choix de l'accès (Nord ou Sud)
- Mode de paiement (CB ou Espèces)
- Système de téléportation automatique des véhicules
- Enregistrement automatique des nouveaux clients/véhicules
- Gestion du Pack Garanti pour super abonnés

### 3. Onglet Accès Sortie
- Recherche par ticket ou immatriculation
- Choix de l'accès de sortie
- Calcul automatique de la durée et du tarif
- Système de téléportation pour récupération du véhicule
- Tarifs différenciés selon le type de client

### 4. Onglet Services (Abonnés uniquement)
- Service de livraison avec choix d'adresse et d'heure
- Service d'entretien
- Service de maintenance
- Affichage des résultats et assignation automatique des voituriers

### 5. Onglet Administration
- Tableau de bord complet avec 3 sous-onglets:
  - **Mouvements**: Historique des entrées/sorties
  - **Revenus**: Statistiques de fréquentation et revenus sur 14 jours
  - **Services**: Liste des services en attente

## Tables de la Base de Données

L'application vérifie et crée automatiquement les tables manquantes:

- **Voiturier**: Gestion des voituriers (3 par défaut)
- **Statistiques_Frequentation**: Données historiques du parking
- **Maintenance**: Demandes de maintenance
- **Entretien**: Demandes d'entretien
- **Livraison**: Demandes de livraison avec adresse et heure

## Utilisation

### Démarrage

```bash
python partie4.py
```

### Opérations de Base

#### Entrée d'un Véhicule
1. Aller dans l'onglet "Accès Entrée"
2. Choisir l'accès (Nord ou Sud)
3. Saisir l'immatriculation (ou cliquer sur "Scanner")
4. Choisir le mode de paiement
5. Cliquer sur "VALIDER L'ENTRÉE"

Si le véhicule n'existe pas, un formulaire d'enregistrement s'affiche automatiquement.

#### Sortie d'un Véhicule
1. Aller dans l'onglet "Accès Sortie"
2. Choisir l'accès de sortie
3. Saisir le ticket ou l'immatriculation
4. Cliquer sur "VALIDER LA SORTIE"
5. Le tarif sera calculé et affiché automatiquement

#### Demander un Service
1. Aller dans l'onglet "Services"
2. Choisir le type de service:
   - Livraison: Remplir nom, adresse et heure
   - Entretien: Saisir l'immatriculation
   - Maintenance: Saisir l'immatriculation
3. Cliquer sur le bouton correspondant

#### Consulter les Statistiques
1. Aller dans l'onglet "Admin"
2. Cliquer sur "Actualiser" pour mettre à jour les données
3. Naviguer entre les sous-onglets:
   - Mouvements: Historique complet
   - Revenus: Performance financière
   - Services: Demandes en cours

## Système de Tarification

- **Standard**: Tarif horaire (minimum 1 heure)
- **Abonné**: Tarif forfaitaire de 5.50€
- **Super Abonné (Pack Garanti)**: Gratuit

## Gestion du Pack Garanti

Les super abonnés bénéficient du Pack Garanti:
- Accès garanti même si le parking est complet
- Service valet automatique
- Stationnement dans un parking partenaire si nécessaire
- Gratuit

## Fonctionnalités Avancées

### Système de Voituriers
- Attribution automatique d'un voiturier pour chaque opération
- 3 voituriers disponibles en rotation
- Affichage du numéro de voiturier assigné

### Panneaux d'Affichage Extérieurs
- Mise à jour en temps réel du nombre de places
- Division équitable entre les 2 accès
- Code couleur dynamique:
  - Vert: Plus de 25 places
  - Orange: Entre 5 et 25 places
  - Rouge: Moins de 5 places

### Système de Téléportation
- Simulation du transport automatique des véhicules
- Affichage du processus de téléportation
- Messages détaillés pour l'entrée et la sortie

## Gestion des Erreurs

L'application gère automatiquement:
- Véhicules non enregistrés (proposition d'enregistrement)
- Véhicules déjà dans le parking
- Tentatives de sortie avec ticket invalide
- Services demandés par des non-abonnés
- Places incompatibles avec les dimensions du véhicule
- Tables manquantes dans la base de données

## Statistiques Générées Automatiquement

Au premier lancement, l'application génère:
- 30 jours de statistiques de fréquentation
- Données aléatoires réalistes:
  - Entrées: 80-150 par jour
  - Sorties: 75-145 par jour
  - Taux d'occupation: 45%-95%
  - Revenus: 800€-1500€ par jour


## Notes Importantes

- L'application utilise `check_same_thread=False` pour SQLite en raison de l'interface graphique
- Les panneaux d'affichage se mettent à jour après chaque entrée/sortie
- Les statistiques d'administration doivent être actualisées manuellement
- Tous les services sont réservés aux abonnés uniquement

## Dépannage

### La base de données n'existe pas
```
Erreur: Table 'X' manquante dans la base de données!
Solution: Exécutez 'python partie3.py' pour créer la base
```

### Problèmes d'affichage
- Vérifier que Tkinter est correctement installé
- Redimensionner la fenêtre si nécessaire (taille minimale: 1100x800)

### Tables manquantes
L'application crée automatiquement:
- Voiturier
- Statistiques_Frequentation
- Maintenance
- Entretien
- Livraison

