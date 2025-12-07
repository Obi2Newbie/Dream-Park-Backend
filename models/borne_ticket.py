"""
Module de gestion de la borne et des tickets du parking DreamPark.
Auteur: [VOTRE NOM]
"""

from datetime import datetime
from .client import Client
from .voiture import Voiture


class BorneTicket:
    """
    Represente une borne d'acces equipee d'un systeme de delivrance de tickets.
    La borne gere l'interaction avec le client pour le stationnement.
    """

    def __init__(self, id_borne, acces):
        """
        Initialise une borne de ticketing.

        Args:
            id_borne (int): Identifiant unique de la borne
            acces (Acces): Reference vers l'acces auquel la borne appartient
        """
        self.id_borne = id_borne
        self.acces = acces
        self.ticket_en_cours = None
        self.abonnements_disponibles = self._initialiser_abonnements()
        self.services_disponibles = self._initialiser_services()

    def _initialiser_abonnements(self):
        """
        Initialise la liste des abonnements proposes aux clients.

        Returns:
            list: Liste de tuples (libelle, prix, estPackGar)
        """
        return [
            ("Mensuel Standard", 50.0, False),
            ("Annuel Premium", 500.0, False),
            ("Pack Garanti Centre-Ville", 80.0, True)
        ]

    def _initialiser_services(self):
        """
        Initialise la liste des services proposes aux abonnes.

        Returns:
            list: Liste de tuples (nom_service, prix)
        """
        return [
            ("Livraison", 15.0),
            ("Entretien", 50.0),
            ("Maintenance", 80.0)
        ]

    def traiter_stationnement(self, client, id_place):
        """
        Traite le stationnement d'un client apres qu'une place soit trouvee.
        Correspond au flux du diagramme d'activite a partir de "une place trouvee".

        Args:
            client (Client): Le client qui souhaite se garer
            id_place (int): Identifiant de la place assignee

        Returns:
            Ticket: Le ticket delivre ou None en cas d'echec
        """
        print(f"\nTraitement du stationnement pour {client.nom}")
        print(f"Place assignee: {id_place}")

        if client.estAbonne:
            print("Client abonne detecte")
            self._traiter_client_abonne(client)
        else:
            print("Client non-abonne")
            self._traiter_client_non_abonne(client)

        ticket = self._delivrer_ticket(client, id_place)

        if ticket:
            print(f"Ticket delivre: {ticket.numero_ticket}")

            succes_teleportation = self._actionner_teleporteur(ticket)

            if succes_teleportation:
                print("Teleportation reussie")
                return ticket
            else:
                print("Echec de la teleportation")
                return None
        else:
            print("Echec de la delivrance du ticket")
            return None

    def _traiter_client_abonne(self, client):
        """
        Traite un client abonne en proposant la liste des services.

        Args:
            client (Client): Le client abonne
        """
        print("\n--- Services disponibles pour abonnes ---")

        for i, (nom_service, prix) in enumerate(self.services_disponibles, 1):
            print(f"{i}. {nom_service} - {prix} euros")

        service_choisi = self._demander_choix_service()

        if service_choisi:
            client.ajouterService(service_choisi)
            print(f"Service selectionne: {service_choisi[0]}")
        else:
            print("Aucun service supplementaire selectionne")

    def _traiter_client_non_abonne(self, client):
        """
        Traite un client non-abonne en demandant le mode de paiement
        et en proposant des abonnements.

        Args:
            client (Client): Le client non-abonne
        """
        print("\n--- Client non-abonne ---")

        mode_paiement = self._demander_mode_paiement()
        client.definirModePaiement(mode_paiement)
        print(f"Mode de paiement: {mode_paiement}")

        print("\n--- Abonnements disponibles ---")
        for i, (libelle, prix, estPackGar) in enumerate(self.abonnements_disponibles, 1):
            pack_info = " (Pack Garanti inclus)" if estPackGar else ""
            print(f"{i}. {libelle} - {prix} euros/mois{pack_info}")

        abonnement_choisi = self._demander_choix_abonnement()

        if abonnement_choisi:
            client.sAbonner(abonnement_choisi)
            print(f"Abonnement souscrit: {abonnement_choisi[0]}")
        else:
            print("Aucun abonnement souscrit")

    def _demander_choix_service(self):
        """
        Simule la demande de choix de service au client.

        Returns:
            tuple: (nom_service, prix) ou None
        """
        return None

    def _demander_mode_paiement(self):
        """
        Demande au client son mode de paiement.

        Returns:
            str: "CB" ou "Especes"
        """
        return "CB"

    def _demander_choix_abonnement(self):
        """
        Demande au client s'il souhaite souscrire a un abonnement.

        Returns:
            tuple: (libelle, prix, estPackGar) ou None
        """
        return None

    def _delivrer_ticket(self, client, id_place):
        """
        Delivre un ticket au client pour le stationnement.

        Args:
            client (Client): Le client
            id_place (int): Identifiant de la place assignee

        Returns:
            Ticket: Le ticket cree ou None en cas d'echec
        """
        try:
            ticket = Ticket(client, id_place, datetime.now())
            self.ticket_en_cours = ticket
            return ticket
        except Exception as e:
            print(f"Erreur lors de la delivrance du ticket: {e}")
            return None

    def _actionner_teleporteur(self, ticket):
        """
        Active un teleporteur pour transporter le vehicule vers sa place.

        Args:
            ticket (Ticket): Le ticket contenant les informations

        Returns:
            bool: True si succes, False sinon
        """
        try:
            teleporteur = self.acces.obtenirTeleporteurDisponible()

            if teleporteur:
                succes = teleporteur.teleporterEntree(
                    ticket.client.voiture,
                    ticket.id_place
                )
                return succes
            else:
                print("Aucun teleporteur disponible")
                return False
        except Exception as e:
            print(f"Erreur lors de l'activation du teleporteur: {e}")
            return False


class Ticket:
    """
    Represente un ticket de stationnement delivre a un client.
    """

    _compteur = 0

    def __init__(self, client, id_place, heure_entree):
        """
        Initialise un nouveau ticket.

        Args:
            client (Client): Le client proprietaire du ticket
            id_place (int): Identifiant de la place assignee
            heure_entree (datetime): Heure d'entree dans le parking
        """
        Ticket._compteur += 1
        self.numero_ticket = f"TK{Ticket._compteur:06d}"
        self.client = client
        self.id_place = id_place
        self.heure_entree = heure_entree
        self.heure_sortie = None
        self.montant = 0.0
        self.paye = False

    def calculer_duree(self):
        """
        Calcule la duree de stationnement en minutes.

        Returns:
            int: Duree en minutes ou 0 si pas encore sorti
        """
        if not self.heure_sortie:
            return 0
        duree = self.heure_sortie - self.heure_entree
        return int(duree.total_seconds() / 60)

    def calculer_montant(self, tarif_horaire=2.0):
        """
        Calcule le montant a payer selon le tarif horaire.

        Args:
            tarif_horaire (float): Tarif par heure

        Returns:
            float: Montant a payer
        """
        if self.client.estAbonne:
            return 0.0

        duree_minutes = self.calculer_duree()
        duree_heures = duree_minutes / 60.0
        self.montant = duree_heures * tarif_horaire
        return self.montant

    def marquer_paye(self):
        """Marque le ticket comme paye."""
        self.paye = True