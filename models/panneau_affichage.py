class Panneau_affichage:
    """
    Représente un panneau d'information dynamique du parking DreamPark.

    Affichage électronique situé aux entrées pour informer les clients
    en temps réel sur l'état du parking (places disponibles, niveaux
    complets, messages d'orientation).
    """

    def afficherNbPlacesDisponibles(self, p):
        """
        Affiche le nombre de places actuellement libres dans le parking.

        Args:
            p (Parking): Le parking dont on veut afficher l'état.

        Returns:
            str: Message formaté indiquant le nombre de places disponibles.
        """