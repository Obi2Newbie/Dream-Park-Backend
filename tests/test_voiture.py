"""
Module de test pour la classe Voiture.
"""

import unittest

class TestVoiture(unittest.TestCase):
    """Regroupe les cas de test pour la classe Voiture."""

    def test_initialisation(self):
        """Vérifie l’initialisation correcte des attributs d’une voiture."""
        pass

    def test_add_placement(self):
        """Teste l’association d’un placement à une voiture."""
        pass
    def test_obtenir_hauteur(self):
        """
        Vérifie que la méthode obtenirHauteur() renvoie la hauteur attendue.

        Comportement attendu :
            - Retourne la valeur définie initialement dans la voiture.
            - Aucune erreur d’accès à l’attribut privé ne doit se produire.
        """
        # TODO: Appeler obtenirHauteur() et vérifier la valeur renvoyée
        pass

    def test_definir_hauteur(self):
        """
        Vérifie que definirHauteur() met à jour la hauteur de la voiture.

        Comportement attendu :
            - La valeur modifiée est bien prise en compte par obtenirHauteur().
        """
        # TODO: Modifier la hauteur via definirHauteur() et valider la mise à jour
        pass

    def test_obtenir_longueur(self):
        """
        Vérifie que la méthode obtenirLongueur() renvoie la longueur correcte.

        Comportement attendu :
            - Retourne la longueur définie dans l’objet Voiture.
        """
        # TODO: Appeler obtenirLongueur() et vérifier la valeur
        pass

    def test_definir_longueur(self):
        """
        Vérifie que definirLongueur() met à jour la longueur du véhicule.

        Comportement attendu :
            - La longueur modifiée est bien enregistrée dans l’objet Voiture.
        """
        # TODO: Modifier la longueur et vérifier le résultat
        pass

    def test_obtenir_immatriculation(self):
        """
        Vérifie que obtenirImmatriculation() renvoie la plaque d’immatriculation actuelle.

        Comportement attendu :
            - Retourne la valeur initiale stockée dans l’objet Voiture.
        """
        # TODO: Appeler obtenirImmatriculation() et vérifier la valeur
        pass

    def test_definir_immatriculation(self):
        """
        Vérifie que definirImmatriculation() met à jour la plaque du véhicule.

        Comportement attendu :
            - La nouvelle immatriculation remplace correctement l’ancienne.
        """
        # TODO: Appeler definirImmatriculation() puis obtenirImmatriculation()
        pass