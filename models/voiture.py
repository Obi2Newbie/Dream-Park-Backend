class Voiture:
    """
    Représente un véhicule géré par le système DreamPark.

    Stocke les caractéristiques physiques du véhicule et son état
    de stationnement actuel (dans/hors parking, placement associé).

    Attributes:
        __hauteur (float): Hauteur du véhicule en mètres (privé).
        __longueur (float): Longueur du véhicule en mètres (privé).
        __immatriculation (str): Plaque d'immatriculation (privé).
        estDansParking (bool): True si le véhicule est actuellement garé.
        proprietaire (Client): Client propriétaire du véhicule.
        monPlacement (Placement): Placement actif si véhicule garé.
    """

    def __init__(self, hauteur, longueur, immatriculation, estDansParking=False):
        """
        Initialise un nouveau véhicule.

        Args:
            hauteur (float): Hauteur en mètres.
            longueur (float): Longueur en mètres.
            immatriculation (str): Numéro de plaque.
            estDansParking (bool, optional): Statut initial. Defaults to False.
        """

    def addPlacementV(self, p):
        """
        Associe un placement à ce véhicule lors du stationnement.

        Args:
            p (Placement): Le placement créé lors de l'entrée au parking.

        Side Effects:
            - Lie le placement au véhicule
            - Met à jour estDansParking = True
        """

    def obtenirHauteur(self):
        """Retourne la hauteur du véhicule en mètres."""

    def definirHauteur(self, hauteur):
        """
        Modifie la hauteur du véhicule.

        Args:
            hauteur (float): Nouvelle hauteur en mètres.
        """

    def obtenirLongueur(self):
        """Retourne la longueur du véhicule en mètres."""


    def definirLongueur(self, longueur):
        """
        Modifie la longueur du véhicule.

        Args:
            longueur (float): Nouvelle longueur en mètres.
        """

    def obtenirImmatriculation(self):
        """Retourne le numéro d'immatriculation du véhicule."""

    def definirImmatriculation(self, immatriculation):
        """
        Modifie le numéro d'immatriculation.

        Args:
            immatriculation (str): Nouvelle plaque d'immatriculation.
        """
