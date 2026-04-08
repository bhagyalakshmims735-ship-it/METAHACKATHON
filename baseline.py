from env import RideEnv
from models import Action

def run():
    env = RideEnv(difficulty="medium")
    state = env.reset()

    # simple agent: pick cheapest ride
    best = min(state.rides, key=lambda r: r.price)

    action = Action(choice=best.name)
    _, reward, _, _ = env.step(action)

    print("Chosen:", best.name)
    print("Reward:", reward)

if __name__ == "__main__":
    run()