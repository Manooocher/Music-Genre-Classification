import argparse
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from joblib import dump


def build_pipelines():
	rf = Pipeline([
		("scaler", StandardScaler(with_mean=False)),
		("clf", RandomForestClassifier(n_estimators=300, random_state=42))
	])
	svm = Pipeline([
		("scaler", StandardScaler()),
		("clf", SVC(kernel="rbf", C=10, gamma="scale", probability=True, random_state=42))
	])
	return {"random_forest": rf, "svm_rbf": svm}


def load_split(csv_path: Path):
	df = pd.read_csv(csv_path)
	y = df["genre"].astype(str)
	X = df.drop(columns=["genre", "filepath"], errors="ignore").replace([np.inf, -np.inf], 0).fillna(0)
	return X, y


def main():
	parser = argparse.ArgumentParser(description="Train baseline classifiers on GTZAN features")
	parser.add_argument("--splits-dir", required=True)
	parser.add_argument("--out-dir", required=True)
	args = parser.parse_args()

	splits_dir = Path(args.splits_dir)
	out_dir = Path(args.out_dir)
	out_dir.mkdir(parents=True, exist_ok=True)

	X_train, y_train = load_split(splits_dir / "train.csv")
	X_val, y_val = load_split(splits_dir / "val.csv")
	X_test, y_test = load_split(splits_dir / "test.csv")

	models = build_pipelines()
	metrics = {}
	for name, model in models.items():
		model.fit(pd.concat([X_train, X_val]), pd.concat([y_train, y_val]))
		pred = model.predict(X_test)
		acc = accuracy_score(y_test, pred)
		report = classification_report(y_test, pred, output_dict=True)
		metrics[name] = {"accuracy": acc, "report": report}
		dump(model, out_dir / f"{name}.joblib")
		print(f"{name}: acc={acc:.3f}")

	with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
		json.dump(metrics, f, indent=2)
	print("saved models and metrics ->", out_dir)


if __name__ == "__main__":
	main()


