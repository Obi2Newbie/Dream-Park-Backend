import unittest
from datetime import date
from models import Livraison

class TestLivraison(unittest.TestCase):
    """Tests pour la classe Livraison."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.date_demande = date.today()
        self.heure_test = 18
        self.adresse_test = "42 Avenue des Champs-Élysées"
        self.livraison = Livraison(self.date_demande, self.heure_test, self.adresse_test)

    def test_initialisation(self):
        """Vérifie la création d’un objet Livraison et l'assignation des attributs."""
        # Vérification de l'héritage et du statut initial via la classe parente
        self.assertIsInstance(self.livraison, Livraison)
        self.assertEqual(self.livraison.rapport, "Livraison non effectué")
        
        # Vérification des attributs spécifiques à la livraison
        self.assertEqual(self.livraison.adresse, self.adresse_test)
        self.assertEqual(self.livraison.heure, self.heure_test)

    def test_effectuer_livraison(self):
        """Teste l’exécution d’une livraison de véhicule et la mise à jour du rapport."""
        # Action : Effectuer la livraison
        resultat = self.livraison.effectuerLivraison()
        
        # Vérification du message de retour formaté
        attendu = f"Livraison effectuée à {self.adresse_test} à {self.heure_test}h"
        self.assertEqual(resultat, attendu)
        
        # Vérification que l'attribut rapport de la classe Service a bien été mis à jour
        self.assertEqual(self.livraison.rapport, attendu)