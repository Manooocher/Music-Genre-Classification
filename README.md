# Automated ML Pipeline for GTZAN (Local Only)

This project builds a local, offline-friendly pipeline for music genre classification using the GTZAN dataset. It avoids external APIs (e.g., Spotify) and extracts audio features locally with `librosa`, trains classical ML baselines, and offers optional UI and orchestration stubs.

## Quickstart

1) Create and activate virtual environment (Windows PowerShell):
```powershell
python -m venv ML_Pipeline
./ML_Pipeline/Scripts/Activate.ps1
```

2) Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

3) Project layout:
```
Automated-ML-Pipeline/
  data/genres/<genre>/*.au
  scripts/
    extract_features.py
    split_dataset.py
    train_models.py
    evaluate.py
    run_pipeline.py
```

4) Run end-to-end:
```powershell
python scripts/run_pipeline.py --data-root data/genres --out-dir artifacts
```

## Notes
- Uses only local GTZAN files; no internet APIs required.
- Feature set: MFCCs, spectral centroid, bandwidth, rolloff, chroma, zero-cross.
- Baselines: RandomForest, SVM; saved under `artifacts/`.
- Optional: Streamlit app (not required for CLI pipeline).
