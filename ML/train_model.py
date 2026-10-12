from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "DATA" / "raw" / "synthesis_results.csv"
MODEL_DIR = PROJECT_ROOT / "ML" / "models"
RESULTS_DIR = PROJECT_ROOT / "ML" / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Load dataset
df = pd.read_csv(DATASET_PATH)

print("=" * 55)
print("AI-GUIDED RTL SYNTHESIS ADVISOR")
print("DELAY PREDICTION MODEL TRAINING")
print("=" * 55)

print(f"\nDataset: {DATASET_PATH}")
print(f"Original dataset size: {len(df)} designs")


# RTL features
FEATURE_COLUMNS = [
    "input_count",
    "output_count",
    "signal_count",
    "process_count",
    "and_count",
    "or_count",
    "xor_count",
    "not_count",
    "add_count",
    "sub_count",
    "mul_count",
    "if_count",
    "case_count",
    "loop_count",
    "when_count",
    "clocked_process",
    "reset_present",
    "register_count",
    "loc",
]

TARGET_COLUMN = "worst_delay_ns"


# Validate columns
required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")


# Convert required values to numeric
df[required_columns] = df[required_columns].apply(
    pd.to_numeric,
    errors="coerce",
)

df = df.dropna(subset=required_columns).copy()

if len(df) < 2:
    raise ValueError("At least two valid designs are required.")

X = df[FEATURE_COLUMNS]
y = df[TARGET_COLUMN]

print(f"Valid designs: {len(df)}")
print(f"Input features: {len(FEATURE_COLUMNS)}")
print(f"Prediction target: {TARGET_COLUMN}")


# Models
models = {
    "random_forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    ),
    "gradient_boosting": GradientBoostingRegressor(
        n_estimators=50,
        learning_rate=0.05,
        max_depth=2,
        random_state=42,
    ),
}


# Train, evaluate on training data, and save
summary = []

for name, model in models.items():
    print(f"\nTraining {name}...")

    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)
    rmse = mean_squared_error(y, predictions) ** 0.5
    r2 = r2_score(y, predictions)

    model_path = MODEL_DIR / f"{name}_delay.joblib"
    joblib.dump(model, model_path)

    print(f"Saved model: {model_path}")
    print(f"Training MAE: {mae:.4f} ns")
    print(f"Training RMSE: {rmse:.4f} ns")
    print(f"Training R2: {r2:.4f}")

    summary.append({
        "model": name,
        "training_samples": len(df),
        "feature_count": len(FEATURE_COLUMNS),
        "target": TARGET_COLUMN,
        "training_mae_ns": mae,
        "training_rmse_ns": rmse,
        "training_r2": r2,
    })


# Save summary
summary_df = pd.DataFrame(summary)

summary_path = RESULTS_DIR / "training_summary.csv"
summary_df.to_csv(summary_path, index=False)

print("\n" + "=" * 55)
print("TRAINING COMPLETED")
print("=" * 55)

print(summary_df.to_string(index=False))
print(f"\nSummary saved to: {summary_path}")

print(
    "\nWARNING: Only four designs are available. "
    "These are training-set metrics, not evidence of "
    "generalization to unseen RTL designs."
)