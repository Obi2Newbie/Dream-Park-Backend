class Abonnement:
    """
    Représente un type d’abonnement proposé par le système DreamPark.

    Attributs :
        libelle (str) : Nom ou désignation de l’abonnement.
        prix (float) : Coût de l’abonnement, généralement exprimé en euros.
        estPackGar (bool) : Indique si cet abonnement inclut le pack garanti.
    """

    def __init__(self, libelle, prix, estPackGar):
        """
        Initialise un nouvel abonnement avec ses caractéristiques principales.

        Args:
            libelle (str): Nom de l’abonnement.
            prix (float): Montant de l’abonnement.
            estPackGar (bool): True si l’abonnement comprend le pack garanti, False sinon.

        Comportement attendu :
            - Enregistre les informations de base liées à l’abonnement.
            - Prépare l’objet pour être associé à un contrat ou un client.
        """
        self.libelle = libelle
        self.prix = prix
        self.estPackGar = estPackGar

    def addContrat(self, contrat):
        return 0;
