from .voiture import Voiture
from .voiturier import Voiturier
from .maintenance import Maintenance
from .livraison import Livraison
from .entretien import Entretien
import time
from datetime import datetime


class Acces:
    """
    Représente un point d'accès du parking DreamPark (entrée/sortie).

    Cette classe orchestre l'ensemble des opérations liées à l'entrée
    et à la sortie des véhicules : identification par caméra, vérification
    du statut client, attribution de place, gestion des services additionnels.

    Attributes:
        MonParking (Parking): Référence vers le parking associé.
        TelEntree (Teleporteur): Téléporteur utilisé pour l'entrée des véhicules.
        __TelSortie (Teleporteur): Téléporteur utilisé pour la sortie (privé).
        maBorne (Borne_ticket): Borne interactive pour les transactions.
        monPanneau (Panneau_affichage): Panneau d'affichage des informations.
        maCamera (Camera): Caméra pour l'identification des véhicules.
    """

    def __init__(self, camera, borne, panneau, tel_entree, tel_sortie, parking):
        """
        Initialise un point d'accès avec tous ses composants.

        Args:
            camera (Camera): Caméra pour capturer les informations véhicule.
            borne (Borne_ticket): Borne pour les interactions client.
            panneau (Panneau_affichage): Panneau d'affichage dynamique.
            tel_entree (Teleporteur): Téléporteur pour les entrées.
            tel_sortie (Teleporteur): Téléporteur pour les sorties.
            parking (Parking): Le parking associé à cet accès.
        """
        self.MonParking = parking
        self.TelEntree = tel_entree
        self.__TelSortie = tel_sortie
        self.maBorne = borne
        self.monPanneau = panneau
        self.maCamera = camera

    def actionnerCamera(self, c):
        """
        Active la caméra pour identifier le véhicule d'un client.

        Capture les dimensions et l'immatriculation du véhicule existant
        du client sans créer de nouvelle instance.

        Args:
            c (Client): Le client dont on veut identifier le véhicule.

        Returns:
            Voiture: Le véhicule existant du client, ou None si absent.

        Note:
            Retourne la voiture existante du client, ne crée pas de nouvelle instance.
        """
        if c.maVoiture:
            vHauteur = self.maCamera.capturerHauteur(c.maVoiture)
            vLongueur = self.maCamera.capturerLongueur(c.maVoiture)
            vImma = self.maCamera.capturerImmatr(c.maVoiture)
            return c.maVoiture
        return None

    def actionnerPanneau(self):
        """
        Active le panneau d'affichage pour informer les clients.

        Returns:
            str: Message indiquant le nombre de places disponibles.

        Note:
            Affiche des informations en temps réel sur l'état du parking.
        """
        if self.MonParking and self.monPanneau:
            return self.monPanneau.afficherNbPlacesDisponibles()

    def lancerProcedureEntree(self, c):
        """
        Orchestre la procédure complète d'entrée d'un client dans le parking.

        Cette méthode gère :
        - L'identification du véhicule via caméra
        - La vérification du statut client (super abonné, abonné, nouveau)
        - La recherche et l'attribution d'une place
        - La proposition d'abonnements aux nouveaux clients
        - La proposition de services aux clients abonnés
        - La téléportation du véhicule

        Args:
            c (Client): Le client souhaitant entrer dans le parking.

        Returns:
            str: Message confirmant l'entrée et la place assignée, ou signalant
                 que le parking est complet.

        Flow:
            1. Super Abonné → Téléportation prioritaire immédiate
            2. Nouveau Client → Tunnel de vente d'abonnement
            3. Abonné Standard → Menu services (maintenance, entretien, livraison)
        """
        # 1. Identification du véhicule via la caméra
        voiture = self.actionnerCamera(c)
        statut = self.maBorne.recupererInfosCarte(c)
        print(statut)

        # 2. Recherche d'une place physique dans le parking
        placeAssignee = self.MonParking.rechercherPlace(voiture)

        # 3. Traitement prioritaire pour les Super Abonnés
        if c.estSuperAbonne:
            message = self.TelEntree.teleporterVoitureSuperAbonne(voiture)
            return f"Bienvenue {c.nom}. {message}"

        elif placeAssignee is not None:
            # 4. Confirmation du statut d'abonné
            while True:
                temp = input("Est vous un abonné ? y/n\n").lower()
                if temp in ["y", "n"]:
                    break
                print("Erreur! Veillez sélectionner que 'y' ou 'n'")

            print("Vérification de votre statut client... Veillez patienter...")
            time.sleep(1)

            # 5. Tunnel de vente pour les non-abonnés
            if not c.estAbonne:
                print("Retour système: Client non Abonné...")
                self.maBorne.proposerTypePaiement()
                self.maBorne.proposerAbonnements(c, self.MonParking)
                print(self.maBorne.deliverTicket(c))
                self.TelEntree.teleporterVoiture(voiture, placeAssignee)
                placeAssignee.definir_estLibre(False)
                return f"Bienvenue {c.nom}. Place assignée : {placeAssignee.obtenir_niveau()}{placeAssignee.numero}"

            # 6. Menu services pour les abonnés
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
                            date_obj = datetime.strptime(date_input, "%d/%m/%Y")
                            if date_obj.date() < datetime.now().date():
                                print("   Erreur : Vous ne pouvez pas choisir une date passée.")
                                continue
                            date_liv = date_input
                            break
                        except ValueError:
                            print("   Erreur : Format invalide. Utilisez le format JJ/MM/AAAA (ex: 25/12/2025).")
                    heure_liv = input("   Veuillez saisir l'heure ex 6 pour 6h ou 18 pour 18h : ")
                    adresse_liv = input("   Veuillez saisir l'adresse de livraison : ")
                    c.demanderLivraison(date_liv, heure_liv, adresse_liv)
                case "4":
                    print(">> Aucun service supplémentaire sélectionné.")

            # 7. Téléportation et confirmation
            print(self.maBorne.deliverTicket(c))
            self.TelEntree.teleporterVoiture(voiture, placeAssignee)
            placeAssignee.definir_estLibre(False)
            return f"Bienvenue {c.nom}. Place assignée : {placeAssignee.obtenir_niveau()}{placeAssignee.numero}"

        return "Aucune place disponible pour votre véhicule."