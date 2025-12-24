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

print("\n--- FIN DE LA PROCÉDURE PARTIE 1 ---")


def executer_partie_2(client, parking, teleporteur):
    """
    Implémentation de la logique de la Partie 2 :
    Sortie, Livraison, Maintenance et Flexibilité.
    """
    print(f"\n--- DÉBUT DE LA PROCÉDURE DE SORTIE POUR {client.nom} ---")

    voiture = client.maVoiture
    if not voiture or not voiture.monPlacement:
        print("Erreur : Aucun véhicule n'est enregistré ou stationné.")
        return

    # --- SCÉNARIO 1 : Reprendre la voiture via le téléporteur ---
    # Le téléporteur récupère la voiture
    # On identifie la place pour informer le parking qu'elle se libère
    place_actuelle = None
    for p in parking.mesPlaces:
        if p.monPlacement == voiture.monPlacement:
            place_actuelle = p
            break

    if place_actuelle:
        print(f"Activation du téléporteur pour la place {place_actuelle.numero}...")
        # Libération de la place
        place_actuelle.definir_estLibre(True)
        place_actuelle.monPlacement = None
        # Notification au parking (via le compteur de places libres)
        parking.nbPlacesLibresParNiveau(place_actuelle.obtenir_niveau())

        # Mise à jour du statut du véhicule
        voiture.partirPlace()
        voiture.estDansParking = False
        print(f"Succès : Le véhicule {voiture.obtenirImmatriculation()} est prêt. La place est libérée.")

    # --- SCÉNARIO 2 : Gestion de la Livraison (Si demandée) ---
    # On imagine que le client appelle pour modifier ses options (Flexibilité)
    reponse = input("\n[Flexibilité] Le client souhaite-t-il ajouter une livraison ? (y/n) : ")
    if reponse.lower() == 'y':
        adresse = input("Adresse de livraison : ")
        heure = int(input("Heure de livraison (ex: 18) : "))

        # On crée le service et on l'ajoute au client (Flexibilité système)
        service_livraison = client.demanderLivraison(date.today(), heure, adresse)

        # Le voiturier effectue la livraison
        voiturier_un = Voiturier(numVoiturier=101)
        confirmation = voiturier_un.livrerVoiture(voiture, date.today(), heure)
        print(confirmation)

    # --- SCÉNARIO 3 : Entretien ou Maintenance ---
    # Le système prend la voiture, fait le service, et la gare au retour.
    reponse_maint = input("\nUne maintenance est-elle prévue ? (y/n) : ")
    if reponse_maint.lower() == 'y':
        if client.estAbonne:
            print("Début du service de maintenance...")
            service_m = client.demanderMaintenance()
            # Effectuer l'action
            service_m.effectuerMaintenance(voiture)

            # Téléportation automatique au retour (car c'est un service système)
            print("Maintenance finie. Téléportation vers une place de parking...")
            log_teleport = teleporteur.teleporterVoitureSuperAbonne(voiture)
            print(log_teleport)
        else:
            print("Maintenance refusée : réservée aux abonnés.")

    print("\n--- FIN DE LA PROCÉDURE PARTIE 2 ---")