import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from models import Client

class TestClient(unittest.TestCase):
    """Classe regroupant les cas de test pour la classe Client."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.client = Client("Kevin", "123 Rue de Toulouse")

    def test_initialisation(self):
        """Vérifie l’initialisation d’un client avec les attributs de base."""
        self.assertEqual(self.client.nom, "Kevin")
        self.assertEqual(self.client.adresse, "123 Rue de Toulouse")
        self.assertFalse(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.nbFrequentation, 0)
        self.assertEqual(len(self.client.mesServices), 0)

    def test_sabonner(self):
        """Teste la souscription d’un client à un abonnement standard et super."""
        mock_abo = MagicMock()
        mock_abo.estPackGar = False

        # Test Abonnement Standard
        resultat = self.client.sAbonner(mock_abo)
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.monAbonnement, mock_abo)
        self.assertEqual(resultat, "Abonnement validé, merci de nous faire confiance!")

        # Test Passage en Super Abonné
        mock_super_abo = MagicMock()
        mock_super_abo.estPackGar = True
        self.client.sAbonner(mock_super_abo)
        self.assertTrue(self.client.estSuperAbonne)

    def test_nouvelle_voiture(self):
        """Vérifie la création et l’association d’une voiture à un client."""
        # On vérifie que maVoiture est None au départ
        self.assertIsNone(self.client.maVoiture)

        self.client.nouvelleVoiture("AB-123-CD", 1.90, 4.50)

        self.assertIsNotNone(self.client.maVoiture)
        self.assertEqual(self.client.maVoiture.obtenirImmatriculation(), "AB-123-CD")
        self.assertEqual(self.client.maVoiture.obtenirHauteur(), 1.90)

    def test_se_desabonner(self):
        """Teste la désactivation de l’abonnement d’un client."""
        # Préparation : on abonne le client
        mock_abo = MagicMock()
        self.client.sAbonner(mock_abo)

        # Action : désabonnement
        self.client.seDesabonner()

        self.assertFalse(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertIsNone(self.client.monAbonnement)

    def test_demander_service(self):
        """Teste la demande de services (Maintenance, Entretien, Livraison)."""
        # Un non-abonné ne peut pas demander de maintenance
        res_fail = self.client.demanderMaintenance()
        self.assertEqual(res_fail, "Service réservé aux abonnés")

        # Devenir abonné pour tester les succès
        self.client.estAbonne = True

        # Test Maintenance
        maintenance = self.client.demanderMaintenance()
        self.assertIn(maintenance, self.client.mesServices)

        # Test Entretien
        self.client.demanderEntretien()
        self.assertEqual(len(self.client.mesServices), 2)

        # Test Livraison (Accessible à tous selon votre code, mais enregistre les infos)
        livraison = self.client.demanderLivraison(date(2025, 12, 25), 14, "Gare de Toulouse")
        self.assertEqual(len(self.client.mesServices), 3)
        self.assertEqual(livraison.adresse, "Gare de Toulouse")

    def test_entrer_parking(self):
        """Vérifie l’entrée d’un client dans le parking via un accès."""
        mock_acces = MagicMock()
        initial_frequentation = self.client.nbFrequentation

        self.client.entreParking(mock_acces)

        # Vérifie que la procédure d'entrée de l'accès a été lancée
        mock_acces.lancerProcedureEntree.assert_called_once_with(self.client)
        # Vérifie que le compteur de fréquentation a augmenté
        self.assertEqual(self.client.nbFrequentation, initial_frequentation + 1)
