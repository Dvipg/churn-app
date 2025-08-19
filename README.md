# 🔮 Customer Churn Prediction App

An end-to-end **Streamlit web application** for predicting customer churn using a machine learning pipeline trained on the Telco Customer Churn dataset.  

The app supports:
- **Single Predictions** → Input customer details in a form to get churn probability instantly.  
- **Batch Predictions** → Upload a CSV file and get predictions for all records at once.  

---

## ⚡ My Journey (Honest Build Log)

This wasn’t a one-shot build — it took me **multiple tries, debugging rounds, and learning moments**.  
Here’s the honest breakdown:

1. **First Attempt (Errors Galore)**  
   - Tried directly exporting the model.  
   - Faced errors like:  
     - `'dict' object has no attribute predict`  
     - `NameError: input_cols not defined`  
     - `KeyError: 'model'`  
   - Realized I needed to properly bundle pipeline + features in a single `.pkl`.

2. **Second Attempt (Streamlit UI working)**  
   - Got a minimal app running with predictions.  
   - But the probability display + batch upload weren’t user-friendly.  
   - Learned how to integrate **form inputs** and improve UI using columns.

3. **Third Attempt (Stable, Professional Version)**  
   - Fixed model loading issues.  
   - Added probability bars, results formatting, and CSV batch support.  
   - Finalized a version that **feels production-ready**.  

This repo is the **final working version** after all that iteration.  
It’s not just the code — it’s proof of problem-solving and persistence.

---

## 📂 Project Structure

ChurnApp/
│

├── app.py # Streamlit web app

├── churn_pipeline.pkl # Saved ML pipeline (model + preprocessing)

├── requirements.txt # Python dependencies

└── .csv # Example input file 


---

## 🚀 Features

- ✅ **Interactive form** for single-customer predictions  
- ✅ **Batch predictions** via CSV upload  
- ✅ **Model pipeline** with preprocessing & classifier bundled together  
- ✅ **Churn probability** visualization with progress bar  
- ✅ **Downloadable results** for batch predictions  

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**
- **Pandas, NumPy**
- **Scikit-Learn**
- (Optional: XGBoost/LightGBM if used in training)

---

## 📊 Demo (Example Output)

**Single Prediction:**

Churn Prediction: No
Churn Probability: 0.48

**Batch Prediction Output:**
| customerID | tenure | MonthlyCharges | TotalCharges | ChurnPrediction | ChurnProbability |
|------------|--------|----------------|--------------|-----------------|------------------|
| 7590-VHVEG | 1      | 29.85          | 29.85        | 1               | 0.73             |
| 5575-GNVDE | 34     | 56.95          | 1889.5       | 0               | 0.22             |

---

## 🔧 How to Run Locally

1. Clone repo:
   ```bash
   git clone https://github.com/<your-username>/churn-app.git
   cd churn-app
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run app:
   ```bash
   streamlit run app.py

  ## 🌍 Deployment

This project is deployable on Streamlit Cloud for free.
Public link format:
   ```bash
   [https://username-churn-app.streamlit.app](https://5e518b13f645f8a9fd45083e272c799784dcc91c-tcmczibukvbwfgfmmkovz.streamlit.app/)
   ```
---
## 🏆 Key Takeaway

This app represents more than just code — it’s a portfolio project that shows:

Technical ability (ML + Streamlit)

Persistence through setbacks

Professional presentation
---
## 📜 License

Open-source, free to use and modify.


