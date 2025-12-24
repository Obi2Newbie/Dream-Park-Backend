from .place import Place


class Parking:
    """
    Représente le parking central du système DreamPark (Singleton).

    Cette classe gère l'ensemble du parking multi-niveaux, incluant :
    - La gestion des places disponibles
    - Les abonnements clients
    - La tarification
    - Les points d'accès

    Implémente le pattern Singleton pour garantir une instance unique.

    Attributes:
        __nbPlacesParNiveau (int): Capacité par niveau du parking.
        __nbPlacesLibres (int): Nombre actuel de places disponibles.
        __prix (float): Tarif horaire de base en euros.
        nBNiveau (int): Nombre total de niveaux dans le parking.
        mesPlaces (list): Liste de toutes les places du parking.
        mesAbonnements (list): Liste des abonnements gérés.
        acces1 (Acces): Premier point d'accès (entrée Nord).
        acces2 (Acces): Second point d'accès (sortie Sud).
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Implémente le pattern Singleton.

        Garantit qu'une seule instance de Parking existe dans l'application.

        Returns:
            Parking: L'instance unique du parking.
        """
        if cls.__instance is None:
            cls.__instance = super(Parking, cls).__new__(cls)
        return cls.__instance

    def __init__(self, nbPlacesParNiveau, nbPlacesLibres, prix, nBNiveau):
        """
        Initialise le parking avec sa configuration de base.

        Args:
            nbPlacesParNiveau (int): Nombre de places par niveau.
            nbPlacesLibres (int): Nombre initial de places libres.
            prix (float): Tarif de base en euros.
            nBNiveau (int): Nombre de niveaux du parking.

        Note:
            N'initialise qu'une seule fois grâce au flag 'initialized'.
        """
        if not hasattr(self, 'initialized'):
            self.__nbPlacesParNiveau = nbPlacesParNiveau
            self.__nbPlacesLibres = nbPlacesLibres
            self.__prix = prix
            self.mesPlaces = []
            self.mesAbonnements = []
            self.nBNiveau = nBNiveau
            self.acces1 = None
            self.acces2 = None
            self.initialized = True

    def rechercherPlace(self, v):
        """
        Recherche une place adaptée aux dimensions d'un véhicule.

        Parcourt les places disponibles et sélectionne la première
        place libre dont les dimensions sont compatibles avec le véhicule.

        Args:
            v (Voiture): Le véhicule cherchant une place.

        Returns:
            Place: La première place compatible trouvée, ou None si aucune
                   place n'est disponible ou compatible.

        Algorithm:
            Vérifie pour chaque place :
            1. Est-elle libre ?
            2. Sa hauteur >= hauteur du véhicule ?
            3. Sa longueur >= longueur du véhicule ?
        """
        for place in self.mesPlaces:
            if (place.obtenir_estLibre() and
                    place.obtenir_hauteur() >= v.obtenirHauteur() and
                    place.obtenir_longueur() >= v.obtenirLongueur()):
                return place
        return None

    def nbPlacesLibresParNiveau(self, niveau):
        """
        Calcule le nombre de places libres pour un niveau spécifique.

        Args:
            niveau (str): Identifiant du niveau (ex: "A", "B", "C").

        Returns:
            int: Nombre de places libres dans ce niveau.

        Side Effects:
            Met à jour l'attribut privé __nbPlacesLibres.
        """
        placeLibre = 0
        for p in self.mesPlaces:
            if p.obtenir_niveau() == niveau and p.obtenir_estLibre():
                placeLibre += 1
        self.__nbPlacesLibres = placeLibre
        return placeLibre

    def addAbonnement(self, ab):
        """
        Enregistre un nouvel abonnement dans le système du parking.

        Args:
            ab (Abonnement): L'abonnement à ajouter.

        Note:
            Permet de suivre tous les abonnements actifs pour statistiques
            et gestion de la clientèle.
        """
        self.mesAbonnements.append(ab)

    def obtenirPrix(self):
        """
        Retourne le tarif de base du parking.

        Returns:
            float: Tarif horaire en euros.
        """
        return self.__prix