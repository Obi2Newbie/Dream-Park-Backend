import time
from datetime import date
from models import (
    Acces, Parking, Client, Camera, Place,
    Borne_ticket, Panneau_affichage, Teleporteur, Abonnement
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
    Place(2, "A", 2.50, 2.10),
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
entree_sud = Teleporteur(parking_central)

# Création de l'objet Acces (Orchestrateur)
mon_acces = Acces(camera, borne, panneau, entree_nord, entree_sud, parking_central)

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
# 5. ÉTAT FINAL
# =================================================================

print("\n" + "=" * 40)
print("--- ÉTAT FINAL DU PARKING ---")
for p in parking_central.mesPlaces:
    print(p)