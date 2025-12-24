import unittest
from unittest.mock import MagicMock, patch
from models import Acces

class TestAcces(unittest.TestCase):
    """Tests pour la gestion des accès au parking."""

    def setUp(self):
        """Configuration initiale des mocks pour chaque test."""
        self.mock_camera = MagicMock()
        self.mock_borne = MagicMock()
        self.mock_panneau = MagicMock()
        self.mock_tel_e = MagicMock()
        self.mock_tel_s = MagicMock()
        self.mock_parking = MagicMock()
        
        self.acces = Acces(
            self.mock_camera, 
            self.mock_borne, 
            self.mock_panneau, 
            self.mock_tel_e, 
            self.mock_tel_s, 
            self.mock_parking
        )

    def test_initialisation(self):
        """Vérifie la création d’un objet Acces et l'assignation des composants."""
        self.assertEqual(self.acces.maBorne, self.mock_borne)
        self.assertEqual(self.acces.maCamera, self.mock_camera)
        self.assertEqual(self.acces.MonParking, self.mock_parking)

    def test_actionner_camera(self):
        """Teste la capture d’informations via la caméra."""
        # Setup du client et de sa voiture
        mock_client = MagicMock()
        mock_client.maVoiture = MagicMock()
        
        # Configuration des retours de la caméra
        self.mock_camera.capturerHauteur.return_value = 2.0
        self.mock_camera.capturerLongueur.return_value = 4.5
        self.mock_camera.capturerImmatr.return_value = "AB-123-CD"
        
        voiture = self.acces.actionnerCamera(mock_client)
        
        self.assertIsNotNone(voiture)
        self.assertEqual(voiture.obtenirHauteur(), 2.0)
        self.assertEqual(voiture.obtenirImmatriculation(), "AB-123-CD")

    def test_actionner_panneau(self):
        """Vérifie l’affichage des informations sur le panneau."""
        self.mock_panneau.afficherNbPlacesDisponibles.return_value = "Places libres : 5"
        
        resultat = self.acces.actionnerPanneau()
        
        self.assertEqual(resultat, "Places libres : 5")
        self.mock_panneau.afficherNbPlacesDisponibles.assert_called_once()

    @patch('builtins.input')
    @patch('time.sleep') # On empêche le sleep de ralentir les tests
    def test_lancer_procedure_entree_super_abonne(self, mock_sleep, mock_input):
        """Teste la procédure d'entrée prioritaire pour un Super Abonné."""
        mock_client = MagicMock()
        mock_client.estSuperAbonne = True
        mock_client.nom = "John"
        
        # Mock de la voiture détectée
        self.mock_camera.capturerHauteur.return_value = 2.0
        
        self.mock_tel_e.teleporterVoitureSuperAbonne.return_value = "Téléportation Prioritaire OK"
        
        resultat = self.acces.lancerProcedureEntree(mock_client)
        
        self.assertIn("Bienvenue John", resultat)
        self.assertIn("Téléportation Prioritaire OK", resultat)
        self.mock_tel_e.teleporterVoitureSuperAbonne.assert_called_once()

    @patch('builtins.input')
    @patch('time.sleep')
    def test_lancer_procedure_entree_client_standard(self, mock_sleep, mock_input):
        """Teste l'entrée d'un abonné standard choisissant un service de maintenance."""
        # 1. Configuration du Client
        mock_client = MagicMock()
        mock_client.estSuperAbonne = False
        mock_client.estAbonne = True
        mock_client.nom = "Weber"
        
        # 2. Configuration du Parking et de la Place
        mock_place = MagicMock()
        mock_place.obtenir_niveau.return_value = "A"
        mock_place.numero = 1
        self.mock_parking.rechercherPlace.return_value = mock_place
        
        # 3. Simulation des entrées utilisateur (input)
        # 1er input: "y" (est abonné)
        # 2e input: "1" (choix service Maintenance via la borne si appelé, 
        #           mais ici votre code appelle self.maBorne.proposerServices())
        mock_input.side_effect = ["y"] 
        self.mock_borne.proposerServices.return_value = "1" # Maintenance
        
        resultat = self.acces.lancerProcedureEntree(mock_client)
        
        # 4. Vérifications
        self.assertIn("Place assignée : A1", resultat)
        mock_client.demanderMaintenance.assert_called_once()
        mock_place.definir_estLibre.assert_called_with(False)
