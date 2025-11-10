from datetime import date
from pydantic import BaseModel

class Placement(BaseModel):
    dateDebut: date
    dateFin: date
    estEnCours: bool