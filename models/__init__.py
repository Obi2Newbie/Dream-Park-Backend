# models/__init__.py

"""
Package `models` du projet DreamPark.
Ce module regroupe et expose toutes les classes principales du modèle de données.
Permet des imports simplifiés :
    from models import Client, Voiture, Parking
"""

from .abonnement import Abonnement
from .acces import Acces
from .borne_ticket import Borne_ticket
from .camera import Camera
from .client import Client
from .contrat import Contrat
from .entretien import Entretien
from .livraison import Livraison
from .maintenance import Maintenance
from .panneau_affichage import Panneau_affichage
from .parking import Parking
from .place import Place
from .placement import Placement
from .service import Service
from .teleporteur import Teleporteur
from .voiture import Voiture
from .voiturier import Voiturier

__all__ = [
    "Abonnement",
    "Acces",
    "Borne_ticket",
    "Camera",
    "Client",
    "Contrat",
    "Entretien",
    "Livraison",
    "Maintenance",
    "Panneau_affichage",
    "Parking",
    "Place",
    "Placement",
    "Service",
    "Teleporteur",
    "Voiture",
    "Voiture"
]

