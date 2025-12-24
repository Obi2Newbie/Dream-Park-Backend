from datetime import date
from .placement import Placement


class Teleporteur:
    """
    Représente le système de téléportation automatique de véhicules.

    Technologie futuriste permettant de déplacer instantanément les
    véhicules vers leur place assignée sans intervention humaine.
    Réduit drastiquement le temps de stationnement.

    Attributes:
        parking (Parking): Référence vers le parking pour rechercher des places.
    """

    def __init__(self, parking_instance):
        """
        Initialise le téléporteur avec référence au parking.

        Args:
            parking_instance (Parking): Le parking où opère ce téléporteur.
        """
        self.parking = parking_instance

    def teleporterVoiture(self, v, p):
        """
        Téléporte un véhicule vers une place spécifique.

        Crée un placement actif et établit tous les liens nécessaires
        entre le véhicule, le placement et la place.

        Args:
            v (Voiture): Le véhicule à téléporter.
            p (Place): La place de destination.

        Returns:
            Placement: L'objet placement créé pour tracer ce stationnement.

        Side Effects:
            - Crée un nouveau Placement
            - Établit les liens Voiture ↔ Placement ↔ Place
            - Met à jour v.estDansParking = True
        """
        nouveau_placement = Placement(date.today(), None, True)

        # Établir les liens bidirectionnels
        p.addPlacementP(nouveau_placement)  # Place ↔ Placement
        v.addPlacementV(nouveau_placement)  # Voiture ↔ Placement

        return nouveau_placement

    def teleporterVoitureSuperAbonne(self, v):
        """
        Téléportation prioritaire pour les clients Super Abonnés (Pack Garanti).

        Recherche automatiquement une place disponible et téléporte le véhicule.
        Si le parking est complet, active le service Valet premium.

        Args:
            v (Voiture): Le véhicule du super abonné.

        Returns:
            str: Message confirmant la téléportation ou l'activation du Valet.

        Algorithm:
            1. Recherche place compatible
            2. Si trouvée → téléportation standard
            3. Si complet → service Valet (garantie pack)
        """
        place = self.parking.rechercherPlace(v)

        if place:
            self.teleporterVoiture(v, place)
            place.definir_estLibre(False)
            return f"Voiture garée dans le parking {place.obtenir_niveau()}{place.numero}"
        else:
            v.estDansParking = True
            return "Parking complet : Voiture prise en charge par le service Valet (Pack Garanti)."