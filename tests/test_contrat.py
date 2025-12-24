import unittest
from datetime import date, timedelta
from models import Contrat

class TestContrat(unittest.TestCase):
    """Tests unitaires pour la gestion des contrats."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.date_debut = date.today()
        # Date de fin prévue dans un an
        self.date_fin = self.date_debut + timedelta(days=365)
        self.contrat = Contrat(self.date_debut, self.date_fin, True)

    def test_initialisation(self):
        """Vérifie la création d’un contrat avec ses attributs."""
        self.assertEqual(self.contrat.dateDebut, self.date_debut)
        self.assertEqual(self.contrat.dateFin, self.date_fin)
        self.assertTrue(self.contrat.estEnCours)
        self.assertIsNone(self.contrat.monAbonnement)

    def test_rompre_contrat(self):
        """Teste la résiliation d’un contrat."""
        # Action : Rompre le contrat
        self.contrat.rompreContract()

        # Vérifications
        self.assertFalse(self.contrat.estEnCours)
        # Selon votre code, rompreContract met la date de DEBUT à aujourd'hui
        self.assertEqual(self.contrat.dateDebut, date.today())

    def test_assignation_abonnement(self):
        """Vérifie que l'on peut associer un objet abonnement au contrat."""

        # Simulation d'un objet abonnement (Mock simple)
        class MockAbonnement: pass

        mon_abo = MockAbonnement()

        self.contrat.monAbonnement = mon_abo
        self.assertEqual(self.contrat.monAbonnement, mon_abo)
