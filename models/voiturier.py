class Voiturier:
    """
    Représente un voiturier du système DreamPark.

    Le voiturier est responsable de la livraison ou de la récupération
    des véhicules des clients, notamment dans le cadre de services
    premium ou de super abonnements.
    """

    def __init__(self, numVoiturier):
        """
        Initialise un objet `Voiturier`.

        Args:
            numVoiturier (int): Numéro d’identification unique du voiturier.

        Comportement attendu :
            - Enregistre l’identifiant du voiturier.
            - Prépare l’objet pour être associé à une opération de livraison ou de récupération.
        """
        self.numVoiturier = numVoiturier

    def livrerVoiture(self, v, date, heure):
        """
        Effectue la livraison d’un véhicule à un client à une date et une heure précises.

        Args:
            v (Voiture): Objet représentant le véhicule à livrer.
            date (date): Date prévue pour la livraison du véhicule.
            heure (int): Heure de la livraison.

        Comportement attendu :
            - Gère la préparation et le déplacement du véhicule pour sa livraison.
            - Coordonne l’action avec le service client ou le téléporteur.
            - Peut générer un rapport ou une confirmation de livraison.
        """
        if not v.estDansParking:
            return f"Erreur : La voiture {v.obtenirImmatriculation()} n'est pas dans le parking."
        if v.monPlacement:
            v.partirPlace()
        if v.proprietaire and hasattr(v.proprietaire, 'mesServices'):
            for service in v.proprietaire.mesServices:
                # Si c'est un service de livraison prévu pour cette date
                if hasattr(service, 'adresse') and service.dateDemande == date:
                    service.dateService = date.today()
                    service.rapport = (f"Livraison effectuée avec succès à {heure}h "
                                       f"par le voiturier n°{self.numVoiturier}.")
                    break

        return f"Le voiturier {self.numVoiturier} a livré la voiture {v.obtenirImmatriculation()} le {date} à {heure}h."
