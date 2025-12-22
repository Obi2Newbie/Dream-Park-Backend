from .voiture import Voiture

class Acces:
    """
    Représente un accès du parking DreamPark, permettant la gestion
    des entrées et des sorties des véhicules et des clients.

    Cette classe regroupe les fonctionnalités liées à :
        - L’activation des caméras à l’entrée ou à la sortie.
        - L’affichage des informations sur les panneaux.
        - Le déclenchement des procédures d’entrée pour les clients.
    """
    def __init__(self, camera, borne, panneau, tel_entree, tel_sortie, parking):
        """
        Initialise un objet `acces`.

        Comportement attendu :
            - Prépare l’accès à être utilisé pour la gestion des entrées et sorties.
            - Peut initialiser les composants associés tels que la caméra et le panneau d’affichage.
            - Les détails d’initialisation (ex. numéro d’accès, position, type) seront définis ultérieurement.
        """
        self.MonParking = parking
        self.TelEntree = tel_entree
        self.__TelSortie = tel_sortie
        self.maBorne = borne
        self.monPanneau = panneau
        self.maCamera = camera

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
        if c.maVoiture:
            vHauteur = self.maCamera.capturerHauteur(c.maVoiture)
            vLongueur = self.maCamera.capturerLongueur(c.maVoiture)
            vImma = self.maCamera.capturerImmatr(c.maVoiture)
            voiture = Voiture(vHauteur, vLongueur, vImma)
            return voiture
        return None

    def actionnerPanneau(self):
        """
        Active le panneau d’affichage situé à l’accès.

        Returns:
            String: Message affiché sur le panneau (par exemple, le nombre de places disponibles).

        Comportement attendu :
            - Affiche des informations dynamiques (places libres, niveau complet, etc.).
            - Sert d’interface visuelle pour les clients à l’entrée et à la sortie.
        """
        if self.MonParking and self.monPanneau:
            return self.monPanneau.afficherNbPlacesDisponibles()

    def lancerProcedureEntree(self, c):
        """
        Lance la procédure d’entrée complète pour un client.
        Gère désormais la priorité pour les Super Abonnés (Pack Garanti).

        Args:
            c (Client): Objet représentant le client souhaitant entrer.

        Returns:
            string: Message indiquant le résultat de la procédure.
        """
        # 1. Identification du véhicule via la caméra
        # Note : actionnerCamera crée ou met à jour l'objet Voiture
        voiture = self.actionnerCamera(c)

        # 2. Recherche d'une place physique dans le parking
        placeAssignee = self.MonParking.rechercherPlace(voiture)

        if placeAssignee:
            # CAS 1 : Il y a de la place
            if not c.estAbonne:
                self.maBorne.deliverTicket(c)

            # Téléportation standard
            self.TelEntree.teleporterVoiture(voiture, placeAssignee)
            return f"Bienvenue {c.nom}. Place assignée : {placeAssignee.numero}"

        else:
            # CAS 2 : Le parking est physiquement complet
            if c.estSuperAbonne:
                # Gestion spécifique pour le Pack Garanti (Stationnement assuré)
                message = self.TelEntree.teleporterVoitureSuperAbonne(voiture)
                return f"Bienvenue {c.nom}. {message}"
            else:
                # Refus d'entrée pour les clients normaux ou abonnés simples
                return "Désolé, le parking est complet."
