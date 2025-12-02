import unittest
from datetime import datetime, timedelta
from models.contrat import Contrat
from models.abonnement import Abonnement


class TestContrat(unittest.TestCase):
    """Tests pour la classe Contrat"""

    def test_creation_contrat(self):
        """Test: Creation d'un contrat"""
        date_debut = datetime.now()
        contrat = Contrat(date_debut, 30)

        self.assertEqual(contrat.date_debut, date_debut)
        self.assertEqual(contrat.duree_jours, 30)
        self.assertIsNotNone(contrat.date_fin)

    def test_contrat_valide(self):
        """Test: Un contrat recent est valide"""
        contrat = Contrat(datetime.now(), 30)
        self.assertTrue(contrat.estValide())

    def test_contrat_expire(self):
        """Test: Un contrat expire est invalide"""
        date_passee = datetime.now() - timedelta(days=60)
        contrat = Contrat(date_passee, 30)
        self.assertFalse(contrat.estValide())

    def test_jours_restants(self):
        """Test: Calcul des jours restants"""
        contrat = Contrat(datetime.now(), 30)
        jours = contrat.jours_restants()
        self.assertGreater(jours, 0)
        self.assertLessEqual(jours, 30)

    def test_jours_restants_contrat_expire(self):
        """Test: Jours restants pour un contrat expire"""
        date_passee = datetime.now() - timedelta(days=60)
        contrat = Contrat(date_passee, 30)
        self.assertEqual(contrat.jours_restants(), 0)


if __name__ == '__main__':
    unittest.main()