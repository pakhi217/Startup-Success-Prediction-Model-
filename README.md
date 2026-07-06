# 🚀 Startup Success Predictor

An AI-powered **Startup Success Prediction Platform** built using **Python, Machine Learning, and Streamlit**. This project analyzes startup data, performs exploratory data analysis, trains multiple machine learning models, and predicts the likelihood of a startup's success based on its characteristics.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Workflow](#-project-workflow)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Streamlit Application](#-streamlit-application)
- [Installation](#-installation)
- [Usage](#-usage)
- [Future Improvements](#-future-improvements)
- [Contributors](#-contributors)

---

# 📖 Project Overview

The **Startup Success Predictor** is an end-to-end Machine Learning project that predicts whether a startup is likely to succeed based on historical startup data from the **Crunchbase Startup Success/Failure Dataset**.

The project combines:

- 🧹 Data Cleaning
- 📊 Exploratory Data Analysis
- ⚙️ Data Preprocessing
- 🤖 Machine Learning
- 📈 Model Evaluation
- 🌐 Interactive Streamlit Dashboard

---

# ✨ Features

- Clean and preprocess real-world startup data
- Interactive visualizations using Plotly
- Multiple machine learning algorithms
- Automatic best model selection
- Startup search and filtering
- AI-based startup success prediction
- Beautiful Streamlit dashboard
- Probability score for predictions

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Plotly |
| Machine Learning | Scikit-learn |
| Frontend | Streamlit |
| Model Saving | Joblib |
| Version Control | Git & GitHub |

---

# 🔄 Project Workflow

```text
Dataset
   │
   ▼
Data Cleaning
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Feature Engineering
   │
   ▼
Data Preprocessing
   │
   ▼
Train Multiple ML Models
   │
   ▼
Model Evaluation
   │
   ▼
Best Model Selection
   │
   ▼
Save Model (.pkl)
   │
   ▼
Streamlit Dashboard
   │
   ▼
Startup Success Prediction
```

---

# 📂 Project Structure

```text
Startup-Success-Predictor/
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── notebooks/
│
├── models/
│   ├── best_model.pkl
│   ├── encoder.pkl
│   └── scaler.pkl
│
├── scripts/
│   ├── cleaning.py
│   ├── eda.py
│   ├── preprocessing.py
│   ├── train_model.py
│   └── evaluate_model.py
│
├── streamlit/
│   ├── Home.py
│   ├── pages/
│   │   ├── Dashboard.py
│   │   ├── Analytics.py
│   │   ├── Startup_Explorer.py
│   │   ├── Prediction.py
│   │   └── About.py
│   └── assets/
│
├── requirements.txt
├── README.md
└── app.py
```

---

# 📊 Dataset

**Dataset:** Crunchbase Startup Success/Failure Dataset (Kaggle)

### Important Features

- Company Name
- Category
- Funding Amount
- Funding Rounds
- Country
- State
- City
- Founded Date
- First Funding Date
- Last Funding Date
- Startup Status (Target Variable)

---

# 📈 Exploratory Data Analysis

The project performs:

- Missing Value Analysis
- Success vs Failure Distribution
- Funding Distribution
- Top Startup Categories
- Country-wise Analysis
- Top Investors
- IPO vs Acquisition Analysis
- Correlation Heatmap
- Histograms
- Box Plots
- Pie Charts
- Bar Charts

---

# ⚙️ Data Preprocessing

The preprocessing pipeline includes:

- Handling Missing Values
- Removing Duplicate Records
- Feature Engineering
- Label/One-Hot Encoding
- Feature Scaling
- Train-Test Split
- Saving Encoder and Scaler

Generated files:

```
processed.csv
encoder.pkl
scaler.pkl
```

---

# 🤖 Machine Learning Models

The following models are trained and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

The best-performing model is automatically saved as:

```
best_model.pkl
```

---

# 📊 Model Evaluation

Evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score
- Confusion Matrix

---

# 🌐 Streamlit Application

The application consists of six pages:

### 🏠 Home

- Project introduction
- Navigation
- Overview

### 📊 Dashboard

- KPI Cards
- Startup Summary
- Dataset Statistics

### 📈 Analytics

- Interactive Charts
- Filters
- Business Insights

### 🔍 Startup Explorer

- Search Startups
- Filter by Country
- Filter by Category
- Funding Filters

### 🤖 Prediction

- User Input Form
- Startup Success Prediction
- Probability Score
- Result Explanation

### ℹ️ About

- Project Details
- Dataset Information
- Team Members

---

# 🔗 Backend-Frontend Integration

Workflow:

1. Backend cleans raw dataset.
2. Generates `clean_startups.csv`.
3. Trains machine learning models.
4. Saves:
   - `best_model.pkl`
   - `encoder.pkl`
   - `scaler.pkl`
5. Streamlit loads saved files.
6. User enters startup details.
7. Input data is encoded and scaled.
8. Model predicts startup success probability.
9. Results are displayed with charts and explanations.

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Startup-Success-Predictor.git
```

## Navigate into Project

```bash
cd Startup-Success-Predictor
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Streamlit

```bash
streamlit run app.py
```

---

# 📦 Requirements

```
Python 3.10+

pandas
numpy
matplotlib
plotly
scikit-learn
streamlit
joblib
```



## 📜 License

This project is intended for educational and learning purposes.
