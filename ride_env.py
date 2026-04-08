import random
import math

class RideEnv:
    def __init__(self):
        self.state = {}

    def reset(self):
        self.state = {}
        return self.state

   
    def distance_km(self, p1, p2):
        lat1, lon1 = p1
        lat2, lon2 = p2

        R = 6371

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(dlon/2)**2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        straight = R * c

        
        factor = random.uniform(1.2, 1.4)
        return round(straight * factor, 2)

    def simulate_availability(self):
        return {
            "Uber": random.randint(0, 10),
            "Ola": random.randint(0, 10),
            "Rapido": random.randint(0, 10),
            "Local": random.randint(0, 10)
        }

    def eta(self, val):
        if val == 0:
            return "Not available"

        base = 15 - val
        noise = random.randint(0, 5)

        eta_min = max(2, base + noise - 2)
        eta_max = eta_min + random.randint(2, 5)

        return f"~{eta_min}-{eta_max} mins"

    def step(self, pickup, drop, radius):

        dist = self.distance_km(pickup, drop)
        availability = self.simulate_availability()

        options = []
        scores = []

       
        links = {
            "Uber": "https://m.uber.com/ul/",
            "Ola": "https://book.olacabs.com/",
            "Rapido": "https://www.rapido.bike/",
            "Local": "https://www.justdial.com/"
        }

        for provider, val in availability.items():

            if val == 0:
                msg = f"{provider}: Not available in {radius} km radius"
                eta_val = "Not available"
                score = 0
            else:
                msg = f"{provider}: Available nearby"
                eta_val = self.eta(val)
                score = val

            scores.append((provider, score))

            options.append({
                "provider": provider,
                "message": msg,
                "eta": eta_val,
                "link": links[provider],
                "note": "Click link to continue booking"
            })

        scores_sorted = sorted(scores, key=lambda x: x[1], reverse=True)

        if scores_sorted[0][1] == 0:
            recommendation = "No rides available. Try local transport."
        else:
            top_score = scores_sorted[0][1]
            best = [p for p, s in scores_sorted if s == top_score]

            recommendation = (
                f"Based on availability, you can consider: {', '.join(best)}. "
                "Other options are also available."
            )

        self.state = {
            "distance_km": dist,
            "radius_km": radius,
            "availability": availability,
            "suggestion": {
                "recommendation": recommendation,
                "options": options
            }
        }

        return self.state

    def get_state(self):
        return self.state