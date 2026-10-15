# 🏥 Apollo Hospitals Operations Dashboard

An interactive, enterprise-grade healthcare analytics dashboard built with **Python**, **Streamlit**, and **Plotly**. This project analyzes over **75,000 patient appointments** to uncover operational bottlenecks, financial leakage from no-shows, and doctor utilization trends.

🔗 **[View Live Dashboard](# 🏥 Apollo Hospitals Operations Dashboard

An interactive, enterprise-grade healthcare analytics dashboard built with **Python**, **Streamlit**, and **Plotly**. This project analyzes over **75,000 patient appointments** to uncover operational bottlenecks, financial leakage from no-shows, and doctor utilization trends.

🔗 **[View Live Dashboard](https://apollo-hospital-xwntmhvra6uup7xbnol9hf.streamlit.app/)

---

## 📊 Project Overview
Hospitals face significant revenue loss and operational inefficiencies due to patient no-shows and poor resource allocation. This dashboard transforms raw Hospital Information System (HIS) data into actionable insights, helping administrators optimize booking channels, improve reminder strategies, and enhance patient satisfaction.

## ✨ Key Features & Insights

###  Business & Operational Metrics
* **Appointment Trends:** Tracks monthly volume, outcome splits (Completed, No-Show, Cancelled), and booking channel performance.
* **No-Show Analysis:** Identifies high-risk specialties, analyzes the impact of booking lead times, and evaluates time-of-day dropout risks.
* **Doctor Utilization:** Tracks daily slot utilization rates and correlates doctor experience with consultation fees.

### 💰 Financial Performance
* **Revenue Leakage:** Calculates exact revenue lost to no-shows based on standard consultation fees.
* **Payment & Insurance Mix:** Analyzes revenue by city, payment mode, and the impact of insurance coverage on patient out-of-pocket expenses.

###  Patient Experience & Quality
* **Wait Time vs. Satisfaction:** Visualizes the correlation between patient wait times and post-consultation satisfaction scores.
* **Demographic Segmentation:** Segments patients by age, chronic conditions, and membership status to understand attendance behavior.

### 🎨 Custom UI/UX
* **Dark Themed Enterprise UI:** Custom CSS injection for a sleek, dark-mode aesthetic with a subtle background image.
* **Glassmorphism Effects:** Transparent, glass-like filter boxes and KPI cards that blend seamlessly with the background.
* **Apollo Branding:** Custom Plotly color palettes matching Apollo Hospitals' corporate identity.

---

## ️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express
* **Web Framework:** Streamlit
* **Machine Learning/Stats:** Statsmodels (for OLS trendlines)
* **Styling:** Custom CSS (Base64 image embedding, Glassmorphism)

---

## 📂 Project Structure
```text
Apollo-Hospital/
│
├── app.py                          # Main Streamlit application
├── apollo_appointments_fact.csv    # Fact table (75k+ appointment records)
├── apollo_doctors_dim.csv          # Dimension table (320 doctor records)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── assets/
    └── apollo_bg.jpg               # Background image for the dashboard)** *(Replace with your actual Streamlit URL)*

---

## 📊 Project Overview
Hospitals face significant revenue loss and operational inefficiencies due to patient no-shows and poor resource allocation. This dashboard transforms raw Hospital Information System (HIS) data into actionable insights, helping administrators optimize booking channels, improve reminder strategies, and enhance patient satisfaction.

## ✨ Key Features & Insights

###  Business & Operational Metrics
* **Appointment Trends:** Tracks monthly volume, outcome splits (Completed, No-Show, Cancelled), and booking channel performance.
* **No-Show Analysis:** Identifies high-risk specialties, analyzes the impact of booking lead times, and evaluates time-of-day dropout risks.
* **Doctor Utilization:** Tracks daily slot utilization rates and correlates doctor experience with consultation fees.

### 💰 Financial Performance
* **Revenue Leakage:** Calculates exact revenue lost to no-shows based on standard consultation fees.
* **Payment & Insurance Mix:** Analyzes revenue by city, payment mode, and the impact of insurance coverage on patient out-of-pocket expenses.

###  Patient Experience & Quality
* **Wait Time vs. Satisfaction:** Visualizes the correlation between patient wait times and post-consultation satisfaction scores.
* **Demographic Segmentation:** Segments patients by age, chronic conditions, and membership status to understand attendance behavior.

### 🎨 Custom UI/UX
* **Dark Themed Enterprise UI:** Custom CSS injection for a sleek, dark-mode aesthetic with a subtle background image.
* **Glassmorphism Effects:** Transparent, glass-like filter boxes and KPI cards that blend seamlessly with the background.
* **Apollo Branding:** Custom Plotly color palettes matching Apollo Hospitals' corporate identity.

---

## ️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express
* **Web Framework:** Streamlit
* **Machine Learning/Stats:** Statsmodels (for OLS trendlines)
* **Styling:** Custom CSS (Base64 image embedding, Glassmorphism)

---

## 📂 Project Structure
```text
Apollo-Hospital/
│
├── app.py                          # Main Streamlit application
├── apollo_appointments_fact.csv    # Fact table (75k+ appointment records)
├── apollo_doctors_dim.csv          # Dimension table (320 doctor records)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── assets/
    └── apollo_bg.jpg               # Background image for the dashboard
