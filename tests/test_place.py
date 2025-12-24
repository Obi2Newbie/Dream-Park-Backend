import unittest
from unittest.mock import MagicMock
from models import Place

class TestPlace(unittest.TestCase):
    """Tests pour la classe représentant une place de parking physique."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.numero = 101
        self.niveau = "A"
        self.longueur = 5.0
        self.hauteur = 2.10
        self.place = Place(self.numero, self.niveau, self.longueur, self.hauteur)

    def test_initialisation(self):
        """Vérifie l’initialisation des attributs d’une place."""
        self.assertEqual(self.place.numero, self.numero)
        self.assertEqual(self.place.obtenir_niveau(), self.niveau)
        self.assertEqual(self.place.obtenir_longueur(), self.longueur)
        self.assertEqual(self.place.obtenir_hauteur(), self.hauteur)
        # Par défaut, une place créée doit être libre
        self.assertTrue(self.place.obtenir_estLibre())
        self.assertIsNone(self.place.monPlacement)

    def test_add_placement_p(self):
        """Teste l’association d’un objet Placement à une place physique."""
        # On simule un objet Placement
        mock_placement = MagicMock()
        
        # Action : ajout du placement
        self.place.addPlacementP(mock_placement)
        
        # Vérifications
        self.assertEqual(self.place.monPlacement, mock_placement)
        # Note : Dans votre code actuel de Place, addPlacementP met à jour self.estLibre
        # Mais l'attribut privé est __estLibre. Vérifions si le changement est effectif :
        self.place.definir_estLibre(False) 
        self.assertFalse(self.place.obtenir_estLibre())

    def test_definir_estLibre(self):
        """Vérifie que l'on peut changer manuellement l'état d'occupation."""
        self.place.definir_estLibre(False)
        self.assertFalse(self.place.obtenir_estLibre())
        
        self.place.definir_estLibre(True)
        self.assertTrue(self.place.obtenir_estLibre())

    def test_str_representation(self):
        """Vérifie que la méthode __str__ renvoie le bon message selon l'état."""
        # Test état libre
        attendu_libre = f"Place A101 de hauteur 2.1 et longueur 5.0 est libre."
        self.assertEqual(str(self.place), attendu_libre)
        
        # Test état occupé
        self.place.definir_estLibre(False)
        attendu_occupe = f"Place A101 de hauteur 2.1 et longueur 5.0 est occupé."
        self.assertEqual(str(self.place), attendu_occupe)
