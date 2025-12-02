import os
from pathlib import Path
from typing import Any, Dict

_model = None

def _model_path(filename: str = 'final_tuned_random_forest_model.joblib') -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / 'ml' / 'Regression model code' / filename

def load_model(filename: str = None):
    global _model
    if _model is not None:
        return _model
    fn = filename or 'final_tuned_random_forest_model.joblib'
    path = _model_path(fn)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at {path}")
    try:
        import joblib
    except Exception as e:
        raise RuntimeError('joblib is required to load the model') from e
    _model = joblib.load(path)
    return _model

def predict(payload: Dict[str, Any]) -> float:
    model = load_model()
    try:
        if hasattr(model, 'feature_names_in_'):
            names = list(model.feature_names_in_)
            row = []
            for n in names:
                v = payload.get(n)
                try:
                    row.append(float(v) if v is not None else 0.0)
                except:
                    row.append(0.0)
            import numpy as np
            X = np.array([row])
            pred = model.predict(X)
            return float(pred[0])

        numeric_vals = []
        for k, v in sorted(payload.items()):
            try:
                numeric_vals.append(float(v))
            except:
                pass
        if numeric_vals:
            import numpy as np
            X = np.array([numeric_vals])
            pred = model.predict(X)
            return float(pred[0])

        pn = str(payload.get('product_name', ''))
        pt = str(payload.get('product_type', ''))
        h = abs(hash(pn)) % 1000
        h2 = abs(hash(pt)) % 1000
        row = [float(h), float(len(pn)), float(len(pt)), float(h2)]
        import numpy as np
        X = np.array([row])
        pred = model.predict(X)
        return float(pred[0])
    except Exception as e:
        raise
