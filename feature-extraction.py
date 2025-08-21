import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env next to this script explicitly
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

client_id = os.getenv('SPOTIPY_CLIENT_ID') or os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET') or os.getenv('SPOTIFY_CLIENT_SECRET')
if not client_id or not client_secret:
	print("Missing Spotify credentials. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in .env")
	raise SystemExit(1)

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# genres from GTZAN
genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
data = []

# search for each genre
for genre in genres:
    print(f"collecting data for genre: {genre}")
    offset = 0
    limit = 50  # maximum limit in each request
    for _ in range(2):  # 2 requests = 100 songs for each genre
        results = sp.search(q=f'genre:{genre}', type='track', limit=limit, offset=offset)
        tracks = results['tracks']['items']
        for track in tracks:
            track_id = track['id']
            artist_id = track['artists'][0]['id']
            
            # audio features (call once and handle errors)
            try:
                features_list = sp.audio_features([track_id])
                audio_features = features_list[0] if features_list and features_list[0] else {}
            except spotipy.exceptions.SpotifyException as e:
                print(f"audio_features error {getattr(e, 'http_status', '?')}: {e}")
                # fallback: single-id endpoint
                try:
                    audio_features = sp._get(f"audio-features/{track_id}") or {}
                except spotipy.exceptions.SpotifyException as e2:
                    print(f"audio_features single error {getattr(e2, 'http_status', '?')}: {e2}")
                    continue

            # artist genres (safe fallback)
            try:
                artist = sp.artist(artist_id)
                artist_genres = ', '.join(artist.get('genres', [])) if artist.get('genres') else genre
            except spotipy.exceptions.SpotifyException as e:
                print(f"artist error {getattr(e, 'http_status', '?')}: {e}")
                artist_genres = genre
                
            row = {
                'track_name': track['name'],
                'artist_name': track['artists'][0]['name'],
                'genre': genre,  # main genre from GTZAN
                'spotify_genres': artist_genres,  # Spotify genres for augmentation
                'danceability': audio_features.get('danceability'),
                'energy': audio_features.get('energy'),
                'tempo': audio_features.get('tempo'),
                'loudness': audio_features.get('loudness'),
                'valence': audio_features.get('valence')
            }
            data.append(row)
        offset += limit
        time.sleep(1)  # prevent rate limit
    print(f"data for genre {genre} collected!")

# save to CSV
df_spotify = pd.DataFrame(data)
df_spotify.to_csv('data/spotify_data.csv', index=False)
print("Spotify data saved!")