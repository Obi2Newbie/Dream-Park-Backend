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
        """Vérifie la création d'un objet Acces et l'assignation des composants."""
        self.assertEqual(self.acces.maBorne, self.mock_borne)
        self.assertEqual(self.acces.maCamera, self.mock_camera)
        self.assertEqual(self.acces.MonParking, self.mock_parking)

    def test_actionner_camera(self):
        """
        Teste la capture d'informations via la caméra.

        Note: actionnerCamera() retourne maintenant la voiture EXISTANTE du client,
        pas une nouvelle instance. On doit donc configurer les méthodes de la voiture mockée.
        """
        # Setup du client et de sa voiture
        mock_client = MagicMock()
        mock_voiture = MagicMock()

        # Configuration de la voiture mockée avec les valeurs attendues
        mock_voiture.obtenirHauteur.return_value = 2.0
        mock_voiture.obtenirLongueur.return_value = 4.5
        mock_voiture.obtenirImmatriculation.return_value = "AB-123-CD"

        mock_client.maVoiture = mock_voiture

        # Configuration des retours de la caméra (pour la capture)
        self.mock_camera.capturerHauteur.return_value = 2.0
        self.mock_camera.capturerLongueur.return_value = 4.5
        self.mock_camera.capturerImmatr.return_value = "AB-123-CD"

        # Appel de la méthode
        voiture = self.acces.actionnerCamera(mock_client)

        # Vérifications
        self.assertIsNotNone(voiture)
        self.assertEqual(voiture, mock_voiture)  # C'est la même voiture qui est retournée
        self.assertEqual(voiture.obtenirHauteur(), 2.0)
        self.assertEqual(voiture.obtenirLongueur(), 4.5)
        self.assertEqual(voiture.obtenirImmatriculation(), "AB-123-CD")

        # Vérifier que la caméra a bien été utilisée
        self.mock_camera.capturerHauteur.assert_called_once_with(mock_voiture)
        self.mock_camera.capturerLongueur.assert_called_once_with(mock_voiture)
        self.mock_camera.capturerImmatr.assert_called_once_with(mock_voiture)

    def test_actionner_camera_sans_voiture(self):
        """Teste actionnerCamera() quand le client n'a pas de voiture."""
        mock_client = MagicMock()
        mock_client.maVoiture = None

        voiture = self.acces.actionnerCamera(mock_client)

        self.assertIsNone(voiture)
        # La caméra ne doit pas être appelée
        self.mock_camera.capturerHauteur.assert_not_called()

    def test_actionner_panneau(self):
        """Vérifie l'affichage des informations sur le panneau."""
        self.mock_panneau.afficherNbPlacesDisponibles.return_value = "Places libres : 5"

        resultat = self.acces.actionnerPanneau()

        self.assertEqual(resultat, "Places libres : 5")
        self.mock_panneau.afficherNbPlacesDisponibles.assert_called_once()

    def test_actionner_panneau_sans_parking(self):
        """Teste actionnerPanneau() quand le parking n'est pas configuré."""
        self.acces.MonParking = None

        resultat = self.acces.actionnerPanneau()

        self.assertIsNone(resultat)

    @patch('builtins.input')
    @patch('time.sleep')  # On empêche le sleep de ralentir les tests
    def test_lancer_procedure_entree_super_abonne(self, mock_sleep, mock_input):
        """Teste la procédure d'entrée prioritaire pour un Super Abonné."""
        # 1. Configuration du Client
        mock_client = MagicMock()
        mock_client.estSuperAbonne = True
        mock_client.nom = "John"

        # 2. Configuration de la voiture mockée
        mock_voiture = MagicMock()
        mock_voiture.obtenirHauteur.return_value = 2.0
        mock_voiture.obtenirLongueur.return_value = 4.5
        mock_voiture.obtenirImmatriculation.return_value = "FS-590-VS"
        mock_client.maVoiture = mock_voiture

        # 3. Configuration de la caméra
        self.mock_camera.capturerHauteur.return_value = 2.0
        self.mock_camera.capturerLongueur.return_value = 4.5
        self.mock_camera.capturerImmatr.return_value = "FS-590-VS"

        # 4. Configuration du téléporteur et de la borne
        self.mock_tel_e.teleporterVoitureSuperAbonne.return_value = "Voiture garée dans le parking A1"
        self.mock_borne.recupererInfosCarte.return_value = "Carte validée pour John"

        # 5. Simulation des entrées utilisateur
        mock_input.return_value = "y"  # Confirmation super abonné

        # 6. Appel de la méthode
        resultat = self.acces.lancerProcedureEntree(mock_client)

        # 7. Vérifications
        self.assertIn("Bienvenue John", resultat)
        self.assertIn("Voiture garée dans le parking A1", resultat)
        self.mock_tel_e.teleporterVoitureSuperAbonne.assert_called_once_with(mock_voiture)
        self.mock_borne.recupererInfosCarte.assert_called_once_with(mock_client)

    @patch('builtins.input')
    @patch('time.sleep')
    def test_lancer_procedure_entree_client_standard(self, mock_sleep, mock_input):
        """Teste l'entrée d'un abonné standard choisissant un service de maintenance."""
        # 1. Configuration du Client
        mock_client = MagicMock()
        mock_client.estSuperAbonne = False
        mock_client.estAbonne = True
        mock_client.nom = "Weber"

        # 2. Configuration de la voiture mockée
        mock_voiture = MagicMock()
        mock_voiture.obtenirHauteur.return_value = 1.8
        mock_voiture.obtenirLongueur.return_value = 3.5
        mock_voiture.obtenirImmatriculation.return_value = "FS-888-MW"
        mock_client.maVoiture = mock_voiture

        # 3. Configuration de la caméra
        self.mock_camera.capturerHauteur.return_value = 1.8
        self.mock_camera.capturerLongueur.return_value = 3.5
        self.mock_camera.capturerImmatr.return_value = "FS-888-MW"

        # 4. Configuration du Parking et de la Place
        mock_place = MagicMock()
        mock_place.obtenir_niveau.return_value = "A"
        mock_place.numero = 1
        self.mock_parking.rechercherPlace.return_value = mock_place

        # 5. Configuration de la borne
        self.mock_borne.recupererInfosCarte.return_value = "Client non super abonné"
        self.mock_borne.proposerServices.return_value = "1"  # Choix Maintenance
        self.mock_borne.deliverTicket.return_value = "Weber-FS-888-MW"

        # 6. Simulation des entrées utilisateur
        # Premier input: "y" (est abonné)
        mock_input.side_effect = ["y"]

        # 7. Appel de la méthode
        resultat = self.acces.lancerProcedureEntree(mock_client)

        # 8. Vérifications
        self.assertIn("Bienvenue Weber", resultat)
        self.assertIn("Place assignée : A1", resultat)
        mock_client.demanderMaintenance.assert_called_once()
        mock_place.definir_estLibre.assert_called_with(False)
        self.mock_tel_e.teleporterVoiture.assert_called_once_with(mock_voiture, mock_place)

    @patch('builtins.input')
    @patch('time.sleep')
    def test_lancer_procedure_entree_nouveau_client(self, mock_sleep, mock_input):
        """Teste l'entrée d'un nouveau client non abonné."""
        # 1. Configuration du Client
        mock_client = MagicMock()
        mock_client.estSuperAbonne = False
        mock_client.estAbonne = False
        mock_client.nom = "John Wee"

        # 2. Configuration de la voiture mockée
        mock_voiture = MagicMock()
        mock_voiture.obtenirHauteur.return_value = 2.0
        mock_voiture.obtenirLongueur.return_value = 5.0
        mock_voiture.obtenirImmatriculation.return_value = "FS-560-VS"
        mock_client.maVoiture = mock_voiture

        # 3. Configuration de la caméra
        self.mock_camera.capturerHauteur.return_value = 2.0
        self.mock_camera.capturerLongueur.return_value = 5.0
        self.mock_camera.capturerImmatr.return_value = "FS-560-VS"

        # 4. Configuration du Parking et de la Place
        mock_place = MagicMock()
        mock_place.obtenir_niveau.return_value = "B"
        mock_place.numero = 2
        self.mock_parking.rechercherPlace.return_value = mock_place

        # 5. Configuration de la borne
        self.mock_borne.recupererInfosCarte.return_value = "Client non super abonné"
        self.mock_borne.deliverTicket.return_value = "John Wee-FS-560-VS"

        # 6. Simulation des entrées utilisateur
        # Premier input: "y" (confirmation super abonné - mais sera rejeté)
        # Deuxième input: "y" (est abonné - mais client.estAbonne = False)
        mock_input.side_effect = ["y", "y"]

        # 7. Appel de la méthode
        resultat = self.acces.lancerProcedureEntree(mock_client)

        # 8. Vérifications
        self.assertIn("Bienvenue John Wee", resultat)
        self.assertIn("Place assignée : B2", resultat)
        self.mock_borne.proposerTypePaiement.assert_called_once()
        self.mock_borne.proposerAbonnements.assert_called_once_with(mock_client, self.mock_parking)
        mock_place.definir_estLibre.assert_called_with(False)
        self.mock_tel_e.teleporterVoiture.assert_called_once_with(mock_voiture, mock_place)

    @patch('builtins.input')
    @patch('time.sleep')
    def test_lancer_procedure_entree_parking_complet(self, mock_sleep, mock_input):
        """Teste l'entrée quand le parking est complet (aucune place disponible)."""
        # 1. Configuration du Client
        mock_client = MagicMock()
        mock_client.estSuperAbonne = False
        mock_client.nom = "Client X"

        # 2. Configuration de la voiture mockée
        mock_voiture = MagicMock()
        mock_voiture.obtenirHauteur.return_value = 2.5
        mock_voiture.obtenirLongueur.return_value = 6.0
        mock_client.maVoiture = mock_voiture

        # 3. Configuration de la caméra
        self.mock_camera.capturerHauteur.return_value = 2.5
        self.mock_camera.capturerLongueur.return_value = 6.0
        self.mock_camera.capturerImmatr.return_value = "XX-999-XX"

        # 4. Parking complet - aucune place disponible
        self.mock_parking.rechercherPlace.return_value = None

        # 5. Configuration de la borne
        self.mock_borne.recupererInfosCarte.return_value = "Client non super abonné"

        # 6. Simulation des entrées utilisateur
        mock_input.return_value = "y"

        # 7. Appel de la méthode
        resultat = self.acces.lancerProcedureEntree(mock_client)

        # 8. Vérifications
        self.assertEqual(resultat, "Aucune place disponible pour votre véhicule.")
        self.mock_tel_e.teleporterVoiture.assert_not_called()
