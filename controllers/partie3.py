import sqlite3
from datetime import datetime, date
import random

# =================================================================
# CRÉATION DE LA BASE DE DONNÉES DREAMPARK
# =================================================================

def creer_base_donnees():
    """
    Crée la structure de la base de données DreamPark basée sur le diagramme de classes.
    """

    conn = sqlite3.connect('dreampark.db')
    cursor = conn.cursor()

    # Suppression des tables existantes (pour réinitialisation)
    tables = [
        'Statistiques_Frequentation', 'Service', 'Placement', 'Contrat',
        'Voiture', 'Client', 'Abonnement', 'Place', 'Parking', 'Voiturier'
    ]

    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')

    print("🗄️  Création de la base de données DreamPark...")

    # ============================================================
    # TABLE: PARKING
    # ============================================================
    cursor.execute('''
    CREATE TABLE Parking (
        id_parking INTEGER PRIMARY KEY AUTOINCREMENT,
        nb_places_par_niveau INTEGER NOT NULL,
        nb_places_libres INTEGER NOT NULL,
        prix REAL NOT NULL,
        nb_niveaux INTEGER NOT NULL
    )
    ''')

    # ============================================================
    # TABLE: PLACE
    # ============================================================
    cursor.execute('''
    CREATE TABLE Place (
        id_place INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL,
        niveau VARCHAR(10) NOT NULL,
        longueur REAL NOT NULL,
        hauteur REAL NOT NULL,
        est_libre BOOLEAN DEFAULT 1,
        id_parking INTEGER NOT NULL,
        FOREIGN KEY (id_parking) REFERENCES Parking(id_parking)
    )
    ''')

    # ============================================================
    # TABLE: ABONNEMENT
    # ============================================================
    cursor.execute('''
    CREATE TABLE Abonnement (
        id_abonnement INTEGER PRIMARY KEY AUTOINCREMENT,
        libelle VARCHAR(100) NOT NULL,
        prix REAL NOT NULL,
        est_pack_garanti BOOLEAN DEFAULT 0
    )
    ''')

    # ============================================================
    # TABLE: CLIENT
    # ============================================================
    cursor.execute('''
    CREATE TABLE Client (
        id_client INTEGER PRIMARY KEY AUTOINCREMENT,
        nom VARCHAR(100) NOT NULL,
        adresse TEXT,
        est_abonne BOOLEAN DEFAULT 0,
        est_super_abonne BOOLEAN DEFAULT 0,
        nb_frequentation INTEGER DEFAULT 0
    )
    ''')

    # ============================================================
    # TABLE: VOITURE
    # ============================================================
    cursor.execute('''
    CREATE TABLE Voiture (
        id_voiture INTEGER PRIMARY KEY AUTOINCREMENT,
        immatriculation VARCHAR(20) UNIQUE NOT NULL,
        hauteur REAL NOT NULL,
        longueur REAL NOT NULL,
        est_dans_parking BOOLEAN DEFAULT 0,
        id_client INTEGER NOT NULL,
        FOREIGN KEY (id_client) REFERENCES Client(id_client)
    )
    ''')

    # ============================================================
    # TABLE: CONTRAT
    # ============================================================
    cursor.execute('''
    CREATE TABLE Contrat (
        id_contrat INTEGER PRIMARY KEY AUTOINCREMENT,
        date_debut DATE NOT NULL,
        date_fin DATE,
        est_en_cours BOOLEAN DEFAULT 1,
        id_client INTEGER NOT NULL,
        id_abonnement INTEGER NOT NULL,
        FOREIGN KEY (id_client) REFERENCES Client(id_client),
        FOREIGN KEY (id_abonnement) REFERENCES Abonnement(id_abonnement)
    )
    ''')

    # ============================================================
    # TABLE: PLACEMENT
    # ============================================================
    cursor.execute('''
    CREATE TABLE Placement (
        id_placement INTEGER PRIMARY KEY AUTOINCREMENT,
        date_debut DATETIME NOT NULL,
        date_fin DATETIME,
        est_en_cours BOOLEAN DEFAULT 1,
        id_voiture INTEGER NOT NULL,
        id_place INTEGER NOT NULL,
        FOREIGN KEY (id_voiture) REFERENCES Voiture(id_voiture),
        FOREIGN KEY (id_place) REFERENCES Place(id_place)
    )
    ''')

    # ============================================================
    # TABLE: SERVICE
    # ============================================================
    cursor.execute('''
    CREATE TABLE Service (
        id_service INTEGER PRIMARY KEY AUTOINCREMENT,
        date_demande DATE NOT NULL,
        date_service DATE,
        rapport TEXT
    )
    ''')

    # ============================================================
    # TABLE: MAINTENANCE (hérite de Service)
    # ============================================================
    cursor.execute('''
    CREATE TABLE Maintenance (
        id_maintenance INTEGER PRIMARY KEY AUTOINCREMENT,
        id_service INTEGER NOT NULL,
        id_client INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES Service(id_service),
        FOREIGN KEY (id_client) REFERENCES Client(id_client)
    )
    ''')

    # ============================================================
    # TABLE: ENTRETIEN (hérite de Service)
    # ============================================================
    cursor.execute('''
    CREATE TABLE Entretien (
        id_entretien INTEGER PRIMARY KEY AUTOINCREMENT,
        id_service INTEGER NOT NULL,
        id_client INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES Service(id_service),
        FOREIGN KEY (id_client) REFERENCES Client(id_client)
    )
    ''')

    # ============================================================
    # TABLE: LIVRAISON (hérite de Service)
    # ============================================================
    cursor.execute('''
    CREATE TABLE Livraison (
        id_livraison INTEGER PRIMARY KEY AUTOINCREMENT,
        id_service INTEGER NOT NULL,
        adresse TEXT,
        heure VARCHAR(10),
        id_client INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES Service(id_service),
        FOREIGN KEY (id_client) REFERENCES Client(id_client)
    )
    ''')

    # ============================================================
    # TABLE: VOITURIER
    # ============================================================
    cursor.execute('''
    CREATE TABLE Voiturier (
        num_voiturier INTEGER PRIMARY KEY AUTOINCREMENT
    )
    ''')

    # ============================================================
    # TABLE: STATISTIQUES_FREQUENTATION
    # ============================================================
    cursor.execute('''
    CREATE TABLE Statistiques_Frequentation (
        id_stat INTEGER PRIMARY KEY AUTOINCREMENT,
        date_stat DATE NOT NULL,
        nb_entrees INTEGER DEFAULT 0,
        nb_sorties INTEGER DEFAULT 0,
        taux_occupation REAL,
        revenue_journalier REAL,
        id_parking INTEGER NOT NULL,
        FOREIGN KEY (id_parking) REFERENCES Parking(id_parking)
    )
    ''')

    conn.commit()
    print("✅ Structure de la base de données créée avec succès!\n")

    return conn


