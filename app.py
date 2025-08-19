import streamlit as st
import pandas as pd
import pickle
import numpy as np

# === LOAD PIPELINE BUNDLE ===
try:
    with open("churn_pipeline.pkl", "rb") as f:
        bundle = pickle.load(f)
    pipe = bundle["pipeline"]
    feature_cols = bundle["feature_cols"]
    cat_cols = bundle["cat_cols"]
    num_cols = bundle["num_cols"]
    model_loaded = True
except FileNotFoundError:
    st.error("Error: The 'churn_pipeline.pkl' model file was not found. Please ensure it's in the same directory as this app.")
    model_loaded = False
except Exception as e:
    st.error(f"Error loading the model file: {e}")
    model_loaded = False


def clean_data(df):
    """Cleans the 'TotalCharges' column by converting blanks to 0."""
    df['TotalCharges'] = df['TotalCharges'].replace(' ', '0').astype(float)
    return df

if model_loaded:
    st.set_page_config(page_title="Churn Predictor", layout="wide")
    st.title("🔮 Customer Churn Prediction App")

    # --- MAIN UI CONTAINER ---
    with st.container():
        st.header("Predict Customer Churn")
        st.markdown(
            """
            This app predicts customer churn based on their service data. 
            You can either get a single prediction using the form below or upload a CSV file for a batch prediction.
            """
        )

        st.markdown("---")
        
        # === INPUT METHOD SELECTION ===
        predict_method = st.radio(
            "Select Prediction Method:", 
            ["Single Prediction", "Batch Prediction"]
        )

        if predict_method == "Single Prediction":
            st.subheader("👤 Enter Customer Data")
            with st.form("single_prediction_form"):
                col1, col2, col3 = st.columns(3)
                
                input_data = {}

                # Load encoder categories from pipeline
                encoder = pipe.named_steps["prep"].transformers_[0][1]
                cat_map = {col: encoder.categories_[i].tolist() for i, col in enumerate(cat_cols)}

                for i, col in enumerate(feature_cols):
                    if i % 3 == 0:
                        with col1:
                            if col in cat_cols:
                                input_data[col] = st.selectbox(col, cat_map.get(col, ["Yes", "No"]))
                            elif col in num_cols:
                                input_data[col] = st.slider(col, min_value=0.0, max_value=72.0, value=30.0)
                    elif i % 3 == 1:
                        with col2:
                            if col in cat_cols:
                                input_data[col] = st.selectbox(col, cat_map.get(col, ["Yes", "No"]))
                            elif col in num_cols:
                                if col == 'MonthlyCharges':
                                    input_data[col] = st.slider(col, min_value=0.0, max_value=120.0, value=60.0)
                                else: # TotalCharges
                                    input_data[col] = st.slider(col, min_value=0.0, max_value=8700.0, value=4000.0)
                    else:
                        with col3:
                            if col in cat_cols:
                                input_data[col] = st.selectbox(col, cat_map.get(col, ["Yes", "No"]))
                            elif col in num_cols:
                                if col == 'MonthlyCharges':
                                    input_data[col] = st.slider(col, min_value=0.0, max_value=120.0, value=60.0)
                                else: # TotalCharges
                                    input_data[col] = st.slider(col, min_value=0.0, max_value=8700.0, value=4000.0)
                
                submitted = st.form_submit_button("Predict Churn")

            if submitted:
                user_df = pd.DataFrame([input_data])
                user_df = clean_data(user_df)
                proba = pipe.predict_proba(user_df)[:, 1][0]
                pred = int(proba >= 0.5)

                st.subheader("🔮 Prediction Results")
                st.markdown(f"**Churn Prediction:** {'<span style="color:red">**⚠️ Yes**</span>' if pred == 1 else '<span style="color:green">**✅ No**</span>'}", unsafe_allow_html=True)
                st.markdown(f"**Churn Probability:** `{proba:.2f}`")
                st.progress(float(proba))


        elif predict_method == "Batch Prediction":
            st.subheader("📂 Upload CSV for Batch Predictions")
            st.info("Upload the 'Telco-Customer-Churn.csv' file to get predictions for all records.")
            
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

            if uploaded_file is not None:
                try:
                    data = pd.read_csv(uploaded_file, encoding="utf-8")
                except UnicodeDecodeError:
                    data = pd.read_csv(uploaded_file, encoding="latin1")

                missing_cols = set(feature_cols) - set(data.columns)
                if missing_cols:
                    st.error(f"Uploaded file is missing the following required columns: {missing_cols}")
                else:
                    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully. Ready to predict on {len(data)} rows.")
                    
                    if st.button("Run Predictions"):
                        data = clean_data(data)
                        preds = pipe.predict(data[feature_cols])
                        probs = pipe.predict_proba(data[feature_cols])[:, 1]
                        data["ChurnPrediction"] = preds
                        data["ChurnProbability"] = probs.round(2)
                        
                        st.subheader("📋 Predictions Table")
                        st.dataframe(data.head())
                        
                        csv_out = data.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="⬇️ Download Predictions CSV",
                            data=csv_out,
                            file_name="predictions.csv",
                            mime="text/csv",
                        )