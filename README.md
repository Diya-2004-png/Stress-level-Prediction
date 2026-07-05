# 🧠 StressInsight AI
### AI-Powered Student Stress Prediction & Recommendation System

> **Predict Stress. Prevent Early. Live Better.**

StressInsight AI is a machine learning-powered web application that predicts a user's stress level using lifestyle habits, digital behavior, and wellness indicators. Instead of relying on traditional self-assessment questionnaires, the system analyzes real-world behavioral patterns to generate accurate stress predictions, confidence scores, and personalized recommendations.

Designed with a modern AI-inspired interface, StressInsight AI transforms daily habits into meaningful insights that help users identify stress early and encourage healthier lifestyle choices.


## 🌟 Features

### 👤 Smart Lifestyle Assessment
The application collects key lifestyle and behavioral information, including:

- Age, Gender, Country
- Academic/Professional Level
- Most Used Social Media Platform
- Purpose of Social Media Usage
- Daily Social Media Usage (Hours)
- Daily Phone Unlock Count
- Study/Work Hours
- Physical Activity
- Sleep Duration
- Mental Health Self-Rating

---

### 📊 Interactive Lifestyle Rhythm Ring

A real-time 24-hour visualization that dynamically displays:

- 😴 Sleep
- 📚 Study
- 🏃 Physical Activity
- 📱 Screen Time
- ⏳ Remaining Free Time

The visualization updates instantly while users fill out the form.

---

### 🤖 AI Stress Prediction

After submission, the Random Forest model predicts:

- ✅ Low Stress
- ✅ Medium Stress
- ✅ High Stress
- ✅ Very High Stress

Along with:

- Prediction Confidence Score
- Probability Distribution
- Timestamped Prediction
- Contextual Warnings
- Personalized Recommendations

---

### 📈 Interactive Dashboard

The results page includes:

- Animated Probability Bars
- Confidence Indicator
- Lifestyle Rhythm Ring
- Observed Factors
- Recommendation Cards
- Smart Warning Messages
- Responsive Modern UI

---

## 🎯 Why StressInsight AI?

Stress is rarely caused by a single event.

It develops gradually through unhealthy daily habits such as:

- Excessive Screen Time
- Poor Sleep Quality
- Low Physical Activity
- Constant Phone Usage
- Imbalanced Study Routine

StressInsight AI identifies these hidden behavioral patterns and predicts stress before it becomes overwhelming, allowing users to make healthier decisions earlier.

---

# 🏗 System Architecture

```text
                 User
                   │
                   ▼
     Modern Web Interface (HTML/CSS/JS)
                   │
                   ▼
             Flask Backend API
                   │
                   ▼
     Random Forest Prediction Model
                   │
                   ▼
      Recommendation Engine
                   │
                   ▼
 Interactive Prediction Dashboard
```

---

# ⚡ Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)

### UI Features

- Responsive Layout
- Glassmorphism Design
- Animated Components
- Live Rhythm Ring
- Interactive Dashboard

---

## Backend

- Python
- Flask

---

## Machine Learning

- Pandas
- NumPy
- Scikit-learn

Algorithms evaluated:

- Random Forest
- Decision Tree
- Logistic Regression
- K-Nearest Neighbors (KNN)

Final Model:

> **Random Forest Classifier (200 Estimators)**

Selected for its superior performance and robustness.

---

## 📊 Exploratory Data Analysis

Performed using:

- Matplotlib
- Seaborn
- Plotly

Visualizations include:

- Distribution Plots
- Correlation Heatmaps
- Feature Importance Charts
- Interactive Gauge Charts

---

## 🧠 Recommendation Engine

StressInsight AI includes a custom recommendation engine built on top of the machine learning model.

Instead of displaying generic advice, the engine analyzes the user's highest-impact lifestyle factors and generates personalized recommendations tailored to the predicted stress level.

Examples include:

- Improve Sleep Schedule
- Reduce Screen Time
- Increase Physical Activity
- Manage Study Load
- Practice Digital Detox
- Maintain Healthy Daily Routine

---

# 📂 Dataset

The model was trained using approximately **5,000 records** containing:

- Demographic Information
- Lifestyle Indicators
- Digital Usage Patterns
- Wellness Metrics

Target Classes:

- Low
- Medium
- High
- Very High

---

# 📈 Model Performance

| Model | Accuracy |
|--------|----------|
| ✅ Random Forest | **87.30%** |
| Decision Tree | 78.60% |
| KNN | 76.80% |
| Logistic Regression | 70.30% |

---

## Classification Report

| Stress Level | Precision | Recall | F1 Score |
|--------------|-----------|--------|----------|
| Low | 0.83 | 0.82 | 0.83 |
| Medium | 0.93 | 0.83 | 0.88 |
| High | 0.82 | 0.87 | 0.84 |
| Very High | 0.92 | 0.94 | 0.93 |

---

## 🔥 Top Predictive Features

Feature Importance analysis revealed the strongest predictors:

- 📱 Daily Social Media Usage
- 🔓 Daily Phone Unlock Count
- 😴 Sleep Hours
- 📚 Study Hours
- 🧠 Mental Health Score

These findings indicate that digital behavior and sleep quality are the most influential indicators of predicted stress.

---

# 📸 Application Preview

## 🏠 Home Page

> *(Add Screenshot Here)*

---

## 📊 Prediction Dashboard

> *(Add Screenshot Here)*

---

## 💡 Recommendation Panel

> *(Add Screenshot Here)*

---



# 🎯 Future Enhancements

- User Authentication
- Stress History Tracking
- Personalized Progress Dashboard
- Wearable Device Integration
- Mobile Application
- Deep Learning Models
- AI Chat Assistant
- Weekly Mental Wellness Reports

---

# 🔒 Privacy

StressInsight AI follows a privacy-first approach.

- No user information is permanently stored.
- Data is processed only to generate predictions.
- The application is intended solely for educational and research purposes.

---

# ⚠ Disclaimer

StressInsight AI is an educational machine learning project.

The predictions generated by this application are **not intended to diagnose mental health conditions** and should not replace professional medical advice or consultation.
