from pydantic import BaseModel
from typing import List

class Ride(BaseModel):
    name: str
    price: float
    time: float


class State(BaseModel):
    rides: List[Ride]
    best_ride: str


class Action(BaseModel):
    distance: float
    traffic: str