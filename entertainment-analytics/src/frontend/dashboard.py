import streamlit as st
import requests
import json
import time

# ───────── PAGE CONFIG ─────────
st.set_page_config(
    page_title="EverythingMovies", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check for plotly to avoid crash
try:
    import plotly.express as px
except ImportError:
    px = None

# ───────── CSS (FIXED FOR BOTH LOGO & SIDEBAR VISIBILITY) ─────────
st.markdown("""
<style>
    /* Ensure the main container doesn't overlap the sidebar area */
    .main .block-container {
        max-width: 1200px;
        padding-top: 5rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    /* Custom Top Header Branding - Adjusted to stay on top but allow sidebar to slide under/beside */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background: #0e1117;
        z-index: 999999; /* Higher than sidebar toggle */
        display: flex;
        align-items: center;
        padding-left: 15px;
        border-bottom: 1px solid #333;
    }
    
    .logo-text {
        color: white;
        font-weight: 800;
        font-size: 1.4rem;
        margin-left: 45px; /* Leave room for the hamburger menu icon */
        letter-spacing: -0.5px;
    }

    /* Sidebar adjustment to not be hidden by our custom header */
    [data-testid="stSidebar"] {
        padding-top: 20px;
    }

    /* Cards Styling */
    .card {
        background: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 15px;
        height: 100%;
        transition: 0.3s;
    }
    
    .card:hover {
        border-color: #ff4b4b;
    }
    
    .tag {
        background: #ff4b4b;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    
    /* Hide the default Streamlit header to prevent double headers */
    header {visibility: hidden;}
</style>

<div class="custom-header">
    <span class="logo-text">🎬 EverythingMovies</span>
</div>
""", unsafe_allow_html=True)

# ───────── SIDEBAR ─────────
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True) # Space for the custom header
    st.title("Navigation")
    category = st.radio("Go to", [
        "Home",
        "Movie Picks",
        "Predictor",
        "Data Roadmap"
    ])
    
    st.divider()
    
    # API Status Check
    api_status = "🔴 Offline"
    try:
        check = requests.get("http://127.0.0.1:8000/", timeout=0.5)
        if check.status_code == 200:
            api_status = "🟢 Connected"
    except:
        pass
    st.info(f"API: {api_status}")

# ───────── API CONFIG ─────────
API_URL = "http://127.0.0.1:8000"

def get_recommendations(movie_title):
    try:
        clean_title = movie_title.strip().title()
        response = requests.get(f"{API_URL}/recommend/content/{clean_title}", timeout=5)
        return response.json().get("recommendations", []) if response.status_code == 200 else None
    except:
        return None

def predict_rating(u_id, m_id):
    try:
        response = requests.get(f"{API_URL}/predict/rating", params={"user_id": u_id, "movie_id": m_id}, timeout=5)
        return response.json().get("predicted_rating") if response.status_code == 200 else None
    except:
        return None

# ───────── PAGE CONTENT ─────────

if px is None:
    st.warning("Plotly is not installed. Visualizations may not load.")

if category == "Home":
    st.title("EverythingMovies")
    st.subheader("Platform Insights")
    
    cols = st.columns(4)
    platforms = [
        {"name": "IMDb Engine", "tags": "AI", "desc": "Content similarity algorithm."},
        {"name": "MovieLens", "tags": "DATA", "desc": "Collaborative filtering data."},
        {"name": "FastAPI", "tags": "API", "desc": "High-performance backend."},
        {"name": "Streamlit", "tags": "UI", "desc": "Analytics frontend."}
    ]
    
    for i, p in enumerate(platforms):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <div style="font-weight:bold; color:white;">{p['name']}</div>
                <div style="margin: 10px 0;"><span class="tag">{p['tags']}</span></div>
                <div style="color:#aaa; font-size:0.85rem;">{p['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

elif category == "Movie Picks":
    st.title("🎬 Discovery Engine")
    movie_input = st.text_input("Search Movie", placeholder="e.g. Toy Story")
    
    if st.button("Generate Picks"):
        if movie_input:
            with st.spinner("Finding matches..."):
                results = get_recommendations(movie_input)
                if results:
                    st.success(f"Top matches for {movie_input}:")
                    for movie in results:
                        st.write(f"- {movie}")
                else:
                    st.error("No results found. Is the FastAPI server running?")

elif category == "Predictor":
    st.title("⭐ Rating Forecaster")
    u_id = st.number_input("User ID", min_value=1, value=1)
    m_id = st.number_input("Movie ID", min_value=1, value=31)
    
    if st.button("Predict Score"):
        score = predict_rating(u_id, m_id)
        if score:
            st.metric("Estimated Rating", f"{score:.2f} / 5.0")
        else:
            st.error("API Error. Please check backend connection.")

elif category == "Data Roadmap":
    st.title("🗺️ Development Roadmap")
    st.write("Current Phase: **Phase 4 - Frontend & API Integration**")
    st.progress(65)
    st.markdown("""
    - [x] Data Ingestion
    - [x] Model Training (SVD & TF-IDF)
    - [x] API Setup (FastAPI)
    - [ ] Real-time Visualization (Plotly)
    - [ ] User Authentication
    """)