from fastapi import FastAPI
from pydantic import BaseModel
from ride_env import RideEnv
from geopy.geocoders import Nominatim

app = FastAPI()
env = RideEnv()

geolocator = Nominatim(user_agent="ride_app", timeout=3)


class RideRequest(BaseModel):
    pickup: str
    drop: str
    radius_km: float = 5


def clean_place(place: str):
    place = place.strip().lower()

    shortcuts = {
        "krpuram": "KR Puram Bangalore",
        "yelahanka": "Yelahanka Bangalore",
        "whitefield": "Whitefield Bangalore",
        "btm": "BTM Layout Bangalore",
        "hebbal": "Hebbal Bangalore",
        "electronic city": "Electronic City Bangalore"
    }

    if place in shortcuts:
        return shortcuts[place]

    if "bangalore" not in place and "bengaluru" not in place:
        place += " Bangalore"

    return place.title()


def get_location(place: str):
    try:
        loc = geolocator.geocode(place)
        if loc:
            return {
                "coords": (loc.latitude, loc.longitude),
                "address": loc.address.lower()
            }
    except:
        return None
    return None


@app.get("/")
def home():
    return {"message": "Smart Ride Suggestion API"}


@app.post("/reset")
def reset():
    env.reset()
    return {"message": "Reset successful"}


@app.post("/step")
def step(req: RideRequest):

    pickup_clean = clean_place(req.pickup)
    drop_clean = clean_place(req.drop)

    pickup_loc = get_location(pickup_clean)
    drop_loc = get_location(drop_clean)

    if not pickup_loc or not drop_loc:
        return {"error": "Invalid location. Try Hebbal, Whitefield, BTM."}

    if "karnataka" not in pickup_loc["address"] or "karnataka" not in drop_loc["address"]:
        return {"error": "Locations must be within Karnataka."}

    temp_distance = env.distance_km(
        pickup_loc["coords"],
        drop_loc["coords"]
    )

    if temp_distance > 100:
        return {"error": "Locations too far. Choose within same city."}

    result = env.step(
        pickup_loc["coords"],
        drop_loc["coords"],
        req.radius_km
    )

    result["pickup"] = pickup_clean
    result["drop"] = drop_clean

    return result


@app.get("/state")
def state():
    state = env.get_state()

    if not state:
        return {"message": "No active ride. Use /step first."}

    return state


@app.get("/recommend")
def recommend():
    state = env.get_state()

    if not state:
        return {"message": "Run /step first"}

    return state

def main(action=None, **kwargs):
    if action == "reset":
        return reset()
    elif action == "state":
        return state()
    elif action == "recommend":
        return state()
    else:
        return {"message": "Smart Ride Suggestion API"}