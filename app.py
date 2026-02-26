import streamlit as st
import joblib
import re

# -----------------------
# Load model + vectorizer
# -----------------------

model = joblib.load("models/phishing_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

# -----------------------
# Utility Functions
# -----------------------

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\W", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def predict_phishing(text):
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    probability = model.predict_proba(vectorized)[0][1]
    return probability

def privacy_risk_analyzer(text):
    risk_keywords = {
        "location": 2,
        "contacts": 3,
        "microphone": 3,
        "camera": 2,
        "tracking": 3,
        "biometric": 4,
        "password": 3
    }
    
    score = 0
    found = []
    
    for word, weight in risk_keywords.items():
        if word in text.lower():
            score += weight
            found.append(word)
    
    if score <= 2:
        level = "Low"
    elif score <= 6:
        level = "Medium"
    else:
        level = "High"
        
    return level, found

def hygiene_score(answers):
    score = sum(answers)
    percentage = (score / 5) * 100
    return percentage


# -----------------------
# Streamlit UI
# -----------------------

st.set_page_config(page_title="AegisEDU AI", layout="wide")

st.title("🛡️ AegisEDU AI")
st.subheader("Explainable Digital Safety Companion for Students")

tabs = st.tabs(["🔎 Phishing Analyzer", "🔐 Privacy Analyzer", "📊 Hygiene Score"])

# -----------------------
# TAB 1 - Phishing
# -----------------------

with tabs[0]:
    st.header("Phishing Risk Detection")
    user_input = st.text_area("Paste suspicious email or message:")
    
    if st.button("Analyze Phishing"):
        if user_input.strip() == "":
            st.warning("Please enter text.")
        else:
            risk = predict_phishing(user_input)
            st.metric("Phishing Risk Score", f"{round(risk*100,2)}%")
            
            if risk > 0.7:
                st.error("⚠ HIGH RISK - Likely phishing attempt")
            elif risk > 0.4:
                st.warning("⚠ MEDIUM RISK - Suspicious content")
            else:
                st.success("✅ LOW RISK - Appears safe")

# -----------------------
# TAB 2 - Privacy
# -----------------------

with tabs[1]:
    st.header("Privacy Risk Analyzer")
    privacy_text = st.text_area("Paste app permissions or privacy policy text:")
    
    if st.button("Analyze Privacy"):
        if privacy_text.strip() == "":
            st.warning("Please enter text.")
        else:
            level, found = privacy_risk_analyzer(privacy_text)
            st.metric("Privacy Risk Level", level)
            
            if found:
                st.write("Detected sensitive keywords:")
                st.write(", ".join(found))
            else:
                st.success("No major sensitive keywords detected.")

# -----------------------
# TAB 3 - Hygiene
# -----------------------

with tabs[2]:
    st.header("Digital Hygiene Assessment")
    
    q1 = st.checkbox("I use strong unique passwords")
    q2 = st.checkbox("I enable 2FA")
    q3 = st.checkbox("I avoid clicking unknown links")
    q4 = st.checkbox("I verify email senders carefully")
    q5 = st.checkbox("I update software regularly")
    
    if st.button("Calculate Hygiene Score"):
        answers = [q1, q2, q3, q4, q5]
        score = hygiene_score(answers)
        st.metric("Digital Hygiene Score", f"{score}%")
        
        if score >= 80:
            st.success("Excellent Digital Safety Practices!")
        elif score >= 50:
            st.warning("Moderate Safety Level - Improve further.")
        else:
            st.error("Low Safety Awareness - Immediate improvement recommended.")