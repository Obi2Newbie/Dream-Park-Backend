import unittest
from datetime import date, timedelta
from models import Placement

class TestPlacementPeriode(unittest.TestCase):
    """Tests pour la gestion des périodes de placement."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.aujourdhui = date.today()
        # Simulation d'un placement qui commence aujourd'hui
        self.placement = Placement(self.aujourdhui)

    def test_initialisation(self):
        """Vérifie la création d’un placement avec date de début et fin par défaut."""
        self.assertEqual(self.placement.dateDebut, self.aujourdhui)
        self.assertIsNone(self.placement.dateFin)
        self.assertTrue(self.placement.estEnCours)

    def test_initialisation_complete(self):
        """Vérifie l'initialisation avec tous les paramètres fournis."""
        date_fin = self.aujourdhui + timedelta(days=1)
        placement_complet = Placement(self.aujourdhui, date_fin, False)
        
        self.assertEqual(placement_complet.dateFin, date_fin)
        self.assertFalse(placement_complet.estEnCours)

    def test_partir_place(self):
        """Teste la méthode partirPlace() (mise à jour du statut et de la date de fin)."""
        # Action : le véhicule quitte la place
        self.placement.partirPlace()
        
        # Vérifications
        self.assertFalse(self.placement.estEnCours)
        self.assertEqual(self.placement.dateFin, date.today())
