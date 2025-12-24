import unittest
from datetime import date
from models import Service

class TestService(unittest.TestCase):
    """Tests pour la classe Service"""

    def setUp(self):
        """Initialisation des données de test communes"""
        self.aujourdhui = date.today()
        self.date_prevue = date(2025, 12, 31)
        self.rapport_initial = "En attente de traitement"

    def test_creation_service(self):
        """Test: Creation d'un service avec tous les paramètres"""
        service = Service(self.aujourdhui, self.date_prevue, self.rapport_initial)

        self.assertEqual(service.dateDemande, self.aujourdhui)
        self.assertEqual(service.dateService, self.date_prevue)
        self.assertEqual(service.rapport, self.rapport_initial)

    def test_creation_service_sans_description(self):
        """Test: Creation d'un service avec un rapport vide ou None"""
        # Dans certains cas, le rapport peut être vide à l'initialisation
        service_vide = Service(self.aujourdhui, None, None)

        self.assertEqual(service_vide.dateDemande, self.aujourdhui)
        self.assertIsNone(service_vide.dateService)
        self.assertIsNone(service_vide.rapport)
