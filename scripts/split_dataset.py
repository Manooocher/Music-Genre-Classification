import argparse
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


def main():
	parser = argparse.ArgumentParser(description="Split dataset CSV into train/val/test")
	parser.add_argument("--features-csv", required=True)
	parser.add_argument("--out-dir", required=True)
	parser.add_argument("--train", type=float, default=0.7)
	parser.add_argument("--val", type=float, default=0.15)
	args = parser.parse_args()

	df = pd.read_csv(args.features_csv)
	X = df.drop(columns=["genre"]) if "genre" in df.columns else df.copy()
	y = df["genre"] if "genre" in df.columns else None

	train_size = args.train
	val_size = args.val
	test_size = 1.0 - train_size - val_size

	X_temp, X_test, y_temp, y_test = train_test_split(
		X, y, test_size=test_size, stratify=y, random_state=42
	)
	val_fraction = val_size / (train_size + val_size)
	X_train, X_val, y_train, y_val = train_test_split(
		X_temp, y_temp, test_size=val_fraction, stratify=y_temp, random_state=42
	)

	out_dir = Path(args.out_dir)
	out_dir.mkdir(parents=True, exist_ok=True)

	pd.concat([X_train, y_train], axis=1).to_csv(out_dir / "train.csv", index=False)
	pd.concat([X_val, y_val], axis=1).to_csv(out_dir / "val.csv", index=False)
	pd.concat([X_test, y_test], axis=1).to_csv(out_dir / "test.csv", index=False)

	print("saved splits ->", out_dir)


if __name__ == "__main__":
	main()


