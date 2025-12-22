from .service import Service
from datetime import date
class Maintenance(Service):
    """
    Représente une opération de maintenance effectuée sur un véhicule
    dans le cadre du système DreamPark.

    Ce service peut inclure des vérifications techniques, des réparations
    mineures ou des interventions programmées pour assurer le bon état du véhicule.
    """
    def __init__(self, dateDemande):
        """
        Initialise un objet `Maintenance`.

        Comportement attendu :
            - Prépare la création d’une opération de maintenance.
            - Peut initialiser des informations internes comme la date, le technicien ou le type de maintenance.
            - Les détails spécifiques seront définis lors de l’exécution de la maintenance.
        """
        super.__init__(dateDemande)

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
        self.rapport = f"Maintenance effectuée sur {v.obtenirImmatriculation()}"
        return self.rapport
