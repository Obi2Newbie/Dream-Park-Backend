import time
from models import Abonnement


class Borne_ticket:
    """
    Représente une borne interactive du système DreamPark.

    Interface principale entre le client et le système, permettant :
    - La délivrance de tickets
    - La souscription d'abonnements
    - La sélection de services additionnels
    - Le choix du mode de paiement
    - La vérification du statut client
    """

    def deliverTicket(self, c):
        """
        Génère et délivre un ticket d'accès au client.

        Le ticket contient l'identifiant du client et l'immatriculation
        de son véhicule pour traçabilité.

        Args:
            c (Client): Le client demandant un ticket.

        Returns:
            str: Ticket formaté "NomClient-Immatriculation".
        """
        return f"{c.nom}-{c.maVoiture.obtenirImmatriculation()}"

    def proposerServices(self):
        """
        Affiche le menu des services disponibles et récupère le choix du client.

        Services proposés :
        1. Maintenance technique
        2. Entretien véhicule
        3. Livraison à domicile (Voiturier)
        4. Aucun service

        Returns:
            str: Code du service sélectionné ("1", "2", "3", ou "4").

        Note:
            Boucle jusqu'à obtention d'une saisie valide.
        """
        while True:
            service = input(
                "Services:\n1. pour Maintenance,\n2. pour Entretien,\n3. pour Livraison,\n4. pour aucun service\n")
            if service in ["1", "2", "3", "4"]:
                break
            print("Erreur! Veillez que choisir 1, 2, 3 ou 4")
        return service

    def proposerAbonnements(self, c, p):
        """
        Présente les formules d'abonnement disponibles et gère la souscription.

        Permet au client de souscrire immédiatement à :
        - Abonnement Standard (10€) : Accès aux services, tarif réduit
        - Super Abonné (5€) : Pack Garanti avec téléportation prioritaire
        - Continuer sans abonnement

        Args:
            c (Client): Le client à qui proposer les abonnements.
            p (Parking): Le parking pour enregistrer l'abonnement souscrit.

        Side Effects:
            Met à jour le statut du client (estAbonne, estSuperAbonne).
            Crée et associe un abonnement au client si souscription.
        """
        print("\n--- BIENVENUE CHEZ DREAMPARK ---")
        print(f"Ravi de vous rencontrer, {c.nom}.")
        print("Souhaitez-vous souscrire à un abonnement pour cette visite ?\n")

        while True:
            choix = input("1. pour abonnement standard\n2. pour super abonné\n3. pour continue sans abonnement\n")
            if choix in ["1", "2", "3"]:
                break
            print("Erreur! Veillez que choisir 1, 2 ou 3")

        match choix:
            case "1":
                abonnement = Abonnement("abonne", 10, False)
                c.estAbonne = True
                c.estSuperAbonne = False
                c.sAbonner(abonnement)
                p.addAbonnement(abonnement)
            case "2":
                abonnement = Abonnement("abonne", 5, True)
                c.estAbonne = True
                c.estSuperAbonne = True
                c.sAbonner(abonnement)
                p.addAbonnement(abonnement)
            case "3":
                c.estAbonne = False
                c.estSuperAbonne = False

        print("Préférences enregistrées.")

    def recupererInfosCarte(self, c):
        """
        Vérifie et valide le statut de super abonné du client.

        Simule la lecture d'une carte d'accès ou badge client pour
        vérifier les privilèges premium.

        Args:
            c (Client): Le client dont on vérifie la carte.

        Returns:
            str: Message de validation ou d'échec de la carte.

        Note:
            Demande une confirmation manuelle pour le test du système.
        """
        while True:
            temp = input("Est vous un super abonné ? y/n\n").lower()
            if temp in ["y", "n"]:
                break
            print("Erreur veillez sélectionner que 'y' ou 'n'")

        print("Vérification de votre statut client... Veillez patienter...")
        time.sleep(1)

        if c.estSuperAbonne:
            print("Retour systeme: Client est super abonné.")
            return f"Carte validée pour {c.nom}"
        return "Client non super abonné"

    def proposerTypePaiement(self):
        """
        Propose les modes de paiement disponibles et enregistre le choix.

        Options :
        1. Carte bancaire
        2. Espèces

        Note:
            Valide la saisie et affiche une confirmation du mode choisi.
        """
        while True:
            paiement = input(
                "Comment allez vous regler le paiement ?: Appuyer sur 1 pour CB / Appuyer sur 2 pour Espèces \n")
            if paiement in ["1", "2"]:
                break
            else:
                print("Erreur : Veuillez appuyer sur le bon bouton.")

        match paiement:
            case "1":
                print("Merci pour avoir sélectionné l'option CB")
            case "2":
                print("Merci pour avoir sélectionné l'option Espèces")