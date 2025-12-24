class Place:
    """
    Représente une place de stationnement physique dans DreamPark.

    Chaque place a des dimensions maximales autorisées et un état
    d'occupation qui évolue dynamiquement avec les entrées/sorties.

    Attributes:
        numero (int): Numéro unique de la place dans son niveau.
        __niveau (str): Identifiant du niveau (ex: "A", "B", "C").
        __longueur (float): Longueur maximale autorisée en mètres.
        __hauteur (float): Hauteur maximale autorisée en mètres.
        __estLibre (bool): True si la place est disponible.
        monPlacement (Placement): Placement actuel si la place est occupée.
    """

    def __init__(self, numero, niveau, longueur, hauteur):
        """
        Initialise une nouvelle place de parking.

        Args:
            numero (int): Numéro de la place.
            niveau (str): Niveau du parking (ex: "A", "B").
            longueur (float): Longueur maximale en mètres.
            hauteur (float): Hauteur maximale en mètres.
        """
        self.numero = numero
        self.__niveau = niveau
        self.__longueur = float(longueur)
        self.__estLibre = True
        self.__hauteur = float(hauteur)
        self.monPlacement = None

    def addPlacementP(self, p):
        """
        Associe un placement (véhicule garé) à cette place.

        Établit une référence bidirectionnelle entre la Place et le Placement
        et marque la place comme occupée.

        Args:
            p (Placement): Le placement à associer.

        Side Effects:
            - Définit p.maPlace = self (référence bidirectionnelle)
            - Marque la place comme occupée (__estLibre = False)
        """
        self.monPlacement = p
        p.maPlace = self  # Référence bidirectionnelle
        self.__estLibre = False

    def obtenir_niveau(self):
        """Retourne l'identifiant du niveau de cette place."""
        return self.__niveau

    def obtenir_longueur(self):
        """Retourne la longueur maximale autorisée en mètres."""
        return self.__longueur

    def obtenir_estLibre(self):
        """Retourne True si la place est actuellement libre."""
        return self.__estLibre

    def definir_estLibre(self, estLibre):
        """
        Modifie l'état de disponibilité de la place.

        Args:
            estLibre (bool): True pour libérer, False pour occuper.

        Side Effects:
            Si estLibre=True, supprime la référence au placement (cleanup).
        """
        self.__estLibre = estLibre
        if estLibre:
            self.monPlacement = None

    def obtenir_hauteur(self):
        """Retourne la hauteur maximale autorisée en mètres."""
        return self.__hauteur

    def __str__(self):
        """
        Représentation textuelle de l'état de la place.

        Returns:
            str: Description formatée de la place et son statut.
        """
        statut = "libre" if self.__estLibre else "occupé"
        return (f"Place {self.__niveau}{self.numero} "
                f"de hauteur {self.__hauteur} et longueur {self.__longueur} "
                f"est {statut}.")