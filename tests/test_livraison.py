import unittest
from datetime import date
from models.livraison import Livraison


class TestLivraison(unittest.TestCase):
    """Tests unitaires pour la classe Livraison."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        # On utilise des types cohérents avec les docstrings de votre classe
        self.date_demande = date.today().strftime("%d/%m/%Y")
        self.heure_test = "18"  # String comme indiqué dans votre docstring
        self.adresse_test = "42 Avenue des Champs-Élysées"
        self.livraison = Livraison(self.date_demande, self.heure_test, self.adresse_test)

    def test_initialisation(self):
        """Vérifie la création d’un objet Livraison et l'assignation des attributs."""
        # Vérification de l'instance
        self.assertIsInstance(self.livraison, Livraison)

        # Vérification du statut initial hérité de Service
        self.assertEqual(self.livraison.rapport, "Livraison non effectué")

        # Vérification des attributs spécifiques
        self.assertEqual(self.livraison.adresse, self.adresse_test)
        self.assertEqual(self.livraison.heure, self.heure_test)
        self.assertEqual(self.livraison.dateDemande, self.date_demande)

    def test_effectuer_livraison(self):
        """Teste l’exécution de la livraison et la mise à jour du rapport."""
        # Note : Votre méthode ne retourne rien (pas de return),
        # elle modifie seulement l'état interne (self.rapport).
        self.livraison.effectuerLivraison()

        # On vérifie que le rapport a été correctement mis à jour
        attendu = f"Livraison effectuée à {self.adresse_test} à {self.heure_test}h"
        self.assertEqual(self.livraison.rapport, attendu)
