from datetime import date
from .service import Service


class Livraison(Service):
    """
    Représente une opération de livraison de véhicule dans le système DreamPark.

    Cette classe gère le processus de remise du véhicule au client,
    qu’il s’agisse d’un service classique ou d’un avantage réservé
    aux abonnés premium.
    """
    def effectuerLivraison(self):
        """
        Effectue la livraison d’un véhicule au client.

        Comportement attendu :
            - Exécute l’action de remise du véhicule au client.
            - Met à jour l’état du véhicule (livré, en attente, etc.).
            - Peut générer un rapport ou une confirmation de livraison.
            - Interagit éventuellement avec un voiturier ou un service associé.
        """
        self.dateService = date()
        self.rapport = f"Livraison effectué le {self.dateService}"
