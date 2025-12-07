from .camera import Camera
class Acces:
    """
    Représente un accès du parking DreamPark, permettant la gestion
    des entrées et des sorties des véhicules et des clients.

    Cette classe regroupe les fonctionnalités liées à :
        - L’activation des caméras à l’entrée ou à la sortie.
        - L’affichage des informations sur les panneaux.
        - Le déclenchement des procédures d’entrée pour les clients.
    """
    def __init__(self):
        """
        Initialise un objet `acces`.

        Comportement attendu :
            - Prépare l’accès à être utilisé pour la gestion des entrées et sorties.
            - Peut initialiser les composants associés tels que la caméra et le panneau d’affichage.
            - Les détails d’initialisation (ex. numéro d’accès, position, type) seront définis ultérieurement.
        """
        self.teleporteurs = []

    def actionnerCamera(self, c):
        """
        Active la caméra associée à cet accès pour identifier un véhicule.

        Args:
            c (Client): Objet représentant le client entrant ou sortant.

        Returns:
            Voiture: Objet contenant les informations capturées sur le véhicule.

        Comportement attendu :
            - Déclenche la caméra pour capturer la plaque d’immatriculation et les dimensions du véhicule.
            - Crée ou met à jour un objet `Voiture` lié au client.
            - Peut être utilisé au moment de l’entrée pour attribuer une place de parking.
        """
        camera = Camera()
        voiture = c.nouvenouvelleVoiture("FS-590-VS", 1.90, 2.00)

    def actionnerPanneau(self):
        """
        Active le panneau d’affichage situé à l’accès.

        Returns:
            String: Message affiché sur le panneau (par exemple, le nombre de places disponibles).

        Comportement attendu :
            - Affiche des informations dynamiques (places libres, niveau complet, etc.).
            - Sert d’interface visuelle pour les clients à l’entrée et à la sortie.
        """
        pass

    def lancerProcedureEntree(self, c):
        """
        Lance la procédure d’entrée complète pour un client.

        Args:
            c (Client): Objet représentant le client souhaitant entrer dans le parking.

        Returns:
            string: Message indiquant le résultat de la procédure (succès, échec, erreur).

        Comportement attendu :
            - Coordonne les actions de la caméra et du panneau.
            - Attribue une place de parking si disponible.
            - Gère les cas où le parking est complet ou la carte d’abonnement est invalide.
        """
        pass

    def obtenirTeleporteurDisponible(self):
        """
        Recherche un teleporteur disponible parmi ceux de l'acces.

        Returns:
            Teleporteur: Un teleporteur disponible ou None
        """
        for teleporteur in self.teleporteurs:
            if teleporteur.estDisponible():
                return teleporteur
        return None
