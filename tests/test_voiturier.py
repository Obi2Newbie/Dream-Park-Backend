import unittest
from unittest.mock import MagicMock
from datetime import date
from models import Voiturier

class TestVoiturier(unittest.TestCase):
    """Tests pour la classe Voiturier."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.num_voiturier = 7
        self.voiturier = Voiturier(self.num_voiturier)
        
        # Mock de la voiture
        self.mock_voiture = MagicMock()
        self.mock_voiture.obtenirImmatriculation.return_value = "GP-555-RR"
        self.mock_voiture.estDansParking = True
        
        # Mock du propriétaire et des services
        self.mock_client = MagicMock()
        self.mock_voiture.proprietaire = self.mock_client
        
        # Mock d'un service de livraison
        self.mock_service = MagicMock()
        # On simule les attributs attendus par la méthode livrerVoiture
        self.mock_service.adresse = "10 Rue du Louvre"
        self.mock_service.dateDemande = date.today()
        
        self.mock_client.mesServices = [self.mock_service]

    def test_initialisation(self):
        """Vérifie la création d’un voiturier."""
        self.assertEqual(self.voiturier.numVoiturier, self.num_voiturier)

    def test_livrer_voiture_succes(self):
        """Teste la livraison réussie d’un véhicule présent dans le parking."""
        d = date.today()
        h = 14
        
        resultat = self.voiturier.livrerVoiture(self.mock_voiture, d, h)
        
        # Vérifications
        self.assertIn(f"voiturier {self.num_voiturier}", resultat)
        self.assertIn("GP-555-RR", resultat)
        
        # Vérifie que la voiture quitte sa place
        self.mock_voiture.partirPlace.assert_called_once()
        
        # Vérifie que le rapport du service a été mis à jour
        self.assertEqual(self.mock_service.dateService, date.today())
        self.assertIn(f"par le voiturier n°{self.num_voiturier}", self.mock_service.rapport)

    def test_livrer_voiture_erreur_absente(self):
        """Vérifie le message d'erreur si la voiture n'est pas dans le parking."""
        self.mock_voiture.estDansParking = False
        
        resultat = self.voiturier.livrerVoiture(self.mock_voiture, date.today(), 10)
        
        self.assertIn("Erreur", resultat)
        self.assertIn("n'est pas dans le parking", resultat)
        # S'assurer que partirPlace n'est pas appelé
        self.mock_voiture.partirPlace.assert_not_called()
