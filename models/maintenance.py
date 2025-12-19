from .service import Service
from datetime import date
class Maintenance(Service):
    """
    Représente une opération de maintenance effectuée sur un véhicule
    dans le cadre du système DreamPark.

    Ce service peut inclure des vérifications techniques, des réparations
    mineures ou des interventions programmées pour assurer le bon état du véhicule.
    """
    def effectuerMaintenance(self, v):
        """
        Effectue la maintenance sur un véhicule donné.

        Args:
            v (Voiture): Objet représentant le véhicule nécessitant une maintenance.

        Comportement attendu :
            - Réalise les actions prévues pour la maintenance du véhicule.
            - Met à jour les informations associées à l’état ou à l’historique du véhicule.
            - Peut générer un rapport de maintenance ou notifier le client.
            - Interagit avec d’autres services (entretien, livraison, etc.) si nécessaire.
        """
        self.dateService = date()
        self.rapport = f"Maintenance effectuée sur {v.obtenirImmatriculation()} le {self.dateService}"
