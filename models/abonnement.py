from pydantic import BaseModel

class Abonnement(BaseModel):
    libelle: str
    prix: float
    estPackGar: bool