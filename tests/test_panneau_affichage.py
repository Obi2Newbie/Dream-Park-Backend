import unittest
from unittest.mock import MagicMock
from models import Panneau_affichage

class TestPanneauAffichage(unittest.TestCase):
    """Tests pour le panneau d’affichage du parking."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.panneau = Panneau_affichage()
        # Création d'un mock pour l'objet Parking
        self.mock_parking = MagicMock()

    def test_initialisation(self):
        """Vérifie la création du panneau d’affichage."""
        self.assertIsInstance(self.panneau, Panneau_affichage)

    def test_afficher_nb_places_disponibles(self):
        """Teste l’affichage du nombre de places disponibles sur le panneau."""
        # Simulation : le parking a 12 places libres
        self.mock_parking.NbPlacesDisponibles.return_value = 12
        
        # Action : on demande au panneau d'afficher l'état du parking mocké
        resultat = self.panneau.afficherNbPlacesDisponibles(self.mock_parking)
        
        # Vérifications
        self.assertEqual(resultat, "Places libres: 12")
        # On vérifie que le panneau a bien interrogé le parking
        self.mock_parking.NbPlacesDisponibles.assert_called_once()

    def test_afficher_nb_places_complet(self):
        """Teste l’affichage lorsque le parking est complet (0 places)."""
        self.mock_parking.NbPlacesDisponibles.return_value = 0
        
        resultat = self.panneau.afficherNbPlacesDisponibles(self.mock_parking)
        
        self.assertEqual(resultat, "Places libres: 0")

if __name__ == '__main__':
    unittest.main()