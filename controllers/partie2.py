import time
from datetime import date
from models import (
    Acces, Parking, Client, Camera, Place,
    Borne_ticket, Panneau_affichage, Teleporteur, Abonnement, Voiturier
)

# =================================================================
# 1. CONFIGURATION DE L'INFRASTRUCTURE DU PARKING
# =================================================================

# Initialisation du Parking (Singleton)
# nbPlacesParNiveau, nbPlacesLibres, prix, nBNiveau
parking_central = Parking(2, 4, 10.50, 2)

# Création et ajout des places physiques
parking_central.mesPlaces = [
    Place(1, "A", 5.00, 2.00),
    Place(2, "A", 5.00, 2.10),
    Place(1, "B", 5.00, 2.00),
    Place(2, "B", 2.50, 2.10)
]

# Configuration des offres d'abonnement disponibles dans ce parking
abo_std = Abonnement("Abonnement Standard", 30.0, False)
abo_vip = Abonnement("Super Abonné (Pack Garanti)", 60.0, True)

parking_central.addAbonnement(abo_std)
parking_central.addAbonnement(abo_vip)

# =================================================================
# 2. INITIALISATION DES COMPOSANTS TECHNIQUES DE L'ACCÈS
# =================================================================

camera = Camera()
borne = Borne_ticket()
panneau = Panneau_affichage()

# Les téléporteurs doivent connaître le parking pour chercher des places
entree_nord = Teleporteur(parking_central)
sortie_sud = Teleporteur(parking_central)

# Création de l'objet Acces (Orchestrateur)
mon_acces = Acces(camera, borne, panneau, entree_nord, sortie_sud, parking_central)

# =================================================================
# 3. CRÉATION DES PROFILS CLIENTS POUR LE TEST
# =================================================================

# Client 1 : Déjà Super Abonné (Priorité automatique)
client_vip = Client("John Doe", "19th Evergreen Terrace", True, True, 10)
client_vip.nouvelleVoiture("FS-590-VS", 1.90, 4.00)

# Client 2 : Déjà Abonné Standard (Accès aux services maintenance/livraison)
client_std = Client("Max Weber", "Something Street", True, False, 2)
client_std.nouvelleVoiture("FS-888-MW", 1.80, 3.50)

# Client 3 : Nouveau client (Non abonné, passera par le tunnel de vente)
client_neuf = Client("John Wee", "6 Impasse Simone", False, False, 0)
client_neuf.nouvelleVoiture("FS-560-VS", 2.00, 5.00)

# =================================================================
# 4. EXÉCUTION DES PROCÉDURES D'ENTRÉE
# =================================================================

print("--- ÉTAT INITIAL DU PARKING ---")
for p in parking_central.mesPlaces:
    print(p)
print("-" * 40)

# --- TEST 1 : Client Super Abonné ---
print(f"\n[TEST] Entrée de {client_vip.nom} (Super Abonné)")
print(mon_acces.lancerProcedureEntree(client_vip))

# --- TEST 2 : Client Nouveau (Tunnel Abonnement) ---
print(f"\n[TEST] Entrée de {client_neuf.nom} (Nouveau Client)")
print(mon_acces.lancerProcedureEntree(client_neuf))

# --- TEST 3 : Client Abonné Standard (Menu Services) ---
print(f"\n[TEST] Entrée de {client_std.nom} (Abonné Standard)")
print(mon_acces.lancerProcedureEntree(client_std))

# =================================================================
# 5. ÉTAT DU PARKING APRÈS LES ENTRÉES
# =================================================================

print("\n" + "=" * 60)
print("--- ÉTAT DU PARKING APRÈS LES ENTRÉES ---")
for p in parking_central.mesPlaces:
    print(p)


# =================================================================
# 6. FONCTION DE CALCUL DE FACTURATION
# =================================================================

def calculer_facture(client, parking):
    """
    Calcule la facture pour un client selon son type d'abonnement.

    Args:
        client (Client): Le client qui sort du parking
        parking (Parking): Le parking pour obtenir le prix de base

    Returns:
        float: Le montant à facturer (0 pour super abonnés,
               50% de réduction pour abonnés standard)
    """
    if client.estSuperAbonne:
        return 0.0
    return parking.obtenirPrix() * (0.5 if client.estAbonne else 1.0)


# =================================================================
# 7. PROCÉDURE DE SORTIE DU PARKING
# =================================================================

def executer_procedure_sortie(client, parking):
    """
    Gère la sortie complète d'un client du parking.

    Args:
        client (Client): Le client qui souhaite sortir
        parking (Parking): Le parking d'où le client sort
    """
    print(f"\n--- SORTIE DE {client.nom} ---")
    voiture = client.maVoiture

    if not voiture:
        print(f"Erreur : {client.nom} n'a pas de véhicule enregistré.")
        return

    placement = voiture.monPlacement

    # Vérifier si le placement existe et a une référence à une place
    if placement and placement.maPlace:
        place = placement.maPlace
        print(f"Téléporteur : Récupération du véhicule en {place.obtenir_niveau()}{place.numero}")

        # Libérer la place (partirPlace() met à jour estLibre automatiquement)
        placement.partirPlace()
        print(f"Place {place.obtenir_niveau()}{place.numero} libérée.")
    else:
        # Cas où le véhicule était pris en charge par le service Valet
        print(f"Service Valet : Restitution du véhicule {voiture.obtenirImmatriculation()}.")

    # Mettre à jour l'état du véhicule et afficher la facture
    voiture.estDansParking = False
    montant = calculer_facture(client, parking)

    print(f"Véhicule {voiture.obtenirImmatriculation()} restitué.")
    if montant > 0:
        print(f"Montant à régler : {montant:.2f} €")
    else:
        print("Aucun frais (Pack Garanti)")


# =================================================================
# 8. EXÉCUTION DES PROCÉDURES DE SORTIE
# =================================================================

print("\n" + "=" * 60)
print("=== PHASE DE SORTIE DES VÉHICULES ===")
print("=" * 60)

# Sortie des trois clients
executer_procedure_sortie(client_vip, parking_central)
executer_procedure_sortie(client_std, parking_central)
executer_procedure_sortie(client_neuf, parking_central)

# =================================================================
# 9. ÉTAT FINAL DU PARKING (TOUTES PLACES LIBÉRÉES)
# =================================================================

print("\n" + "=" * 60)
print("--- ÉTAT FINAL DU PARKING (APRÈS SORTIES) ---")
for p in parking_central.mesPlaces:
    print(p)
print("=" * 60)