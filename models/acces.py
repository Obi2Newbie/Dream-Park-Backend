from .voiture import Voiture
from .voiturier import Voiturier
from .maintenance import Maintenance
from .livraison import Livraison
from .entretien import Entretien
import time
from datetime import datetime


class Acces:
    """
    Représente un accès du parking DreamPark, permettant la gestion
    des entrées et des sorties des véhicules et des clients.

    Cette classe regroupe les fonctionnalités liées à :
        - L'activation des caméras à l'entrée ou à la sortie.
        - L'affichage des informations sur les panneaux.
        - Le déclenchement des procédures d'entrée pour les clients.
    """

    def __init__(self, camera, borne, panneau, tel_entree, tel_sortie, parking):
        """
        Initialise un objet `acces`.

        Comportement attendu :
            - Prépare l'accès à être utilisé pour la gestion des entrées et sorties.
            - Peut initialiser les composants associés tels que la caméra et le panneau d'affichage.
            - Les détails d'initialisation (ex. numéro d'accès, position, type) seront définis ultérieurement.
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
            Voiture: L'objet Voiture du client (pas une nouvelle instance).

        Comportement attendu :
            - Déclenche la caméra pour capturer la plaque d'immatriculation et les dimensions du véhicule.
            - Retourne la voiture existante du client.
            - Peut être utilisé au moment de l'entrée pour attribuer une place de parking.
        """
        if c.maVoiture:
            # On utilise la voiture existante du client, pas une nouvelle
            vHauteur = self.maCamera.capturerHauteur(c.maVoiture)
            vLongueur = self.maCamera.capturerLongueur(c.maVoiture)
            vImma = self.maCamera.capturerImmatr(c.maVoiture)

            # Retourner la voiture existante, pas en créer une nouvelle
            return c.maVoiture
        return None

    def actionnerPanneau(self):
        """
        Active le panneau d'affichage situé à l'accès.

        Returns:
            String: Message affiché sur le panneau (par exemple, le nombre de places disponibles).

        Comportement attendu :
            - Affiche des informations dynamiques (places libres, niveau complet, etc.).
            - Sert d'interface visuelle pour les clients à l'entrée et à la sortie.
        """
        if self.MonParking and self.monPanneau:
            return self.monPanneau.afficherNbPlacesDisponibles()

    def lancerProcedureEntree(self, c):
        """
        Lance la procédure d'entrée complète pour un client.
        Gère désormais la priorité pour les Super Abonnés (Pack Garanti).

        Args:
            c (Client): Objet représentant le client souhaitant entrer.

        Returns:
            string: Message indiquant le résultat de la procédure.
        """
        # 1. Identification du véhicule via la caméra
        # Note : actionnerCamera retourne maintenant la voiture existante du client
        voiture = self.actionnerCamera(c)
        statut = self.maBorne.recupererInfosCarte(c)
        print(statut)

        # 2. Recherche d'une place physique dans le parking
        placeAssignee = self.MonParking.rechercherPlace(voiture)

        if c.estSuperAbonne:
            message = self.TelEntree.teleporterVoitureSuperAbonne(voiture)
            return f"Bienvenue {c.nom}. {message}"

        elif placeAssignee is not None:
            # CAS 1 : Il y a de la place
            while True:
                temp = input("Est vous un abonné ? y/n\n").lower()
                if temp in ["y", "n"]:
                    break
                print("Erreur! Veillez sélectionner que 'y' ou 'n'")
            print("Vérification de votre statut client... Veillez patienter...")
            time.sleep(1)
            if not c.estAbonne:
                print("Retour système: Client non Abonné...")
                self.maBorne.proposerTypePaiement()
                self.maBorne.proposerAbonnements(c, self.MonParking)
                print(self.maBorne.deliverTicket(c))
                self.TelEntree.teleporterVoiture(voiture, placeAssignee)
                placeAssignee.definir_estLibre(False)
                return f"Bienvenue {c.nom}. Place assignée : {placeAssignee.obtenir_niveau()}{placeAssignee.numero}"

            # Téléportation standard
            print("Retour système: Client est un abonné")
            service = self.maBorne.proposerServices()
            print("Service est ", service)
            match service:
                case "1":
                    print(">> Ajout du service : Maintenance Technique")
                    c.demanderMaintenance()
                case "2":
                    print(">> Ajout du service : Entretien Véhicule")
                    c.demanderEntretien()
                case "3":
                    print(">> Ajout du service : Livraison (Voiturier)")
                    while True:
                        date_input = input("   Veuillez saisir la date de livraison (JJ/MM/AAAA) : ")
                        try:
                            # 1. On essaie de convertir la chaîne en objet Date
                            date_obj = datetime.strptime(date_input, "%d/%m/%Y")

                            # 2. (Optionnel) Vérifier que la date n'est pas passée
                            if date_obj.date() < datetime.now().date():
                                print("   Erreur : Vous ne pouvez pas choisir une date passée.")
                                continue

                            # Si tout est bon, on valide et on garde la chaîne
                            date_liv = date_input
                            break
                        except ValueError:
                            print("   Erreur : Format invalide. Utilisez le format JJ/MM/AAAA (ex: 25/12/2025).")
                    heure_liv = input("   Veuillez saisir l'heure ex 6 pour 6h ou 18 pour 18h : ")
                    adresse_liv = input("   Veuillez saisir l'adresse de livraison : ")
                    c.demanderLivraison(date_liv, heure_liv, adresse_liv)
                case "4":
                    print(">> Aucun service supplémentaire sélectionné.")
            print(self.maBorne.deliverTicket(c))
            self.TelEntree.teleporterVoiture(voiture, placeAssignee)
            placeAssignee.definir_estLibre(False)
            return f"Bienvenue {c.nom}. Place assignée : {placeAssignee.obtenir_niveau()}{placeAssignee.numero}"
        return "Aucune place disponible pour votre véhicule."