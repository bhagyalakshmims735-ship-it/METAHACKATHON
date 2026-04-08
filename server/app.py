from fastapi import FastAPI
from inference import main

app = FastAPI()

@app.get("/")
def root():
    return {"message": "OpenEnv API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommend")
def recommend():
    return main()