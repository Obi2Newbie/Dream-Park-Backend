class Service:
    """
    Represente un service propose par le parking DreamPark.
    Les services sont disponibles pour les clients abonnes.
    """

    def __init__(self, nom, prix, description=""):
        """
        Initialise un service.

        Args:
            nom (str): Nom du service
            prix (float): Prix du service
            description (str): Description optionnelle
        """
        self.nom = nom
        self.prix = prix
        self.description = description

    def __repr__(self):
        return f"Service({self.nom}, {self.prix} euros)"