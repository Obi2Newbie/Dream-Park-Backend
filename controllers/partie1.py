from models import Voiture, Camera, Acces, Client

# Création de l'acces
acces = Acces()

# Création de la caméra pour récupérer les infos de la voiture
camera = Camera()

# Création des clients abonnés et non abonnés.

client_abonne = Client("John Doe", "19th Evergreen Terrace, Springfield", True, True, 10)
client_abonne.nouvelleVoiture("FS-590-VS", 1.90, 2.00)

# Activité : Arriver devant accès.
acces.lancerProcedureEntree(client_abonne)