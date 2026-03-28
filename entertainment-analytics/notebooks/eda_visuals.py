import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def run_analysis():
    print("🚀 Starting Exploratory Data Analysis...")
    
    # Paths to your data (adjusted for running from the root folder)
    spotify_path = 'data/raw/spotify_tracks.csv'
    imdb_path = 'data/raw/imdb_metadata.csv'
    ratings_path = 'data/raw/ml-latest-small/ratings.csv'

    # 1. Load Datasets
    try:
        spotify_df = pd.read_csv(spotify_path)
        imdb_df = pd.read_csv(imdb_path)
        ratings_df = pd.read_csv(ratings_path)
        print("✅ All datasets loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return

    # 2. MovieLens: Rating Distribution
    print("📊 Generating MovieLens Rating Distribution...")
    plt.figure()
    sns.countplot(x='rating', data=ratings_df, palette='viridis')
    plt.title('Distribution of MovieLens Ratings')
    plt.xlabel('Rating (0.5 - 5.0)')
    plt.ylabel('Count')
    plt.savefig('outputs/movielens_ratings.png')
    print("Saved: outputs/movielens_ratings.png")

    # 3. Spotify: Popularity vs. Danceability
    print("📊 Generating Spotify Danceability Chart...")
    plt.figure()
    sns.scatterplot(x='danceability', y='track_popularity', data=spotify_df, alpha=0.3, color='green')
    plt.title('Spotify: Danceability vs Popularity')
    plt.savefig('outputs/spotify_popularity.png')
    print("Saved: outputs/spotify_popularity.png")

    # 4. IMDb: Top 10 Genres
    print("📊 Generating IMDb Genre Chart...")
    plt.figure()
    top_genres = imdb_df.groupby('genres')['imdb_score'].mean().sort_values(ascending=False).head(10)
    top_genres.plot(kind='barh', color='skyblue')
    plt.title('Top 10 Movie Genre Combinations by IMDb Score')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('outputs/imdb_top_genres.png')
    print("Saved: outputs/imdb_top_genres.png")
    
    print("\n🎉 Phase 3 Complete! Check your 'outputs' folder for the graphs.")

if __name__ == "__main__":
    run_analysis()