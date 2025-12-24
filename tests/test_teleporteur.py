import unittest
from unittest.mock import MagicMock
from datetime import date
from models import Teleporteur

class TestTeleporteur(unittest.TestCase):
    """Tests pour la téléportation de véhicules."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.mock_parking = MagicMock()
        self.teleporteur = Teleporteur(self.mock_parking)
        self.mock_voiture = MagicMock()
        self.mock_place = MagicMock()

    def test_initialisation(self):
        """Vérifie la création du téléporteur et l'association au parking."""
        self.assertEqual(self.teleporteur.parking, self.mock_parking)

    def test_teleporter_voiture(self):
        """Teste la téléportation d’une voiture vers une place spécifique."""
        # Action
        placement = self.teleporteur.teleporterVoiture(self.mock_voiture, self.mock_place)
        
        # Vérifications
        self.assertEqual(placement.dateDebut, date.today())
        self.assertTrue(placement.estEnCours)
        
        # Vérifier que la place et la voiture ont reçu l'objet placement
        self.mock_place.addPlacementP.assert_called_once_with(placement)
        self.mock_voiture.addPlacementV.assert_called_once_with(placement)

    def test_teleporter_voiture_super_abonne_parking_libre(self):
        """Teste la téléportation prioritaire lorsqu'une place est disponible."""
        # Configurer le mock parking pour retourner une place
        self.mock_place.obtenir_niveau.return_value = "Niveau 1"
        self.mock_place.numero = 50
        self.mock_parking.rechercherPlace.return_value = self.mock_place
        
        # Action
        resultat = self.teleporteur.teleporterVoitureSuperAbonne(self.mock_voiture)
        
        # Vérifications
        self.assertIn("Voiture garée dans le parking Niveau 150", resultat)
        self.mock_place.definir_estLibre.assert_called_with(False)
        self.mock_voiture.addPlacementV.assert_called()

    def test_teleporter_voiture_super_abonne_parking_plein(self):
        """Teste le service Valet (Pack Garanti) quand le parking est complet."""
        # Le parking ne trouve aucune place
        self.mock_parking.rechercherPlace.return_value = None
        
        # Action
        resultat = self.teleporteur.teleporterVoitureSuperAbonne(self.mock_voiture)
        
        # Vérifications
        self.assertIn("Parking complet : Voiture prise en charge par le service Valet (Pack Garanti).", resultat)
        self.assertTrue(self.mock_voiture.estDansParking)
