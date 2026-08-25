🚀 Startup Success Predictor

An AI-powered startup analytics and prediction platform that uses machine learning to analyze startup data and predict potential business outcomes.

The project combines data preprocessing, exploratory data analysis, machine learning, interactive visualizations, and a Streamlit web application into a single end-to-end workflow.

---

📌 Project Overview

Startups operate in an environment of uncertainty, competition, changing markets, and limited resources. Historical startup data can provide valuable insights into the factors associated with business outcomes.

Startup Success Predictor analyzes startup-related data to identify patterns and uses supervised machine learning models to predict whether a startup is likely to succeed or fail.

The platform is designed as an analytical and educational decision-support system, not as a guarantee of future business performance.

---

🎯 Objectives

- Clean and preprocess raw startup data.
- Handle missing values and duplicate records.
- Perform Exploratory Data Analysis (EDA).
- Identify patterns related to startup success and failure.
- Analyze relationships between funding, industries, countries, investors, and startup outcomes.
- Train and compare multiple machine learning classification models.
- Evaluate models using standard classification metrics.
- Build an interactive Streamlit dashboard.
- Provide a startup prediction interface.
- Save and reuse trained models and preprocessing objects.

---

🛠️ Tech Stack

Programming Language

- Python

Data Analysis & Processing

- Pandas
- NumPy

Machine Learning

- Scikit-learn
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Data Visualization

- Matplotlib
- Plotly

Web Application

- Streamlit

Model Persistence

- Joblib

---

📊 Dataset

The project uses the Crunchbase Startup Success/Failure Dataset available through Kaggle.

The dataset contains startup-related attributes that are analyzed to understand patterns associated with startup outcomes.

Data Processing Steps

1. Load and inspect the dataset.
2. Identify columns, data types, and missing values.
3. Remove duplicate records.
4. Remove irrelevant columns.
5. Handle missing and inconsistent data.
6. Encode categorical variables.
7. Perform feature engineering where applicable.
8. Split the dataset into training and testing sets.

---

🔄 Project Workflow

Kaggle Dataset
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Train / Test Split
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Best Model Selection
      ↓
Model & Preprocessor Saving
      ↓
Streamlit Dashboard
      ↓
Startup Prediction

---

🤖 Machine Learning Models

The project considers multiple classification algorithms:

1. Logistic Regression

A baseline classification algorithm used to model the relationship between startup features and the target outcome.

2. Decision Tree

A tree-based model that makes predictions through a sequence of feature-based decisions.

3. Random Forest

An ensemble learning algorithm that combines multiple decision trees to improve predictive performance and robustness.

4. Gradient Boosting

An ensemble technique that builds models sequentially to improve prediction performance.

The final model can be selected based on the evaluation results.

---

📈 Model Evaluation

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Confusion Matrix

«Exact numerical performance values should be added after running the final model evaluation.»

---

🖥️ Streamlit Application

The project includes an interactive Streamlit frontend.

🏠 Home

Provides an overview of the project and its purpose.

📊 Dashboard

Displays important startup analytics and KPIs.

📈 Analytics

Provides interactive visualizations for exploring startup trends and relationships.

🔎 Startup Explorer

Allows users to explore startup data using search and filtering functionality.

🔮 Prediction

Allows users to enter startup characteristics and receive:

- Predicted startup outcome
- Prediction probability

ℹ️ About

Provides information about the project, dataset, technologies, and methodology.

---

📁 Project Structure

Startup-Success-Predictor/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│
├── models/
│
├── scripts/
│
├── streamlit/
│   ├── app.py
│   └── pages/
│
│
└── README.md

---

⚙️ Installation

1. Clone the repository

git clone https://github.com/your-username/startup-success-predictor.git

2. Navigate to the project directory

cd startup-success-predictor

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

5. Install dependencies

pip install -r requirements.txt

---

▶️ Run the Application

Start the Streamlit application using:

streamlit run app.py

The application will open in your browser.

---

💡 Key Features

- 📊 Interactive startup analytics
- 📈 Data visualization
- 🔎 Startup exploration
- 🤖 Multiple ML classification models
- 🔮 Startup outcome prediction
- 📋 Model evaluation
- 💾 Saved ML model and preprocessing pipeline
- 🖥️ Interactive Streamlit interface
- 📚 End-to-end machine learning workflow

---

🧠 Learning Outcomes

This project provided practical experience in:

- Python programming
- Data cleaning and preprocessing
- Exploratory Data Analysis
- Data visualization
- Feature engineering
- Categorical encoding
- Machine learning classification
- Model evaluation
- Model persistence using Joblib
- Streamlit application development
- Debugging and testing
- Documentation and presentation

---

⚠️ Limitations

- Prediction quality depends on the quality, completeness, and representativeness of the historical dataset.
- Startup outcomes are influenced by many real-world factors that may not be present in the dataset.
- A machine learning prediction should not be considered a guarantee of future startup success.
- Model performance may vary depending on preprocessing, feature selection, and training data.

---

🔮 Future Scope

The platform can be extended by:

- Using larger and more diverse startup datasets.
- Experimenting with additional machine-learning and ensemble methods.
- Exploring deep-learning approaches where appropriate.
- Deploying the Streamlit application to the cloud.
- Developing a dedicated mobile or web application.
- Adding richer real-time analytics.
- Adding recommendation capabilities.
- Implementing Explainable AI (XAI) to show which factors influenced a prediction.
- Introducing automatic dataset updates and model retraining pipelines.

---

👥 Contributors

- Pakhi Saxena
- Jigyasa Chuphal
- Jiya Adhikari
- Himanshi Gupta
- Aanya Gupta

---

📚 References

- Crunchbase Startup Success/Failure Dataset — Kaggle
- Scikit-learn Documentation
- Pandas Documentation
- NumPy Documentation
- Streamlit Documentation
- Plotly Documentation

---

⭐ Acknowledgement

This project was developed as part of a summer internship/project focused on Data Analytics, Machine Learning, and Interactive Application Development.

If you found this project useful, consider giving the repository a ⭐.
