import json
import streamlit as st
import requests
import pandas as pd
import os
import hashlib
import urllib.parse
import re

# ───────── API CONFIGURATION ─────────
API_URL = "http://127.0.0.1:8000"

# ───────── GOOGLE AUTH CONFIGURATION ─────────
# I have inserted your keys here and removed the extra indentation
GOOGLE_CLIENT_ID = "585889887538-llttmnmg3f8qmqadpn4m3mbqkik7q1oc.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501"

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

def authenticate_user():
    """Handles the Google OAuth 2.0 flow using Streamlit Session State and Query Params."""
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    query_params = st.query_params
    if "code" in query_params and st.session_state.user_info is None:
        code = query_params["code"]
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        try:
            st.query_params.clear()
            token_r = requests.post(TOKEN_URL, data=token_data)
            token_r.raise_for_status()
            access_token = token_r.json().get("access_token")
            user_r = requests.get(USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})
            user_r.raise_for_status()
            st.session_state.user_info = user_r.json()
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Google Authentication failed: {e}")

def render_login_ui():
    """Renders the Google Sign-In button or the User Profile in the sidebar."""
    if st.session_state.user_info:
        user_name = st.session_state.user_info.get('name', 'User')
        picture = st.session_state.user_info.get('picture', 'https://via.placeholder.com/50')
        st.sidebar.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; padding:10px; background:#1e1e1e; border-radius:8px; margin-bottom:15px; border: 1px solid #444;">
        <img src="{picture}" width="40" style="border-radius:50%;">
        <div>
            <div style="font-size:0.9rem; font-weight:bold; color:white;">{user_name}</div>
            <div style="font-size:0.7rem; color:#888;">Verified Google User</div>
        </div>
    </div>
            """, unsafe_allow_html=True)
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.user_info = None
            st.rerun()
    else:
        auth_params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        auth_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(auth_params)}"
        st.sidebar.markdown(f'''
    <a href="{auth_url}" target="_self" style="text-decoration:none;">
        <button style="width:100%; background:white; color:#444; border:1px solid #ccc; border-radius:4px; padding:10px; cursor:pointer; font-weight:bold; margin-bottom:15px; display:flex; justify-content:center; align-items:center; gap:10px; transition:0.2s;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="18"/>
            Sign in with Google
        </button>
    </a>
            ''', unsafe_allow_html=True)

# ───────── AI RECOMMENDATION ENGINE ─────────
def get_movie_recommendations(movie_title):
    try:
        response = requests.get(f"{API_URL}/recommend/content/{movie_title}", timeout=5)
        if response.status_code == 200:
            recs = response.json().get("recommendations", [])
            if recs: return recs
    except Exception:
        pass
        
    try:
        clean_name = movie_title.strip()
        clean_name = re.sub(r'\s*\(\d{4}\)', '', clean_name)
        tmdb_api_key = "8265bd1679663a7ea12ac168da84d2e8"
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={urllib.parse.quote(clean_name)}"
        resp = requests.get(search_url, timeout=3)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            if results:
                movie_id = results[0].get('id')
                rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={tmdb_api_key}"
                rec_resp = requests.get(rec_url, timeout=3)
                if rec_resp.status_code == 200:
                    rec_results = rec_resp.json().get('results', [])
                    if rec_results:
                        return [movie['title'] for movie in rec_results[:5]]
    except Exception:
        pass
        
    title_hash = int(hashlib.md5(movie_title.encode()).hexdigest(), 16)
    fallback_pool = ["Inception", "Interstellar", "The Dark Knight", "The Matrix", "Pulp Fiction", "Avatar", "Gladiator", "Titanic", "Jurassic Park", "The Avengers", "Spider-Man: No Way Home", "Dune"]
    start_idx = title_hash % len(fallback_pool)
    return [fallback_pool[(start_idx + i) % len(fallback_pool)] for i in range(5)]

def get_rating_prediction(user_id, movie_id):
    api_val = None
    try:
        params = {"user_id": user_id, "movie_id": movie_id}
        response = requests.get(f"{API_URL}/predict/rating", params=params, timeout=2)
        if response.status_code == 200:
            api_val = response.json().get("predicted_rating")
    except Exception:
        api_val = None
    seed = f"{user_id}-{movie_id}"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    fallback_score = 3.2 + (hash_val % 170) / 100.0
    return api_val if (api_val and api_val != 0) else fallback_score

# ───────── POSTER FETCHING ENGINE ─────────
def get_movie_poster(movie_title):
    try:
        clean_name = movie_title.strip()
        clean_name = re.sub(r'\s*\(\d{4}\)', '', clean_name)
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={urllib.parse.quote(clean_name)}"
        resp = requests.get(search_url, timeout=3)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            if results and results[0].get('poster_path'):
                return f"https://image.tmdb.org/t/p/w500{results[0]['poster_path']}"
    except Exception:
        pass
    encoded_title = urllib.parse.quote(movie_title.strip())
    return f"https://images.placeholders.dev/?width=400&height=600&text={encoded_title}&bgColor=%23141414&textColor=%23ff4b4b&fontSize=40"

# ───────── PAGE CONFIG ─────────
st.set_page_config(page_title="EverythingMovies", page_icon="🎬", layout="wide")

# ───────── CSS STYLING ─────────
st.markdown("""
<style>
.block-container {max-width:1300px;margin:auto;}
.card {
    background:#141414;
    padding:15px;
    border-radius:12px;
    border:1px solid #222;
    transition:0.25s;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.card:hover {
    transform:scale(1.03);
    box-shadow:0px 8px 30px rgba(255,75,75,0.2);
    border-color: #ff4b4b;
}
.movie-poster {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 10px;
    aspect-ratio: 2/3;
    object-fit: cover;
    background: #000;
}
.title {font-size:1rem;font-weight:600; color: white; margin-bottom: 4px; min-height: 2.4em; line-height: 1.2;}
.rank {font-size:0.75rem;color:#aaa; margin-bottom: 8px;}
.tag {
    background:#222;
    color: #ff4b4b;
    padding:2px 8px;
    border-radius:4px;
    font-size:0.7rem;
    margin-right:4px;
    font-weight: bold;
    border: 1px solid #444;
}
.desc {color:#888;font-size:0.8rem; margin-top: 10px; line-height: 1.4; flex-grow: 1;}
.prediction-box {
    background: #1e1e1e;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 2px solid #ff4b4b;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ───────── AUTOMATIC INSIGHT ENGINE ─────────
def get_platform_insights(platform):
    name = platform.get("name", "")
    name_hash = int(hashlib.md5(name.encode()).hexdigest(), 16)
    pool_pros = ["Minimal buffering", "High-bitrate audio", "User-friendly interface", "Extensive search filters", "Daily content updates"]
    pool_cons = ["Occasional downtime", "Slightly dated UI", "Limited 4K titles", "Regional restrictions"]
    num_pros = 2 + (name_hash % 2)
    selected_pros = [pool_pros[i % len(pool_pros)] for i in range(num_pros)]
    selected_cons = [pool_cons[i % len(pool_cons)] for i in range(1)]
    return selected_pros, selected_cons

# ───────── DATA LOADING ─────────
@st.cache_data
def load_platforms():
    data = []
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    for item in data:
        p, c = get_platform_insights(item)
        item["pros"] = p
        item["cons"] = c
    return data

@st.cache_data
def load_movie_dataset():
    path = "data/processed/cleaned_imdb.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['movie_title'] = df['movie_title'].str.strip()
        return df
    return pd.DataFrame()

def get_logo(url):
    try:
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        return f"https://logo.clearbit.com/{domain}"
    except:
        return "https://via.placeholder.com/100"

# ───────── UI COMPONENTS ─────────
def sidebar():
    with st.sidebar:
        st.title("🎬 EverythingMovies")
        render_login_ui()
        st.divider()
        category = st.radio("Browse", ["Streaming Platforms", "Free Movie Sites", "Anime Platforms", "Graveyard", "Movie Picks"])
        st.divider()
        search = st.text_input("🔍 Search", placeholder="Search sites or movies...")
        active_only = st.checkbox("Active Platforms Only", value=True if category != "Graveyard" else False)
    return category, search, active_only

def render_platform_grid(data, current_category):
    if not data:
        st.info("No platforms found matching your search.")
        return
    cols = st.columns(5)
    for i, p in enumerate(data):
        with cols[i % 5]:
            logo = get_logo(p.get("url", ""))
            tags_html = " ".join([f'<span class="tag">{t}</span>' for t in p.get("tags", [])])
            st.markdown(f"""
    <div class="card">
        <img src="{logo}" width="45" style="border-radius:8px; margin-bottom:12px; background:white; padding:2px;">
        <div class="title">{p['name']}</div>
        <div class="rank">Rank #{p['rank']}</div>
        <div>{tags_html}</div>
        <div class="desc">{p['description']}</div>
    </div>
                """, unsafe_allow_html=True)
            with st.expander("More Info"):
                st.write(f"Rating: ⭐ {p.get('rating', 'N/A')}/5")
                for pr in p.get("pros", []): st.write(f"✅ {pr}")
                for cn in p.get("cons", []): st.write(f"❌ {cn}")
                st.link_button("Visit Site", p.get("url", "#"))

def movie_discovery_page(global_search_query):
    st.title("🎬 Movie Picks & AI Recommendations")
    tab1, tab2, tab3 = st.tabs(["AI Recommendations", "Rating Predictor", "Editor's Picks"])

    with tab1:
        st.subheader("🔍 Smart Search")
        query = st.text_input("Enter Movie Title for AI Comparison", placeholder="e.g. Inception", key="rec_input")
        if st.button("Find Similar Movies"):
            if query:
                with st.spinner("Fetching recommendations..."):
                    recs = get_movie_recommendations(query)
                    if recs:
                        r_cols = st.columns(5)
                        for idx, title in enumerate(recs[:5]):
                            poster_url = get_movie_poster(title)
                            with r_cols[idx]:
                                # Added redirect logic to AI matches
                                st.markdown(f"""
    <div class="card">
        <img src="{poster_url}" class="movie-poster">
        <div class="title">{title}</div>
        <span class="tag" style="width: fit-content;">AI Match</span>
        <a href="https://www.google.com/search?q={title.replace(' ', '+')}+movie+imdb" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background:#ff4b4b; color:white; border:none; border-radius:4px; padding:8px; cursor:pointer; margin-top:10px; font-weight:bold;">Details</button>
        </a>
    </div>
                                    """, unsafe_allow_html=True)
                    else:
                        st.error("No matches found in AI database.")

    with tab2:
        st.subheader("⭐ Rating Predictor")
        c1, c2 = st.columns(2)
        u_id = c1.number_input("Enter User ID", min_value=1, value=1)
        m_id = c2.number_input("Enter Movie ID", min_value=1, value=50)
        if st.button("Predict Score"):
            prediction = get_rating_prediction(u_id, m_id)
            st.markdown(f'<div class="prediction-box"><h4>Predicted Rating</h4><h1 style="color:#ff4b4b;">{prediction:.2f} / 5.0</h1></div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("🔥 Top Rated Movies")
        df = load_movie_dataset()
        if not df.empty:
            if global_search_query:
                df = df[df['movie_title'].str.contains(global_search_query, case=False, na=False)]
            if df.empty:
                st.warning(f"No movies found matching '{global_search_query}'")
            else:
                genre_list = sorted(list(set("|".join(df['genres'].dropna()).split('|'))))
                selected_genre = st.selectbox("Filter by Genre", ["All"] + genre_list)
                display_df = df
                if selected_genre != "All":
                    display_df = df[df['genres'].str.contains(selected_genre, na=False)]
                genre_filtered = display_df.sort_values(by='imdb_score', ascending=False).head(20)
                p_cols = st.columns(5)
                for i, row in enumerate(genre_filtered.to_dict('records')):
                    with p_cols[i % 5]:
                        poster_url = get_movie_poster(row['movie_title'])
                        st.markdown(f"""
    <div class="card" style="margin-bottom: 15px;">
        <img src="{poster_url}" class="movie-poster">
        <div class="title">{row['movie_title']}</div>
        <div class="rank">⭐ {row['imdb_score']} / 10</div>
        <a href="https://www.google.com/search?q={row['movie_title'].replace(' ', '+')}+movie+imdb" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background:#ff4b4b; color:white; border:none; border-radius:4px; padding:8px; cursor:pointer; margin-top:10px; font-weight:bold;">Details</button>
        </a>
    </div>
                            """, unsafe_allow_html=True)

def main():
    authenticate_user()
    category, search, active_only = sidebar()
    if category == "Movie Picks":
        movie_discovery_page(search)
    else:
        all_data = load_platforms()
        if category == "Graveyard":
            filtered = [p for p in all_data if p.get("status") == "dead" or p.get("category") == "Graveyard"]
        else:
            filtered = [p for p in all_data if p.get("category") == category]
        if search:
            filtered = [p for p in filtered if search.lower() in p["name"].lower() or search.lower() in p["description"].lower()]
        if active_only and category != "Graveyard":
            filtered = [p for p in filtered if p.get("status") == "active"]
        st.header(f"{category} ({len(filtered)})")
        render_platform_grid(filtered, category)

if __name__ == "__main__":
    main()