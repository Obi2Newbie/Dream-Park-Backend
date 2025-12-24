# DreamPark - Partie 3 : Base de Données SQLite

## Objectif

Créer une base de données SQLite pour le système DreamPark permettant de stocker et gérer toutes les informations du parking de manière persistante.

## Fichier

```
partie3.py    # Script de création et peuplement de la base de données
```

## Structure de la Base de Données

La base de données respecte strictement le diagramme de classes fourni dans le projet.

### Table : Parking

```sql
CREATE TABLE Parking (
    id_parking INTEGER PRIMARY KEY,
    nb_places_par_niveau INTEGER NOT NULL,
    nb_places_libres INTEGER NOT NULL,
    prix REAL NOT NULL,
    nb_niveaux INTEGER NOT NULL
)
```

### Table : Place

```sql
CREATE TABLE Place (
    id_place INTEGER PRIMARY KEY,
    numero INTEGER NOT NULL,
    niveau VARCHAR(10) NOT NULL,
    longueur REAL NOT NULL,
    hauteur REAL NOT NULL,
    est_libre BOOLEAN DEFAULT 1,
    id_parking INTEGER NOT NULL,
    FOREIGN KEY (id_parking) REFERENCES Parking(id_parking)
)
```

### Table : Client

```sql
CREATE TABLE Client (
    id_client INTEGER PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    adresse TEXT,
    est_abonne BOOLEAN DEFAULT 0,
    est_super_abonne BOOLEAN DEFAULT 0,
    nb_frequentation INTEGER DEFAULT 0
)
```

### Table : Voiture

```sql
CREATE TABLE Voiture (
    id_voiture INTEGER PRIMARY KEY,
    immatriculation VARCHAR(20) UNIQUE NOT NULL,
    hauteur REAL NOT NULL,
    longueur REAL NOT NULL,
    est_dans_parking BOOLEAN DEFAULT 0,
    id_client INTEGER NOT NULL,
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
)
```

### Table : Abonnement

```sql
CREATE TABLE Abonnement (
    id_abonnement INTEGER PRIMARY KEY,
    libelle VARCHAR(100) NOT NULL,
    prix REAL NOT NULL,
    est_pack_garanti BOOLEAN DEFAULT 0
)
```

### Table : Contrat

```sql
CREATE TABLE Contrat (
    id_contrat INTEGER PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE,
    est_en_cours BOOLEAN DEFAULT 1,
    id_client INTEGER NOT NULL,
    id_abonnement INTEGER NOT NULL,
    FOREIGN KEY (id_client) REFERENCES Client(id_client),
    FOREIGN KEY (id_abonnement) REFERENCES Abonnement(id_abonnement)
)
```

### Table : Placement

```sql
CREATE TABLE Placement (
    id_placement INTEGER PRIMARY KEY,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME,
    est_en_cours BOOLEAN DEFAULT 1,
    id_voiture INTEGER NOT NULL,
    id_place INTEGER NOT NULL,
    FOREIGN KEY (id_voiture) REFERENCES Voiture(id_voiture),
    FOREIGN KEY (id_place) REFERENCES Place(id_place)
)
```

### Table : Service

```sql
CREATE TABLE Service (
    id_service INTEGER PRIMARY KEY,
    date_demande DATE NOT NULL,
    date_service DATE,
    rapport TEXT
)
```

### Table : Maintenance

```sql
CREATE TABLE Maintenance (
    id_maintenance INTEGER PRIMARY KEY,
    id_service INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    FOREIGN KEY (id_service) REFERENCES Service(id_service),
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
)
```

### Table : Entretien

```sql
CREATE TABLE Entretien (
    id_entretien INTEGER PRIMARY KEY,
    id_service INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    FOREIGN KEY (id_service) REFERENCES Service(id_service),
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
)
```

### Table : Livraison

