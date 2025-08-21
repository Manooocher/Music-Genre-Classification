import os
import json
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    print("Missing SPOTIPY_CLIENT_ID/SECRET in .env")
    raise SystemExit(1)

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
token = auth_manager.get_access_token()
if isinstance(token, dict):
    token = token.get("access_token")

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "SpotifyAPI-Test/1.0 (+https://developer.spotify.com)",
}

# Optional proxies from environment
proxies = {}
http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
if http_proxy:
    proxies["http"] = http_proxy
if https_proxy:
    proxies["https"] = https_proxy
if not proxies:
    proxies = None

def short(text: str, n: int = 300) -> str:
    try:
        return text if len(text) <= n else text[:n] + "..."
    except Exception:
        return str(text)[:n]

def call(name: str, method: str, url: str, params: dict | None = None):
    full_url = url if not params else url + ("?" + urlencode(params))
    try:
        resp = requests.request(method, full_url, headers=headers, proxies=proxies, timeout=20)
        print(f"{name} -> {resp.status_code}")
        ct = resp.headers.get("content-type", "")
        body = resp.text
        if "application/json" in ct:
            try:
                body = json.dumps(resp.json(), ensure_ascii=False)
            except Exception:
                pass
        print(short(body))
    except requests.RequestException as e:
        print(f"{name} error: {e}")

# Show external IP to ensure Python is routed via VPN
try:
    ip_resp = requests.get("https://api.ipify.org?format=json", timeout=10, proxies=proxies)
    print("public_ip:", ip_resp.text)
except Exception as e:
    print("public_ip error:", e)

track_id = "2Fxmhks0bxGSBdJ92vM42m"  # Bad Guy
call("audio-features (single)", "GET", f"https://api.spotify.com/v1/audio-features/{track_id}")
call("audio-features (batch)", "GET", "https://api.spotify.com/v1/audio-features", {"ids": track_id})
call("audio-analysis", "GET", f"https://api.spotify.com/v1/audio-analysis/{track_id}")
call("track (single)", "GET", f"https://api.spotify.com/v1/tracks/{track_id}")
call("search (track)", "GET", "https://api.spotify.com/v1/search", {"q": "track:bad guy artist:billie eilish", "type": "track", "limit": 1})


