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