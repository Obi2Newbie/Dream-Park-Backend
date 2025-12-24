from .placement import Placement


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
        self.__hauteur = float(hauteur)
        self.__longueur = float(longueur)
        self.__immatriculation = immatriculation
        self.estDansParking = estDansParking
        self.proprietaire = None
        self.monPlacement = None

    def addPlacementV(self, p):
        """
        Associe un placement à ce véhicule lors du stationnement.

        Args:
            p (Placement): Le placement créé lors de l'entrée au parking.

        Side Effects:
            - Lie le placement au véhicule
            - Met à jour estDansParking = True
        """
        self.monPlacement = p
        self.estDansParking = True

    def obtenirHauteur(self):
        """Retourne la hauteur du véhicule en mètres."""
        return self.__hauteur

    def definirHauteur(self, hauteur):
        """
        Modifie la hauteur du véhicule.

        Args:
            hauteur (float): Nouvelle hauteur en mètres.
        """
        self.__hauteur = hauteur

    def obtenirLongueur(self):
        """Retourne la longueur du véhicule en mètres."""
        return self.__longueur

    def definirLongueur(self, longueur):
        """
        Modifie la longueur du véhicule.

        Args:
            longueur (float): Nouvelle longueur en mètres.
        """
        self.__longueur = longueur

    def obtenirImmatriculation(self):
        """Retourne le numéro d'immatriculation du véhicule."""
        return self.__immatriculation

    def definirImmatriculation(self, immatriculation):
        """
        Modifie le numéro d'immatriculation.

        Args:
            immatriculation (str): Nouvelle plaque d'immatriculation.
        """
        self.__immatriculation = immatriculation