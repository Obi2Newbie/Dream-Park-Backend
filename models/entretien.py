from .service import Service


class Entretien(Service):
    """
    Représente un service d'entretien de véhicule dans DreamPark.

    Service incluant nettoyage intérieur/extérieur, vérifications
    techniques mineures, et maintenance préventive de base.

    Hérite de Service pour la gestion des dates et rapports.
    """

    def __init__(self, dateDemande):
        """
        Initialise une demande d'entretien.

        Args:
            dateDemande (date): Date à laquelle le client a demandé le service.
        """
        super().__init__(dateDemande, None, "Entretien non effectué")

    def effectuerEntretien(self):
        """
        Exécute le service d'entretien et génère un rapport.

        Returns:
            str: Rapport confirmant la réalisation de l'entretien.

        Side Effects:
            Met à jour l'attribut rapport avec le compte-rendu.
        """
        self.rapport = "L'entretien demandé par le client est fait."
        return self.rapport