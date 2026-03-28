import pandas as pd
import numpy as np
import os
import logging
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
import joblib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CollaborativeFilter")

class CollaborativeRecommender:
    def __init__(self, ratings_path="data/raw/ml-latest-small/ratings.csv"):
        """Initialize using the MovieLens ratings data."""
        if not os.path.exists(ratings_path):
            raise FileNotFoundError(f"Ratings data not found at {ratings_path}")
            
        self.ratings_df = pd.read_csv(ratings_path)
        self.user_item_matrix = None
        self.model = None
        self.user_features = None
        self.item_features = None

    def train(self):
        """Train a Matrix Factorization model using TruncatedSVD."""
        logger.info("Creating User-Item matrix...")
        
        # Pivot the dataframe to create a matrix where rows are users and columns are movies
        self.user_item_matrix = self.ratings_df.pivot(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0) # Fill missing ratings with 0
        
        logger.info(f"Matrix Shape: {self.user_item_matrix.shape}")
        
        # Initialize TruncatedSVD (Matrix Factorization)
        # n_components=50 is a standard starting point for latent features
        self.model = TruncatedSVD(n_components=50, random_state=42)
        
        logger.info("Training Matrix Factorization (SVD)...")
        # Decompose the matrix into User Features and Item Features
        self.user_features = self.model.fit_transform(self.user_item_matrix)
        self.item_features = self.model.components_
        
        # Calculate reconstruction error (RMSE) for training data
        # We reconstruct the matrix: User_Features * Item_Features
        reconstructed_matrix = np.dot(self.user_features, self.item_features)
        
        # We only calculate error for the ratings that actually exist (non-zero)
        mask = self.user_item_matrix.values > 0
        rmse = np.sqrt(mean_squared_error(
            self.user_item_matrix.values[mask], 
            reconstructed_matrix[mask]
        ))
        
        logger.info(f"Model Training Complete. RMSE: {rmse:.4f}")
        return rmse

    def predict_user_rating(self, user_id, movie_id):
        """Predict what rating a specific user would give to a specific movie."""
        try:
            # Get internal indices for the user and movie
            user_idx = self.user_item_matrix.index.get_loc(user_id)
            movie_idx = self.user_item_matrix.columns.get_loc(movie_id)
            
            # Dot product of the user's latent features and the item's latent features
            prediction = np.dot(self.user_features[user_idx, :], self.item_features[:, movie_idx])
            
            # Clip the rating to the standard 0.5 - 5.0 scale
            return np.clip(prediction, 0.5, 5.0)
        except (KeyError, IndexError):
            # If user or movie wasn't in the training set, return global average
            return self.ratings_df['rating'].mean()

def main():
    try:
        engine = CollaborativeRecommender()
        engine.train()
        
        # Test Case: Predicting rating for User #1 on Movie #31 (Toy Story)
        user_id = 1
        movie_id = 31
        estimated_rating = engine.predict_user_rating(user_id, movie_id)
        
        print(f"\n👤 User ID: {user_id}")
        print(f"🎬 Movie ID: {movie_id}")
        print(f"⭐ Predicted Rating: {estimated_rating:.2f} / 5.0")
        
        print("\n✅ Phase 6: Advanced Collaborative Model is now functional (using Scikit-Learn compatibility)!")
        
    except Exception as e:
        logger.error(f"Error in Advanced Model: {e}")

if __name__ == "__main__":
    main()