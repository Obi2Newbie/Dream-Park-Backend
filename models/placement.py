class Placement:
    """
    Représente le placement d'un véhicule dans une place de parking DreamPark.

    Attributs :
        dateDebut (date) : Date à laquelle le véhicule a été garé.
        dateFin (date) : Date prévue ou réelle de départ du véhicule.
        estEnCours (bool) : Indique si le placement est actuellement actif.
    """

    def __init__(self, dateDebut, dateFin=None, estEnCours=True):
        """
        Initialise un nouveau placement pour un véhicule dans le parking.

        Args:
            dateDebut (date): Date à laquelle le véhicule est entré dans le parking.
            dateFin (date, optionnel): Date prévue ou réelle de sortie (par défaut None).
            estEnCours (bool, optionnel): True si le véhicule est toujours garé (par défaut True).
        """
        pass

    def partirPlace(self):
        """
        Termine le placement actuel lorsque le véhicule quitte le parking.

        """
        pass
