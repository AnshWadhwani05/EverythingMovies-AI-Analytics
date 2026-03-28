import pandas as pd
import numpy as np
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Preprocessing")

class DataCleaner:
    def __init__(self, input_path="data/raw", output_path="data/processed"):
        self.input_path = input_path
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def clean_imdb(self):
        """Cleans IMDb metadata: handles missing values and simplifies genres."""
        logger.info("Cleaning IMDb metadata...")
        df = pd.read_csv(f"{self.input_path}/imdb_metadata.csv")
        
        # Fill missing numeric values with the median
        cols_to_fix = ['gross', 'budget', 'title_year', 'aspect_ratio']
        for col in cols_to_fix:
            df[col] = df[col].fillna(df[col].median())
            
        # Fill missing text with 'Unknown'
        df['director_name'] = df['director_name'].fillna('Unknown')
        
        # Save processed version
        df.to_csv(f"{self.output_path}/cleaned_imdb.csv", index=False)
        return df

    def clean_spotify(self):
        """Cleans Spotify data: removes duplicates and handles track metadata."""
        logger.info("Cleaning Spotify data...")
        df = pd.read_csv(f"{self.input_path}/spotify_tracks.csv")
        
        # Remove tracks with missing names/artists
        df = df.dropna(subset=['track_name', 'track_artist'])
        
        # Remove duplicate track IDs
        df = df.drop_duplicates(subset=['track_id'])
        
        df.to_csv(f"{self.output_path}/cleaned_spotify.csv", index=False)
        return df

    def create_master_movies(self, imdb_df):
        """Prepares a movie feature set for the recommendation engine."""
        logger.info("Creating Master Movie Features...")
        
        # Select relevant columns for recommendation
        features = imdb_df[['movie_title', 'director_name', 'genres', 'imdb_score', 'plot_keywords']].copy()
        
        # Simple cleanup of titles (remove trailing spaces)
        features['movie_title'] = features['movie_title'].str.strip()
        
        features.to_csv(f"{self.output_path}/movie_features.csv", index=False)
        logger.info("Master features saved to data/processed/movie_features.csv")

def main():
    cleaner = DataCleaner()
    
    # Run cleaning tasks
    imdb_cleaned = cleaner.clean_imdb()
    cleaner.clean_spotify()
    cleaner.create_master_movies(imdb_cleaned)
    
    logger.info("Phase 4: Preprocessing completed successfully!")

if __name__ == "__main__":
    main()