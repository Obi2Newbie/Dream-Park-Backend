from models import Acces, Parking, Client, Camera, Place, Borne_ticket, Panneau_affichage

# Création de l'acces
camera = Camera()
borne = Borne_ticket()
panneau = Panneau_affichage()
tel_entree = "Entré Nord"
tel_sortie = "Sortie Sud"
parking = Parking(2,2,10.50, 2)
parking.mesPlaces.append(Place(1, "A",5.00,2.00))
parking.mesPlaces.append(Place(2, "A",2.50,2.10))
parking.mesPlaces.append(Place(1, "B",5.00,2.00))
parking.mesPlaces.append(Place(2, "B",2.50,2.10))
acces = Acces(camera, borne, panneau, tel_entree, tel_sortie, parking)
for parking in parking.mesPlaces:
    print(parking)

client_abonne = Client("John Doe", "19th Evergreen Terrace, Springfield", True, True, 10)
client_abonne.nouvelleVoiture("FS-590-VS", 1.90, 2.00)

# Activité : Arriver devant accès.
acces.lancerProcedureEntree(client_abonne)