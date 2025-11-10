from pydantic import BaseModel

class Place(BaseModel):
    numero: int
    niveau: str
    longeur: float
    hauteur: float
    estLibre: bool