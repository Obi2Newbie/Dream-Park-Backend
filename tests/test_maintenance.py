import unittest
from unittest.mock import MagicMock
from datetime import date
from models import Maintenance

class TestMaintenance(unittest.TestCase):
    """Tests pour la classe Maintenance."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.date_test = date.today()
        self.maintenance = Maintenance(self.date_test)

    def test_initialisation(self):
        """Vérifie la création d’un objet Maintenance et l'état initial."""
        # Vérification de l'instance
        self.assertIsInstance(self.maintenance, Maintenance)
        
        # Vérification des valeurs initiales transmises au super (Service)
        # Note: On teste "Maintenance non effectué" tel que défini dans votre __init__
        self.assertEqual(self.maintenance.rapport, "Maintenance non effectué")

    def test_effectuer_maintenance(self):
        """Teste la méthode effectuerMaintenance() avec un mock de voiture."""
        # Création d'un mock pour l'objet Voiture
        mock_voiture = MagicMock()
        mock_voiture.obtenirImmatriculation.return_value = "XYZ-123-FR"

        # Action : Exécuter la maintenance
        resultat = self.maintenance.effectuerMaintenance(mock_voiture)

        # Vérifications
        attendu = "Maintenance effectuée sur XYZ-123-FR"
        self.assertEqual(resultat, attendu)
        self.assertEqual(self.maintenance.rapport, attendu)
        
        # Vérifie que la méthode de la voiture a bien été appelée
        mock_voiture.obtenirImmatriculation.assert_called_once()