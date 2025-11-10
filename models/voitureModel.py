from pydantic import BaseModel

class Voiture(BaseModel):
    hauteur: float
    longeur: float
    immatriculation: str
    estDansParking: bool