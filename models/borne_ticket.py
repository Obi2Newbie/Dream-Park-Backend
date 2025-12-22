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
        return "Services: Maintenance, Entretien, Livraison"

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
        while True:
            abonnement = input("Abonnements disponibles: Appuyer sur 1 pour Standard / Appuyer sur 2 pour Super Abonné / Appuyer sur 3 pour Aucun Abonnement\n")
            if abonnement in ["1", "2", "3"]:
                break
            else:
                print("Erreur : Veuillez appuyer sur le bon bouton.")
        match abonnement:
            case "1":
                print("Merci pour avoir sélectionné l'abonnement Standard")
            case "2":
                print("Merci pour avoir sélectionné l'abonnement Super Abonné")
            case "3":
                print("Dommage, veillez récupérer votre ticket")

    def recupererInfosCarte(self, c):
        """
        Récupère les informations de la carte d’accès ou de paiement d’un client.

        Args:
            c (Client): Objet représentant le client utilisant la borne.
            p (Parking): Objet représentant le parking associé à la carte.

        Returns:
            string: Informations de la carte ou message d’état (succès/échec).

        Comportement attendu :
            - Lit ou scanne la carte d’accès ou de paiement du client.
            - Vérifie la validité de la carte (date d’expiration, abonnement actif, etc.).
            - Met à jour les informations du client dans le système.
        """
        if c.estAbonne:
            return f"Carte validée pour {c.nom}"
        return "Aucun carte détectée"

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
                "Abonnements disponibles: Appuyer sur 1 pour CB / Appuyer sur 2 pour Espèces \n")
            if paiement in ["1", "2"]:
                break
            else:
                print("Erreur : Veuillez appuyer sur le bon bouton.")
        match paiement:
            case "1":
                print("Merci pour avoir sélectionné l'option CB")
            case "2":
                print("Merci pour avoir sélectionné l'option Espèces")
