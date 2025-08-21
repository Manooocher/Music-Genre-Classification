import argparse
from pathlib import Path
import subprocess
import sys


def run(cmd: list[str]):
	print("$", " ".join(cmd))
	res = subprocess.run(cmd, check=True)
	return res.returncode


def main():
	parser = argparse.ArgumentParser(description="Run local GTZAN pipeline end-to-end")
	parser.add_argument("--data-root", required=True)
	parser.add_argument("--out-dir", required=True)
	args = parser.parse_args()

	root = Path(args.data_root)
	art = Path(args.out_dir)
	art.mkdir(parents=True, exist_ok=True)

	features_csv = art / "features.csv"
	splits_dir = art / "splits"
	models_dir = art / "models"
	models_dir.mkdir(exist_ok=True)

	run([sys.executable, "scripts/extract_features.py", "--data-root", str(root), "--out-csv", str(features_csv)])
	run([sys.executable, "scripts/split_dataset.py", "--features-csv", str(features_csv), "--out-dir", str(splits_dir)])
	run([sys.executable, "scripts/train_models.py", "--splits-dir", str(splits_dir), "--out-dir", str(models_dir)])
	run([sys.executable, "scripts/evaluate.py", "--splits-dir", str(splits_dir), "--model-metrics", str(models_dir / "metrics.json"), "--out-dir", str(art)]))


if __name__ == "__main__":
	main()