```sql
CREATE TABLE Livraison (
    id_livraison INTEGER PRIMARY KEY,
    id_service INTEGER NOT NULL,
    adresse TEXT,
    heure VARCHAR(10),
    id_client INTEGER NOT NULL,
    FOREIGN KEY (id_service) REFERENCES Service(id_service),
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
)
```

### Table : Voiturier

```sql
CREATE TABLE Voiturier (
    num_voiturier INTEGER PRIMARY KEY AUTOINCREMENT
)
```

### Table : Statistiques_Frequentation

```sql
CREATE TABLE Statistiques_Frequentation (
    id_stat INTEGER PRIMARY KEY,
    date_stat DATE NOT NULL,
    nb_entrees INTEGER DEFAULT 0,
    nb_sorties INTEGER DEFAULT 0,
    taux_occupation REAL,
    revenue_journalier REAL,
    id_parking INTEGER NOT NULL,
    FOREIGN KEY (id_parking) REFERENCES Parking(id_parking)
)
```

## Utilisation

### Créer la base de données

```bash
python partie3.py
```

Cette commande va :
1. Créer le fichier `dreampark.db`
2. Créer toutes les tables
3. Insérer des données de test :
   - 1 parking avec 4 niveaux
   - 200 places de stationnement (50 par niveau A, B, C, D)
   - 5 clients
   - 5 véhicules
   - 2 types d'abonnements
   - 4 contrats
   - 3 voituriers
   - 1 placement en cours
   - 2 services
   - 30 jours de statistiques

### Consulter la base de données

```bash
sqlite3 dreampark.db
```

## Exemples de Requêtes SQL

### Voir tous les clients
```sql
SELECT * FROM Client;
```

### Voir toutes les places libres
```sql
SELECT * FROM Place WHERE est_libre = 1;
```

### Voir les véhicules actuellement dans le parking
```sql
SELECT v.immatriculation, c.nom
FROM Voiture v
JOIN Client c ON v.id_client = c.id_client
WHERE v.est_dans_parking = 1;
```

### Voir les placements en cours
```sql
SELECT p.date_debut, v.immatriculation, pl.niveau, pl.numero
FROM Placement p
JOIN Voiture v ON p.id_voiture = v.id_voiture
JOIN Place pl ON p.id_place = pl.id_place
WHERE p.est_en_cours = 1;
```

### Voir les contrats actifs
```sql
SELECT c.nom, a.libelle, co.date_debut
FROM Contrat co
JOIN Client c ON co.id_client = c.id_client
JOIN Abonnement a ON co.id_abonnement = a.id_abonnement
WHERE co.est_en_cours = 1;
```

### Calculer le taux d'occupation
```sql
SELECT 
    (COUNT(CASE WHEN est_libre = 0 THEN 1 END) * 100.0 / COUNT(*)) as taux_occupation
FROM Place;
```

## Données de Test Insérées

### Clients
- John Doe (Super Abonné, 10 visites)
- Max Weber (Abonné Standard, 5 visites)
- John Wee (Non abonné, 0 visite)
- Claire Durand (Abonné Standard, 8 visites)
- Pierre Moreau (Super Abonné, 15 visites)

### Véhicules
- FS-590-VS (John Doe)
- FS-888-MW (Max Weber)
- FS-560-VS (John Wee)
- AB-123-CD (Claire Durand)
- EF-456-GH (Pierre Moreau) - actuellement dans le parking

### Abonnements
- Abonnement Standard (30 EUR/mois)
- Super Abonné - Pack Garanti (60 EUR/mois)

## Relations entre Tables

```
Parking 1 ----< * Place
Client 1 ----< * Voiture
Client * ----< * Abonnement (via Contrat)
Voiture 1 ----< * Placement >---- 1 Place
Service 1 ----< 1 Maintenance/Entretien/Livraison
```

## Réinitialiser la Base de Données

Pour recréer la base de données :

```bash
rm dreampark.db
python partie3.py
```

## Informations Techniques

- Base de données : SQLite 3
- Encodage : UTF-8
- Format des dates : YYYY-MM-DD
- Format des dates/heures : YYYY-MM-DD HH:MM:SS