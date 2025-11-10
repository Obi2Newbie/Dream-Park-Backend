class Place:
    """
    Représente une place physique dans le parking DreamPark.

    Attributs :
        numero (int) : Numéro unique identifiant la place.
        __niveau (str) : Niveau ou étage où se trouve la place
        __longueur (float) : Longueur maximale disponible pour un véhicule sur cette place.
        __estLibre (bool) : Indique si la place est actuellement libre ou occupée.
        hauteur (float) : Hauteur maximale autorisée pour les véhicules.
    """

    def __init__(self, numero, niveau, longueur, estLibre, hauteur):
        """
        Initialise une place de parking avec ses caractéristiques principales.

        Attributs:
            numero (int): Numéro identifiant la place.
            niveau (str): Niveau du parking où se trouve la place.
            longueur (float): Longueur maximale acceptée pour un véhicule.
            estLibre (bool): True si la place est libre, False si elle est occupée.
            hauteur (float): Hauteur maximale autorisée pour un véhicule.

        Comportement attendu :
            - Enregistre les caractéristiques physiques de la place.
            - Définit son état initial (libre ou occupée).
        """
        pass

    def addPlacementP(self, p):
        """
        Associe un objet `placement` (correspondant à un stationnement effectif)
        à cette place de parking.

        Attributs:
            p (placement): Objet représentant le placement d’un véhicule sur cette place.

        Comportement attendu :
            - Lie la place à un placement spécifique.
            - Peut mettre à jour l’état `__estLibre` selon le statut du placement.
            - Sert à tracer quel véhicule occupe actuellement cette place.
        """
        pass
