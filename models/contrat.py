class Contrat:
    """
    Représente un contrat d'abonnement entre un client et DreamPark.

    Le contrat matérialise juridiquement la relation d'abonnement,
    définissant la durée de validité et le statut actif/inactif.

    Attributes:
        dateDebut (date): Date de début de validité du contrat.
        dateFin (date): Date de fin prévue (None si durée indéterminée).
        estEnCours (bool): True si le contrat est actuellement actif.
        monAbonnement (Abonnement): L'abonnement associé à ce contrat.
    """

    def __init__(self, dateDebut, dateFin, estEnCours):
        """
        Initialise un nouveau contrat d'abonnement.

        Args:
            dateDebut (date): Date d'entrée en vigueur.
            dateFin (date): Date de fin prévue (peut être None).
            estEnCours (bool): Statut initial du contrat (True = actif).
        """

    def rompreContract(self):
        """
        Résilie le contrat avant sa date de fin naturelle.

        Désactive le contrat et enregistre la date de rupture.

        Note:
            La date de fin est mise à jour avec la date du jour de résiliation.
        """