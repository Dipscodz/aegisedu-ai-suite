import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier



data = pd.read_csv("data/phishing_sample.csv")


if "id" in data.columns:
    data = data.drop(columns=["id"])



X = data.drop(columns=["CLASS_LABEL"])
y = data["CLASS_LABEL"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)



model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    eval_metric="logloss"
)

model.fit(X_train, y_train)



y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


joblib.dump(model, "models/phishing_model.joblib")
joblib.dump(X.columns.tolist(), "models/feature_columns.joblib")

print("\nModel saved successfully!")