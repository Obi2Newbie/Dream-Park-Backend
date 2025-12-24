from .service import Service


class Livraison(Service):
    """
    Représente un service de livraison de véhicule par voiturier.

    Service permettant au client de faire livrer son véhicule à une
    adresse spécifique à une date et heure précises, sans avoir à
    revenir au parking.

    Hérite de Service pour la gestion des dates et rapports.

    Attributes (en plus de Service):
        adresse (str): Adresse de destination de la livraison.
        heure (str): Heure prévue de livraison.
    """

    def __init__(self, dateDemande, heure, adresse):
        """
        Initialise une demande de livraison.

        Args:
            dateDemande (str): Date souhaitée pour la livraison (format "JJ/MM/AAAA").
            heure (str): Heure de livraison souhaitée (ex: "14" pour 14h).
            adresse (str): Adresse complète de destination.
        """
        super().__init__(dateDemande, None, "Livraison non effectué")
        self.adresse = adresse
        self.heure = heure

    def effectuerLivraison(self):
        """
        Exécute la livraison et génère le rapport de confirmation.

        Returns:
            str: Rapport détaillant l'adresse et l'heure de livraison.

        Side Effects:
            Met à jour l'attribut rapport avec les détails de livraison.
        """
        self.rapport = f"Livraison effectuée à {self.adresse} à {self.heure}h"