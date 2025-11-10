from pydantic import BaseModel
from datetime import date

class Contrat(BaseModel):
    dateDebut: date
    dateFin: date
    estEnCours: bool