class Voiturier:
    """
    Représente un employé voiturier du service premium DreamPark.

    Professionnel chargé de la livraison et récupération des véhicules
    des clients Super Abonnés ou ayant souscrit au service de livraison.

    Attributes:
        numVoiturier (int): Identifiant unique du voiturier.
    """

    def __init__(self, numVoiturier):
        """
        Initialise un voiturier avec son identifiant.

        Args:
            numVoiturier (int): Numéro d'identification unique.
        """
        self.numVoiturier = numVoiturier

    def livrerVoiture(self, v, date, heure):
        """
        Effectue la livraison d'un véhicule à l'adresse du client.

        Le voiturier récupère le véhicule dans le parking, le conduit
        jusqu'à l'adresse de livraison programmée et génère un rapport.

        Args:
            v (Voiture): Le véhicule à livrer.
            date (date): Date prévue de livraison.
            heure (str): Heure de livraison (ex: "14" pour 14h).

        Returns:
            str: Message confirmant la livraison ou erreur si véhicule absent.

        Side Effects:
            - Termine le placement du véhicule (v.partirPlace())
            - Met à jour le rapport du service de livraison associé
            - Marque le service comme effectué

        Raises:
            Retourne un message d'erreur si le véhicule n'est pas dans le parking.
        """
        if not v.estDansParking:
            return f"Erreur : La voiture {v.obtenirImmatriculation()} n'est pas dans le parking."

        if v.monPlacement:
            v.monPlacement.partirPlace()

        # Mise à jour du service de livraison si trouvé
        if v.proprietaire and hasattr(v.proprietaire, 'mesServices'):
            for service in v.proprietaire.mesServices:
                if hasattr(service, 'adresse') and service.dateDemande == date:
                    service.dateService = date.today()
                    service.rapport = (f"Livraison effectuée avec succès à {heure}h "
                                       f"par le voiturier n°{self.numVoiturier}.")
                    break

        return f"Le voiturier {self.numVoiturier} a livré la voiture {v.obtenirImmatriculation()} le {date} à {heure}h."