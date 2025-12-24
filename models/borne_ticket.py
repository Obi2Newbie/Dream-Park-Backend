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


    def proposerTypePaiement(self):
        """
        Propose les modes de paiement disponibles et enregistre le choix.

        Options :
        1. Carte bancaire
        2. Espèces

        Note:
            Valide la saisie et affiche une confirmation du mode choisi.
        """
