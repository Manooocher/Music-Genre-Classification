import streamlit as st
import pandas as pd
import numpy as np
import librosa
from pathlib import Path
from joblib import load
from prompt_explanations import explain_prediction


st.set_page_config(page_title="GTZAN Genre Classifier", layout="centered")
st.title("GTZAN Genre Classifier (Local)")

model_path = st.text_input("Path to model .joblib", "artifacts/models/random_forest.joblib")

uploaded = st.file_uploader("Upload audio file (.wav/.au)", type=["wav", "au"])

if uploaded and model_path:
	with st.spinner("Loading model and extracting features..."):
		model = load(model_path)
		# Save upload to temp file
		tmp = Path("_tmp_upload")
		tmp.write_bytes(uploaded.getbuffer())
		y, sr = librosa.load(str(tmp), sr=22050, mono=True)
		mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
		chroma = librosa.feature.chroma_stft(y=y, sr=sr)
		spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
		spec_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
		spec_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
		zcr = librosa.feature.zero_crossing_rate(y=y)

		feat = {}
		feat["mfcc_mean"] = float(np.mean(mfcc))
		for i in range(min(13, mfcc.shape[0])):
			feat[f"mfcc{i+1}_mean"] = float(np.mean(mfcc[i]))
		feat["chroma_mean"] = float(np.mean(chroma))
		feat["spec_centroid_mean"] = float(np.mean(spec_centroid))
		feat["spec_bandwidth_mean"] = float(np.mean(spec_bandwidth))
		feat["spec_rolloff_mean"] = float(np.mean(spec_rolloff))
		feat["zcr_mean"] = float(np.mean(zcr))

		X = pd.DataFrame([feat])
		pred = model.predict(X)[0]
		st.success(f"Predicted genre: {pred}")
		st.info(explain_prediction(feat, str(pred)))


