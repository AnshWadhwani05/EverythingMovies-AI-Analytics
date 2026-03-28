import os
import logging
import pandas as pd
import requests
import zipfile
from typing import Optional

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("outputs/ingestion.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DataIngestion")

class DataDataLoader:
    """Handles downloading and initial loading of entertainment datasets."""
    
    def __init__(self, raw_data_path: str = "data/raw"):
        self.raw_data_path = raw_data_path
        os.makedirs(self.raw_data_path, exist_ok=True)

    def download_file(self, url: str, filename: str):
        """Downloads a file from a URL if it doesn't exist."""
        target_path = os.path.join(self.raw_data_path, filename)
        if os.path.exists(target_path):
            logger.info(f"File {filename} already exists. Skipping download.")
            return target_path
        
        logger.info(f"Downloading {filename} from {url}...")
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Successfully downloaded {filename}")
            return target_path
        except Exception as e:
            logger.error(f"Failed to download {filename}: {e}")
            return None

    def load_dataset(self, file_path: str, sep: str = ',', encoding: str = 'utf-8') -> Optional[pd.DataFrame]:
        """Loads a CSV into a DataFrame and prints a summary for validation."""
        if not file_path or not os.path.exists(file_path):
            return None
        
        try:
            df = pd.read_csv(file_path, sep=sep, low_memory=False, encoding=encoding)
            logger.info(f"--- Dataset Summary: {os.path.basename(file_path)} ---")
            logger.info(f"Shape: {df.shape}")
            logger.info(f"Sample Data (First 3 rows): \n{df.head(3)}")
            return df
        except Exception as e:
            logger.error(f"Error loading dataset {file_path}: {e}")
            return None

def main():
    loader = DataDataLoader()
    
    # Focused datasets for Capstone: Movies (IMDb/MovieLens) and Music (Spotify)
    datasets = {
        "movielens_small": "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
        "spotify_sample": "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv",
        "imdb_sample": "https://raw.githubusercontent.com/sundeepblue/movie_rating_prediction/master/movie_metadata.csv"
    }
    
    # 1. MovieLens
    ml_zip = loader.download_file(datasets["movielens_small"], "ml-small.zip")
    if ml_zip:
        with zipfile.ZipFile(ml_zip, 'r') as zip_ref:
            zip_ref.extractall(loader.raw_data_path)
            logger.info("Extracted MovieLens files.")

    # 2. Spotify
    spotify_path = loader.download_file(datasets["spotify_sample"], "spotify_tracks.csv")
    loader.load_dataset(spotify_path)

    # 3. IMDb
    imdb_path = loader.download_file(datasets["imdb_sample"], "imdb_metadata.csv")
    loader.load_dataset(imdb_path)

    logger.info("Phase 2: Data Ingestion completed successfully.")

if __name__ == "__main__":
    main()