import unittest
from unittest.mock import MagicMock
from models import Camera

class TestCamera(unittest.TestCase):
    """Tests pour la classe Camera."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.camera = Camera()
        # Création d'un mock de l'objet Voiture
        self.mock_voiture = MagicMock()

    def test_initialisation(self):
        """Vérifie la création d’une caméra."""
        self.assertIsInstance(self.camera, Camera)

    def test_capturer_hauteur(self):
        """Teste la capture de la hauteur du véhicule."""
        # On définit une valeur de retour pour le mock
        self.mock_voiture.obtenirHauteur.return_value = 1.95

        hauteur = self.camera.capturerHauteur(self.mock_voiture)

        # Vérification de la valeur retournée
        self.assertEqual(hauteur, 1.95)
        # Vérification que la méthode de l'objet voiture a bien été appelée
        self.mock_voiture.obtenirHauteur.assert_called_once()

    def test_capturer_longueur(self):
        """Teste la capture de la longueur du véhicule."""
        self.mock_voiture.obtenirLongueur.return_value = 4.20

        longueur = self.camera.capturerLongueur(self.mock_voiture)

        self.assertEqual(longueur, 4.20)
        self.mock_voiture.obtenirLongueur.assert_called_once()

    def test_capturer_immatriculation(self):
        """Teste la lecture de la plaque d’immatriculation."""
        self.mock_voiture.obtenirImmatriculation.return_value = "AB-123-CD"

        immat = self.camera.capturerImmatr(self.mock_voiture)

        self.assertEqual(immat, "AB-123-CD")
        self.mock_voiture.obtenirImmatriculation.assert_called_once()
