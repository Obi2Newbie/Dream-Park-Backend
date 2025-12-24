import unittest
from models import Abonnement
class TestAbonnement(unittest.TestCase):
    """Tests pour la création et la gestion des abonnements."""

    def setUp(self):
        """Configuration initiale avant chaque test."""
        self.libelle = "Pack Garanti"
        self.prix = 59.90
        self.est_pack_gar = True
        self.abonnement = Abonnement(self.libelle, self.prix, self.est_pack_gar)

    def test_initialisation(self):
        """Vérifie la création d’un abonnement avec libellé, prix et pack garanti."""
        self.assertEqual(self.abonnement.libelle, self.libelle)
        self.assertEqual(self.abonnement.prix, self.prix)
        self.assertTrue(self.abonnement.estPackGar)
        # Vérifie que la liste des abonnements (contrats) est vide à l'initialisation
        self.assertEqual(len(self.abonnement.mesAbonnements), 0)
        # Vérifie que le prix est bien converti en float
        self.assertIsInstance(self.abonnement.prix, float)

    def test_add_contrat(self):
        """Teste l’ajout d’un contrat à un abonnement."""
        # On simule un objet contrat (on peut utiliser une chaîne ou un objet Mock)
        contrat_test = "Contrat_001"
        
        # Action : ajout du contrat
        self.abonnement.addContrat(contrat_test)
        
        # Vérifications
        self.assertIn(contrat_test, self.abonnement.mesAbonnements)
        self.assertEqual(len(self.abonnement.mesAbonnements), 1)
        
        # Test de sécurité : vérifier qu'on ne peut pas ajouter deux fois le même contrat
        self.abonnement.addContrat(contrat_test)
        self.assertEqual(len(self.abonnement.mesAbonnements), 1, "Le contrat ne doit pas être ajouté en double.")