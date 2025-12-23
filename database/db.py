import sqlite3 as sql

conn = sql.connect("parking.db")
cur = conn.cursor()

sql_script = """
CREATE TABLE IF NOT EXISTS Client (
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    adresse TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Abonnement (
    id_abonnement INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    type_abonnement TEXT DEFAULT "estAbonne" CHECK (type_abonnement IN ('estAbonne', 'estSuperAbonne')),
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
);

CREATE TABLE IF NOT EXISTS Place (
    id_place INTEGER PRIMARY KEY AUTOINCREMENT,
    niveau INTEGER,
    longueur REAL,
    hauteur REAL,
    est_occupee BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Vehicule (
    immatriculation TEXT PRIMARY KEY,
    longueur REAL,
    hauteur REAL,
    id_client INTEGER,
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
);

CREATE TABLE IF NOT EXISTS Service(
    id_service INTEGER PRIMARY KEY AUTOINCREMENT,
    type_service TEXT NOT NULL CHECK (type_service IN ('Livraison', 'Entretien', 'Maintenance')),
    id_voiture TEXT NOT NULL,
    FOREIGN KEY (id_voiture) REFERENCES Vehicule(immatriculation)
);

CREATE TABLE IF NOT EXISTS Ticket (
    id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vehicule TEXT NOT NULL,
    id_place INTEGER,
    date_entree DATETIME NOT NULL,
    date_sortie DATETIME,
    mode_paiement  TEXT DEFAULT "CB" CHECK (mode_paiement IN ('CB', 'ESPECES', 'ABONNEMENT')),
    montant REAL,
    FOREIGN KEY (id_vehicule) REFERENCES Vehicule(immatriculation),
    FOREIGN KEY (id_place) REFERENCES Place(id_place)
);

CREATE TABLE IF NOT EXISTS Livraison (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    adresse TEXT NOT NULL,
    heure_livraison DATETIME,
    statut TEXT DEFAULT 'en attente',
    FOREIGN KEY (ticket_id) REFERENCES Ticket(id_ticket)
);

CREATE TABLE IF NOT EXISTS Historique (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vehicule TEXT NOT NULL,
    action TEXT,
    date_action DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_vehicule) REFERENCES Vehicule(immatriculation)
);
"""

cur.executescript(sql_script)
conn.commit()
conn.close()