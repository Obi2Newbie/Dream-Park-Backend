import time
from datetime import date
from models import (
    Acces, Parking, Client, Camera, Place,
    Borne_ticket, Panneau_affichage, Teleporteur, Abonnement, Voiturier
)

# =================================================================
# 1. INFRASTRUCTURE SETUP
# =================================================================
parking_central = Parking(2, 4, 10.50, 2)

# Important: Ensure at least one spot is large enough for Max Weber (3.5m)
parking_central.mesPlaces = [
    Place(1, "A", 5.00, 2.00),  # Large
    Place(2, "A", 5.00, 2.10),  # Large (Increased length for test)
    Place(1, "B", 5.00, 2.00),  # Large
    Place(2, "B", 2.50, 2.10)  # Small
]

abo_std = Abonnement("Abonnement Standard", 30.0, False)
abo_vip = Abonnement("Super Abonné (Pack Garanti)", 60.0, True)
parking_central.addAbonnement(abo_std)
parking_central.addAbonnement(abo_vip)

mon_acces = Acces(Camera(), Borne_ticket(), Panneau_affichage(),
                  Teleporteur(parking_central), Teleporteur(parking_central), parking_central)

# =================================================================
# 2. CLIENT PROFILES
# =================================================================
client_vip = Client("John Doe", "19th Evergreen Terrace", True, True, 10)
client_vip.nouvelleVoiture("FS-590-VS", 1.90, 4.00)

client_std = Client("Max Weber", "Something Street", True, False, 2)
client_std.nouvelleVoiture("FS-888-MW", 1.80, 3.50)

client_neuf = Client("John Wee", "6 Impasse Simone", False, False, 0)
client_neuf.nouvelleVoiture("FS-560-VS", 2.00, 5.00)

# =================================================================
# 3. ENTRY SIMULATION
# =================================================================
print("--- ÉTAT INITIAL DU PARKING ---")
for p in parking_central.mesPlaces: print(p)
print("-" * 40)

print(f"\n[TEST] Entrée de {client_vip.nom}")
print(mon_acces.lancerProcedureEntree(client_vip))

print(f"\n[TEST] Entrée de {client_neuf.nom}")
print(mon_acces.lancerProcedureEntree(client_neuf))

print(f"\n[TEST] Entrée de {client_std.nom}")
print(mon_acces.lancerProcedureEntree(client_std))

print("\n" + "=" * 40)
print("--- ÉTAT DU PARKING APRÈS ENTRÉES ---")
for p in parking_central.mesPlaces: print(p)


# =================================================================
# 4. EXIT SIMULATION (Unified Logic)
# =================================================================

def calculer_facture(client, parking):
    if client.estSuperAbonne: return 0.0
    return (parking.obtenirPrix() * (0.5 if client.estAbonne else 1.0))


def executer_partie_2(client, parking):
    print(f"\n--- SORTIE POUR {client.nom} ---")
    voiture = client.maVoiture
    placement = voiture.monPlacement

    # Si la voiture a un placement qui connaît sa place
    if placement and hasattr(placement, 'maPlace') and placement.maPlace:
        p = placement.maPlace
        print(f"Téléporteur : Récupération du véhicule en {p.obtenir_niveau()}{p.numero}")

        # CETTE LIGNE FAIT TOUT :
        # 1. finit le temps
        # 2. libère la place
        # 3. enlève le lien
        placement.partirPlace()

        parking.nbPlacesLibres += 1
    else:
        # Si on arrive ici, c'est que le lien Voiture -> Placement -> Place est cassé
        print(f"Service Valet : Restitution du véhicule {voiture.obtenirImmatriculation()}.")

    # Facturation et état final
    voiture.estDansParking = False
    print(f"Véhicule {voiture.obtenirImmatriculation()} restitué.")


# Run exits
executer_partie_2(client_vip, parking_central)
executer_partie_2(client_std, parking_central)
executer_partie_2(client_neuf, parking_central)

print("\n" + "=" * 60)
print("--- ÉTAT FINAL DU PARKING (LIBÉRÉ) ---")
for p in parking_central.mesPlaces: print(p)
print("=" * 60)