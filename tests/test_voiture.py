import unittest
from unittest.mock import MagicMock
from models import Voiture

class TestVoiture(unittest.TestCase):
    """Regroupe les cas de test pour la classe Voiture."""

    def setUp(self):
        """Initialisation d'une instance de voiture pour les tests."""
        self.hauteur_init = 1.90
        self.longueur_init = 4.50
        self.immat_init = "AB-123-CD"
        self.voiture = Voiture(self.hauteur_init, self.longueur_init, self.immat_init)

    def test_initialisation(self):
        """Vérifie l’initialisation correcte des attributs d’une voiture."""
        self.assertEqual(self.voiture.obtenirHauteur(), self.hauteur_init)
        self.assertEqual(self.voiture.obtenirLongueur(), self.longueur_init)
        self.assertEqual(self.voiture.obtenirImmatriculation(), self.immat_init)
        self.assertFalse(self.voiture.estDansParking)
        self.assertIsNone(self.voiture.monPlacement)

    def test_add_placement(self):
        """Teste l’association d’un placement à une voiture."""
        mock_placement = MagicMock()
        
        self.voiture.addPlacementV(mock_placement)
        
        self.assertEqual(self.voiture.monPlacement, mock_placement)
        self.assertTrue(self.voiture.estDansParking)

    def test_obtenir_hauteur(self):
        """Vérifie que la méthode obtenirHauteur() renvoie la hauteur attendue."""
        self.assertEqual(self.voiture.obtenirHauteur(), 1.90)

    def test_definir_hauteur(self):
        """Vérifie que definirHauteur() met à jour la hauteur de la voiture."""
        nouvelle_hauteur = 2.10
        self.voiture.definirHauteur(nouvelle_hauteur)
        self.assertEqual(self.voiture.obtenirHauteur(), nouvelle_hauteur)

    def test_obtenir_longueur(self):
        """Vérifie que la méthode obtenirLongueur() renvoie la longueur correcte."""
        self.assertEqual(self.voiture.obtenirLongueur(), 4.50)

    def test_definir_longueur(self):
        """Vérifie que definirLongueur() met à jour la longueur du véhicule."""
        nouvelle_longueur = 5.20
        self.voiture.definirLongueur(nouvelle_longueur)
        self.assertEqual(self.voiture.obtenirLongueur(), nouvelle_longueur)

    def test_obtenir_immatriculation(self):
        """Vérifie que obtenirImmatriculation() renvoie la plaque d’immatriculation actuelle."""
        self.assertEqual(self.voiture.obtenirImmatriculation(), "AB-123-CD")

    def test_definir_immatriculation(self):
        """Vérifie que definirImmatriculation() met à jour la plaque du véhicule."""
        nouvelle_immat = "XX-999-ZZ"
        self.voiture.definirImmatriculation(nouvelle_immat)
        self.assertEqual(self.voiture.obtenirImmatriculation(), nouvelle_immat)
