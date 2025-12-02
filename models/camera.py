from .voiture import Voiture

class Camera:
    """
    Représente une caméra du système DreamPark, utilisée pour capturer
    les informations d’un véhicule entrant ou sortant du parking.

    Les caméras sont généralement placées aux accès afin de mesurer
    les dimensions du véhicule et d’identifier son immatriculation.
    """
    def capturerHauteur(self, v):
        """
        Capture et renvoie la hauteur du véhicule.

        Args:
            v (Voiture): Objet représentant le véhicule à analyser.

        Returns:
            float: Valeur mesurée correspondant à la hauteur du véhicule (en mètres).

        Comportement attendu :
            - Mesure la hauteur du véhicule à l’aide des capteurs ou de la caméra.
            - Met à jour l’objet `Voiture` avec la hauteur capturée.
            - Peut enregistrer la donnée pour le contrôle de compatibilité avec les places disponibles.
        """
        return v.obtenirHauteur()

    def capturerLongueur(self, v):
        """
        Capture et renvoie la longueur du véhicule.

        Args:
            v (Voiture): Objet représentant le véhicule à analyser.

        Returns:
            float: Valeur mesurée correspondant à la longueur du véhicule (en mètres).

        Comportement attendu :
            - Mesure la longueur du véhicule grâce à la caméra ou à un capteur dédié.
            - Met à jour l’objet `Voiture` avec la longueur détectée.
            - Peut être utilisé pour déterminer si le véhicule peut entrer dans une place donnée.
        """
        return v.obtenirLongueur()

    def capturerImmatr(self, v):
        """
        Capture l’immatriculation du véhicule à partir de la caméra.

        Args:
            v (Voiture): Objet représentant le véhicule à identifier.

        Returns:
            string: Numéro d’immatriculation détecté.

        Comportement attendu :
            - Détecte et lit la plaque d’immatriculation du véhicule via reconnaissance optique.
            - Met à jour l’objet `Voiture` avec le numéro d’immatriculation.
            - Sert à vérifier la correspondance avec un client ou un abonnement enregistré.
        """
        return v.obtenirImmatriculation()
