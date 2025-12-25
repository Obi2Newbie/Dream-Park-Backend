import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import random
import time
import threading


# ============================================================================
# MODEL (MVC Pattern)
# ============================================================================

class DreamParkModel:
    """Modèle - Gestion base de données et logique métier"""

    def __init__(self, db_path='dreampark.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.verifier_tables()

    def verifier_tables(self):
        """Vérifie que toutes les tables nécessaires existent"""
        try:
            # Vérifier les tables critiques
            tables_requises = [
                'Parking', 'Place', 'Client', 'Voiture', 'Abonnement',
                'Contrat', 'Placement', 'Service'
            ]

            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables_existantes = [row[0] for row in self.cursor.fetchall()]

            for table in tables_requises:
                if table not in tables_existantes:
                    raise Exception(
                        f"Table '{table}' manquante dans la base de données!\nExécutez 'python partie3.py' pour créer la base.")

            # Créer la table Voiturier si elle n'existe pas
            if 'Voiturier' not in tables_existantes:
                print("⚠️ Création de la table Voiturier...")
                self.cursor.execute('''
                                    CREATE TABLE Voiturier
                                    (
                                        num_voiturier INTEGER PRIMARY KEY AUTOINCREMENT
                                    )
                                    ''')

                # Ajouter 3 voituriers par défaut
                for _ in range(3):
                    self.cursor.execute('INSERT INTO Voiturier DEFAULT VALUES')

                self.conn.commit()
                print("✅ Table Voiturier créée avec 3 voituriers")

            # Créer la table Statistiques_Frequentation si elle n'existe pas
            if 'Statistiques_Frequentation' not in tables_existantes:
                print("⚠️ Création de la table Statistiques_Frequentation...")
                self.cursor.execute('''
                                    CREATE TABLE Statistiques_Frequentation
                                    (
                                        id_stat            INTEGER PRIMARY KEY AUTOINCREMENT,
                                        date_stat          DATE    NOT NULL,
                                        nb_entrees         INTEGER DEFAULT 0,
                                        nb_sorties         INTEGER DEFAULT 0,
                                        taux_occupation    REAL,
                                        revenue_journalier REAL,
                                        id_parking         INTEGER NOT NULL,
                                        FOREIGN KEY (id_parking) REFERENCES Parking (id_parking)
                                    )
                                    ''')

                # Générer quelques statistiques de base
                from datetime import timedelta
                for jour in range(30):
                    date_stat = (datetime.now() - timedelta(days=jour)).date()
                    nb_entrees = random.randint(80, 150)
                    nb_sorties = random.randint(75, 145)
                    taux_occ = random.uniform(0.45, 0.95)
                    revenue = random.uniform(800, 1500)

                    self.cursor.execute('''
                                        INSERT INTO Statistiques_Frequentation
                                        (date_stat, nb_entrees, nb_sorties, taux_occupation, revenue_journalier,
                                         id_parking)
                                        VALUES (?, ?, ?, ?, ?, 1)
                                        ''', (date_stat, nb_entrees, nb_sorties, round(taux_occ, 2), round(revenue, 2)))

                self.conn.commit()
                print("✅ Table Statistiques_Frequentation créée avec succès")

            # Créer les tables de services si elles n'existent pas
            if 'Maintenance' not in tables_existantes:
                print("⚠️ Création de la table Maintenance...")
                self.cursor.execute('''
                                    CREATE TABLE Maintenance
                                    (
                                        id_maintenance INTEGER PRIMARY KEY AUTOINCREMENT,
                                        id_service     INTEGER NOT NULL,
                                        id_client      INTEGER NOT NULL,
                                        FOREIGN KEY (id_service) REFERENCES Service (id_service),
                                        FOREIGN KEY (id_client) REFERENCES Client (id_client)
                                    )
                                    ''')
                self.conn.commit()
                print("✅ Table Maintenance créée")

            if 'Entretien' not in tables_existantes:
                print("⚠️ Création de la table Entretien...")
                self.cursor.execute('''
                                    CREATE TABLE Entretien
                                    (
                                        id_entretien INTEGER PRIMARY KEY AUTOINCREMENT,
                                        id_service   INTEGER NOT NULL,
                                        id_client    INTEGER NOT NULL,
                                        FOREIGN KEY (id_service) REFERENCES Service (id_service),
                                        FOREIGN KEY (id_client) REFERENCES Client (id_client)
                                    )
                                    ''')
                self.conn.commit()
                print("✅ Table Entretien créée")

            if 'Livraison' not in tables_existantes:
                print("⚠️ Création de la table Livraison...")
                self.cursor.execute('''
                                    CREATE TABLE Livraison
                                    (
                                        id_livraison INTEGER PRIMARY KEY AUTOINCREMENT,
                                        id_service   INTEGER NOT NULL,
                                        adresse      TEXT,
                                        heure        VARCHAR(10),
                                        id_client    INTEGER NOT NULL,
                                        FOREIGN KEY (id_service) REFERENCES Service (id_service),
                                        FOREIGN KEY (id_client) REFERENCES Client (id_client)
                                    )
                                    ''')
                self.conn.commit()
                print("✅ Table Livraison créée")

        except Exception as e:
            print(f"❌ Erreur lors de la vérification des tables: {e}")
            raise

    def generer_ticket(self):
        """Génère un ticket unique"""
        return f"TKT-{int(time.time())}-{random.randint(1000, 9999)}"

    def obtenir_voiturier_disponible(self):
        """Retourne un voiturier aléatoire"""
        self.cursor.execute("SELECT num_voiturier FROM Voiturier ORDER BY RANDOM() LIMIT 1")
        result = self.cursor.fetchone()
        return result[0] if result else 1

    def ajouter_nouveau_client(self, nom, adresse, est_abonne, est_super_abonne):
        """Ajoute un nouveau client"""
        try:
            self.cursor.execute("""
                                INSERT INTO Client (nom, adresse, est_abonne, est_super_abonne, nb_frequentation)
                                VALUES (?, ?, ?, ?, 0)
                                """, (nom, adresse, 1 if est_abonne else 0, 1 if est_super_abonne else 0))
            self.conn.commit()
            return True, self.cursor.lastrowid
        except Exception as e:
            return False, str(e)

    def ajouter_nouveau_vehicule(self, immatriculation, hauteur, longueur, id_client):
        """Ajoute un nouveau véhicule"""
        try:
            self.cursor.execute("""
                                INSERT INTO Voiture (immatriculation, hauteur, longueur, est_dans_parking, id_client)
                                VALUES (?, ?, ?, 0, ?)
                                """, (immatriculation.upper(), hauteur, longueur, id_client))
            self.conn.commit()
            return True, self.cursor.lastrowid
        except Exception as e:
            return False, str(e)

    def creer_contrat_abonnement(self, id_client, type_abonnement):
        """Crée un contrat d'abonnement"""
        try:
            if type_abonnement == "super":
                self.cursor.execute("SELECT id_abonnement FROM Abonnement WHERE est_pack_garanti = 1 LIMIT 1")
            else:
                self.cursor.execute("SELECT id_abonnement FROM Abonnement WHERE est_pack_garanti = 0 LIMIT 1")

            abonnement = self.cursor.fetchone()
            if not abonnement:
                return False, "Type d'abonnement introuvable"

            self.cursor.execute("""
                                INSERT INTO Contrat (date_debut, id_client, id_abonnement, est_en_cours)
                                VALUES (?, ?, ?, 1)
                                """, (datetime.now().date(), id_client, abonnement[0]))
            self.conn.commit()
            return True, "Contrat créé"
        except Exception as e:
            return False, str(e)

    def simuler_entree_vehicule(self, immatriculation, mode_paiement="CB"):
        """Simule l'entrée d'un véhicule avec caméra et téléporteur"""
        immat = immatriculation.upper().strip()

        # Vérifier si le véhicule existe
        self.cursor.execute("""
                            SELECT v.id_voiture,
                                   v.hauteur,
                                   v.longueur,
                                   v.est_dans_parking,
                                   c.id_client,
                                   c.nom,
                                   c.est_abonne,
                                   c.est_super_abonne
                            FROM Voiture v
                                     JOIN Client c ON v.id_client = c.id_client
                            WHERE v.immatriculation = ?
                            """, (immat,))

        vehicule = self.cursor.fetchone()

        if not vehicule:
            return None, "NOUVEAU_VEHICULE", None

        id_voiture, hauteur, longueur, dans_parking, id_client, nom, est_abonne, est_super_abonne = vehicule

        if dans_parking:
            return False, f"❌ Véhicule {immat} déjà dans le parking", None

        # Chercher une place compatible
        self.cursor.execute("""
                            SELECT id_place, niveau, numero
                            FROM Place
                            WHERE est_libre = 1
                              AND hauteur >= ?
                              AND longueur >= ?
                            ORDER BY niveau, numero LIMIT 1
                            """, (hauteur, longueur))

        place = self.cursor.fetchone()
        ticket = self.generer_ticket()

        if place:
            id_place, niveau, numero = place

            # Créer le placement
            self.cursor.execute("""
                                INSERT INTO Placement (date_debut, id_voiture, id_place, est_en_cours)
                                VALUES (?, ?, ?, 1)
                                """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id_voiture, id_place))

            # Mettre à jour les statuts
            self.cursor.execute("UPDATE Place SET est_libre = 0 WHERE id_place = ?", (id_place,))
            self.cursor.execute("UPDATE Voiture SET est_dans_parking = 1 WHERE id_voiture = ?", (id_voiture,))
            self.cursor.execute("UPDATE Parking SET nb_places_libres = nb_places_libres - 1")
            self.cursor.execute("UPDATE Client SET nb_frequentation = nb_frequentation + 1 WHERE id_client = ?",
                                (id_client,))

            self.conn.commit()

            type_client = "Super Abonné" if est_super_abonne else ("Abonné" if est_abonne else "Standard")
            voiturier = self.obtenir_voiturier_disponible()

            return True, {
                'nom': nom,
                'type_client': type_client,
                'place': f"{niveau}{numero}",
                'ticket': ticket,
                'mode_paiement': mode_paiement,
                'voiturier': voiturier,
                'hauteur': hauteur,
                'longueur': longueur,
                'pack_garanti': False
            }, ticket

        elif est_super_abonne:
            # Pack Garanti - Service Valet
            self.cursor.execute("UPDATE Voiture SET est_dans_parking = 1 WHERE id_voiture = ?", (id_voiture,))
            self.conn.commit()

            voiturier = self.obtenir_voiturier_disponible()
            return True, {
                'nom': nom,
                'pack_garanti': True,
                'ticket': ticket,
                'voiturier': voiturier,
                'mode_paiement': mode_paiement
            }, ticket

        else:
            return False, f"❌ Aucune place compatible (H={hauteur}m, L={longueur}m)", None

    def simuler_sortie_vehicule(self, ticket_ou_immat):
        """Simule la sortie d'un véhicule avec téléporteur"""
        immat = ticket_ou_immat.upper().strip()

        self.cursor.execute("""
                            SELECT v.id_voiture,
                                   v.immatriculation,
                                   p.id_placement,
                                   p.id_place,
                                   p.date_debut,
                                   c.nom,
                                   c.est_abonne,
                                   c.est_super_abonne,
                                   pl.niveau,
                                   pl.numero
                            FROM Voiture v
                                     JOIN Placement p ON v.id_voiture = p.id_voiture
                                     JOIN Client c ON v.id_client = c.id_client
                                     LEFT JOIN Place pl ON p.id_place = pl.id_place
                            WHERE v.immatriculation = ?
                              AND p.est_en_cours = 1
                            """, (immat,))

        placement = self.cursor.fetchone()

        if not placement:
            return False, "❌ Véhicule non trouvé ou pas actuellement stationné", None

        id_voiture, immatriculation, id_placement, id_place, date_debut, nom, est_abonne, est_super_abonne, niveau, numero = placement

        # Calculer durée et tarif
        debut = datetime.strptime(date_debut, '%Y-%m-%d %H:%M:%S')
        fin = datetime.now()
        duree = (fin - debut).total_seconds() / 3600

        if est_super_abonne:
            tarif = 0
            type_tarif = "Super Abonné - Gratuit"
        elif est_abonne:
            tarif = 5.5
            type_tarif = "Abonné"
        else:
            self.cursor.execute("SELECT prix FROM Parking LIMIT 1")
            prix_heure = self.cursor.fetchone()[0]
            tarif = max(prix_heure, duree * prix_heure)
            type_tarif = "Standard"

        # Libérer la place
        if id_place:
            self.cursor.execute("UPDATE Place SET est_libre = 1 WHERE id_place = ?", (id_place,))

        self.cursor.execute("UPDATE Voiture SET est_dans_parking = 0 WHERE id_voiture = ?", (id_voiture,))
        self.cursor.execute("""
                            UPDATE Placement
                            SET est_en_cours = 0,
                                date_fin     = ?
                            WHERE id_placement = ?
                            """, (fin.strftime('%Y-%m-%d %H:%M:%S'), id_placement))
        self.cursor.execute("UPDATE Parking SET nb_places_libres = nb_places_libres + 1")

        self.conn.commit()

        voiturier = self.obtenir_voiturier_disponible()
        place_str = f"{niveau}{numero}" if niveau and numero else "Parking Partenaire"

        return True, {
            'nom': nom,
            'immatriculation': immatriculation,
            'duree': duree,
            'tarif': tarif,
            'type_tarif': type_tarif,
            'place': place_str,
            'voiturier': voiturier
        }, tarif

    def demander_service_livraison(self, client_nom, adresse, heure):
        """Service de livraison"""
        self.cursor.execute("SELECT id_client, est_abonne FROM Client WHERE nom LIKE ?", (f"%{client_nom}%",))
        client = self.cursor.fetchone()

        if not client:
            return False, "Client non trouvé"

        id_client, est_abonne = client
        if not est_abonne:
            return False, "Service réservé aux abonnés"

        self.cursor.execute("INSERT INTO Service (date_demande, rapport) VALUES (?, 'Livraison demandée')",
                            (datetime.now().date(),))
        id_service = self.cursor.lastrowid

        self.cursor.execute("INSERT INTO Livraison (id_service, adresse, heure, id_client) VALUES (?, ?, ?, ?)",
                            (id_service, adresse, heure, id_client))

        self.conn.commit()
        voiturier = self.obtenir_voiturier_disponible()
        return True, f"✅ Livraison enregistrée\n📍 {adresse}\n⏰ {heure}h\n🚗 Voiturier #{voiturier}"

    def demander_service_entretien(self, immatriculation):
        """Service d'entretien"""
        self.cursor.execute("""
                            SELECT v.id_voiture, c.id_client, c.nom, c.est_abonne
                            FROM Voiture v
                                     JOIN Client c ON v.id_client = c.id_client
                            WHERE v.immatriculation = ?
                            """, (immatriculation.upper(),))

        vehicule = self.cursor.fetchone()
        if not vehicule:
            return False, "Véhicule non trouvé"

        _, id_client, nom, est_abonne = vehicule
        if not est_abonne:
            return False, "Service réservé aux abonnés"

        self.cursor.execute("INSERT INTO Service (date_demande, rapport) VALUES (?, 'Entretien demandé')",
                            (datetime.now().date(),))
        id_service = self.cursor.lastrowid

        self.cursor.execute("INSERT INTO Entretien (id_service, id_client) VALUES (?, ?)",
                            (id_service, id_client))

        self.conn.commit()
        return True, f"✅ Entretien enregistré pour {nom}"

    def demander_service_maintenance(self, immatriculation):
        """Service de maintenance"""
        self.cursor.execute("""
                            SELECT v.id_voiture, c.id_client, c.nom, c.est_abonne
                            FROM Voiture v
                                     JOIN Client c ON v.id_client = c.id_client
                            WHERE v.immatriculation = ?
                            """, (immatriculation.upper(),))

        vehicule = self.cursor.fetchone()
        if not vehicule:
            return False, "Véhicule non trouvé"

        _, id_client, nom, est_abonne = vehicule
        if not est_abonne:
            return False, "Service réservé aux abonnés"

        self.cursor.execute("INSERT INTO Service (date_demande, rapport) VALUES (?, 'Maintenance demandée')",
                            (datetime.now().date(),))
        id_service = self.cursor.lastrowid

        self.cursor.execute("INSERT INTO Maintenance (id_service, id_client) VALUES (?, ?)",
                            (id_service, id_client))

        self.conn.commit()
        return True, f"✅ Maintenance enregistrée pour {nom}"

    def modifier_service(self, id_service, nouvelle_adresse=None, nouvelle_heure=None):
        """Modifier un service existant (flexibilité téléphonique)"""
        try:
            if nouvelle_adresse:
                self.cursor.execute("UPDATE Livraison SET adresse = ? WHERE id_service = ?",
                                    (nouvelle_adresse, id_service))
            if nouvelle_heure:
                self.cursor.execute("UPDATE Livraison SET heure = ? WHERE id_service = ?",
                                    (nouvelle_heure, id_service))

            self.cursor.execute("UPDATE Service SET rapport = ? WHERE id_service = ?",
                                (f"Modifié le {datetime.now()}", id_service))
            self.conn.commit()
            return True, "Service modifié"
        except Exception as e:
            return False, str(e)

    def obtenir_statistiques(self):
        """Statistiques du parking"""
        stats = {}
        self.cursor.execute("SELECT COUNT(*) FROM Place")
        stats['total_places'] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Place WHERE est_libre = 1")
        stats['places_libres'] = self.cursor.fetchone()[0]

        stats['places_occupees'] = stats['total_places'] - stats['places_libres']
        stats['taux_occupation'] = (stats['places_occupees'] / stats['total_places'] * 100) if stats[
                                                                                                   'total_places'] > 0 else 0

        self.cursor.execute("SELECT COUNT(*) FROM Client")
        stats['total_clients'] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Voiture WHERE est_dans_parking = 1")
        stats['vehicules_presents'] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Service WHERE date_service IS NULL")
        stats['services_en_attente'] = self.cursor.fetchone()[0]

        return stats

    def obtenir_derniers_mouvements(self, limite=20):
        """Derniers mouvements"""
        self.cursor.execute("""
                            SELECT v.immatriculation,
                                   c.nom,
                                   p.date_debut,
                                   p.date_fin,
                                   pl.niveau,
                                   pl.numero,
                                   p.est_en_cours
                            FROM Placement p
                                     JOIN Voiture v ON p.id_voiture = v.id_voiture
                                     JOIN Client c ON v.id_client = c.id_client
                                     LEFT JOIN Place pl ON p.id_place = pl.id_place
                            ORDER BY p.date_debut DESC LIMIT ?
                            """, (limite,))
        return self.cursor.fetchall()

    def obtenir_revenus_recents(self, jours=14):
        """Revenus récents"""
        try:
            self.cursor.execute("""
                                SELECT date_stat, nb_entrees, nb_sorties, taux_occupation, revenue_journalier
                                FROM Statistiques_Frequentation
                                ORDER BY date_stat DESC LIMIT ?
                                """, (jours,))
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"⚠️ Erreur lors de la récupération des revenus: {e}")
            return []

    def obtenir_services_en_attente(self):
        """Services en attente"""
        try:
            self.cursor.execute("""
                                SELECT s.id_service, s.date_demande, c.nom, l.adresse, l.heure, 'Livraison' as type
                                FROM Service s
                                         JOIN Livraison l ON s.id_service = l.id_service
                                         JOIN Client c ON l.id_client = c.id_client
                                WHERE s.date_service IS NULL
                                UNION
                                SELECT s.id_service, s.date_demande, c.nom, NULL, NULL, 'Entretien'
                                FROM Service s
                                         JOIN Entretien e ON s.id_service = e.id_service
                                         JOIN Client c ON e.id_client = c.id_client
                                WHERE s.date_service IS NULL
                                UNION
                                SELECT s.id_service, s.date_demande, c.nom, NULL, NULL, 'Maintenance'
                                FROM Service s
                                         JOIN Maintenance m ON s.id_service = m.id_service
                                         JOIN Client c ON m.id_client = c.id_client
                                WHERE s.date_service IS NULL
                                """)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"⚠️ Erreur lors de la récupération des services: {e}")
            return []

    def close(self):
        self.conn.close()


