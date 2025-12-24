import time
from datetime import date
from models import (
    Acces, Parking, Client, Camera, Place,
    Borne_ticket, Panneau_affichage, Teleporteur, Abonnement, Voiturier, reprendre_la_voiture
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
# 6. EXÉCUTION DES SERVICES DEMANDÉS
# =================================================================

print("\n" + "=" * 60)
print("=== PHASE D'EXÉCUTION DES SERVICES ===")
print("=" * 60)

# Création d'un voiturier pour les livraisons
voiturier_1 = Voiturier(1)

# Parcourir tous les clients pour exécuter leurs services
tous_les_clients = [client_vip, client_std, client_neuf]

for client in tous_les_clients:
    if client.mesServices:
        print(f"\n--- Services demandés par {client.nom} ---")

        for service in client.mesServices:
            # Vérifier le type de service et l'exécuter
            if hasattr(service, 'effectuerMaintenance'):  # Service Maintenance
                print(f"🔧 Exécution de la maintenance pour {client.maVoiture.obtenirImmatriculation()}")
                rapport = service.effectuerMaintenance(client.maVoiture)
                print(f"   ✓ {rapport}")

            elif hasattr(service, 'effectuerEntretien'):  # Service Entretien
                print(f"🧼 Exécution de l'entretien pour {client.maVoiture.obtenirImmatriculation()}")
                rapport = service.effectuerEntretien()
                print(f"   ✓ {rapport}")

            elif hasattr(service, 'effectuerLivraison'):  # Service Livraison
                print(f"🚗 Préparation de la livraison pour {client.maVoiture.obtenirImmatriculation()}")
                service.effectuerLivraison()
                print(f"   ✓ {service.rapport}")

                # Le voiturier effectue la livraison
                resultat = voiturier_1.livrerVoiture(
                    client.maVoiture,
                    service.dateDemande,
                    service.heure
                )
                print(f"   📍 {resultat}")
    else:
        print(f"\n{client.nom} n'a demandé aucun service additionnel.")

print("\n" + "=" * 60)
print("=== PHASE DE SORTIE DES VÉHICULES ===")
print("=" * 60)

# =================================================================
# 7. PROCÉDURE DE SORTIE DU PARKING
# =================================================================

# Sortie des clients (seulement ceux qui n'ont pas demandé de livraison)
for client in tous_les_clients:
    # Vérifier si le client a demandé une livraison
    a_demande_livraison = any(
        hasattr(service, 'effectuerLivraison')
        for service in client.mesServices
    )

    if not a_demande_livraison:
        reprendre_la_voiture.executer_procedure_sortie(client, parking_central)
    else:
        print(f"\n--- {client.nom} ---")
        print(f"Véhicule déjà livré à domicile via le service Voiturier.")

# =================================================================
# 8. ÉTAT FINAL DU PARKING (TOUTES PLACES LIBÉRÉES)
# =================================================================

print("\n" + "=" * 60)
print("--- ÉTAT FINAL DU PARKING (APRÈS SORTIES) ---")
for p in parking_central.mesPlaces:
    print(p)
print("=" * 60)

# =================================================================
# 9. RÉSUMÉ DES SERVICES EXÉCUTÉS
# =================================================================

print("\n" + "=" * 60)
print("=== RÉSUMÉ DES SERVICES EXÉCUTÉS ===")
print("=" * 60)

for client in tous_les_clients:
    print(f"\n{client.nom}:")
    if client.mesServices:
        for idx, service in enumerate(client.mesServices, 1):
            print(f"   {idx}. {service.__class__.__name__}: {service.rapport}")
    else:
        print("   Aucun service demandé")

print("\n" + "=" * 60)