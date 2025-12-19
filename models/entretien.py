from .service import Service
from datetime import date

class Entretien(Service):
    """
    Représente une opération d’entretien de véhicule dans le système DreamPark.

    Cette classe correspond à un service effectué sur un véhicule,
    tel qu’un nettoyage, une révision ou une vérification technique.
    """

    def effectuerEntretien(self):
        """
        Exécute le service d’entretien du véhicule.

        Comportement attendu :
            - Réalise les actions prévues dans le cadre de l’entretien.
            - Met à jour l’état du véhicule ou du dossier d’entretien.
            - Peut générer un rapport détaillant les opérations effectuées.
            - Interagit éventuellement avec d’autres services du système DreamPark.
        """
        self.dateService = date()
        self.rapport = f"L'entretien demandé par le client est fait le {self.dateService}"
