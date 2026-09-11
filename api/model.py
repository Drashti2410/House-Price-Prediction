import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from api.db import query_all

CAT_COLS = ["mainroad", "guestroom", "basement", "hotwaterheating",
            "airconditioning", "prefarea", "furnishingstatus"]
NUM_COLS = ["area", "bedrooms", "bathrooms", "stories", "parking"]

def build_pipeline(model):
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS)
    ], remainder="passthrough")
    return Pipeline([("prep", preprocessor), ("model", model)])

def train_and_compare():
    df = query_all()
    X = df[NUM_COLS + CAT_COLS]
    y = df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    candidates = {
        "linear": LinearRegression(),
        "elasticnet": ElasticNet(alpha=0.1),
        "random_forest": RandomForestRegressor(n_estimators=200, random_state=42)
    }

    results = []
    best_pipeline, best_mae = None, float("inf")
    for name, model in candidates.items():
        pipe = build_pipeline(model)
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        results.append({"model": name, "mae": mae, "r2": r2})
        print(f"{name}: MAE={mae:,.0f}, R2={r2:.3f}")
        if mae < best_mae:
            best_pipeline, best_mae = pipe, mae

    with open("api/best_model.pkl", "wb") as f:
        pickle.dump(best_pipeline, f)
    return results

if __name__ == "__main__":
    train_and_compare()
