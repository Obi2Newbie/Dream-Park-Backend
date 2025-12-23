import time

from models import Abonnement


class Borne_ticket:
    """
    Représente une borne de ticket du système DreamPark.

    Cette borne permet aux clients d’interagir avec le système du parking :
        - Délivrance de tickets pour les clients non abonnés.
        - Proposition de services ou d’abonnements.
        - Gestion des informations de paiement et de carte.
    """

    def deliverTicket(self, c):
        """
        Délivre un ticket au client spécifié.

        Args:
            c (Client): Objet représentant le client demandant un ticket.

        Returns:
            string: Message confirmant la délivrance du ticket ou indiquant une erreur.

        Comportement attendu :
            - Génère un ticket pour un client non abonné.
            - Enregistre les informations nécessaires (heure d’entrée, identifiant du ticket, etc.).
            - Peut imprimer le ticket physiquement ou l’envoyer sous format numérique.
        """
        return f"{c.nom}-{c.maVoiture.obtenirImmatriculation()}"

    def proposerServices(self):
        """
        Propose différents services disponibles via la borne.

        Returns:
            string: Liste ou description textuelle des services proposés.

        Comportement attendu :
            - Présente les services offerts (entretien, lavage, maintenance, etc.).
            - Permet au client de sélectionner une option parmi les propositions.
            - Peut afficher les coûts ou les avantages associés.
        """
        while True:
            service = input("Services:\n1. pour Maintenance,\n2. pour Entretien,\n3. pour Livraison,\n4. pour aucun service\n")
            if service in ["1", "2", "3", "4"]:
                break
        return service

    def proposerAbonnements(self, c, p):
        """
        Propose différents abonnements disponibles au client.

        Args:
            c (Client): Objet représentant le client concerné.
            p (Parking): Objet représentant le parking où l’abonnement est proposé.

        Returns:
            string: Message ou liste des abonnements disponibles.

        Comportement attendu :
            - Affiche les formules d’abonnement en fonction du profil du client et du parking.
            - Permet la souscription immédiate si le client accepte une offre.
            - Peut inclure des offres spéciales ou des réductions pour les utilisateurs fréquents.
        """
        print("\n--- BIENVENUE CHEZ DREAMPARK ---")
        print(f"Ravi de vous rencontrer, {c.nom}.")
        print("Souhaitez-vous souscrire à un abonnement pour cette visite ?\n")
        while True:
            choix = input("1. pour abonnement standard\n2. pour super abonné\n3. pour continue sans abonnement\n")
            if choix in ["1", "2", "3"]:
                break
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
                c.estAbonne = True
                c.estSuperAbonne = False
        print("Préférences enregistrées.")

    def recupererInfosCarte(self, c):
        """
        Récupère les informations de la carte d’accès ou de paiement d’un client.

        Args:
            c (Client): Objet représentant le client utilisant la borne.

        Returns:
            string: Informations de la carte ou message d’état (succès/échec).

        Comportement attendu :
            - Lit ou scanne la carte d’accès ou de paiement du client.
            - Vérifie la validité de la carte (date d’expiration, abonnement actif, etc.).
            - Met à jour les informations du client dans le système.
        """
        while True:
            temp = input("Est vous un super abonné ? y/n\n").lower()
            if temp in ["y", "n"]:
                break
        print("Vérification de votre statut client... Veillez patienter...")
        time.sleep(1)
        if c.estSuperAbonne and temp == 'y':
            return f"Carte validée pour {c.nom}"
        return "Client non super abonné"

    def proposerTypePaiement(self):
        """
        Propose différents modes de paiement disponibles via la borne.

        Returns:
            string: Message ou liste des types de paiement proposés.

        Comportement attendu :
            - Affiche les options disponibles (espèces, carte bancaire, paiement mobile, etc.).
            - Permet au client de choisir son mode de paiement préféré.
            - Peut vérifier la disponibilité des terminaux avant validation.
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
