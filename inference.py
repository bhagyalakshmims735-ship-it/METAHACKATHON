from fastapi import FastAPI
import os
import requests
from openai import OpenAI
from grader import grade

app = FastAPI()

API_BASE = "http://localhost:7860"

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME")


def run_task(task_name):
    state = requests.post(f"{API_BASE}/reset").json()

    prompt = f"""
    Distance: {state['distance']} km
    Traffic: {state['traffic']}
    Choose best platform from: uber, rapido, ola
    Only return platform name.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    platform = response.choices[0].message.content.strip().lower()

    if platform not in ["uber", "rapido", "ola"]:
        platform = "rapido"

    result = requests.post(
        f"{API_BASE}/step",
        json={"platform": platform}
    ).json()

    score = grade(result)
    return score


@app.get("/")
def home():
    return {"message": "Server is running"}


@app.post("/run")
def run():
    tasks = ["short_distance", "medium_distance", "long_distance"]

    scores = []
    for task in tasks:
        scores.append(run_task(task))

    avg_score = sum(scores) / len(scores)

    return {"score": avg_score}