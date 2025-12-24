import unittest
from unittest.mock import MagicMock
from datetime import date
from models.voiturier import Voiturier


class TestVoiturier(unittest.TestCase):
    """Tests unitaires pour la classe Voiturier."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.num_voiturier = 7
        self.voiturier = Voiturier(self.num_voiturier)

        # 1. Mock du Placement (pour la libération de place)
        self.mock_placement = MagicMock()

        # 2. Mock de la Voiture
        self.mock_voiture = MagicMock()
        self.mock_voiture.obtenirImmatriculation.return_value = "GP-555-RR"
        self.mock_voiture.estDansParking = True
        self.mock_voiture.monPlacement = self.mock_placement

        # 3. Mock du Propriétaire (Client)
        self.mock_client = MagicMock()
        self.mock_voiture.proprietaire = self.mock_client

        # 4. Mock du Service de Livraison
        self.mock_service = MagicMock()
        # On définit les attributs testés par 'livrerVoiture'
        self.mock_service.adresse = "10 Rue du Louvre"
        self.mock_service.dateDemande = date.today()
        self.mock_service.rapport = "Initial"

        self.mock_client.mesServices = [self.mock_service]

    def test_initialisation(self):
        """Vérifie l'assignation correcte de l'identifiant du voiturier."""
        self.assertEqual(self.voiturier.numVoiturier, self.num_voiturier)

    def test_livrer_voiture_succes(self):
        """Teste la livraison réussie d’un véhicule et la mise à jour des données."""
        d_test = date.today()
        h_test = "14"  # Format str comme spécifié dans la docstring

        resultat = self.voiturier.livrerVoiture(self.mock_voiture, d_test, h_test)

        # Vérification du message de retour
        self.assertIn(f"Le voiturier {self.num_voiturier}", resultat)
        self.assertIn("GP-555-RR", resultat)
        self.assertIn(f"le {d_test}", resultat)

        # Vérifie que la libération de la place a été déclenchée via le placement
        self.mock_placement.partirPlace.assert_called_once()

        # Vérifie la mise à jour du service de livraison associé au client
        self.assertEqual(self.mock_service.dateService, date.today())
        self.assertIn(f"par le voiturier n°{self.num_voiturier}", self.mock_service.rapport)

    def test_livrer_voiture_erreur_absente(self):
        """Vérifie le comportement si la voiture n'est pas détectée dans le parking."""
        self.mock_voiture.estDansParking = False

        resultat = self.voiturier.livrerVoiture(self.mock_voiture, date.today(), "10")

        # Vérification du message d'erreur
        self.assertIn("Erreur", resultat)
        self.assertIn("n'est pas dans le parking", resultat)

        # On s'assure qu'aucune procédure de sortie de place n'a été lancée
        self.mock_placement.partirPlace.assert_not_called()
