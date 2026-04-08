import os
import requests
from openai import OpenAI
from grader import grade

API_BASE = "http://localhost:7860"

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME")

def run_task(task_name):
    print(f"[START] task={task_name}")

    # Step 1: Reset
    print("[STEP] reset_environment")
    state = requests.post(f"{API_BASE}/reset").json()

    # Step 2: LLM decision
    prompt = f"""
    Distance: {state['distance']} km
    Traffic: {state['traffic']}
    Choose best platform from: uber, rapido, ola
    Only return platform name.
    """

    print("[STEP] calling_llm")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    platform = response.choices[0].message.content.strip().lower()

    if platform not in ["uber", "rapido", "ola"]:
        platform = "rapido"  # fallback

    # Step 3: Call step
    print("[STEP] calling_environment_step")
    result = requests.post(
        f"{API_BASE}/step",
        json={"platform": platform}
    ).json()

    # Step 4: Grading
    score = grade(result)

    print(f"[END] task={task_name} score={score}\n")

    return score


if __name__ == "__main__":
    tasks = ["short_distance", "medium_distance", "long_distance"]

    scores = []
    for task in tasks:
        score = run_task(task)
        scores.append(score)

    avg_score = sum(scores) / len(scores)
    print(f"[FINAL_SCORE] {avg_score}")