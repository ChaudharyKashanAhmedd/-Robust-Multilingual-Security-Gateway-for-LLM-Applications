import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import joblib


# Load dataset
data = pd.read_csv("data/training_data.csv")

X = data["text"]
y = data["label"]


# Create pipeline
model = Pipeline([

    ("tfidf", TfidfVectorizer()),

    ("classifier", LogisticRegression())

])


# Train model
model.fit(X, y)


# Save model
joblib.dump(model, "models/injection_model.pkl")

print("Model trained and saved.")