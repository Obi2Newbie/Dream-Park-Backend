import unittest
from models.service import Service


class TestService(unittest.TestCase):
    """Tests pour la classe Service"""

    def test_creation_service(self):
        """Test: Creation d'un service"""
        service = Service("Livraison", 15.0, "Livraison du vehicule")

        self.assertEqual(service.nom, "Livraison")
        self.assertEqual(service.prix, 15.0)
        self.assertEqual(service.description, "Livraison du vehicule")

    def test_creation_service_sans_description(self):
        """Test: Creation d'un service sans description"""
        service = Service("Entretien", 50.0)

        self.assertEqual(service.nom, "Entretien")
        self.assertEqual(service.prix, 50.0)
        self.assertEqual(service.description, "")


if __name__ == '__main__':
    unittest.main()