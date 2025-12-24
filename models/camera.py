class Camera:
    """
    Représente une caméra de reconnaissance du système DreamPark.

    Équipement de surveillance et d'identification installé aux accès
    du parking pour capturer automatiquement les caractéristiques
    physiques des véhicules (dimensions, immatriculation).

    Note:
        Dans cette implémentation, la caméra lit les données déjà
        présentes dans l'objet Voiture (simulation).
    """

    def capturerHauteur(self, v):
        """
        Mesure la hauteur d'un véhicule.

        Args:
            v (Voiture): Le véhicule à analyser.

        Returns:
            float: Hauteur du véhicule en mètres.
        """


    def capturerLongueur(self, v):
        """
        Mesure la longueur d'un véhicule.

        Args:
            v (Voiture): Le véhicule à analyser.

        Returns:
            float: Longueur du véhicule en mètres.
        """


    def capturerImmatr(self, v):
        """
        Lit et reconnaît la plaque d'immatriculation d'un véhicule.

        Args:
            v (Voiture): Le véhicule à identifier.

        Returns:
            str: Numéro d'immatriculation détecté.
        """
