class Abonnement:
    """
    Représente un type d'abonnement proposé par le système DreamPark.

    Un abonnement définit les privilèges tarifaires et les services auxquels
    un client a accès dans le parking (téléportation prioritaire, services
    additionnels, etc.).

    Attributes:
        libelle (str): Nom ou désignation de l'abonnement (ex: "Standard", "Premium").
        prix (float): Coût mensuel de l'abonnement en euros.
        estPackGar (bool): True si l'abonnement inclut le pack garanti (Super Abonné)
                           avec téléportation prioritaire et service Valet.
        mesAbonnements (list): Liste des contrats associés à cet abonnement.
    """

    def __init__(self, libelle, prix, estPackGar):
        """
        Initialise un nouvel abonnement avec ses caractéristiques.

        Args:
            libelle (str): Nom de l'abonnement.
            prix (float): Montant mensuel de l'abonnement.
            estPackGar (bool): True si l'abonnement comprend le pack garanti.
        """
        self.libelle = libelle
        self.prix = float(prix)
        self.estPackGar = estPackGar
        self.mesAbonnements = []

    def addContrat(self, contrat):
        """
        Associe un contrat à cet abonnement.

        Permet de lier un client à cet abonnement via un contrat qui
        définit la durée et le statut de la souscription.

        Args:
            contrat (Contrat): Le contrat à associer à cet abonnement.

        Note:
            Évite les doublons en vérifiant si le contrat n'est pas déjà présent.
        """
        if contrat not in self.mesAbonnements:
            self.mesAbonnements.append(contrat)