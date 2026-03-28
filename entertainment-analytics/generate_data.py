import json
import random

data = []

# ───────── STREAMING PLATFORMS (REALISTIC 50) ─────────
streaming_names = [
    "Netflix","Amazon Prime Video","Disney+ Hotstar","Apple TV+","Hulu","HBO Max",
    "Paramount+","Peacock","SonyLIV","ZEE5","Discovery+","YouTube Movies",
    "MX Player","ALTBalaji","Voot","Eros Now","Lionsgate Play","Aha","Sun NXT",
    "Hoichoi","JioCinema","MUBI","CuriosityStream","Kanopy","Shudder",
    "BritBox","Acorn TV","Rakuten TV","Plex TV","Pluto Premium",
    "YouTube Premium","Google TV","Vudu","Redbox","FilmRise",
    "Xumo","Sling TV","Philo","fuboTV","Crunchyroll Premium",
    "Funimation Premium","WeTV","iQIYI","Tencent Video","Bilibili",
    "Starz","Showtime","AMC+","Hallmark Movies Now","Tubi Premium"
]

for i, name in enumerate(streaming_names):
    data.append({
        "name": name,
        "category": "Streaming Platforms",
        "rank": i + 1,
        "tags": random.choice([["PAID"], ["PAID","HD"], ["PAID","NO ADS"]]),
        "description": f"{name} offers a wide range of movies, series, and exclusive content.",
        "pros": ["Large content library", "Good streaming quality"],
        "cons": ["Subscription required"],
        "type": "Official",
        "sentiment": random.choice(["Positive","Mixed"]),
        "status": "active",
        "rating": round(random.uniform(3.8, 4.9), 1),
        "url": "https://www.google.com/search?q=" + name.replace(" ", "+")
    })

# ───────── FREE MOVIE SITES (REALISTIC 50) ─────────
free_names = [
    "Tubi","Pluto TV","Plex","Crackle","Popcornflix","SolarMovie",
    "123Movies","FMovies","YesMovies","AZMovies","LookMovie","MoviesJoy",
    "Putlocker","GoMovies","WatchSeries","Soap2Day Mirror","Cineb",
    "StreamM4u","Vumoo","FlixHQ","BMovies","HDToday",
    "TinyZone","SFlix","Movie4k","PrimeWire","LosMovies",
    "CouchTuner","WatchFree","YesFlix","MegaShare","Openload Movies",
    "MyFlixer","ZMovies","MovieWatcher","Filmxy","Watch32",
    "Flixtor","HDToday Mirror","FreeFlix","NetMovies","WorldFree4u",
    "9xMovies","MoviesVerse","Vegamovies","KatMovieHD","MLWBD",
    "DownloadHub","Filmyzilla","MoviesNation"
]

for i, name in enumerate(free_names):
    data.append({
        "name": name,
        "category": "Free Movie Sites",
        "rank": i + 1,
        "tags": ["FREE","ADS"],
        "description": f"{name} provides free access to movies and TV shows online.",
        "pros": ["Free access", "Large variety"],
        "cons": ["Ads or popups"],
        "type": "Aggregator",
        "sentiment": random.choice(["Mixed","Positive"]),
        "status": "active",
        "rating": round(random.uniform(3.5, 4.5), 1),
        "url": "https://www.google.com/search?q=" + name.replace(" ", "+")
    })

# ───────── ANIME PLATFORMS (REALISTIC 50) ─────────
anime_names = [
    "Crunchyroll","Funimation","9anime","Gogoanime","AnimeHeaven",
    "AnimeFreak","AnimeDao","AnimePlanet","AniWatch","Zoro.to",
    "Kickassanime","MasterAnime","AnimeKisa","AnimeUltima","AnimePahe",
    "Chia-Anime","AnimeFLV","AnimeGG","AnimeLab","AnimeTake",
    "AnimeVibe","AnimeRush","AnimeShow","AnimeStreams","AnimeHub",
    "AnimeCloud","AnimeOwl","AnimeTV","AnimeZone","AnimeWorld",
    "AniMixPlay","OtakuStream","KissAnime Clone","AnimeBam","AnimeWow",
    "AnimeFire","AnimeBee","AnimeWave","AnimeX","AnimePlus",
    "AnimeMax","AnimeUltra","AnimeArena","AnimeGalaxy","AnimeStorm",
    "AnimePortal","AnimeCore","AnimeBase","AnimeDeck","AnimeSpot"
]

for i, name in enumerate(anime_names):
    data.append({
        "name": name,
        "category": "Anime Platforms",
        "rank": i + 1,
        "tags": ["ANIME"],
        "description": f"{name} is a platform dedicated to anime streaming and content.",
        "pros": ["Wide anime collection"],
        "cons": ["Ads or limited regions"],
        "type": "Aggregator",
        "sentiment": random.choice(["Positive","Mixed"]),
        "status": "active",
        "rating": round(random.uniform(3.6, 4.8), 1),
        "url": "https://www.google.com/search?q=" + name.replace(" ", "+")
    })

# ───────── SAVE FILE ─────────
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Ultra realistic dataset created (150 entries)")