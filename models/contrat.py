from datetime import datetime, timedelta


class Contrat:
    """
    Represente un contrat liant un client a un abonnement.
    Le contrat a une date de debut et une duree.
    """

    def __init__(self, date_debut, duree_jours):
        """
        Initialise un contrat.

        Args:
            date_debut (datetime): Date de debut du contrat
            duree_jours (int): Duree du contrat en jours
        """
        self.date_debut = date_debut
        self.duree_jours = duree_jours
        self.date_fin = date_debut + timedelta(days=duree_jours)
        self.abonnement = None

    def estValide(self):
        """
        Verifie si le contrat est encore valide.

        Returns:
            bool: True si valide, False sinon
        """
        return datetime.now() < self.date_fin

    def jours_restants(self):
        """
        Calcule le nombre de jours restants avant expiration.

        Returns:
            int: Nombre de jours restants
        """
        if not self.estValide():
            return 0
        delta = self.date_fin - datetime.now()
        return delta.days