# ============================================================================
# CONTROLLER (MVC Pattern)
# ============================================================================

class DreamParkController:
    """Contrôleur - Logique de contrôle"""

    def __init__(self):
        self.model = DreamParkModel()
        self.view = None

    def set_view(self, view):
        self.view = view

    def traiter_entree(self):
        """Traite l'entrée d'un véhicule"""
        if not self.view:
            return

        immat = self.view.entry_immat_entree.get().strip()
        if not immat:
            messagebox.showerror("Erreur", "Entrez une immatriculation")
            return

        mode_paiement = self.view.var_paiement.get()
        acces = self.view.var_acces_entree.get()

        success, result, ticket = self.model.simuler_entree_vehicule(immat, mode_paiement)

        if success is None and result == "NOUVEAU_VEHICULE":
            reponse = messagebox.askyesno(
                "Véhicule Non Enregistré",
                f"Le véhicule {immat} n'existe pas.\n\nEnregistrer ce nouveau client/véhicule?"
            )
            if reponse:
                self.view.ouvrir_formulaire_nouveau_client(immat)
            return

        # Afficher résultat
        self.view.text_resultat_entree.delete(1.0, tk.END)
        self.view.text_resultat_entree.insert(tk.END, "=" * 70 + "\n")
        self.view.text_resultat_entree.insert(tk.END,
                                              f"🎫 ENTRÉE - ACCÈS {acces.upper()} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.view.text_resultat_entree.insert(tk.END, "=" * 70 + "\n\n")

        if success:
            if result.get('pack_garanti'):
                message = f"""✨ PACK GARANTI ACTIVÉ

🚗 Client: {result['nom']}
🎫 Ticket: {result['ticket']}
💳 Paiement: {result['mode_paiement']}
👤 Voiturier #{result['voiturier']}: En charge

⚡ SERVICE VALET ACTIVÉ
Votre véhicule sera stationné dans un parking partenaire.
Un voiturier vous contactera à votre retour."""
            else:
                message = f"""✅ ENTRÉE VALIDÉE

🚗 Client: {result['nom']} ({result['type_client']})
🎫 Ticket: {result['ticket']}
🅿️  Place assignée: {result['place']}
💳 Paiement: {result['mode_paiement']}
📏 Dimensions: H={result['hauteur']}m, L={result['longueur']}m
👤 Voiturier #{result['voiturier']}: Assigné

⚡ TÉLÉPORTEUR ACTIVÉ
Votre véhicule est en cours de téléportation...
└─→ Niveau {result['place'][0]} - Place {result['place'][1:]}

✓ Téléportation terminée! Bonne journée!"""

            self.view.text_resultat_entree.insert(tk.END, message)
            messagebox.showinfo("Succès", f"Entrée validée!\nTicket: {ticket}")
            self.view.entry_immat_entree.delete(0, tk.END)
            self.update_display()
        else:
            self.view.text_resultat_entree.insert(tk.END, result)
            messagebox.showerror("Erreur", result)

    def traiter_sortie(self):
        """Traite la sortie d'un véhicule"""
        if not self.view:
            return

        immat_ticket = self.view.entry_immat_sortie.get().strip()
        if not immat_ticket:
            messagebox.showerror("Erreur", "Entrez une immatriculation ou un ticket")
            return

        acces = self.view.var_acces_sortie.get()
        success, result, tarif = self.model.simuler_sortie_vehicule(immat_ticket)

        self.view.text_resultat_sortie.delete(1.0, tk.END)
        self.view.text_resultat_sortie.insert(tk.END, "=" * 70 + "\n")
        self.view.text_resultat_sortie.insert(tk.END,
                                              f"🚪 SORTIE - ACCÈS {acces.upper()} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.view.text_resultat_sortie.insert(tk.END, "=" * 70 + "\n\n")

        if success:
            message = f"""✅ SORTIE VALIDÉE

🚗 Client: {result['nom']}
🚙 Immatriculation: {result['immatriculation']}
🅿️  Place: {result['place']}
⏱️  Durée: {result['duree']:.2f} heures
💰 Tarif ({result['type_tarif']}): {result['tarif']:.2f}€
👤 Voiturier #{result['voiturier']}: Assigné

⚡ TÉLÉPORTEUR ACTIVÉ
Récupération de votre véhicule en cours...
└─→ Transport depuis {result['place']}

✓ Véhicule prêt à l'accès {acces}!
💳 Montant à régler: {result['tarif']:.2f}€
Merci et à bientôt!"""

            self.view.text_resultat_sortie.insert(tk.END, message)
            messagebox.showinfo("Succès", f"Sortie validée!\nMontant: {tarif:.2f}€")
            self.view.entry_immat_sortie.delete(0, tk.END)
            self.update_display()
        else:
            self.view.text_resultat_sortie.insert(tk.END, result)
            messagebox.showerror("Erreur", result)

    def traiter_livraison(self):
        """Traite service livraison"""
        client = self.view.entry_client_livraison.get().strip()
        adresse = self.view.entry_adresse_livraison.get().strip()
        heure = self.view.entry_heure_livraison.get().strip()

        if not all([client, adresse, heure]):
            messagebox.showerror("Erreur", "Remplissez tous les champs")
            return

        success, message = self.model.demander_service_livraison(client, adresse, heure)

        self.view.text_resultat_services.delete(1.0, tk.END)
        self.view.text_resultat_services.insert(tk.END,
                                                f"🚗 LIVRAISON - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 60}\n\n{message}")

        if success:
            messagebox.showinfo("Succès", "Livraison enregistrée!")
            self.view.entry_client_livraison.delete(0, tk.END)
            self.view.entry_adresse_livraison.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", message)

    def traiter_entretien(self):
        """Traite service entretien"""
        immat = self.view.entry_immat_entretien.get().strip()

        if not immat:
            messagebox.showerror("Erreur", "Entrez une immatriculation")
            return

        success, message = self.model.demander_service_entretien(immat)

        self.view.text_resultat_services.delete(1.0, tk.END)
        self.view.text_resultat_services.insert(tk.END,
                                                f"🔧 ENTRETIEN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 60}\n\n{message}")

        if success:
            messagebox.showinfo("Succès", "Entretien enregistré!")
            self.view.entry_immat_entretien.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", message)

    def traiter_maintenance(self):
        """Traite service maintenance"""
        immat = self.view.entry_immat_maintenance.get().strip()

        if not immat:
            messagebox.showerror("Erreur", "Entrez une immatriculation")
            return

        success, message = self.model.demander_service_maintenance(immat)

        self.view.text_resultat_services.delete(1.0, tk.END)
        self.view.text_resultat_services.insert(tk.END,
                                                f"⚙️ MAINTENANCE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 60}\n\n{message}")

        if success:
            messagebox.showinfo("Succès", "Maintenance enregistrée!")
            self.view.entry_immat_maintenance.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", message)

    def update_display(self):
        """Met à jour l'affichage"""
        stats = self.model.obtenir_statistiques()

        # Panneaux d'affichage (même nombre pour les 2 accès)
        places_par_acces = stats['places_libres'] // 2

        for panneau, label in [(self.view.panneau_nord, self.view.label_places_nord),
                               (self.view.panneau_sud, self.view.label_places_sud)]:
            label.config(text=str(places_par_acces))

            # Couleur selon disponibilité
            if places_par_acces < 5:
                color = '#e74c3c'
            elif places_par_acces < 25:
                color = '#f39c12'
            else:
                color = '#27ae60'

            panneau.config(bg=color)
            label.config(bg=color)
            for child in panneau.winfo_children():
                child.config(bg=color)

        # Stats
        self.view.stat_labels['occupation'].config(text=f"{stats['taux_occupation']:.1f}%")
        self.view.stat_labels['vehicules'].config(text=str(stats['vehicules_presents']))
        self.view.stat_labels['clients'].config(text=str(stats['total_clients']))
        self.view.stat_labels['services'].config(text=str(stats['services_en_attente']))

    def update_admin_display(self):
        """Met à jour admin"""
        # Mouvements
        for item in self.view.tree_mouvements.get_children():
            self.view.tree_mouvements.delete(item)

        for mouv in self.model.obtenir_derniers_mouvements(20):
            immat, nom, entree, sortie, niveau, numero, en_cours = mouv
            place = f"{niveau}{numero}" if niveau else "Valet"
            statut = "✓ Présent" if en_cours else "✗ Sorti"
            self.view.tree_mouvements.insert('', 'end', values=(
                immat, nom, entree, sortie or "-", place, statut
            ))

        # Revenus
        for item in self.view.tree_revenus.get_children():
            self.view.tree_revenus.delete(item)

        for rev in self.model.obtenir_revenus_recents(14):
            date_stat, entrees, sorties, taux, revenu = rev
            self.view.tree_revenus.insert('', 'end', values=(
                date_stat, entrees, sorties, f"{taux * 100:.1f}%", f"{revenu:.2f}€"
            ))

        # Services en attente
        for item in self.view.tree_services.get_children():
            self.view.tree_services.delete(item)

        for service in self.model.obtenir_services_en_attente():
            id_service, date_demande, nom, adresse, heure, type_service = service
            details = f"{adresse} à {heure}h" if adresse else "-"
            self.view.tree_services.insert('', 'end', values=(
                id_service, date_demande, nom, type_service, details
            ))


# ============================================================================
# VIEW (MVC Pattern)
# ============================================================================

class DreamParkView:
    """Vue - Interface graphique complète"""

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("🅿️ DreamPark - Système de Gestion Intelligent")
        self.root.geometry("1100x800")

        style = ttk.Style()
        style.theme_use('clam')

        self.create_main_interface()

    def create_main_interface(self):
        """Crée l'interface principale avec onglets"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_accueil_tab()
        self.create_entree_tab()
        self.create_sortie_tab()
        self.create_services_tab()
        self.create_admin_tab()

    def create_accueil_tab(self):
        """Onglet d'accueil avec panneaux d'affichage extérieurs"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏠 Accueil")

        # Titre
        title_frame = tk.Frame(tab, bg='#2c3e50', pady=20)
        title_frame.pack(fill='x')

        tk.Label(title_frame, text="🅿️ DREAMPARK", font=('Arial', 32, 'bold'),
                 bg='#2c3e50', fg='white').pack()
        tk.Label(title_frame, text="Parking Intelligent du Centre-Ville",
                 font=('Arial', 14), bg='#2c3e50', fg='#ecf0f1').pack()

        # Panneaux d'affichage des 2 accès (visibles depuis l'extérieur)
        panneaux_frame = tk.Frame(tab, pady=20)
        panneaux_frame.pack(fill='x')

        # Accès Nord
        self.panneau_nord = tk.Frame(panneaux_frame, bg='#27ae60', relief='raised', bd=5)
        self.panneau_nord.pack(side='left', padx=20, expand=True, fill='both')

        tk.Label(self.panneau_nord, text="📍 ACCÈS NORD", font=('Arial', 16, 'bold'),
                 bg='#27ae60', fg='white').pack(pady=10)
        tk.Label(self.panneau_nord, text="Places Disponibles", font=('Arial', 12),
                 bg='#27ae60', fg='white').pack()
        self.label_places_nord = tk.Label(self.panneau_nord, text="0",
                                          font=('Arial', 60, 'bold'), bg='#27ae60', fg='white')
        self.label_places_nord.pack(pady=10)

        # Accès Sud
        self.panneau_sud = tk.Frame(panneaux_frame, bg='#27ae60', relief='raised', bd=5)
        self.panneau_sud.pack(side='right', padx=20, expand=True, fill='both')

        tk.Label(self.panneau_sud, text="📍 ACCÈS SUD", font=('Arial', 16, 'bold'),
                 bg='#27ae60', fg='white').pack(pady=10)
        tk.Label(self.panneau_sud, text="Places Disponibles", font=('Arial', 12),
                 bg='#27ae60', fg='white').pack()
        self.label_places_sud = tk.Label(self.panneau_sud, text="0",
                                         font=('Arial', 60, 'bold'), bg='#27ae60', fg='white')
        self.label_places_sud.pack(pady=10)

        # Statistiques rapides
        stats_frame = tk.Frame(tab, pady=20)
        stats_frame.pack()

        self.stat_labels = {}
        stats_info = [
            ('occupation', 'Taux Occupation', '#3498db'),
            ('vehicules', 'Véhicules Présents', '#e74c3c'),
            ('clients', 'Clients Totaux', '#9b59b6'),
            ('services', 'Services Actifs', '#f39c12')
        ]

        for key, label, color in stats_info:
            frame = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
            frame.pack(side='left', padx=10)

            tk.Label(frame, text=label, font=('Arial', 10, 'bold'),
                     bg=color, fg='white').pack(pady=5, padx=15)
            self.stat_labels[key] = tk.Label(frame, text="0",
                                             font=('Arial', 20, 'bold'), bg=color, fg='white')
            self.stat_labels[key].pack(pady=5, padx=15)

        tk.Button(tab, text="🔄 Actualiser l'Affichage", font=('Arial', 12, 'bold'),
                  bg='#34495e', fg='white', command=self.controller.update_display,
                  padx=30, pady=10).pack(pady=20)

    def create_entree_tab(self):
        """Onglet d'entrée avec caméra, borne et téléporteur"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🚗 Accès Entrée")

        tk.Label(tab, text="🎥 BORNE D'ACCÈS - ENTRÉE", font=('Arial', 22, 'bold')).pack(pady=20)

        # Choix de l'accès
        acces_frame = tk.Frame(tab)
        acces_frame.pack(pady=10)

        tk.Label(acces_frame, text="Choisir l'accès:", font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        self.var_acces_entree = tk.StringVar(value="Nord")
        tk.Radiobutton(acces_frame, text="📍 Accès Nord", variable=self.var_acces_entree,
                       value="Nord", font=('Arial', 11)).pack(side='left', padx=10)
        tk.Radiobutton(acces_frame, text="📍 Accès Sud", variable=self.var_acces_entree,
                       value="Sud", font=('Arial', 11)).pack(side='left', padx=10)

        # Simulation caméra
        camera_frame = tk.LabelFrame(tab, text="📹 Caméra - Capture Automatique",
                                     font=('Arial', 12, 'bold'), padx=20, pady=15)
        camera_frame.pack(pady=10, padx=20, fill='x')

        form_frame = tk.Frame(camera_frame)
        form_frame.pack()

        tk.Label(form_frame, text="Immatriculation:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=8,
                                                                               sticky='e')
        self.entry_immat_entree = tk.Entry(form_frame, font=('Arial', 12, 'bold'), width=20)
        self.entry_immat_entree.grid(row=0, column=1, padx=10, pady=8)

        tk.Button(form_frame, text="📸 Scanner", font=('Arial', 10),
                  bg='#3498db', fg='white', command=self.simulated_scan,
                  padx=15, pady=5).grid(row=0, column=2, padx=10)

        # Mode de paiement
        paiement_frame = tk.LabelFrame(tab, text="💳 Mode de Paiement",
                                       font=('Arial', 12, 'bold'), padx=20, pady=15)
        paiement_frame.pack(pady=10, padx=20, fill='x')

        self.var_paiement = tk.StringVar(value="CB")
        tk.Radiobutton(paiement_frame, text="💳 Carte Bancaire", variable=self.var_paiement,
                       value="CB", font=('Arial', 11)).pack(side='left', padx=20)
        tk.Radiobutton(paiement_frame, text="💵 Espèces", variable=self.var_paiement,
                       value="Especes", font=('Arial', 11)).pack(side='left', padx=20)

        # Bouton d'entrée
        tk.Button(tab, text="✅ VALIDER L'ENTRÉE", font=('Arial', 14, 'bold'),
                  bg='#27ae60', fg='white', command=self.controller.traiter_entree,
                  padx=40, pady=15).pack(pady=20)

        # Zone de résultat
        result_frame = tk.LabelFrame(tab, text="📋 Résultat & Téléporteur", font=('Arial', 11, 'bold'))
        result_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.text_resultat_entree = scrolledtext.ScrolledText(result_frame, height=10, width=85,
                                                              font=('Courier', 10))
        self.text_resultat_entree.pack(pady=10, padx=10, fill='both', expand=True)

    def create_sortie_tab(self):
        """Onglet de sortie avec téléporteur et paiement"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🚙 Accès Sortie")

        tk.Label(tab, text="🎫 BORNE DE SORTIE", font=('Arial', 22, 'bold')).pack(pady=20)

        # Choix de l'accès
        acces_frame = tk.Frame(tab)
        acces_frame.pack(pady=10)

        tk.Label(acces_frame, text="Choisir l'accès:", font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        self.var_acces_sortie = tk.StringVar(value="Nord")
        tk.Radiobutton(acces_frame, text="📍 Accès Nord", variable=self.var_acces_sortie,
                       value="Nord", font=('Arial', 11)).pack(side='left', padx=10)
        tk.Radiobutton(acces_frame, text="📍 Accès Sud", variable=self.var_acces_sortie,
                       value="Sud", font=('Arial', 11)).pack(side='left', padx=10)

        # Formulaire sortie
        form_frame = tk.LabelFrame(tab, text="🎫 Ticket ou Immatriculation",
                                   font=('Arial', 12, 'bold'), padx=20, pady=15)
        form_frame.pack(pady=10, padx=20, fill='x')

        entry_frame = tk.Frame(form_frame)
        entry_frame.pack()

        tk.Label(entry_frame, text="Ticket/Immat:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=8,
                                                                             sticky='e')
        self.entry_immat_sortie = tk.Entry(entry_frame, font=('Arial', 12, 'bold'), width=30)
        self.entry_immat_sortie.grid(row=0, column=1, padx=10, pady=8)

        # Bouton sortie
        tk.Button(tab, text="✅ VALIDER LA SORTIE", font=('Arial', 14, 'bold'),
                  bg='#e74c3c', fg='white', command=self.controller.traiter_sortie,
                  padx=40, pady=15).pack(pady=20)

        # Zone de résultat
        result_frame = tk.LabelFrame(tab, text="📋 Résultat & Téléporteur", font=('Arial', 11, 'bold'))
        result_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.text_resultat_sortie = scrolledtext.ScrolledText(result_frame, height=10, width=85,
                                                              font=('Courier', 10))
        self.text_resultat_sortie.pack(pady=10, padx=10, fill='both', expand=True)

    def create_services_tab(self):
        """Onglet des services pour abonnés"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛠️ Services")

        tk.Label(tab, text="📞 SERVICES POUR ABONNÉS", font=('Arial', 20, 'bold')).pack(pady=20)

        # Service Livraison
        livraison_frame = tk.LabelFrame(tab, text="🚗 Service Livraison", font=('Arial', 12, 'bold'), padx=20, pady=15)
        livraison_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(livraison_frame, text="Nom client:", font=('Arial', 10)).grid(row=0, column=0, sticky='e', padx=5,
                                                                               pady=5)
        self.entry_client_livraison = tk.Entry(livraison_frame, font=('Arial', 10), width=30)
        self.entry_client_livraison.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(livraison_frame, text="Adresse:", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_adresse_livraison = tk.Entry(livraison_frame, font=('Arial', 10), width=30)
        self.entry_adresse_livraison.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(livraison_frame, text="Heure:", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_heure_livraison = tk.Entry(livraison_frame, font=('Arial', 10), width=30)
        self.entry_heure_livraison.insert(0, "18:00")
        self.entry_heure_livraison.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(livraison_frame, text="Demander Livraison", font=('Arial', 10, 'bold'),
                  bg='#3498db', fg='white', command=self.controller.traiter_livraison,
                  padx=15, pady=8).grid(row=3, column=0, columnspan=2, pady=10)

        # Services Entretien et Maintenance
        services_frame = tk.Frame(tab)
        services_frame.pack(pady=10, padx=20, fill='x')

        # Entretien
        entretien_frame = tk.LabelFrame(services_frame, text="🔧 Service Entretien",
                                        font=('Arial', 12, 'bold'), padx=20, pady=15)
        entretien_frame.pack(side='left', expand=True, fill='both', padx=5)

        tk.Label(entretien_frame, text="Immatriculation:", font=('Arial', 10)).pack(pady=5)
        self.entry_immat_entretien = tk.Entry(entretien_frame, font=('Arial', 10), width=20)
        self.entry_immat_entretien.pack(pady=5)

        tk.Button(entretien_frame, text="Demander Entretien", font=('Arial', 10, 'bold'),
                  bg='#9b59b6', fg='white', command=self.controller.traiter_entretien,
                  padx=15, pady=8).pack(pady=10)

        # Maintenance
        maintenance_frame = tk.LabelFrame(services_frame, text="⚙️ Service Maintenance",
                                          font=('Arial', 12, 'bold'), padx=20, pady=15)
        maintenance_frame.pack(side='right', expand=True, fill='both', padx=5)

        tk.Label(maintenance_frame, text="Immatriculation:", font=('Arial', 10)).pack(pady=5)
        self.entry_immat_maintenance = tk.Entry(maintenance_frame, font=('Arial', 10), width=20)
        self.entry_immat_maintenance.pack(pady=5)

        tk.Button(maintenance_frame, text="Demander Maintenance", font=('Arial', 10, 'bold'),
                  bg='#e67e22', fg='white', command=self.controller.traiter_maintenance,
                  padx=15, pady=8).pack(pady=10)

        # Zone de résultat
        result_frame = tk.LabelFrame(tab, text="📋 Résultat", font=('Arial', 11, 'bold'))
        result_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.text_resultat_services = scrolledtext.ScrolledText(result_frame, height=8, width=85,
                                                                font=('Courier', 10))
        self.text_resultat_services.pack(pady=10, padx=10, fill='both', expand=True)

    def create_admin_tab(self):
        """Onglet administrateur avec statistiques"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👤 Admin")

        tk.Label(tab, text="📊 TABLEAU DE BORD ADMINISTRATEUR", font=('Arial', 20, 'bold')).pack(pady=20)

        tk.Button(tab, text="🔄 Actualiser", font=('Arial', 10),
                  command=self.controller.update_admin_display, padx=15, pady=5).pack()

        # Notebook interne
        admin_notebook = ttk.Notebook(tab)
        admin_notebook.pack(fill='both', expand=True, padx=20, pady=10)

        # Onglet Mouvements
        mouv_tab = ttk.Frame(admin_notebook)
        admin_notebook.add(mouv_tab, text="Mouvements")

        self.tree_mouvements = ttk.Treeview(mouv_tab,
                                            columns=('Immat', 'Client', 'Entrée', 'Sortie', 'Place', 'Statut'),
                                            show='headings', height=15)
        self.tree_mouvements.heading('Immat', text='Immatriculation')
        self.tree_mouvements.heading('Client', text='Client')
        self.tree_mouvements.heading('Entrée', text='Date Entrée')
        self.tree_mouvements.heading('Sortie', text='Date Sortie')
        self.tree_mouvements.heading('Place', text='Place')
        self.tree_mouvements.heading('Statut', text='Statut')

        self.tree_mouvements.column('Immat', width=100)
        self.tree_mouvements.column('Client', width=120)
        self.tree_mouvements.column('Entrée', width=130)
        self.tree_mouvements.column('Sortie', width=130)
        self.tree_mouvements.column('Place', width=60)
        self.tree_mouvements.column('Statut', width=80)

        self.tree_mouvements.pack(fill='both', expand=True, padx=10, pady=10)

        # Onglet Revenus
        revenus_tab = ttk.Frame(admin_notebook)
        admin_notebook.add(revenus_tab, text="Revenus")

        self.tree_revenus = ttk.Treeview(revenus_tab, columns=('Date', 'Entrées', 'Sorties', 'Taux Occ.', 'Revenu'),
                                         show='headings', height=15)
        self.tree_revenus.heading('Date', text='Date')
        self.tree_revenus.heading('Entrées', text='Entrées')
        self.tree_revenus.heading('Sorties', text='Sorties')
        self.tree_revenus.heading('Taux Occ.', text='Taux Occupation')
        self.tree_revenus.heading('Revenu', text='Revenu')

        self.tree_revenus.column('Date', width=100)
        self.tree_revenus.column('Entrées', width=80)
        self.tree_revenus.column('Sorties', width=80)
        self.tree_revenus.column('Taux Occ.', width=120)
        self.tree_revenus.column('Revenu', width=100)

        self.tree_revenus.pack(fill='both', expand=True, padx=10, pady=10)

        # Onglet Services
        services_tab = ttk.Frame(admin_notebook)
        admin_notebook.add(services_tab, text="Services En Attente")

        self.tree_services = ttk.Treeview(services_tab, columns=('ID', 'Date', 'Client', 'Type', 'Détails'),
                                          show='headings', height=15)
        self.tree_services.heading('ID', text='ID')
        self.tree_services.heading('Date', text='Date Demande')
        self.tree_services.heading('Client', text='Client')
        self.tree_services.heading('Type', text='Type')
        self.tree_services.heading('Détails', text='Détails')

        self.tree_services.column('ID', width=60)
        self.tree_services.column('Date', width=100)
        self.tree_services.column('Client', width=120)
        self.tree_services.column('Type', width=100)
        self.tree_services.column('Détails', width=200)

        self.tree_services.pack(fill='both', expand=True, padx=10, pady=10)

    def simulated_scan(self):
        """Simulation du scan de la caméra"""
        immat = self.entry_immat_entree.get().strip()
        if immat:
            messagebox.showinfo("📸 Caméra", f"Scan effectué!\n\n✓ Immatriculation: {immat}\n✓ Dimensions capturées")

    def ouvrir_formulaire_nouveau_client(self, immatriculation):
        """Formulaire d'enregistrement nouveau client/véhicule"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouveau Client/Véhicule")
        dialog.geometry("500x650")
        dialog.grab_set()

        tk.Label(dialog, text="📝 ENREGISTREMENT NOUVEAU CLIENT",
                 font=('Arial', 16, 'bold')).pack(pady=20)

        form = tk.Frame(dialog)
        form.pack(pady=20, padx=30, fill='both', expand=True)

        # Informations Client
        tk.Label(form, text="INFORMATIONS CLIENT", font=('Arial', 12, 'bold', 'underline')).grid(
            row=0, column=0, columnspan=2, pady=10)

        tk.Label(form, text="Nom complet:*", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        entry_nom = tk.Entry(form, font=('Arial', 10), width=30)
        entry_nom.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Adresse:*", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        entry_adresse = tk.Entry(form, font=('Arial', 10), width=30)
        entry_adresse.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Type d'abonnement:", font=('Arial', 10)).grid(row=3, column=0, sticky='e', padx=5, pady=5)
        var_abonnement = tk.StringVar(value="aucun")
        frame_abo = tk.Frame(form)
        frame_abo.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        tk.Radiobutton(frame_abo, text="Aucun", variable=var_abonnement, value="aucun").pack(anchor='w')
        tk.Radiobutton(frame_abo, text="Standard (30€)", variable=var_abonnement, value="standard").pack(anchor='w')
        tk.Radiobutton(frame_abo, text="Super Abonné - Pack Garanti (60€)",
                       variable=var_abonnement, value="super").pack(anchor='w')

        # Informations Véhicule
        tk.Label(form, text="INFORMATIONS VÉHICULE", font=('Arial', 12, 'bold', 'underline')).grid(
            row=4, column=0, columnspan=2, pady=(20, 10))

        tk.Label(form, text="Immatriculation:*", font=('Arial', 10)).grid(row=5, column=0, sticky='e', padx=5, pady=5)
        entry_immat = tk.Entry(form, font=('Arial', 10), width=30)
        entry_immat.insert(0, immatriculation.upper())
        entry_immat.config(state='readonly')
        entry_immat.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(form, text="Hauteur (m):*", font=('Arial', 10)).grid(row=6, column=0, sticky='e', padx=5, pady=5)
        entry_hauteur = tk.Entry(form, font=('Arial', 10), width=30)
        entry_hauteur.insert(0, "2.0")
        entry_hauteur.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(form, text="Longueur (m):*", font=('Arial', 10)).grid(row=7, column=0, sticky='e', padx=5, pady=5)
        entry_longueur = tk.Entry(form, font=('Arial', 10), width=30)
        entry_longueur.insert(0, "4.5")
        entry_longueur.grid(row=7, column=1, padx=5, pady=5)

        def valider_nouveau():
            nom = entry_nom.get().strip()
            adresse = entry_adresse.get().strip()

            if not nom or not adresse:
                messagebox.showerror("Erreur", "Remplissez tous les champs obligatoires (*)")
                return

            try:
                hauteur = float(entry_hauteur.get())
                longueur = float(entry_longueur.get())

                if hauteur <= 0 or longueur <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Hauteur et longueur doivent être > 0")
                return

            # Déterminer le type d'abonnement
            type_abo = var_abonnement.get()
            est_abonne = type_abo in ["standard", "super"]
            est_super_abonne = type_abo == "super"

            # Ajouter le client
            success, id_client = self.controller.model.ajouter_nouveau_client(nom, adresse, est_abonne,
                                                                              est_super_abonne)

            if not success:
                messagebox.showerror("Erreur", f"Erreur client: {id_client}")
                return

            # Ajouter le véhicule
            success, id_vehicule = self.controller.model.ajouter_nouveau_vehicule(immatriculation, hauteur, longueur,
                                                                                  id_client)

            if not success:
                messagebox.showerror("Erreur", f"Erreur véhicule: {id_vehicule}")
                return

            # Créer un contrat si abonné
            if est_abonne:
                self.controller.model.creer_contrat_abonnement(id_client, "super" if est_super_abonne else "standard")

            messagebox.showinfo("Succès", f"✅ Enregistrement réussi!\n\nClient: {nom}\nVéhicule: {immatriculation}")
            dialog.destroy()

            # Traiter l'entrée automatiquement
            self.controller.traiter_entree()

        # Boutons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Enregistrer et Entrer", font=('Arial', 11, 'bold'),
                  bg='#27ae60', fg='white', command=valider_nouveau,
                  padx=20, pady=10).pack(side='left', padx=10)

        tk.Button(btn_frame, text="Annuler", font=('Arial', 11),
                  bg='#e74c3c', fg='white', command=dialog.destroy,
                  padx=20, pady=10).pack(side='left', padx=10)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Point d'entrée principal"""
    try:
        root = tk.Tk()

        # Créer le contrôleur
        controller = DreamParkController()

        # Créer la vue
        view = DreamParkView(root, controller)

        # Lier la vue au contrôleur
        controller.set_view(view)

        # Mettre à jour l'affichage initial après que la vue soit complètement initialisée
        controller.update_display()
        controller.update_admin_display()

        # Gestion de la fermeture
        def on_closing():
            controller.model.close()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Lancer l'application
        root.mainloop()

    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        messagebox.showerror("Erreur",
                             f"Impossible de démarrer l'application:\n\n{e}\n\nVérifiez que le fichier 'dreampark.db' existe.\nExécutez 'python partie3.py' pour créer la base de données.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()