class Voiture:
    """
    Représente une voiture gérée par le système DreamPark.

    Attributs :
        __hauteur (float) : Hauteur du véhicule en mètres.
        __longueur (float) : Longueur du véhicule en mètres.
        __immatriculation (str) : Numéro d'immatriculation du véhicule.
        estDansParking (bool) : Indique si le véhicule est actuellement stationné dans le parking.
    """

    def __init__(self, hauteur, longueur, immatriculation, estDansParking):
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
        pass

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
