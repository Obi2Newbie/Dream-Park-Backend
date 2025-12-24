from .service import Service


class Maintenance(Service):
    """
    Représente un service de maintenance technique pour véhicules.

    Service incluant diagnostics techniques, vérifications approfondies
    et interventions mécaniques mineures réalisées par des techniciens
    qualifiés dans le parking DreamPark.

    Hérite de Service pour la gestion des dates et rapports.
    """

    def __init__(self, dateDemande):
        """
        Initialise une demande de maintenance.

        Args:
            dateDemande (date): Date à laquelle le client a demandé le service.
        """
        super().__init__(dateDemande, None, "Maintenance non effectué")

    def effectuerMaintenance(self, v):
        """
        Exécute la maintenance sur un véhicule et génère un rapport.

        Args:
            v (Voiture): Le véhicule nécessitant la maintenance.

        Returns:
            str: Rapport confirmant la maintenance avec l'immatriculation.

        Side Effects:
            Met à jour l'attribut rapport avec les détails d'intervention.
        """
        self.rapport = f"Maintenance effectuée sur {v.obtenirImmatriculation()}"
        return self.rapport