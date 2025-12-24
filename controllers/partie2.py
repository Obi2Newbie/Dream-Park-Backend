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
parking_central = Parking(2, 4, 10.50, 2)

# Création et ajout des places physiques
parking_central.mesPlaces = [
    Place(1, "A", 5.00, 2.00),
    Place(2, "A", 2.50, 2.10),
    Place(1, "B", 5.00, 2.00),
    Place(2, "B", 2.50, 2.10)
]

# Configuration des offres d'abonnement
parking_central.mesAbonnements = []  # Reset pour éviter les doublons
abo_std = Abonnement("Abonnement Standard", 30.0, False)
abo_vip = Abonnement("Super Abonné (Pack Garanti)", 60.0, True)

parking_central.addAbonnement(abo_std)
parking_central.addAbonnement(abo_vip)

# =================================================================
# 2. INITIALISATION DES COMPOSANTS TECHNIQUES
# =================================================================

camera = Camera()
borne = Borne_ticket()
panneau = Panneau_affichage()

entree_nord = Teleporteur(parking_central)
entree_sud = Teleporteur(parking_central)

mon_acces = Acces(camera, borne, panneau, entree_nord, entree_sud, parking_central)

# =================================================================
# 3. CRÉATION DES PROFILS CLIENTS
# =================================================================

client_vip = Client("John Doe", "19th Evergreen Terrace", True, True, 10)
client_vip.nouvelleVoiture("FS-590-VS", 1.90, 4.00)

client_std = Client("Max Weber", "Something Street", True, False, 2)
client_std.nouvelleVoiture("FS-888-MW", 1.80, 3.50)

client_neuf = Client("John Wee", "6 Impasse Simone", False, False, 0)
client_neuf.nouvelleVoiture("FS-560-VS", 2.00, 5.00)

# =================================================================
# 4. EXÉCUTION DES PROCÉDURES D'ENTRÉE (Strictement identique à Partie 1)
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

# Synchronisation pour la sortie
for c in [client_vip, client_std, client_neuf]:
    c.maVoiture.estDansParking = True

print("\n" + "=" * 40)
print("--- ÉTAT FINAL DU PARKING ---")
for p in parking_central.mesPlaces:
    print(p)


# =================================================================
# 5. LOGIQUE DE CALCUL DE PRIX ET SORTIE (PARTIE 2)
# =================================================================

def calculer_facture(client, parking):
    """Calcule le prix selon le statut de l'abonnement."""
    prix_base = parking.obtenirPrix()
    nb_jours = 1
    if client.estSuperAbonne:
        return prix_base * 0.1 * nb_jours

    if client.estAbonne:
        return (prix_base * 0.5) * nb_jours
    else:
        return prix_base * nb_jours


def executer_partie_2(client, parking):
    print(f"\n--- SORTIE POUR {client.nom} ---")
    voiture = client.maVoiture

    # 1. On récupère le placement stocké DANS la voiture
    placement_voiture = voiture.monPlacement
    print("Placement Voiture",placement_voiture)

    place_physique = None

    # 2. On cherche la place qui possède CE placement précis
    if placement_voiture:
        for p in parking.mesPlaces:
            # On compare l'objet placement de la place avec celui de la voiture
            if c.monPlacement == placement_voiture:
                place_physique = p
                break

    # 3. Libération de l'infrastructure
    if place_physique:
        print(f"Téléporteur : Récupération du véhicule en {place_physique.obtenir_niveau()}{place_physique.numero}")

        # Mise à jour de la Place selon les méthodes de votre classe Place
        place_physique.definir_estLibre(True)  # Change l'état interne pour le __str__
        place_physique.monPlacement = None  # Supprime le lien avec le placement

        # Mise à jour du compteur global du parking
        parking.nbPlacesLibres += 1
    else:
        # Cas où la voiture n'a pas de place (ex: Super Abonné / Pack Garanti)
        print(f"Service Valet : Restitution du véhicule {voiture.obtenirImmatriculation()}.")

    # 4. Facturation
    prix = calculer_facture(client, parking)
    print(f"[*] Facturation : {prix}€")

    # 5. Flexibilité (Livraison)
    if client.estAbonne or client.estSuperAbonne:
        rep = input(f"{client.nom}, souhaitez-vous une livraison à domicile ? (y/n) : ")
        if rep.lower() == 'y':
            vtr = Voiturier(101)
            print(vtr.livrerVoiture(voiture, date.today(), 18))

    # 6. Mise à jour finale de la voiture et du placement
    voiture.estDansParking = False
    if voiture.monPlacement:
        voiture.monPlacement.partirPlace()  # Met estEnCours à False

    print(f"Véhicule {voiture.obtenirImmatriculation()} restitué. Bonne route !")


# =================================================================
# 6. LANCEMENT DE LA SORTIE
# =================================================================

executer_partie_2(client_vip, parking_central)
executer_partie_2(client_std, parking_central)
executer_partie_2(client_neuf, parking_central)

print("\n" + "=" * 60)
print("--- ÉTAT FINAL DU PARKING (LIBÉRÉ) ---")
for p in parking_central.mesPlaces:
    print(p)
print("=" * 60)