import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
print("spotipy", spotipy.__version__)
tid = sp.search(q="track:bad guy artist:billie eilish", type="track", limit=1)["tracks"]["items"][0]["id"]
try:
    features = sp.audio_features([tid])
    print(features)
except SpotifyException as e:
    print(f"batch audio_features error {getattr(e, 'http_status', '?')}: {e}")
    try:
        single = sp._get(f"audio-features/{tid}")
        print([single])
    except SpotifyException as e2:
        print(f"single audio_features error {getattr(e2, 'http_status', '?')}: {e2}")