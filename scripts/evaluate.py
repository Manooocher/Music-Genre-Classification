import argparse
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def main():
	parser = argparse.ArgumentParser(description="Evaluate saved metrics and plot confusion matrix")
	parser.add_argument("--splits-dir", required=True)
	parser.add_argument("--model-metrics", required=True)
	parser.add_argument("--out-dir", required=True)
	parser.add_argument("--model-name", default="random_forest")
	args = parser.parse_args()

	splits_dir = Path(args.splits_dir)
	out_dir = Path(args.out_dir)
	out_dir.mkdir(parents=True, exist_ok=True)

	with open(args.model_metrics, "r", encoding="utf-8") as f:
		metrics = json.load(f)
	print("best model:", args.model_name, metrics.get(args.model_name, {}).get("accuracy"))

	# For confusion matrix, reload test split and run a quick prediction if model exists
	# (kept minimal: users can extend to load model and predict again)
	print("Confusion matrix plotting skipped (model reload not implemented in this script).")
	with open(out_dir / "summary.txt", "w", encoding="utf-8") as f:
		json.dump(metrics, f, indent=2)
	print("saved evaluation summary ->", out_dir)


if __name__ == "__main__":
	main()


