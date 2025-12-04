import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ------------------------ CSS ------------------------
def load_custom_css():
    st.markdown("""
        <style>

        .main {
            background-color: #f8f9fa;
        }

        .title {
            font-size: 36px;
            font-weight: 700;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 20px;
        }

        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }

        .stCard {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        .stButton > button {
            background-color: #2E86C1;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 24px;
        }

        .stButton > button:hover {
            background-color: #1B4F72;
        }
        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ------------------------ USERS ------------------------
users = {"Rutuja": "rutu"}

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("<h1 class='title'>🔐 User Login</h1>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["authenticated"] = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
        return False

    return True

# ------------------------ SAVE PREDICTION ------------------------
def save_prediction(soil, temp, rain, past, pred):
    file_path = "crop_yield_data.csv"

    # Create empty storage file if not exists
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=[
            "Soil_Quality", "Temperature", "Rainfall", "Past_Yield", "Predicted_Yield"
        ])
        df.to_csv(file_path, index=False)

    df = pd.read_csv(file_path)

    new_row = {
        "Soil_Quality": soil,
        "Temperature": temp,
        "Rainfall": rain,
        "Past_Yield": past,
        "Predicted_Yield": pred
    }

    df.loc[len(df)] = new_row
    df.to_csv(file_path, index=False)

# ------------------------ PREDICTION PAGE ------------------------
def crop_yield_predict():
    st.markdown("<h1 class='title'>🌾 Crop Yield Prediction 🌾</h1>", unsafe_allow_html=True)

    model_path = r"C:\Users\rutuj\OneDrive\Desktop\Crop Yield\crop_yield_model (1).pkl"
    if not os.path.exists(model_path):
        st.error("❌ Model not found!")
        return

    model = joblib.load(model_path)

    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("""<div style="background:#e8f4fc; padding:10px; border-radius:8px; border-left:5px solid #2E86C1;">📌 <b>Note:</b> These are default readings. You can change them as per your requirement.</div>""", unsafe_allow_html=True)


    col1, col2 = st.columns(2)
    with col1:
        soil_quality = st.number_input("🌱 Soil Quality (pH)", 0.0, 14.0, 6.5, 0.01)
        rainfall = st.number_input("🌧 Rainfall (mm)", 0.0, 1000.0, 150.0, 0.1)
    with col2:
        temperature = st.number_input("🌡 Temperature (°C)", -10.0, 50.0, 25.0, 0.1)
        past_yield = st.number_input("🌾 Past Crop Yield (kg/ha)", 0.0, 10000.0, 2000.0, 1.0)

    if st.button("🔍 Predict Crop Yield"):
        features = pd.DataFrame([{"Soil_Quality": soil_quality,"Temperature": temperature,"Rainfall": rainfall,"Past_Yield": past_yield}])
        pred = model.predict(features)[0]
        st.success(f"🌱 Predicted Crop Yield: **{pred:.2f} kg/ha**")

        # Save prediction to storage
        save_prediction(soil_quality, temperature, rainfall, past_yield, pred)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------ STORAGE PAGE ------------------------
def data_storage():
    st.markdown("<h1 class='title'>🗂 Stored Crop Yield Predictions</h1>", unsafe_allow_html=True)

    file_path = "crop_yield_data.csv"

    st.markdown("<div class='stCard'>", unsafe_allow_html=True)

    if not os.path.exists(file_path):
        st.warning("⚠ No data found!")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    df = pd.read_csv(file_path)
    st.dataframe(df, width='stretch')

    if st.button("🧹 Delete All Data"):
        os.remove(file_path)
        st.warning("Data deleted!")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------ MAIN ------------------------
def main():
    if not authenticate_user():
        return

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Crop Yield Prediction", "Data Storage"])

    if page == "Crop Yield Prediction":
        crop_yield_predict()

    elif page == "Data Storage":
        data_storage()

if __name__ == "__main__":
    main()
