import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load("credit_card_model.pkl")

st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")

st.title("💳 Credit Card Fraud Detection System")

# Input form
with st.form("input_form"):
    st.subheader("Enter Transaction Details (V1–V28 + Amount)")

    col1, col2, col3 = st.columns(3)
    v_values = []

    for i in range(1, 29):
        with [col1, col2, col3][(i-1)%3]:
            value = st.text_input(f"V{i}", key=f"V{i}")
            v_values.append(value)

    amount = st.text_input("Transaction Amount", key="amount")

    submitted = st.form_submit_button("🔍 Predict Fraud")

    if submitted:
        try:
            features = [float(v) for v in v_values]
            features.append(float(amount))
            columns = [f'V{i}' for i in range(1, 29)] + ['Amount']
            input_df = pd.DataFrame([features], columns=columns)
            prediction = model.predict(input_df)[0]

            if prediction == 1:
                st.error("🚨 This transaction appears **fraudulent**.")
            else:
                st.success("✅ This transaction appears **safe**.")
        except:
            st.warning("⚠️ Please enter valid numeric values for all fields.")

# Paste full row
st.subheader("📋 Paste Full Row (V1–V28, Amount)")
full_row = st.text_area("Paste comma-separated values for V1 to V28 and Amount (29 values total):")

if st.button("Paste & Autofill"):
    try:
        parts = [x.strip() for x in full_row.replace("\n", "").split(",")]
        if len(parts) != 29:
            st.error("Please paste exactly 29 comma-separated values.")
        else:
            for i in range(28):
                st.session_state[f"V{i+1}"] = parts[i]
            st.session_state["amount"] = parts[28]
            st.success("Fields autofilled successfully!")
    except:
        st.error("Ensure all values are numeric and correctly formatted.")

# Upload CSV
st.subheader("📂 Detect Fraudulent Transactions from CSV")
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        expected_cols = [f'V{i}' for i in range(1, 29)] + ['Amount']
        if not all(col in df.columns for col in expected_cols):
            st.error("CSV must contain V1–V28 and Amount columns.")
        else:
            predictions = model.predict(df[expected_cols])
            df["Prediction"] = predictions
            fraud_df = df[df["Prediction"] == 1]

            if fraud_df.empty:
                st.success("✅ No fraudulent transactions found.")
            else:
                st.warning(f"⚠️ {len(fraud_df)} fraudulent transactions found:")
                st.dataframe(fraud_df)
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Footer
st.markdown("---")
st.markdown("<center><sub>Developed by Shakti, Shobhit, Pranjal, Abhishek</sub></center>", unsafe_allow_html=True)
