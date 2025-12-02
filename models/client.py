from .voiture import Voiture
from .abonnement import Abonnement

class Client:
    """
    Représente un client du système DreamPark.

    Attributs :
        nom (str) : Nom du client.
        adresse (str) : Adresse principale du client.
        estAbonne (bool) : Indique si le client possède un abonnement actif.
        estSuperAbonne (bool) : Indique si le client dispose du pack garanti (super abonnement).
        nbFrequentation (int) : Nombre de visites ou de passages enregistrés dans le parking.
    """

    def __init__(self, nom, adresse, estAbonne, estSuperAbonne, nbFrequentation):
        """
        Initialise un nouveau client avec ses informations de base.

        Attributs:
            nom (str): Nom du client.
            adresse (str): Adresse principale du client.
            estAbonne (bool, optionnel): Statut d'abonnement (par défaut False).
            estSuperAbonne (bool, optionnel): Statut de pack garanti (par défaut False).
            nbFrequentation (int, optionnel): Nombre initial de fréquentations (par défaut 0).
        """
        self.nom = nom
        self.adresse = adresse
        self.estAbonne = estAbonne
        self.estSuperAbonne = estSuperAbonne
        self.nbFrequentation = nbFrequentation
        self.voiture = None
        self.mode_paiement = None
        self.services_demandes = []

    def sAbonner(self, ab):
        """
        Permet au client de souscrire à un abonnement spécifique.

        Attributs:
            ab: Type ou objet représentant l'abonnement choisi.

        Comportement attendu :
            - Vérifie si le client est déjà abonné.
            - Si non, applique les avantages liés à l'abonnement choisi.
            - Met à jour les attributs `estAbonne` et éventuellement `estSuperAbonne`.
        """
        pass

    def nouvelleVoiture(self, imma, hautV, longV):
        """
        Enregistre une nouvelle voiture appartenant au client.

        Attributs:
            imma (str): Immatriculation du véhicule.
            hautV (float): Hauteur du véhicule.
            longV (float): Longueur du véhicule.

        Comportement attendu :
            - Crée un objet Véhicule avec les informations fournies.
            - Associe le véhicule à ce client.
            - Vérifie la validité de l'immatriculation.
        """
        voiture = Voiture
        voiture.definirHauteur(hautV)
        voiture.definirLongueur(longV)
        voiture.definirImmatriculation(imma)


    def seDesabonner(self):
        """
        Met fin à l'abonnement actuel du client.

        Comportement attendu :
            - Supprime les privilèges d'abonné ou de super abonné.
            - Met à jour les attributs `estAbonne` et `estSuperAbonne` à False.
            - Peut déclencher une notification ou un message de confirmation.
        """
        pass

    def demanderMaintenance(self):
        """
        Permet au client de demander une opération de maintenance pour son véhicule.

        Comportement attendu :
            - Vérifie que le client possède au moins un véhicule enregistré.
            - Crée une demande de maintenance associée à ce véhicule.
            - Retourne un identifiant ou un objet de suivi de maintenance.
        """
        pass

    def demanderLivraison(self, dateLiv, heure, adresseLiv):
        """
        Permet de demander la livraison du véhicule à une adresse donnée,
        à une date et heure précises.

        Attributs:
            dateLiv (date): Date souhaitée pour la livraison.
            heure (int): Heure prévue de la livraison.
            adresseLiv (str): Adresse de destination du véhicule.

        Comportement attendu :
            - Vérifie si le client est abonné (ou applique des frais pour les non-abonnés).
            - Planifie la livraison dans le système.
            - Retourne un objet de confirmation ou une référence de livraison.
        """
        pass

    def demanderEntretien(self):
        """
        Permet au client de demander un service d'entretien.

        Comportement attendu :
            - Crée une demande d'entretien dans le système.
            - Associe cette demande au véhicule principal du client.
            - Retourne un reçu ou une confirmation d'entretien planifié.
        """
        pass

    def entreParking(self, a):
        """
        Décrit l'action d'entrée du client dans le parking via un accès.

        Attributs:
            a: Objet représentant l'accès ou la porte utilisée pour entrer.

        Comportement attendu :
            - Déclenche la capture des informations du véhicule (caméra, taille, plaque).
            - Met à jour le nombre de fréquentations du client (`nbFrequentation`).
            - Lance le processus d'attribution d'une place via le système de parking.
        """
        pass

    def definirModePaiement(self, mode_paiement):
        """
        Definit le mode de paiement du client.

        Args:
            mode_paiement (str): "CB" ou "Especes"
        """
        self.mode_paiement = mode_paiement

    def souscrireContrat(self, contrat):
        """
        Fait souscrire le client a un contrat d'abonnement.

        Args:
            contrat (Contrat): Le contrat a associer
        """
        self.contrat = contrat

    def ajouterService(self, service):
        """
        Ajoute un service demande par le client.

        Args:
            service (Service): Le service a ajouter
        """
        if not hasattr(self, 'services_demandes'):
            self.services_demandes = []
        self.services_demandes.append(service)