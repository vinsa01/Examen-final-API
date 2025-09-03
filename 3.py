from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

class Characteristics(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristics

app = FastAPI(
    title="API de Voitures",
    description="Une API simple pour gérer des voitures en mémoire."
)
cars_db = []



# a
@app.get("/ping", response_class=str)
def ping():
    """
    Vérification de l'état de l'API.
    Retourne "pong".
    """
    return "pong"

# b
@app.post("/cars", status_code=status.HTTP_201_CREATED, response_model=List[Car])
def create_cars(cars: List[Car]):
    """
    Crée et sauvegarde une liste de voitures.
    """
    cars_db.extend(cars)
    return cars_db

# c
@app.get("/cars", response_model=List[Car])
def get_all_cars():
    """
    Récupère la liste de toutes les voitures sauvegardées.
    """
    return cars_db

# d GET /cars/{id}
@app.get("/cars/{id}", response_model=Car)
def get_car_by_id(id: str):
    """
    Récupère une voiture spécifique par son identifiant.
    Retourne une erreur 404 si la voiture n'est pas trouvée.
    """
    for car in cars_db:
        if car.identifier == id:
            return car
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The car with id '{id}' does not exist or was not found."

    )
