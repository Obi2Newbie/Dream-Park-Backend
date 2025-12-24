class Placement:
    """
    Représente le stationnement effectif d'un véhicule dans une place.

    Lie un véhicule à une place spécifique avec traçabilité temporelle
    (dates d'entrée et sortie). Fait le lien entre Voiture et Place.

    Attributes:
        dateDebut (date): Date et heure d'entrée du véhicule.
        dateFin (date): Date et heure de sortie (None si encore garé).
        estEnCours (bool): True si le véhicule est encore dans la place.
        maPlace (Place): Référence vers la place occupée.
    """

    def __init__(self, dateDebut, dateFin=None, estEnCours=True):
        """
        Initialise un nouveau placement.

        Args:
            dateDebut (date): Date d'entrée du véhicule.
            dateFin (date, optional): Date de sortie prévue. Defaults to None.
            estEnCours (bool, optional): Statut actif. Defaults to True.
        """

    def partirPlace(self):
        """
        Termine le placement et libère automatiquement la place associée.

        Appelé lors de la sortie du véhicule pour mettre à jour tous
        les états (placement terminé + place libérée).

        Side Effects:
            - Désactive le placement (estEnCours = False)
            - Enregistre la date de sortie
            - Libère automatiquement la place (maPlace.definir_estLibre(True))
        """