import kaggle
import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests import Session

# Custom session with retries
session = Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504, 10054])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Authenticate with custom session
api = KaggleApi()
api._session = session  # Override the session
api.authenticate()

# Download
dataset = 'andradaolteanu/gtzan-dataset-music-genre-classification'
path = 'data/gtzan'
os.makedirs(path, exist_ok=True)
api.dataset_download_files(dataset, path=path, unzip=False)

# Unzip
zip_path = os.path.join(path, 'gtzan-dataset-music-genre-classification.zip')
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(path)
os.remove(zip_path)

print("GTZAN downloaded and unzipped!")