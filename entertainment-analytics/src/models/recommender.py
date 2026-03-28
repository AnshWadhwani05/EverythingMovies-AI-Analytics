import pandas as pd
import numpy as np
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Recommender")

class ContentRecommender:
    def __init__(self, data_path="data/processed/movie_features.csv"):
        """Initialize the recommender and load processed features."""
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Processed data not found at {data_path}")
            
        self.df = pd.read_csv(data_path)
        
        # CLEANING DATA: The IMDb dataset often has invisible trailing spaces
        # We strip them globally during initialization
        self.df['movie_title'] = self.df['movie_title'].str.strip()
        
        self.df['genres'] = self.df['genres'].fillna('')
        self.df['plot_keywords'] = self.df['plot_keywords'].fillna('')
        self.df['director_name'] = self.df['director_name'].fillna('')
        
        # Combine features for the TF-IDF vectorizer
        self.df['combined_features'] = (
            self.df['genres'] + " " + 
            self.df['plot_keywords'] + " " + 
            self.df['director_name']
        )
        
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.cosine_sim = None

    def fit(self):
        """Convert text descriptions into a matrix and calculate similarity."""
        logger.info("Training the recommendation engine...")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        logger.info("Similarity matrix calculated successfully.")

    def get_recommendations(self, title, num_recommendations=5):
        """Find the most similar movies to a given title."""
        if self.cosine_sim is None:
            return "Engine not trained. Please call fit() first."

        # FUZZY/CASE-INSENSITIVE MATCHING
        search_title = title.strip().lower()
        
        # Attempt 1: Exact Match (ignoring case/whitespace)
        match = self.df[self.df['movie_title'].str.lower() == search_title]
        
        # Attempt 2: Partial Match (if exact match fails)
        if match.empty:
            match = self.df[self.df['movie_title'].str.lower().str.contains(search_title)]
            
        if match.empty:
            return f"Movie '{title}' not found in database. Please check the spelling."
        
        # Take the first match if multiple exist
        idx = match.index[0]
        actual_title = self.df.iloc[idx]['movie_title']
        logger.info(f"Finding recommendations for matched title: {actual_title}")

        # Calculate scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Skip the first one (itself) and take top N
        sim_scores = sim_scores[1:num_recommendations+1]
        
        movie_indices = [i[0] for i in sim_scores]
        return self.df['movie_title'].iloc[movie_indices].tolist()