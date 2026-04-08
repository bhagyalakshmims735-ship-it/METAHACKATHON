import random
from models import State, Ride

class RideEnv:

    def reset(self):
        rides = self._generate_rides()
        best = self._select_best(rides)

        return State(
            rides=rides,
            best_ride=best.name
        )

    def step(self, action):
        rides = self._generate_rides()
        best = self._select_best(rides)

        reward = 100 - best.price
        done = True

        info = {
            "reason": "Selected lowest price ride"
        }

        return (
            State(
                rides=rides,
                best_ride=best.name
            ),
            reward,
            done,
            info
        )

    def _generate_rides(self):
        return [
            Ride(name="Uber", price=random.randint(100, 300), time=random.randint(5, 20)),
            Ride(name="Rapido", price=random.randint(50, 200), time=random.randint(5, 25)),
            Ride(name="Ola", price=random.randint(80, 250), time=random.randint(5, 20))
        ]

    def _select_best(self, rides):
        return min(rides, key=lambda x: x.price)