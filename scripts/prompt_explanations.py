"""
Offline-safe stub for prompt-based explanations.
This module simulates an LLM by using deterministic templates.
Replace with a real local LLM (e.g., llama.cpp or transformers) if available.
"""

from typing import Dict, Any


def explain_prediction(features: Dict[str, Any], predicted_genre: str) -> str:
	energy = float(features.get("spec_centroid_mean", 0))
	zcr = float(features.get("zcr_mean", 0))
	mfcc1 = float(features.get("mfcc1_mean", 0))

	clauses = []
	if energy > 2000:
		clauses.append("high spectral centroid suggests brighter/energetic timbre")
	if zcr > 0.05:
		clauses.append("higher zero-crossing rate indicates noisier or percussive content")
	if mfcc1 < -100:
		clauses.append("low MFCC1 implies darker tonal balance")

	reason = "; ".join(clauses) if clauses else "overall timbral profile"
	return f"Predicted '{predicted_genre}' because {reason}."


