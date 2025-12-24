import unittest
from unittest.mock import MagicMock
from models import Parking

class TestParking(unittest.TestCase):
    """Tests pour la classe Parking."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        # Initialisation du parking (Singleton)
        self.parking = Parking(nbPlacesParNiveau=10, nbPlacesLibres=20, prix=10.5, nBNiveau=2)
        # On réinitialise les listes pour chaque test à cause du Singleton
        self.parking.mesPlaces = []
        self.parking.mesAbonnements = []

    def test_initialisation(self):
        """Vérifie l’initialisation d’un objet Parking et son unicité (Singleton)."""
        self.assertEqual(self.parking.nBNiveau, 2)
        
        # Test du Singleton : une nouvelle instanciation doit retourner le même objet
        autre_parking = Parking(5, 5, 5, 5)
        self.assertIs(self.parking, autre_parking)
        # Les valeurs ne doivent pas avoir changé car 'initialized' est True
        self.assertEqual(autre_parking.nBNiveau, 2)

    def test_rechercher_place(self):
        """Teste la recherche d’une place adaptée à un véhicule (dimensions et disponibilité)."""
        # 1. Création de places de tailles différentes
        place_petite = MagicMock()
        place_petite.obtenir_estLibre.return_value = True
        place_petite.obtenir_hauteur.return_value = 1.8
        place_petite.obtenir_longueur.return_value = 3.0

        place_grande = MagicMock()
        place_grande.obtenir_estLibre.return_value = True
        place_grande.obtenir_hauteur.return_value = 2.5
        place_grande.obtenir_longueur.return_value = 5.0

        self.parking.mesPlaces = [place_petite, place_grande]

        # 2. Mock d'un véhicule (SUV) qui ne rentre pas dans la petite place
        mock_voiture = MagicMock()
        mock_voiture.obtenirHauteur.return_value = 2.0
        mock_voiture.obtenirLongueur.return_value = 4.5

        # 3. Action
        resultat = self.parking.rechercherPlace(mock_voiture)

        # 4. Vérification : il doit avoir trouvé la grande place
        self.assertEqual(resultat, place_grande)

    def test_rechercher_place_aucune_disponible(self):
        """Vérifie que None est retourné si aucune place ne correspond ou n'est libre."""
        place_occupee = MagicMock()
        place_occupee.obtenir_estLibre.return_value = False
        place_occupee.obtenir_hauteur.return_value = 3.0
        place_occupee.obtenir_longueur.return_value = 6.0
        
        self.parking.mesPlaces = [place_occupee]
        
        mock_voiture = MagicMock()
        mock_voiture.obtenirHauteur.return_value = 1.5
        
        resultat = self.parking.rechercherPlace(mock_voiture)
        self.assertIsNone(resultat)

    def test_nb_places_libres_par_niveau(self):
        """Vérifie le calcul du nombre de places libres par niveau."""
        p1 = MagicMock()
        p1.obtenir_niveau.return_value = "A"
        p1.obtenir_estLibre.return_value = True

        p2 = MagicMock()
        p2.obtenir_niveau.return_value = "A"
        p2.obtenir_estLibre.return_value = False # Occupée

        p3 = MagicMock()
        p3.obtenir_niveau.return_value = "B"
        p3.obtenir_estLibre.return_value = True

        self.parking.mesPlaces = [p1, p2, p3]

        # Vérification pour le niveau A
        self.assertEqual(self.parking.nbPlacesLibresParNiveau("A"), 1)
        # Vérification pour le niveau B
        self.assertEqual(self.parking.nbPlacesLibresParNiveau("B"), 1)

    def test_add_abonnement(self):
        """Teste l’ajout d’un abonnement dans le parking."""
        mock_abo = MagicMock()
        self.parking.addAbonnement(mock_abo)
        
        self.assertIn(mock_abo, self.parking.mesAbonnements)
        self.assertEqual(len(self.parking.mesAbonnements), 1)