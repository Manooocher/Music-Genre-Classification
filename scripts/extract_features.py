import argparse
import os
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import librosa


def extract_features_from_file(audio_path: Path, sr: int = 22050) -> Dict[str, Any]:

	# Load audio (librosa supports .au via audioread)
	y, sr = librosa.load(str(audio_path), sr=sr, mono=True)

	# Frame-level features
	mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
	chroma = librosa.feature.chroma_stft(y=y, sr=sr)
	spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
	spec_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
	spec_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
	zcr = librosa.feature.zero_crossing_rate(y=y)

	def stats(name: str, arr: np.ndarray) -> Dict[str, float]:
		arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
		return {
			f"{name}_mean": float(np.mean(arr)),
			f"{name}_std": float(np.std(arr)),
			f"{name}_min": float(np.min(arr)),
			f"{name}_max": float(np.max(arr)),
		}

	features = {}
	features.update(stats("mfcc", mfcc))
	# Also add per-coefficient means for first 13 MFCCs
	for i in range(min(13, mfcc.shape[0])):
		features[f"mfcc{i+1}_mean"] = float(np.mean(mfcc[i]))

	features.update(stats("chroma", chroma))
	features.update(stats("spec_centroid", spec_centroid))
	features.update(stats("spec_bandwidth", spec_bandwidth))
	features.update(stats("spec_rolloff", spec_rolloff))
	features.update(stats("zcr", zcr))

	return features


def walk_dataset(data_root: Path) -> List[Path]:
	return [p for p in data_root.rglob('*.au')]


def main():
	parser = argparse.ArgumentParser(description="Extract audio features locally from GTZAN .au files")
	parser.add_argument("--data-root", type=str, required=True, help="Root folder containing genre subfolders with .au files")
	parser.add_argument("--out-csv", type=str, required=True, help="Output CSV path")
	parser.add_argument("--sr", type=int, default=22050)
	args = parser.parse_args()

	data_root = Path(args.data_root)
	all_files = walk_dataset(data_root)
	rows = []
	for audio_path in all_files:
		genre = audio_path.parent.name
		try:
			features = extract_features_from_file(audio_path, sr=args.sr)
			features.update({
				"filepath": str(audio_path),
				"genre": genre,
			})
			rows.append(features)
		except Exception as e:
			print(f"skip {audio_path}: {e}")

	df = pd.DataFrame(rows)
	df.to_csv(args.out_csv, index=False)
	print(f"saved features -> {args.out_csv} ({len(df)} rows)")


if __name__ == "__main__":
	main()


