class Contrat:
    """
    Représente un contrat liant un client au système DreamPark,
    par exemple un contrat d'abonnement ou de service.

    Attributs :
        dateDebut (date) : Date de début du contrat.
        dateFin (date) : Date de fin prévue du contrat.
        estEnCours (bool) : Indique si le contrat est toujours actif.
    """

    def __init__(self, dateDebut, dateFin, estEnCours):
        """
        Initialise un nouvel objet Contrat.

        Attributs:
            dateDebut (date): Date à laquelle le contrat entre en vigueur.
            dateFin (date): Date prévue pour la fin du contrat.
            estEnCours (bool): True si le contrat est actuellement actif.

        Comportement attendu :
            - Enregistre les dates de début et de fin.
            - Définit le statut du contrat (actif ou terminé).
        """
        pass

    def rompreContract(self):
        """
        Met fin au contrat actuel avant sa date de fin prévue.
        """
        pass