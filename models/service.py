
class Service:
    """
    Représente un service fourni par le système DreamPark,
    tel qu'une livraison, un entretien ou une maintenance.

    Attributs :
        dateDemande (date) : Date à laquelle le client a effectué la demande du service.
        dateService (date) : Date prévue ou réalisée pour la prestation du service.
        rapport (str) : Compte rendu ou rapport généré à la suite du service.
    """

    def __init__(self, dateDemande, dateService, rapport):
        """
        Initialise un objet Service.

        Comportement attendu :
            - Crée une nouvelle instance de service avec des attributs par défaut.
            - Prépare l'objet pour l'enregistrement ou l'utilisation dans le système.
            - Les dates et le rapport seront définis ou mis à jour ultérieurement.
        """
        self.dateDemande = dateDemande
        self.dateService = dateService
        self.rapport = rapport
