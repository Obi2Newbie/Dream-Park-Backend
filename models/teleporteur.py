from datetime import date
from .placement import Placement
class Teleporteur:
    """
    Représente le téléporteur du système DreamPark.

    Cet équipement permet de déplacer automatiquement un véhicule
    vers une place de parking spécifique, sans intervention humaine.
    """
    def __init__(self, parking_instance):
        self.parking = parking_instance

    def teleporterVoiture(self, v, p):
        """
        Téléporte un véhicule donné vers une place de parking précise.

        Args:
            v (Voiture): Objet représentant le véhicule à déplacer.
            p (Place): Objet représentant la place de destination dans le parking.

        Returns:
            Placement: Objet indiquant le nouveau placement du véhicule après la téléportation.

        Comportement attendu :
            - Transfère virtuellement le véhicule jusqu’à la place spécifiée.
            - Met à jour le statut du véhicule et de la place.
            - Génère un objet `Placement` reflétant la nouvelle position du véhicule.
        """
        nouveau_placement = Placement(date.today(), None, True)
        p.addPlacementP(nouveau_placement)
        v.addPlacementV(nouveau_placement)
        return nouveau_placement

    def teleporterVoitureSuperAbonne(self, v):
        """
        Téléporte automatiquement le véhicule d’un client super abonné.

        Args:
            v (Voiture): Objet représentant le véhicule du super abonné.

        Returns:
            String: Message décrivant le résultat de la téléportation (succès, échec, etc.).

        Comportement attendu :
            - Identifie une place premium réservée aux super abonnés.
            - Téléporte directement le véhicule sans intervention manuelle.
            - Confirme la réussite de l’opération via un message ou un rapport système.
        """

        place = self.parking.rechercherPlace(v)

        if place:
            self.teleporterVoiture(v, place)
            place.definir_estLibre(False)
            return f"Voiture garée dans le parking {place.obtenir_niveau()}{place.numero}"
        else:
            v.estDansParking = True
            return "Parking complet : Voiture prise en charge par le service Valet (Pack Garanti)."