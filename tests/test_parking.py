import unittest

class TestParking(unittest.TestCase):
    """Tests pour la classe Parking."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        pass

    def test_initialisation(self):
        """Vérifie l’initialisation d’un objet Parking et son unicité (Singleton)."""
        pass

    def test_rechercher_place(self):
        """Teste la recherche d’une place adaptée à un véhicule (dimensions et disponibilité)."""
        pass

    def test_rechercher_place_aucune_disponible(self):
        """Vérifie que None est retourné si aucune place ne correspond ou n'est libre."""
        pass

    def test_nb_places_libres_par_niveau(self):
        """Vérifie le calcul du nombre de places libres par niveau."""
        pass

    def test_add_abonnement(self):
        """Teste l’ajout d’un abonnement dans le parking."""
        pass