def peupler_base_donnees(conn):
    """
    Remplit la base de données avec des données de test.
    """
    cursor = conn.cursor()

    print("📊 Population de la base de données...")

    # ============================================================
    # 1. INSERTION DU PARKING
    # ============================================================
    print("\n1️⃣  Insertion du parking...")
    cursor.execute('''
    INSERT INTO Parking (nb_places_par_niveau, nb_places_libres, prix, nb_niveaux)
    VALUES (50, 200, 10.50, 4)
    ''')
    id_parking = cursor.lastrowid
    print(f"   ✓ Parking créé (ID: {id_parking})")

    # ============================================================
    # 2. INSERTION DES PLACES
    # ============================================================
    print("2️⃣  Création des places de stationnement...")
    niveaux = ['A', 'B', 'C', 'D']
    places_creees = 0

    for niveau in niveaux:
        for numero in range(1, 51):  # 50 places par niveau
            longueur = random.choice([4.5, 5.0, 5.5, 6.0])
            hauteur = random.choice([2.0, 2.1, 2.5])
            cursor.execute('''
            INSERT INTO Place (numero, niveau, longueur, hauteur, est_libre, id_parking)
            VALUES (?, ?, ?, ?, 1, ?)
            ''', (numero, niveau, longueur, hauteur, id_parking))
            places_creees += 1

    print(f"   ✓ {places_creees} places créées")

    # ============================================================
    # 3. INSERTION DES ABONNEMENTS
    # ============================================================
    print("3️⃣  Création des formules d'abonnement...")
    abonnements_data = [
        ('Abonnement Standard', 30.0, 0),
        ('Super Abonné - Pack Garanti', 60.0, 1),
    ]

    abonnements = []
    for libelle, prix, pack_gar in abonnements_data:
        cursor.execute('''
        INSERT INTO Abonnement (libelle, prix, est_pack_garanti)
        VALUES (?, ?, ?)
        ''', (libelle, prix, pack_gar))
        abonnements.append(cursor.lastrowid)

    print(f"   ✓ {len(abonnements)} formules créées")

    # ============================================================
    # 4. INSERTION DES VOITURIERS
    # ============================================================
    print("4️⃣  Création des voituriers...")
    for _ in range(3):
        cursor.execute('INSERT INTO Voiturier DEFAULT VALUES')

    print(f"   ✓ 3 voituriers créés")

    # ============================================================
    # 5. INSERTION DES CLIENTS
    # ============================================================
    print("5️⃣  Enregistrement des clients...")

    clients_data = [
        ('John Doe', '19 Evergreen Terrace', 1, 1, 10),
        ('Max Weber', 'Something Street', 1, 0, 5),
        ('John Wee', '6 Impasse Simone', 0, 0, 0),
        ('Claire Durand', '15 Rue des Fleurs', 1, 0, 8),
        ('Pierre Moreau', '88 Boulevard Victor Hugo', 1, 1, 15),
    ]

    clients = []
    for nom, adresse, abonne, super_ab, freq in clients_data:
        cursor.execute('''
        INSERT INTO Client (nom, adresse, est_abonne, est_super_abonne, nb_frequentation)
        VALUES (?, ?, ?, ?, ?)
        ''', (nom, adresse, abonne, super_ab, freq))
        clients.append(cursor.lastrowid)

    print(f"   ✓ {len(clients)} clients enregistrés")

    # ============================================================
    # 6. INSERTION DES VOITURES
    # ============================================================
    print("6️⃣  Enregistrement des véhicules...")

    voitures_data = [
        ('FS-590-VS', 1.90, 4.00, 0, clients[0]),
        ('FS-888-MW', 1.80, 3.50, 0, clients[1]),
        ('FS-560-VS', 2.00, 5.00, 0, clients[2]),
        ('AB-123-CD', 1.75, 4.20, 0, clients[3]),
        ('EF-456-GH', 2.10, 4.80, 1, clients[4]),
    ]

    voitures = []
    for immat, haut, long, dans_park, id_cli in voitures_data:
        cursor.execute('''
        INSERT INTO Voiture (immatriculation, hauteur, longueur, est_dans_parking, id_client)
        VALUES (?, ?, ?, ?, ?)
        ''', (immat, haut, long, dans_park, id_cli))
        voitures.append(cursor.lastrowid)

    print(f"   ✓ {len(voitures)} véhicules enregistrés")

    # ============================================================
    # 7. INSERTION DES CONTRATS
    # ============================================================
    print("7️⃣  Création des contrats d'abonnement...")

    contrats_data = [
        (clients[0], abonnements[1], '2023-01-10', None, 1),  # John Doe - Super Abonné
        (clients[1], abonnements[0], '2023-05-15', None, 1),  # Max Weber - Standard
        (clients[3], abonnements[0], '2023-08-22', None, 1),  # Claire Durand - Standard
        (clients[4], abonnements[1], '2022-11-05', None, 1),  # Pierre Moreau - Super Abonné
    ]

    for id_cli, id_abo, date_deb, date_fin, en_cours in contrats_data:
        cursor.execute('''
        INSERT INTO Contrat (id_client, id_abonnement, date_debut, date_fin, est_en_cours)
        VALUES (?, ?, ?, ?, ?)
        ''', (id_cli, id_abo, date_deb, date_fin, en_cours))

    print(f"   ✓ {len(contrats_data)} contrats créés")

    # ============================================================
    # 8. INSERTION DE QUELQUES PLACEMENTS
    # ============================================================
    print("8️⃣  Génération de l'historique des stationnements...")

    # Un placement en cours
    cursor.execute('''
    INSERT INTO Placement (id_voiture, id_place, date_debut, date_fin, est_en_cours)
    VALUES (?, ?, ?, NULL, 1)
    ''', (voitures[4], 45, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    # Marquer la place comme occupée
    cursor.execute('UPDATE Place SET est_libre = 0 WHERE id_place = ?', (45,))

    print(f"   ✓ Placements créés")

    # ============================================================
    # 9. INSERTION DE QUELQUES SERVICES
    # ============================================================
    print("9️⃣  Enregistrement des services...")

    # Service Maintenance
    cursor.execute('''
    INSERT INTO Service (date_demande, date_service, rapport)
    VALUES (?, NULL, 'Maintenance non effectué')
    ''', (date.today(),))
    id_service_maint = cursor.lastrowid

    cursor.execute('''
    INSERT INTO Maintenance (id_service, id_client)
    VALUES (?, ?)
    ''', (id_service_maint, clients[1]))

    # Service Livraison
    cursor.execute('''
    INSERT INTO Service (date_demande, date_service, rapport)
    VALUES (?, NULL, 'Livraison non effectuée')
    ''', (date.today(),))
    id_service_liv = cursor.lastrowid

    cursor.execute('''
    INSERT INTO Livraison (id_service, adresse, heure, id_client)
    VALUES (?, ?, ?, ?)
    ''', (id_service_liv, 'Something Street', '18', clients[1]))

    print(f"   ✓ Services enregistrés")

    # ============================================================
    # 10. GÉNÉRATION DES STATISTIQUES
    # ============================================================
    print("🔟 Génération des statistiques de fréquentation...")

    from datetime import timedelta

    for jour in range(30):
        date_stat = (datetime.now() - timedelta(days=jour)).date()
        nb_entrees = random.randint(80, 150)
        nb_sorties = random.randint(75, 145)
        taux_occ = random.uniform(0.45, 0.95)
        revenue = random.uniform(800, 1500)

        cursor.execute('''
        INSERT INTO Statistiques_Frequentation (date_stat, nb_entrees, nb_sorties, taux_occupation, revenue_journalier, id_parking)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (date_stat, nb_entrees, nb_sorties, round(taux_occ, 2), round(revenue, 2), id_parking))

    print(f"   ✓ 30 jours de statistiques générées")

    conn.commit()
    print("\n✅ Base de données entièrement peuplée!\n")


def afficher_statistiques(conn):
    """
    Affiche un résumé des données dans la base.
    """
    cursor = conn.cursor()

    print("=" * 70)
    print("📊 RÉSUMÉ DES DONNÉES DREAMPARK")
    print("=" * 70)

    cursor.execute('SELECT COUNT(*) FROM Client')
    nb_clients = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM Client WHERE est_abonne = 1')
    nb_abonnes = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM Voiture')
    nb_voitures = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM Place')
    nb_places_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM Place WHERE est_libre = 1')
    nb_places_libres = cursor.fetchone()[0]

    print(f"\n👥 CLIENTS: {nb_clients} (dont {nb_abonnes} abonnés)")
    print(f"🚗 VÉHICULES: {nb_voitures}")
    print(f"🅿️  PLACES: {nb_places_total} (dont {nb_places_libres} libres)")
    print(f"📊 Taux occupation: {((nb_places_total - nb_places_libres) / nb_places_total * 100):.1f}%")

    print("\n" + "=" * 70)


def main():
    """
    Point d'entrée principal.
    """
    print("\n" + "=" * 70)
    print("🚀 INITIALISATION DE LA BASE DE DONNÉES DREAMPARK")
    print("=" * 70 + "\n")

    # Créer la structure
    conn = creer_base_donnees()

    # Peupler avec des données
    peupler_base_donnees(conn)

    # Afficher les statistiques
    afficher_statistiques(conn)

    # Fermer la connexion
    conn.close()

    print("\n✨ Base de données 'dreampark.db' prête à l'emploi!")
    print("   Vous pouvez maintenant l'utiliser dans votre application.\n")


if __name__ == "__main__":
    main()