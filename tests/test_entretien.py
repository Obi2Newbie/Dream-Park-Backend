import unittest
from datetime import date
from models import Entretien

class TestEntretien(unittest.TestCase):
    """Tests pour la classe Entretien."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.date_test = date.today()
        self.entretien = Entretien(self.date_test)

    def test_initialisation(self):
        """Vérifie la création d’un objet Entretien et ses valeurs par défaut."""
        # Vérifie que l'objet est bien une instance de Entretien et de Service
        self.assertIsInstance(self.entretien, Entretien)
        
        # Vérifie que le rapport initial est bien celui défini dans le super().__init__
        self.assertEqual(self.entretien.rapport, "Entretien non effectué")
        
        # Note: Si votre classe Service stocke la date dans self.dateService :
        # self.assertEqual(self.entretien.dateService, self.date_test)

    def test_effectuer_entretien(self):
        """Teste la méthode effectuerEntretien() et la mise à jour du rapport."""
        # Action : Exécuter l'entretien
        resultat = self.entretien.effectuerEntretien()
        
        # Vérification du message de retour
        attendu = "L'entretien demandé par le client est fait."
        self.assertEqual(resultat, attendu)
        
        # Vérification que l'attribut rapport a bien été mis à jour
        self.assertEqual(self.entretien.rapport, attendu)
