# Web & Social Media Analytics Dashboard 🚀

A comprehensive, interactive Streamlit web application designed for the **Web & Social Media Analytics** course project. This project integrates live Natural Language Processing (NLP), web scraping capabilities, Google Analytics 4 (GA4) traffic case study analytics, and interactive Plotly data visualizations.

---

## 📌 Course Objectives Coverage

This application directly addresses and satisfies the 4 core course objectives:

### 1. NLP & Text Preprocessing (Objective 1)
* **Text Preprocessing Pipeline**: Automatically transforms raw user text or reviews through lowercasing, regex cleaning (stripping URLs, punctuation, special characters, and digits), word tokenization, and NLTK stopword removal.
* **Sentiment Analysis**: Leverages `TextBlob` to calculate **Polarity** (-1.0 to +1.0) and **Subjectivity** (0.0 to 1.0) scores, classifying sentiment into *Positive*, *Neutral*, or *Negative*.
* **Interactive UI**: Users can paste custom customer reviews or select from curated sample datasets to visualize step-by-step text transformation.

### 2. Web Scraping Engine (Objective 2)
* **Live Scraper**: Built using `requests` and `BeautifulSoup4` to fetch real-time public headlines and article content from specified URLs or topic queries.
* **Resilient Architecture**: Includes HTTP headers (User-Agent simulation), error handling, and a fallback mock scraper to ensure uninterrupted performance during network restrictions or anti-scraping blocks.
* **Data Integration**: Automatically runs batch sentiment analysis on scraped content and presents the output in an interactive, searchable Pandas DataFrame with CSV export capability.

### 3. GA4 Traffic Analytics Case Study (Objective 3)
* **Google Merchandise Store GA4 Dataset Simulation**: Recreates authentic GA4 channel acquisition models (Organic Search, Direct, Social Referral, Paid Search, Email, Display).
* **Key Metrics & KPIs**: Tracks Total Users, Sessions, Engagement Rate, Bounce Rate, E-commerce Conversions, and Revenue.
* **Interactive Filtering**: Provides date range selection, channel slicing, and device type breakdowns for deep traffic attribution analysis.

### 4. Data Visualization (Objective 4)
* **Interactive Plotly Visualizations**:
  * **Sentiment Distribution**: Donut charts and Polarity vs. Subjectivity scatter plots.
  * **Word Frequency**: Top 15 cleaned keyword frequency bar charts.
  * **Traffic Trends**: Dual-axis line and area charts for daily sessions vs. conversion rate over time.
  * **Channel Performance**: Acquisition funnel and Revenue by Traffic Source bar charts.

---

## 🛠️ Project Structure

```
Web-Analytics App/
├── app.py              # Main Streamlit Python Application
├── requirements.txt    # Python package dependencies
└── README.md           # Course project documentation & guide
```

---

## ⚙️ Installation & Local Setup

### Prerequisites
* Python 3.9 or higher installed on your system.

### Step-by-Step Instructions

1. **Clone / Open Project Directory**:
   ```bash
   cd "c:/Users/Aahelee/OneDrive/Desktop/Web-Analytics App"
   ```

2. **Create a Virtual Environment**:
   * On Windows (PowerShell/CMD):
     ```powershell
     python -m venv .venv
     ```
   * On macOS/Linux:
     ```bash
     python3 -m venv .venv
     ```

3. **Activate Virtual Environment & Install Dependencies**:
   * On Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     .\.venv\Scripts\pip install -r requirements.txt
     ```
   * On Windows (CMD):
     ```cmd
     .venv\Scripts\activate.bat
     .venv\Scripts\pip install -r requirements.txt
     ```
   * On macOS/Linux:
     ```bash
     source .venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Launch the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```
   The application will automatically open in your default browser at `http://localhost:8501`.

---

## 💡 Feature Highlights

* **Modern Dark UI**: Features custom CSS glassmorphism metric cards, responsive multi-tab layout, and dynamic sidebar navigation.
* **Real-Time NLP Inspection**: Displays step-by-step breakdown of text cleaning (Raw -> Cleaned -> Tokens -> Filtered Words).
* **Automated Data Export**: Download scraped sentiment datasets and GA4 traffic metrics as CSV files.
* **Executive Summary Tab**: Generates a high-level managerial report summarizing key sentiment trends and traffic insights.

---

## 🎓 Course Project Credits
Created for the **Web & Social Media Analytics** Course. Built with Python, Streamlit, NLTK, TextBlob, BeautifulSoup4, Pandas, and Plotly.
