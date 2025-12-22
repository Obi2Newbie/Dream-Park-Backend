from models import Acces, Parking, Client, Camera, Place, Borne_ticket, Panneau_affichage, Teleporteur

# Création de l'acces
camera = Camera()
borne = Borne_ticket()
panneau = Panneau_affichage()
parking = Parking(2,4,10.50, 2)
parking.mesPlaces.append(Place(1, "A",5.00,2.00))
parking.mesPlaces.append(Place(2, "A",2.50,2.10))
parking.mesPlaces.append(Place(1, "B",5.00,2.00))
parking.mesPlaces.append(Place(2, "B",2.50,2.10))
entree_nord = Teleporteur(parking)
entree_sud = Teleporteur(parking)
acces = Acces(camera, borne, panneau, entree_nord, entree_sud, parking)
for t in parking.mesPlaces:
    print(t)

client_abonne = Client("John Doe", "19th Evergreen Terrace, Springfield", True, True, 10)
client_abonne.nouvelleVoiture("FS-590-VS", 2.01, 2.4)
client_non_abonne = Client("John Wee", "6 Impasse Simone de Beauvoir",False,False, 0)
client_non_abonne.nouvelleVoiture("FS-560-VS", 2.00, 5.00)

# Activité : Arriver devant accès.
print(acces.lancerProcedureEntree(client_abonne))
print(acces.lancerProcedureEntree(client_non_abonne))
for t in parking.mesPlaces:
    print(t)