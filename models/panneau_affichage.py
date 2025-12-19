class Panneau_affichage:
    """
    Représente un panneau d’affichage du système DreamPark.

    Ce panneau sert à informer les clients sur l’état du parking,
    notamment le nombre de places disponibles ou les messages d’accès.
    """
    def afficherNbPlacesDisponibles(self, p):
        """
        Affiche sur le panneau le nombre de places actuellement disponibles
        dans le parking spécifié.

        Args:
            p (Parking): Objet représentant le parking dont on veut afficher l’état.

        Returns:
            string: Message affiché sur le panneau, indiquant le nombre de places libres.

        Comportement attendu :
            - Récupère les données du parking via l’objet `p`.
            - Met à jour l’affichage visuel pour informer les clients.
            - Peut afficher des messages spéciaux si le parking est complet ou réservé.
        """
        return p.NbPlacesDisponibles()
