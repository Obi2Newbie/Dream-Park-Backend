class Service:
    """
    Classe de base abstraite pour tous les services DreamPark.

    Fournit la structure commune pour Maintenance, Entretien et Livraison,
    avec gestion des dates et génération de rapports.

    Attributes:
        dateDemande (date): Date à laquelle le service a été demandé.
        dateService (date): Date effective de réalisation du service.
        rapport (str): Compte-rendu généré après exécution du service.
    """

    def __init__(self, dateDemande, dateService, rapport):
        """
        Initialise un service avec ses informations de base.

        Args:
            dateDemande (date): Date de la demande client.
            dateService (date): Date prévue/réalisée du service.
            rapport (str): État initial du rapport.
        """