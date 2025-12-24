import unittest
from unittest.mock import MagicMock, patch
from models import Borne_ticket

class TestBorneTicket(unittest.TestCase):
    """Tests pour la borne de tickets et paiements."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.borne = Borne_ticket()

        # Mock du client et de sa voiture
        self.mock_client = MagicMock()
        self.mock_client.nom = "Alice"
        self.mock_voiture = MagicMock()
        self.mock_voiture.obtenirImmatriculation.return_value = "AA-123-BB"
        self.mock_client.maVoiture = self.mock_voiture

        # Mock du parking
        self.mock_parking = MagicMock()

    def test_deliver_ticket(self):
        """Teste la génération d’un ticket pour un client."""
        resultat = self.borne.deliverTicket(self.mock_client)
        self.assertEqual(resultat, "Alice-AA-123-BB")

    @patch('builtins.input', return_value="1")
    def test_proposer_services(self, mock_input):
        """Vérifie la sélection d'un service (Maintenance)."""
        resultat = self.borne.proposerServices()
        self.assertEqual(resultat, "1")
        self.assertEqual(mock_input.call_count, 1)

    @patch('builtins.input', return_value="2")
    def test_proposer_abonnements_super(self, mock_input):
        """Teste la souscription à l'abonnement Super Abonné."""
        self.borne.proposerAbonnements(self.mock_client, self.mock_parking)

        # Vérification des changements d'état sur le client
        self.assertTrue(self.mock_client.estAbonne)
        self.assertTrue(self.mock_client.estSuperAbonne)

        # Vérifie que les méthodes d'enregistrement ont été appelées
        self.mock_client.sAbonner.assert_called_once()
        self.mock_parking.addAbonnement.assert_called_once()

    @patch('builtins.input', return_value="y")
    @patch('time.sleep', return_value=None)  # Pour ne pas attendre 1s
    def test_recuperer_infos_carte_succes(self, mock_sleep, mock_input):
        """Teste la validation de carte pour un super abonné."""
        self.mock_client.estSuperAbonne = True

        resultat = self.borne.recupererInfosCarte(self.mock_client)
        self.assertEqual(resultat, "Carte validée pour Alice")

    @patch('builtins.input', return_value="n")
    @patch('time.sleep', return_value=None)
    def test_recuperer_infos_carte_echec(self, mock_sleep, mock_input):
        """Teste le retour si le client n'est pas reconnu comme super abonné."""
        self.mock_client.estSuperAbonne = False

        resultat = self.borne.recupererInfosCarte(self.mock_client)
        self.assertEqual(resultat, "Client non super abonné")

    @patch('builtins.input', side_effect=["3", "1"])  # Test d'une erreur puis succès
    def test_proposer_type_paiement(self, mock_input):
        """Vérifie la sélection du paiement par CB après un mauvais choix."""
        # On ne vérifie pas le print, mais on s'assure que la boucle se termine
        with patch('builtins.print') as mock_print:
            self.borne.proposerTypePaiement()
            # Vérifie que le message d'erreur a été affiché pour le choix "3"
            mock_print.assert_any_call("Erreur : Veuillez appuyer sur le bon bouton.")
            # Vérifie que le succès a été affiché pour le choix "1"
            mock_print.assert_any_call("Merci pour avoir sélectionné l'option CB")
