from .voiture import Voiture
from .contrat import Contrat
from .maintenance import Maintenance
from .livraison import Livraison
from .entretien import Entretien
from datetime import date


class Client:
    """
    Représente un utilisateur du système DreamPark.

    Un client peut posséder un ou plusieurs véhicules, souscrire à des
    abonnements, demander des services additionnels et accéder au parking
    selon son statut (visiteur, abonné, super abonné).

    Attributes:
        nom (str): Nom complet du client.
        adresse (str): Adresse postale principale.
        estAbonne (bool): True si le client possède un abonnement actif.
        estSuperAbonne (bool): True si le client dispose du pack garanti.
        nbFrequentation (int): Nombre de visites effectuées dans le parking.
        mesServices (list): Liste des services demandés (Maintenance, Entretien, Livraison).
        maVoiture (Voiture): Véhicule principal du client.
        monAbonnement (Abonnement): Abonnement actif du client.
        monContrat (Contrat): Contrat d'abonnement en cours.
    """

    def __init__(self, nom, adresse, estAbonne=False, estSuperAbonne=False, nbFrequentation=0):
        """
        Initialise un nouveau client avec son profil de base.

        Args:
            nom (str): Nom du client.
            adresse (str): Adresse principale.
            estAbonne (bool, optional): Statut d'abonnement. Defaults to False.
            estSuperAbonne (bool, optional): Statut pack garanti. Defaults to False.
            nbFrequentation (int, optional): Nombre de visites. Defaults to 0.
        """
        self.nom = nom
        self.adresse = adresse
        self.estAbonne = estAbonne
        self.estSuperAbonne = estSuperAbonne
        self.nbFrequentation = nbFrequentation
        self.mesServices = []
        self.maVoiture = None
        self.monAbonnement = None
        self.monContrat = None

    def sAbonner(self, ab):
        """
        Souscrit à un abonnement et crée le contrat associé.

        Crée automatiquement un contrat actif et met à jour le statut
        du client selon le type d'abonnement (standard ou pack garanti).

        Args:
            ab (Abonnement): L'abonnement à souscrire.

        Returns:
            str: Message de confirmation de souscription.

        Side Effects:
            - Crée un nouveau Contrat
            - Lie le contrat à l'abonnement
            - Met à jour estAbonne et potentiellement estSuperAbonne
        """
        nouvContrat = Contrat(date.today(), None, True)
        nouvContrat.monAbonnement = ab
        ab.addContrat(nouvContrat)

        self.monContrat = nouvContrat
        self.monAbonnement = ab
        self.estAbonne = True

        if ab.estPackGar:
            self.estSuperAbonne = True

        return "Abonnement validé, merci de nous faire confiance!"

    def nouvelleVoiture(self, imma, hautV, longV):
        """
        Enregistre un nouveau véhicule pour ce client.

        Args:
            imma (str): Numéro d'immatriculation.
            hautV (float): Hauteur du véhicule en mètres.
            longV (float): Longueur du véhicule en mètres.

        Note:
            Remplace le véhicule précédent s'il existait.
        """
        self.maVoiture = Voiture(hautV, longV, imma)

    def seDesabonner(self):
        """
        Résilie l'abonnement actuel du client.

        Rompt le contrat en cours et réinitialise tous les privilèges
        d'abonnement (standard et pack garanti).

        Side Effects:
            - Rompt le contrat actif
            - Réinitialise estAbonne et estSuperAbonne à False
            - Supprime la référence à l'abonnement
        """
        if self.monContrat:
            self.monContrat.rompreContract()
        self.estAbonne = False
        self.estSuperAbonne = False
        self.monAbonnement = None

    def demanderMaintenance(self):
        """
        Demande une opération de maintenance technique pour le véhicule.

        Service réservé aux clients abonnés (standard ou pack garanti).

        Returns:
            Maintenance: Objet représentant la demande de maintenance,
                        ou str avec message d'erreur si non abonné.
        """
        if self.estAbonne:
            service = Maintenance(date.today())
            self.mesServices.append(service)
            return service
        return "Service réservé aux abonnés"

    def demanderLivraison(self, dateLiv, heure, adresseLiv):
        """
        Demande la livraison du véhicule à une adresse et date précises.

        Un voiturier récupérera le véhicule dans le parking et le livrera
        à l'adresse indiquée à l'heure prévue.

        Args:
            dateLiv (str): Date de livraison au format "JJ/MM/AAAA".
            heure (str): Heure de livraison (ex: "14" pour 14h).
            adresseLiv (str): Adresse de destination complète.

        Returns:
            Livraison: Objet représentant la demande de livraison.
        """
        livraison = Livraison(dateLiv, heure, adresseLiv)
        self.mesServices.append(livraison)
        return livraison

    def demanderEntretien(self):
        """
        Demande un service d'entretien pour le véhicule.

        Service réservé aux clients abonnés (nettoyage, révision, etc.).

        Returns:
            Entretien: Objet représentant la demande d'entretien,
                      ou str avec message d'erreur si non abonné.
        """
        if self.estAbonne:
            service = Entretien(date.today())
            self.mesServices.append(service)
            return service
        return "Seule les abonnés peuvent rajouter ce service"

    def entreParking(self, a):
        """
        Déclenche l'entrée du client dans le parking via un accès.

        Lance la procédure complète d'identification, de recherche de place
        et de téléportation, puis incrémente le compteur de fréquentation.

        Args:
            a (Acces): Le point d'accès utilisé pour entrer.
        """
        a.lancerProcedureEntree(self)
        self.nbFrequentation += 1