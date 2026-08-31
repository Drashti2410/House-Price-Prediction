# House Price Prediction

This project builds a machine learning model to predict residential house prices based on real-estate property attributes such as area, number of bedrooms, bathrooms, furnishing status, and location-related features.

## Project Overview

The goal of this project is to analyze a housing dataset and train a regression model that can estimate the selling price of a house. The project combines data exploration, feature analysis, and predictive modeling using Python and scikit-learn.

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

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Seaborn
- scikit-learn

## Project Structure

- `Housing.csv` — housing dataset used for training and analysis
- `main.py` — entry point for the project
- `SEP785_project_notebook.ipynb` — exploratory notebook with analysis and experiments
- `pyproject.toml` — project dependencies and Python package configuration

## Setup

1. Clone the repository.
2. Open the project folder.
3. Create and activate a virtual environment.
4. Install dependencies from the project configuration:

```bash
pip install -e .
```

If you prefer to install the libraries manually, use:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Run the Project

From the project root, execute:

```bash
python main.py
```

## Typical Workflow

1. Load the dataset from `Housing.csv`
2. Explore the data and identify patterns
3. Clean and preprocess features
4. Encode categorical variables
5. Train a regression model
6. Evaluate prediction accuracy
7. Generate insights from model performance

## Expected Outcome

The model should be able to estimate a house price based on commonly available property characteristics, helping users understand how key features influence valuation in the dataset.

## Notes

This project is suitable for learning regression-based predictive modeling, feature engineering, and data visualization in a real-estate context.
