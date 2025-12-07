from .placement import Placement

class Voiture:
    """
    Représente une voiture gérée par le système DreamPark.

    Attributs :
        __hauteur (float) : Hauteur du véhicule en mètres.
        __longueur (float) : Longueur du véhicule en mètres.
        __immatriculation (str) : Numéro d'immatriculation du véhicule.
        estDansParking (bool) : Indique si le véhicule est actuellement stationné dans le parking.
    """

    def __init__(self, hauteur = 0, longueur = 0, immatriculation = "", estDansParking = False):
        """
        Initialise une nouvelle voiture avec ses caractéristiques physiques
        et son statut de stationnement.

        Attributs:
            hauteur (float): Hauteur du véhicule en mètres.
            longueur (float): Longueur du véhicule en mètres.
            immatriculation (str): Numéro d'immatriculation du véhicule.
            estDansParking (bool, optionnel): True si le véhicule est déjà stationné
                dans le parking (par défaut False).
        """
        self.__hauteur = hauteur
        self.__longueur = longueur
        self.__immatriculation = immatriculation
        self.estDansParking = estDansParking

    def addPlacementV(self, p):
        """
        Associe un objet `Placement` à cette voiture, indiquant
        l’endroit précis où elle est garée dans le parking.

        Attributs:
            p: Objet représentant la place attribuée à la voiture.

        Comportement attendu :
            - Enregistre la place dans laquelle le véhicule est garé.
            - Met à jour l’attribut `estDansParking` à True.
            - Peut notifier le système central du changement d’état du véhicule.
        """
        pass

    def obtenirHauteur(self):
        """
        Retourne la hauteur actuelle du véhicule.

        Returns:
            float: La hauteur du véhicule (en mètres).

        Comportement attendu :
            - Fournit la valeur enregistrée de la hauteur du véhicule.
            - Utilisé notamment par la caméra ou le système de vérification de gabarit.
        """
        return self.__hauteur

    def definirHauteur(self, hauteur):
        """
        Définit la hauteur du véhicule.

        Args:
            hauteur (float): Nouvelle valeur de la hauteur (en mètres).

        Comportement attendu :
            - Met à jour la hauteur enregistrée du véhicule.
            - Peut être appelée après une mesure effectuée par la caméra.
        """
        self.__hauteur = hauteur

    def obtenirLongueur(self):
        """
        Retourne la longueur actuelle du véhicule.

        Returns:
            float: La longueur du véhicule (en mètres).

        Comportement attendu :
            - Fournit la valeur enregistrée de la longueur du véhicule.
            - Utilisé pour déterminer la compatibilité avec les emplacements disponibles.
        """
        return self.__longueur

    def definirLongueur(self, longueur):
        """
        Définit la longueur du véhicule.

        Args:
            longueur (float): Nouvelle valeur de la longueur (en mètres).

        Comportement attendu :
            - Met à jour la longueur du véhicule.
            - Peut être appelée après une mesure effectuée par la caméra ou le capteur.
        """
        self.__longueur = longueur

    def obtenirImmatriculation(self):
        """
        Retourne l’immatriculation actuelle du véhicule.

        Returns:
            str: Numéro d’immatriculation du véhicule.

        Comportement attendu :
            - Fournit la plaque d’immatriculation du véhicule.
            - Sert à identifier le véhicule lors des entrées/sorties ou pour les abonnements.
        """
        return self.__immatriculation

    def definirImmatriculation(self, immatriculation):
        """
        Définit le numéro d’immatriculation du véhicule.

        Args:
            immatriculation (str): Nouvelle immatriculation du véhicule.

        Comportement attendu :
            - Met à jour l’immatriculation enregistrée.
            - Peut être appelée après une reconnaissance optique de la plaque par la caméra.
        """
        self.__immatriculation = immatriculation

