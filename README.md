**Smart Ride Suggestion API**

**Overview**
The Smart Ride Suggestion API is a backend system designed to simulate intelligent ride selection based on availability, ETA (Estimated Time of Arrival), and realistic distance.
Instead of automatically choosing one service, the system provides neutral recommendations and lets users decide — similar to real-world platforms like Uber, Ola, and Rapido.

**Project Structure**
BHAGYA/
│── app.py              # Main FastAPI application
│── ride_env.py         # Core ride simulation logic
│── env.py              # Environment setup (provided template)
│── baseline.py         # Baseline logic (provided)
│── inference.py        # Inference handling
│── models.py           # Data models
│── grader.py           # Evaluation logic
│── tasks.py            # Task definitions
│── Dockerfile          # Container setup
│── requirements.txt    # Dependencies
│── openenv.yaml        # OpenEnv configuration


**Features**
Smart ride suggestions based on availability
Supports real Bangalore locations (Hebbal, Whitefield, BTM, Yelahanka, etc.)
Realistic distance calculation (Haversine + road factor)
Dynamic ETA (varies each request)
No bias toward any provider
Direct booking/deep links for each ride service
Supports reset, step, and state APIs
Reinforcement-learning inspired environment design


**Tech Stack**
Backend: FastAPI
Language: Python
Geolocation: Geopy (Nominatim)
Server: Uvicorn
Containerization: Docker


**API Endpoints**
1. /
GET
Returns API status.
2. /reset
POST
Resets the environment.
3. /step
POST
Generates ride suggestions.
Request Example:
{
  "pickup": "hebbal",
  "drop": "whitefield",
  "radius_km": 5
}

Response Includes:
Distance (km)
Ride availability
ETA for each provider
Booking links
Recommendation

4. /state
GET
Returns the last computed state.

**How It Works**

1. User inputs pickup and drop locations

2. Input is cleaned (e.g., “btm” → “BTM Layout Bangalore”)

3. Locations converted to coordinates using Geopy

4. Distance calculated using Haversine formula

5. Adjusted using a factor (1.2–1.4) for realistic road distance

6. Ride availability simulated dynamically

7. ETA generated based on availability + randomness

8. System suggests best options without bias

9. Users can continue booking via provided links

**Distance Logic**
Base: Haversine formula
Adjustment: Multiplied by 1.2–1.4
Ensures realistic city travel distances

**ETA Logic**
Higher availability → Lower ETA
Lower availability → Higher ETA
Random variation simulates real-world conditions

**Ride Providers**
The system supports:
1.Uber
2.Ola
3.Rapido
4.Local services (via Justdial)

Each option includes a direct booking link.

**Notes**
Links appear as plain text in Swagger UI (not clickable)
They can be copied and opened in a browser
No paid APIs are used (fully self-contained)

**Running the Project**
1. Install dependencies
    pip install -r requirements.txt
2. Run the server
    uvicorn app:app --reload
3. Open in browser
    http://127.0.0.1:8000/docs

**Conclusion**
This project demonstrates a practical backend system for intelligent ride suggestion using simulation, geolocation, and decision logic. It emphasizes user choice, neutrality, and real-world behavior.
