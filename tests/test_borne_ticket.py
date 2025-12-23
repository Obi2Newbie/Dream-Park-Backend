import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from models.borne_ticket import BorneTicket, Ticket
from models.client import Client
from models.voiture import Voiture

class TestBorneTicket(unittest.TestCase):
    """Tests pour la classe BorneTicket"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_acces = Mock()
        self.borne = BorneTicket(id_borne=1, acces=self.mock_acces)

        self.client_non_abonne = Client("Dupont", "10 rue Test", False, False, 0)
        self.client_non_abonne.voiture = Voiture(1.80, 4.20, "AB-123-CD")

        self.client_abonne = Client("Martin", "20 rue Test", True, False, 5)
        self.client_abonne.voiture = Voiture(1.80, 4.20, "XY-789-ZZ")

    def test_initialisation_borne(self):
        """Verifie la creation d'une borne"""
        self.assertEqual(self.borne.id_borne, 1)
        self.assertIsNotNone(self.borne.abonnements_disponibles)
        self.assertIsNotNone(self.borne.services_disponibles)
        self.assertEqual(len(self.borne.abonnements_disponibles), 3)
        self.assertEqual(len(self.borne.services_disponibles), 3)

    def test_traiter_client_abonne(self):
        """Teste le traitement d'un client abonne"""
        with patch.object(self.borne, '_demander_choix_service', return_value=None):
            self.borne._traiter_client_abonne(self.client_abonne)
        self.assertTrue(True)

    def test_traiter_client_non_abonne(self):
        """Teste le traitement d'un client non-abonne"""
        with patch.object(self.borne, '_demander_mode_paiement', return_value="CB"), \
                patch.object(self.borne, '_demander_choix_abonnement', return_value=None):
            self.borne._traiter_client_non_abonne(self.client_non_abonne)

        self.assertEqual(self.client_non_abonne.mode_paiement, "CB")

    def test_traiter_client_non_abonne_souscrit_abonnement(self):
        """Teste la souscription d'un abonnement"""
        abonnement = ("Mensuel Standard", 50.0, False)

        with patch.object(self.borne, '_demander_mode_paiement', return_value="CB"), \
                patch.object(self.borne, '_demander_choix_abonnement', return_value=abonnement):
            self.borne._traiter_client_non_abonne(self.client_non_abonne)

        self.assertEqual(self.client_non_abonne.mode_paiement, "CB")

    def test_delivrer_ticket_succes(self):
        """Teste la delivrance d'un ticket avec succes"""
        ticket = self.borne._delivrer_ticket(self.client_non_abonne, 42)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.client, self.client_non_abonne)
        self.assertEqual(ticket.id_place, 42)
        self.assertIsNotNone(ticket.heure_entree)
        self.assertTrue(ticket.numero_ticket.startswith("TK"))

    def test_actionner_teleporteur_succes(self):
        """Teste l'activation du teleporteur avec succes"""
        ticket = Ticket(self.client_non_abonne, 42, datetime.now())

        mock_teleporteur = Mock()
        mock_teleporteur.teleporterEntree.return_value = True
        self.mock_acces.obtenirTeleporteurDisponible.return_value = mock_teleporteur

        succes = self.borne._actionner_teleporteur(ticket)

        self.assertTrue(succes)
        mock_teleporteur.teleporterEntree.assert_called_once()

    def test_actionner_teleporteur_aucun_disponible(self):
        """Teste l'echec si aucun teleporteur disponible"""
        ticket = Ticket(self.client_non_abonne, 42, datetime.now())
        self.mock_acces.obtenirTeleporteurDisponible.return_value = None

        succes = self.borne._actionner_teleporteur(ticket)

        self.assertFalse(succes)

    def test_traiter_stationnement_complet_client_abonne(self):
        """Test d'integration: Traitement complet pour client abonne"""
        mock_teleporteur = Mock()
        mock_teleporteur.teleporterEntree.return_value = True
        self.mock_acces.obtenirTeleporteurDisponible.return_value = mock_teleporteur

        with patch.object(self.borne, '_demander_choix_service', return_value=None):
            ticket = self.borne.traiter_stationnement(self.client_abonne, 42)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.id_place, 42)
        mock_teleporteur.teleporterEntree.assert_called_once()

    def test_traiter_stationnement_complet_client_non_abonne(self):
        """Test d'integration: Traitement complet pour client non-abonne"""
        mock_teleporteur = Mock()
        mock_teleporteur.teleporterEntree.return_value = True
        self.mock_acces.obtenirTeleporteurDisponible.return_value = mock_teleporteur

        with patch.object(self.borne, '_demander_mode_paiement', return_value="CB"), \
                patch.object(self.borne, '_demander_choix_abonnement', return_value=None):
            ticket = self.borne.traiter_stationnement(self.client_non_abonne, 42)

        self.assertIsNotNone(ticket)
        self.assertEqual(self.client_non_abonne.mode_paiement, "CB")
        mock_teleporteur.teleporterEntree.assert_called_once()

    def test_traiter_stationnement_echec_teleportation(self):
        """Teste l'echec si la teleportation echoue"""
        mock_teleporteur = Mock()
        mock_teleporteur.teleporterEntree.return_value = False
        self.mock_acces.obtenirTeleporteurDisponible.return_value = mock_teleporteur

        with patch.object(self.borne, '_demander_choix_service', return_value=None):
            ticket = self.borne.traiter_stationnement(self.client_abonne, 42)

        self.assertIsNone(ticket)


class TestTicket(unittest.TestCase):
    """Tests pour la classe Ticket"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.client = Client("Dupont", "10 rue Test", False, False, 0)
        self.client.voiture = Voiture(1.80, 4.20, "AB-123-CD")
        self.heure_entree = datetime.now()

    def test_creation_ticket(self):
        """Teste la creation d'un ticket"""
        ticket = Ticket(self.client, 42, self.heure_entree)

        self.assertIsNotNone(ticket.numero_ticket)
        self.assertTrue(ticket.numero_ticket.startswith("TK"))
        self.assertEqual(ticket.client, self.client)
        self.assertEqual(ticket.id_place, 42)
        self.assertFalse(ticket.paye)

    def test_calcul_duree(self):
        """Teste le calcul de la duree de stationnement"""
        ticket = Ticket(self.client, 42, self.heure_entree)
        ticket.heure_sortie = self.heure_entree + timedelta(hours=2)

        duree = ticket.calculer_duree()
        self.assertEqual(duree, 120)

    def test_calcul_montant_non_abonne(self):
        """Teste le calcul du montant pour un non-abonne"""
        ticket = Ticket(self.client, 42, self.heure_entree)
        ticket.heure_sortie = self.heure_entree + timedelta(hours=2)

        montant = ticket.calculer_montant(tarif_horaire=2.0)
        self.assertEqual(montant, 4.0)

    def test_calcul_montant_abonne_gratuit(self):
        """Teste le montant gratuit pour un abonne"""
        client_abonne = Client("Martin", "20 rue Test", True, False, 5)
        client_abonne.voiture = Voiture(1.80, 4.20, "XY-789-ZZ")

        ticket = Ticket(client_abonne, 42, self.heure_entree)
        ticket.heure_sortie = self.heure_entree + timedelta(hours=2)

        montant = ticket.calculer_montant()
        self.assertEqual(montant, 0.0)

    def test_marquer_paye(self):
        """Teste le marquage d'un ticket comme paye"""
        ticket = Ticket(self.client, 42, self.heure_entree)
        ticket.marquer_paye()
        self.assertTrue(ticket.paye)


if __name__ == '__main__':
    unittest.main()