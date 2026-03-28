🎬 Entertainment & Media Analytics Platform📖 OverviewAn end-to-end Machine Learning web platform that ingests raw entertainment data (MovieLens, IMDb, Spotify, YouTube), cleans it, trains multiple predictive models, and serves interactive visualizations and forecasts via a robust API and frontend dashboard.🎯 ObjectivesData Engineering: Automated ingestion and preprocessing of disparate media datasets.Machine Learning: Collaborative filtering, content-based recommendations, sentiment analysis, and churn prediction.Time-Series Forecasting: Predicting future platform growth and content trends.Full-Stack Deployment: Serving models via FastAPI and providing user interactivity through a dashboard.🏗️ Architecturegraph TD
    A[Raw Datasets <br/> IMDb, Spotify, Kaggle] -->|Ingestion| B(Data Loaders)
    B --> C{Preprocessing Pipeline}
    C -->|Clean Data| D[(Processed Data)]
    D --> E[EDA & Analysis]
    D --> F[Model Training <br/> RecSys, Sentiment, XGBoost]
    F --> G[(Saved Models)]
    G --> H[FastAPI Backend]
    D --> H
    H --> I[Frontend Dashboard <br/> React / Streamlit]
    H --> J[Future Forecasting <br/> Prophet / ARIMA]

##  Dataset Sources
- MovieLens 25M
- TMDb Metadata
- IMDB Reviews Dataset
- Spotify Tracks Dataset

## Features Implemented
- Multi-source data integration
- Fuzzy matching for sentiment mapping
- Aggregated rating analytics
- Unified content schema
- SQLite database for querying
🚀 Setup Instructions

1. Local Development

# Clone the repository
git clone [https://github.com/AnshWadhwani05/entertainment-analytics.git](https://github.com/AnshWadhwani05/entertainment-analytics.git)
cd entertainment-analytics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API locally
uvicorn src.api.main:app --reload


2. Run with Docker

docker-compose up --build


🗺️ Roadmap

[ ] Phase 1: Project Scaffolding
[ ] Phase 2: Data Ingestion & Schema Validation
[ ] Phase 3: Exploratory Data Analysis (EDA)
[ ] Phase 4: Feature Engineering & Preprocessing
[ ] Phase 5: ML Model Development (6 Models)
[ ] Phase 6: Forecasting & Time Series
[ ] Phase 7: API Development
[ ] Phase 8: Frontend Dashboard

📸 Screenshots

(Placeholders for future dashboard screenshots)

Dashboard Overview: ![Overview](outputs/eda/placeholder.png)

Recommendation Engine: ![RecSys](outputs/eda/placeholder.png)

Built as a Final Year Capstone Project.