import pandas as pd
import numpy as np
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier


# --------------------------
# 1. Load Dataset
# --------------------------

# Replace with your dataset path
data = pd.read_csv("data/phishing_sample.csv")

# Expected columns: 'text' and 'label'
# label: 1 = phishing, 0 = safe


# --------------------------
# 2. Text Cleaning Function
# --------------------------

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)  # remove links
    text = re.sub(r"\W", " ", text)      # remove special chars
    text = re.sub(r"\s+", " ", text)     # remove extra spaces
    return text.strip()


data["cleaned_text"] = data["text"].apply(clean_text)


# --------------------------
# 3. Train Test Split
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(
    data["cleaned_text"],
    data["label"],
    test_size=0.2,
    random_state=42
)


# --------------------------
# 4. TF-IDF Vectorization
# --------------------------

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 3)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# --------------------------
# 5. Train XGBoost Model
# --------------------------

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="logloss"
)

model.fit(X_train_tfidf, y_train)


# --------------------------
# 6. Evaluation
# --------------------------

y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# --------------------------
# 7. Save Model
# --------------------------

joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel and vectorizer saved successfully!")