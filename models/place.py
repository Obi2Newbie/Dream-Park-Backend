class Place:
    """
    Représente une place physique dans le parking DreamPark.

    Attributs :
        numero (int) : Numéro unique identifiant la place.
        __niveau (str) : Niveau ou étage où se trouve la place
        __longueur (float) : Longueur maximale disponible pour un véhicule sur cette place.
        __estLibre (bool) : Indique si la place est actuellement libre ou occupée.
        __hauteur (float) : Hauteur maximale autorisée pour les véhicules.
    """

    def __init__(self, numero, niveau, longueur, hauteur):
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
        self.numero = numero
        self.__niveau = niveau
        self.__longueur = longueur
        self.__estLibre = True
        self.__hauteur = hauteur
        self.monPlacement = None

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
        self.monPlacement = p
        self.estLibre = False

    def obtenir_niveau(self):
        """
        Retourne le niveau ou l'étage où se situe la place.

        Returns:
            str: L'identifiant du niveau (ex: "Niveau 0").
        """
        return self.__niveau

    def obtenir_longueur(self):
        """
        Retourne la longueur maximale autorisée pour cette place.

        Returns:
            float: La longueur de la place en mètres.
        """
        return self.__longueur

    def obtenir_estLibre(self):
        """
        Vérifie si la place est actuellement disponible.

        Returns:
            bool: True si la place est libre, False si elle est occupée.
        """
        return self.__estLibre

    def definir_estLibre(self, estLibre):
        """
        Modifie l'état de disponibilité de la place.

        Args:
            estLibre (bool): Le nouvel état (True pour libre, False pour occupé).

        Comportement attendu :
            - Met à jour l'attribut privé __estLibre.
            - Permet au système de parking de suivre l'occupation en temps réel.
        """
        self.__estLibre = estLibre

    def obtenir_hauteur(self):
        """
        Retourne la hauteur maximale autorisée pour cette place.

        Returns:
            float: La hauteur de la place en mètres.
        """
        return self.__hauteur
