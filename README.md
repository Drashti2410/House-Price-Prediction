# House Price Prediction

This project builds a machine learning model to predict residential house prices based on real-estate property attributes such as area, number of bedrooms, bathrooms, furnishing status, and location-related features. It also ships the trained model as a containerized REST API backed by a SQL database.

## Project Overview

The goal of this project is to analyze a housing dataset and train a regression model that can estimate the selling price of a house. The project combines data exploration, feature analysis, and predictive modeling using Python and scikit-learn, then exposes the model through a FastAPI service with automated tests, a Docker image, and a CI pipeline.

## Dataset

The dataset is stored in `Housing.csv` and contains house listings with both numerical and categorical attributes. The main target variable is:

- `price`

Key features include:

- `area`
- `bedrooms`
- `bathrooms`
- `stories`
- `mainroad`
- `guestroom`
- `basement`
- `hotwaterheating`
- `airconditioning`
- `parking`
- `prefarea`
- `furnishingstatus`

## Tech Stack

- Python 3.11
- Pandas / NumPy
- Matplotlib / Seaborn (notebook analysis)
- scikit-learn
- SQLAlchemy + SQLite
- FastAPI + Uvicorn
- pytest + httpx
- Docker
- GitHub Actions

## Project Structure

- `Housing.csv` — housing dataset used for training and analysis
- `main.py` — original entry point for the project
- `SEP785_project_notebook.ipynb` — exploratory notebook with analysis and experiments
- `pyproject.toml` — project dependencies and Python package configuration
- `api/db.py` — loads `Housing.csv` into a SQLite database via SQLAlchemy and provides query helpers
- `api/model.py` — trains and compares Linear, ElasticNet, and Random Forest models, then saves the best one to `api/best_model.pkl`
- `api/schemas.py` — Pydantic request/response models with input validation
- `api/main.py` — FastAPI service exposing `/health`, `/predict`, and `/listings`
- `tests/test_api.py` — pytest suite covering the API endpoints and validation
- `data/housing.db` — generated SQLite database (created by `api/db.py`)
- `requirements-api.txt` — pinned dependencies for the API
- `Dockerfile` — builds a self-contained image (DB + model built at image build time)
- `.github/workflows/ci.yml` — CI pipeline: install, build DB, train model, run tests, build image

## Setup

1. Clone the repository.
2. Open the project folder.
3. Create and activate a virtual environment.
4. Install dependencies.

For the machine learning project:

```bash
pip install -e .
```

For the API:

```bash
pip install -r requirements-api.txt
```

## Run the Original Project

From the project root, execute:

```bash
python main.py
```

## Build the Database and Train the Model

All API commands are run from the project root so that the `api` package imports resolve.

```bash
# Load Housing.csv into data/housing.db
python api/db.py

# Train and compare models, saving the best pipeline to api/best_model.pkl
python api/model.py
```

`api/model.py` trains Linear Regression, ElasticNet, and Random Forest inside a
scikit-learn pipeline (one-hot encoding for categorical columns), then selects the
model with the lowest held-out test MAE. On this small dataset Random Forest
overfits — its training score is high but test performance is worse than the
regularized linear model — so model selection is driven by test metrics, not
training metrics.

## Run the API

```bash
uvicorn api.main:app --reload
```

Interactive docs are available at `http://127.0.0.1:8000/docs`.

### Endpoints

- `GET /health` — returns `ok` when the model is loaded, `degraded` otherwise
- `POST /predict` — accepts validated house features and returns a predicted price
- `GET /listings` — returns rows from the SQLite database, with optional
  `min_price` and `max_bedrooms` query filters

Example prediction request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"area": 3500, "bedrooms": 3, "bathrooms": 2, "stories": 2, "parking": 1,
       "mainroad": "yes", "guestroom": "no", "basement": "yes",
       "hotwaterheating": "no", "airconditioning": "yes", "prefarea": "yes",
       "furnishingstatus": "semi-furnished"}'
```

## Tests

```bash
pytest tests/
```

## Docker

The image builds the database and trains the model at build time, so the running
container is self-contained and needs no external volume for a demo.

```bash
docker build -t house-price-api .
docker run -p 8000:8000 house-price-api
```

Trade-off: retraining requires rebuilding the image. In production this would be
replaced by a separate training pipeline and a model registry.

## Continuous Integration

`.github/workflows/ci.yml` runs on every push: it installs the API dependencies,
builds the database, trains the model, runs the pytest suite, and builds the
Docker image.

## Typical Workflow

1. Load the dataset from `Housing.csv`
2. Explore the data and identify patterns
3. Clean and preprocess features
4. Encode categorical variables
5. Train and compare regression models
6. Evaluate prediction accuracy on held-out data
7. Serve the best model through the API
8. Validate with automated tests and CI

## Expected Outcome

The model estimates a house price based on commonly available property
characteristics, and the API makes those predictions available over HTTP with
input validation and SQL-backed listing queries.

## Notes

This project is suitable for learning regression-based predictive modeling,
feature engineering, data visualization, and packaging a model as a tested,
containerized service.
