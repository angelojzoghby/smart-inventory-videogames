import joblib
import numpy as np
from pathlib import Path

root = Path(__file__).resolve().parents[2]
model = joblib.load(root / "ml" / "Regression model code" / "random_forest_price_predictor.joblib")
genre_list = joblib.load(root / "ml" / "Regression model code" / "genre_list.joblib")
base_price_map = joblib.load(root / "ml" / "Regression model code" / "base_price_map.joblib")

def preprocess_for_model(payload):
    title = payload.get("title", "").strip().lower()
    genres = payload.get("genres", [])
    dlc = int(payload.get("dlc", 0))
    f2p = int(payload.get("f2p", 0))
    gamepass = int(payload.get("gamepass", 0))
    discount = int(payload.get("discount", 0))

    base_price = float(base_price_map.get(title, np.median(list(base_price_map.values()))))

    g_vec = [1 if g in genres else 0 for g in genre_list]

    row = [dlc, f2p, gamepass, discount, base_price] + g_vec
    return np.array(row).reshape(1, -1)

def predict(payload):
    X = preprocess_for_model(payload)
    return float(model.predict(X)[0])
