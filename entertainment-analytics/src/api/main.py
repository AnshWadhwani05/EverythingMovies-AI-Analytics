from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import sys
import os

# Add the project root to the python path so 'src' can be found
# This fixes: ModuleNotFoundError: No module named 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the models we built earlier
from src.models.recommender import ContentRecommender
from src.models.collaborative_recommender import CollaborativeRecommender

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

app = FastAPI(
    title="Entertainment Analytics API",
    description="API for Movie and Music Recommendations",
    version="1.0.0"
)

# Global instances of our models
content_engine = None
collab_engine = None

@app.on_event("startup")
async def startup_event():
    """Load and train models when the API starts."""
    global content_engine, collab_engine
    logger.info("Initializing models...")
    
    try:
        # Initialize Content-Based Engine
        content_engine = ContentRecommender()
        content_engine.fit()
        
        # Initialize Collaborative Engine
        collab_engine = CollaborativeRecommender()
        collab_engine.train()
        
        logger.info("All models loaded and ready!")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Entertainment Analytics API", "status": "online"}

@app.get("/recommend/content/{movie_title}")
def get_content_recommendations(movie_title: str):
    """Get recommendations based on movie features (Genres/Keywords)."""
    recommendations = content_engine.get_recommendations(movie_title)
    if isinstance(recommendations, str):
        raise HTTPException(status_code=404, detail=recommendations)
    return {"movie": movie_title, "recommendations": recommendations}

@app.get("/predict/rating")
def predict_rating(user_id: int, movie_id: int):
    """Predict what rating a user would give to a specific movie."""
    try:
        rating = collab_engine.predict_user_rating(user_id, movie_id)
        return {
            "user_id": user_id,
            "movie_id": movie_id,
            "predicted_rating": round(float(rating), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # When running as main, use the string path to support reload if needed
    uvicorn.run(app, host="0.0.0.0", port=8000)