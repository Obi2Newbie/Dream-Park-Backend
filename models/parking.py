class Parking:
    """
    Représente le parking principal du système DreamPark.

    Attributs :
        __nbPlacesParNiveau (int) : Nombre total de places disponibles à chaque niveau du parking.
        __nbPlacesLibres (int) : Nombre de places actuellement libres dans le parking.
        __prix (float) : Tarif de stationnement appliqué aux utilisateurs non abonnés.
        nbNiveau (int) : Nombre total de niveaux ou d’étages dans le parking.
    """

    def __init__(self, nbPlacesParNiveau, nbPlacesLibres, prix, nBNiveau):
        """
        Initialise un objet Parking avec ses capacités principales.

        Args:
            nbPlacesParNiveau (int) : Nombre de places disponibles par niveau.
            nbPlacesLibres (int) : Nombre de places libres au moment de l’initialisation.
            __prix (float) : Tarif de stationnement appliqué aux utilisateurs non abonnés.
            nbNiveau (int) : Nombre total de niveaux ou d’étages dans le parking.

        Comportement attendu:
            - Définit la capacité du parking.
            - Initialise le nombre de places libres.
            - Prépare l’objet à la gestion des véhicules et des abonnements.
        """
        self.__nbPlacesParNiveau = nbPlacesParNiveau
        self.__nbPlacesLibres = nbPlacesLibres
        self.__prix = prix
        self.places = []
        self.__nBNiveau = nBNiveau

    def rechercherPlace(self, v):
        """
        Recherche une place adaptée pour un véhicule donné.

        Args:
            v (voiture): Objet représentant le véhicule cherchant à se garer.

        Returns:
            Place: L’objet représentant la place attribuée au véhicule.

        Comportement attendu :
            - Évalue les dimensions du véhicule et trouve une place compatible.
            - Prend en compte la hauteur et la longueur maximales autorisées.
            - Met à jour l’état des places disponibles.
        """
        pass

    def nbPlacesLibresParNiveau(self, niveau: str):
        """
        Calcule et retourne le nombre de places libres pour un niveau spécifique.

        Args:
            niveau (str): Identifiant ou nom du niveau.

        Returns:
            int: Nombre de places libres à ce niveau.

        Comportement attendu :
            - Parcourt les places associées au niveau indiqué.
            - Compte uniquement celles marquées comme libres.
            - Peut être utilisé pour afficher des informations sur les panneaux d’entrée.
        """
        placeLibre = 0
        for p in self.places:
            if p.obtenir_niveau() == niveau and p.obtenir_estLibre():
                placeLibre += 1
        return placeLibre
    def addAbonnement(self, ab):
        """
        Ajoute un abonnement au système de gestion du parking.

        Args:
            ab (Abonnement): Objet représentant l’abonnement à enregistrer.

        Comportement attendu :
            - Enregistre l’abonnement dans le système de gestion.
            - Peut ajuster les statistiques liées aux abonnés.
            - Sert à gérer les droits ou tarifs spécifiques des clients abonnés.
        """
        pass
