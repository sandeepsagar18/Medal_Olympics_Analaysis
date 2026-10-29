# 🏅 Olympics Data Analytics Web Application (1896 – 2024)

An interactive, end-to-end data science and analytics dashboard built with **Streamlit**, **Pandas**, and **Plotly** to explore 128 years of modern Summer Olympic history, updated with verified results from **Tokyo 2020** and **Paris 2024**.

![Olympics Banner](https://images.unsplash.com/photo-1569517282132-25d22f4573e6?auto=format&fit=crop&w=1200&q=80)

---

## 🚀 Key Features

### 1. 🌍 All-Time & Year-Wise Medal Tally
- Filterable by **Olympic Year (1896–2024)** and **Country / Delegation**.
- Official Olympic ranking tiebreakers (sorted by Gold 🥇, Silver 🥈, Bronze 🥉).
- **Interactive Choropleth World Map**: Visualize global medal distributions with rich hover cards.
- **Data Export**: One-click download of filtered medal tallies in CSV format.

### 2. 📊 Historic Overall Analysis
- Track grand totals: Editions, Host Cities, Sports, Events, Athletes, and Participating Nations.
- Growth trajectory lines for participating countries, athlete counts, and events over time.
- High-resolution interactive heatmap showing the density and introduction of events across sports.
- Most decorated Olympic athletes of all time and filtered by individual sport.

### 3. 🏆 Country-Wise Deep Dive
- Detailed trajectory curves showing a country's medal haul per edition.
- Quick metrics displaying total medals, best Olympic edition, and peak single-games performance.
- Sport specialization heatmap identifying disciplines where a nation dominates.
- Top 10 most successful athletes for any chosen nation.

### 4. ⚔️ Head-to-Head Country Comparison
- Compare any two countries side-by-side (e.g., *USA vs China*, *India vs Pakistan*, *UK vs France*).
- Comparative medal timeline charts showing historic dominance shifts.
- Comparative tabular data breakdown.

### 5. 🏃 Athlete Demographics & Trends
- **Age Distribution**: Kernel density estimates comparing age profiles of gold, silver, bronze, and non-medalists.
- **Physique Explorer (Height vs Weight)**: Interactive scatter plot with athlete-level tooltips across sports and genders.
- **Gender Inclusivity**: Male vs Female participation progression over the decades.

---

## 🛠️ Tech Stack
- **Frontend / Dashboard Framework**: Streamlit
- **Data Processing & Wrangling**: Pandas, NumPy
- **Interactive Visualizations**: Plotly Express, Plotly Figure Factory, Seaborn, Matplotlib

---

## 📁 Repository Structure
```
├── app.py                      # Main Streamlit web application & UI logic
├── helper.py                   # Data analytics & aggregation utility functions
├── preprocessor.py             # Data cleaning, season filtering & one-hot encoding
├── athlete_events.csv          # Merged Olympic dataset (1896 - 2024)
├── noc_regions.csv             # 3-letter NOC to Country/Region mapping
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
└── README.md                   # Documentation & overview
```

---

## 💻 Getting Started

### Prerequisites
Make sure you have Python 3.9+ installed.

### 1. Clone the Repository
```bash
git clone https://github.com/sandeepsagar18/Medal_Olympics_Analaysis.git
cd Medal_Olympics_Analaysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Then open your browser at **`http://localhost:8501`**.

---

## 📈 Recent Updates
- ✅ **Tokyo 2020 & Paris 2024 Verified Integration**: Rebuilt and validated directly from official International Olympic Committee (IOC) results.
- ✅ **Performance Caching**: Added `@st.cache_data` for instant page loads.
- ✅ **Country Comparison Engine**: Added head-to-head comparison module.
- ✅ **CSV Exporter**: Export filtered insights directly from the dashboard.

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
