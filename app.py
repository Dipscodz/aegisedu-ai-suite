import streamlit as st
import joblib
import pandas as pd
from feature_extractor import extract_features

model = joblib.load("models/phishing_model.joblib")
feature_columns = joblib.load("models/feature_columns.joblib")


st.set_page_config(page_title="AegisEDU AI", layout="wide")

st.title(" AegisEDU AI")
st.subheader("AI-Powered URL Phishing Detection System")

url_input = st.text_input("Enter a URL to analyze:")

if st.button("Analyze URL"):
    if url_input.strip() == "":
        st.warning("Please enter a URL.")
    else:
        features = extract_features(url_input)

    
        input_df = pd.DataFrame([features])

       
        input_df = input_df.reindex(columns=feature_columns, fill_value=0)

        probability = model.predict_proba(input_df)[0][1]

        st.metric("Phishing Risk Score", f"{round(probability*100,2)}%")

        if probability > 0.7:
            st.error("⚠ HIGH RISK - Likely phishing URL")
        elif probability > 0.4:
            st.warning("⚠ MEDIUM RISK - Suspicious URL")
        else:
            st.success(" LOW RISK - Appears legitimate")
            