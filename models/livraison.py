from .service import Service

class Livraison(Service):
    """
    Représente une opération de livraison de véhicule dans le système DreamPark.

    Cette classe gère le processus de remise du véhicule au client,
    qu’il s’agisse d’un service classique ou d’un avantage réservé
    aux abonnés premium.
    """
    def __init__(self, dateDemande, heure, adresse):
        super().__init__(dateDemande, None,"Livraison non effectué")
        self.adresse = adresse
        self.heure = heure

    def effectuerLivraison(self):
        """
        Effectue la livraison d’un véhicule au client.

        Comportement attendu :
            - Exécute l’action de remise du véhicule au client.
            - Met à jour l’état du véhicule (livré, en attente, etc.).
            - Peut générer un rapport ou une confirmation de livraison.
            - Interagit éventuellement avec un voiturier ou un service associé.
        """
        self.rapport = f"Livraison effectuée à {self.adresse} à {self.heure}h"
        return self.rapport
