<div align="center">

# 🎬 Movie Economics & Ratings Analytics Pipeline

### *200 movies. Two APIs joined on imdb_id. 8 answered business questions, no database required.*

---

<!-- Tech Stack -->
![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12%20|%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.21+-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-11557c?style=for-the-badge&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.11+-4c72b0?style=for-the-badge&logo=python&logoColor=white)

<!-- Links -->
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Viraj%20More-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/viraj-uttam-more-a24a80391)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:virajmore.data888@gmail.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

---

**[📝 Full Report](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/tree/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/docs) · [📦 Output](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/tree/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/Output) · [🐍 Python Code](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/tree/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/python) · [📦 Requirements](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/blob/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/requirements.txt) · [🤝 Contributing](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/blob/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/CONTRIBUTING.md)**

</div>

---

## 👋 About This Project

This is an **end to end data analytics pipeline** built on **Python and Pandas**, going from two live APIs all the way to a written report and a set of charts, with no database required.

Movie metadata and movie ratings live in two completely separate places. TMDB knows what a movie cost to make and how much it earned. OMDB knows how critics and audiences actually rated it. Neither API on its own can answer the question that actually matters to a studio: *does spending more money make a better movie?*

This project pulls both datasets live: 200 movies of budget/revenue/genre data from TMDB, joined with IMDb, Rotten Tomatoes, and Metascore ratings from OMDB. It cleans each source independently, verifies and joins them on `imdb_id`, then explores the result with charts and a written insights report.

> If you are a recruiter or fellow analyst, the TL;DR below tells you everything in 30 seconds. The rest of the README is for anyone who wants the full pipeline detail.

---

## ⚡ TL;DR - Key Findings

| # | Finding | Business Impact |
|---|---------|----------------|
| 1 | 🎯 **Adventure has the best average ROI at 71.1x** across 53 movies with both budget & revenue reported | Adventure is the highest-return genre by a wide margin, a strong signal for where budget bets pay off |
| 2 | ⭐ **IMDb and Rotten Tomatoes agree fairly well** (correlation of 0.75 across 192 movies) | Critic and audience scores are broadly aligned, but not identical; outliers are worth investigating individually |
| 3 | 📉 **Budget has almost no link to IMDb rating** (correlation of -0.13) | Spending more does not buy a better-rated movie; rating quality is driven by something other than budget |
| 4 | 🎬 **Action is the most common genre** (60 movies), followed by Adventure (53) | Reflects a market heavily weighted toward big, high-budget action releases |
| 5 | 📊 **Average IMDb rating has drifted down over time**, 8.60 in 1977 vs 7.20 in 2026 | Older, smaller releases in this dataset rate higher on average than recent ones |
| 6 | 💰 **199/200 movies report budget, 200/200 report revenue** | Very high data completeness; TMDB's per-movie detail endpoint reliably fills in financials |

---

## 🎯 What Makes This Project Different

Most movie analytics projects work off a single pre-packaged Kaggle CSV. This one is built entirely on live API calls.

| Typical Movie Analytics Project | This Project |
|---|---|
| Starts from one static, pre-cleaned CSV | Pulls fresh data live from TMDB and OMDB on every run |
| Uses a single data source | Joins two independent APIs on `imdb_id` to combine financials with ratings |
| Cleans the data once | Explores raw API responses first, then cleans, then re-verifies before joining |
| Shows a single summary stat | Answers 8 specific business questions with numpy-backed statistics |
| Notebook with mixed logic | Modular pipeline: fetch, clean, EDA, verify, visualize, and report as separate scripts |
| Needs a database | Runs entirely off local CSVs, no database setup required |

---

## 💡 Key Business Insights

### 1. 🎯 Best ROI by Genre

**Adventure leads with an average ROI of 71.1x**, based on 53 movies with both budget and revenue reported. This is the single strongest financial signal in the dataset: Adventure movies return far more per dollar spent than any other genre.

---

### 2. ⭐ IMDb vs Rotten Tomatoes Agreement

Across 192 movies with both scores available, IMDb and Rotten Tomatoes have a **correlation of 0.75**, fairly well aligned, but far from a perfect match. The biggest gap in the dataset belongs to **Transformers: Revenge of the Fallen**, at an IMDb rating of 6.0/10 against a Rotten Tomatoes score of just 19%.

---

### 3. 📉 Budget vs Rating Relationship

The correlation between budget and IMDb rating is **-0.13**, essentially no relationship, and if anything a very weak negative one. A bigger production budget does not translate into a better-rated movie.

---

### 4. 📦 Data Completeness

**199 of 200 movies (99.5%) report usable budget data**, and **200 of 200 (100.0%) report usable revenue data**. TMDB's per-movie detail call reliably fills in financials that the list/discover endpoints leave out.

---

### 5. 🎬 Most Common Genre

**Action appears most often in the dataset at 60 movies**, followed by Adventure at 53. This reflects the dataset's skew toward big-budget, wide-release films.

---

### 6. 📈 IMDb Rating Trend Over Time

Average IMDb rating has moved from **8.60 in 1977 down to 7.20 in 2026**. Earlier, more selective releases in this dataset rate noticeably higher than the broader, more recent slate.

---

### 7. 💵 Best Rating-Per-Dollar

**Star Wars (1977)** delivers the best return on rating relative to spend: an IMDb score of 8.6/10 on an $11.0M budget, making it the standout value pick in the dataset.

---

## 📋 Key Metrics At A Glance

| Metric | Value |
|--------|-------|
| **Total Movie Records** | 200 |
| **Best ROI Genre** | Adventure (71.1x) |
| **IMDb vs Rotten Tomatoes Correlation** | 0.75 (192 movies) |
| **Budget vs IMDb Rating Correlation** | -0.13 |
| **Most Common Genre** | Action (60 movies) |
| **Budget Data Completeness** | 199 / 200 (99.5%) |
| **Revenue Data Completeness** | 200 / 200 (100.0%) |
| **IMDb Rating Trend (1977 → 2026)** | 8.60 → 7.20 |
| **Best Rating-Per-Dollar Movie** | Star Wars (8.6/10 on $11.0M) |

---

## ⚙️ Technical Architecture

Built as a two-API pipeline joined on a shared key, so the project mirrors how real analytics teams combine disconnected data sources without needing a database.

| Technique | Implementation Detail |
|---|---|
| **Dual API Integration** | TMDB (budget, revenue, genres, runtime) and OMDB (IMDb, Rotten Tomatoes, Metascore) pulled live via `fetch.py` |
| **Data Cleaning** | Zero-value budget/revenue treated as "not reported" (flagged, not zeroed); OMDB's literal `"N/A"` strings converted to proper nulls, via `cleaning.py` |
| **Exploratory Data Analysis** | Distribution plots on raw, pre-cleaning API responses via `EDA.py`, to measure real-world data quality |
| **Verification Layer** | Cleaned tables re-checked and joined on `imdb_id` only once both pass, via `verification.py` |
| **Master Table Construction** | `movies` + `ratings` joined into a single master table, with a trimmed `insights_subset.csv` built for downstream analysis |
| **Business Insight Generation** | 8 movie-economics questions answered with `numpy` in `insights.py`, printed and saved as a text report |
| **Visualization** | 5 charts built with `Matplotlib`/`Seaborn` in `visualization.py` |

---

## 🛠️ Skills Demonstrated

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `REST API Integration` · `Data Cleaning` · `Data Verification` · `Exploratory Data Analysis` · `Business Intelligence` · `Data Visualization`

---

## 🚀 Run This Project Locally

### Prerequisites
- Python 3.10 to 3.13
- pip
- Free API keys from [TMDB](https://www.themoviedb.org/) and [OMDB](https://www.omdbapi.com/)

### Step 1: Clone
```bash
git clone https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis.git
cd movie-budget-revenue-ratings-analysis
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Keys

Copy `.env.example` to `.env` and fill in your keys:

```
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

Only `fetch.py` reads these keys directly; `cleaning.py` and `EDA.py` get raw data by importing `fetch.py`'s functions and never touch the keys themselves.

### Step 4: Run the Pipeline
```bash
python -i cleaning.py       # pulls live data via fetch.py, cleans it -> Output/cleaned_data/
python -i EDA.py            # exploratory plots on raw API data -> Output/eda_plots/
python -i verification.py   # verifies, joins on imdb_id, builds master table -> Output/master_data/
python visualization.py     # 5 charts -> Output/charts/
python insights.py          # insights report -> Output/reports/
```

Each step depends on the files the previous step produces, so run them in order. See the full run guide with function calls in [docs/](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/tree/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/docs).

---

## 📦 Dependencies

📄 [View requirements.txt](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/blob/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/requirements.txt)

```
pandas
numpy
matplotlib
seaborn
requests
python-dotenv
```

---

## 📊 Dataset At A Glance

| Attribute | Value |
|---|---|
| **Source** | Live TMDB API (movie metadata) joined with live OMDB API (ratings), not a static pre-packaged CSV |
| **Total Movie Records** | 200 |
| **Join Key** | `imdb_id` |
| **TMDB Fields** | budget, revenue, genres, runtime, popularity, vote average/count |
| **OMDB Fields** | IMDb rating, Rotten Tomatoes score, Metascore, box office, awards |
| **Movies with Full Budget/Revenue** | 199 / 200 |
| **Movies with Both Rating Scores** | 192 / 200 |

---

## 📂 Repository Structure

```
movie-budget-revenue-ratings-analysis/
|
+-- python/
|   +-- fetch.py                       # TMDB + OMDB API connector functions
|   +-- cleaning.py                    # Cleans raw data pulled via fetch.py
|   +-- EDA.py                         # Exploratory analysis on raw API data
|   +-- verification.py                # Verifies cleaned data, joins on imdb_id, builds master table
|   +-- visualization.py               # 5 charts from insights_subset.csv
|   +-- insights.py                    # 8 movie-economics questions answered, saved as report
|
+-- Output/
|   +-- cleaned_data/                  # movies_cleaned.csv, ratings_cleaned.csv
|   +-- master_data/                   # master_table.csv, insights_subset.csv
|   +-- eda_plots/                     # Raw distribution plots
|   +-- charts/                        # 5 charts (ROI, ratings, budget/revenue, genre, trend)
|   +-- reports/                       # insights_report.txt
|
+-- docs/
|   +-- Movie_Analysis_Report_Viraj_More.pdf   # Full written report
|   +-- Movie_Analysis_Presentation.pdf        # Stakeholder-ready slide deck
|
+-- requirements.txt
+-- CONTRIBUTING.md
+-- .env.example
+-- .gitignore
+-- README.md
```

---

## 🤝 Connect & Contribute

- 🔗 **LinkedIn:** [Viraj More](https://www.linkedin.com/in/viraj-uttam-more-a24a80391)
- 📧 **Email:** [virajmore.data888@gmail.com](mailto:virajmore.data888@gmail.com)
- 💻 **GitHub:** [movie-budget-revenue-ratings-analysis](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis)

Found something to improve? Open an **Issue** or submit a **Pull Request**, contributions are welcome.
Read the **[Contributing Guide](https://github.com/Virajmore888/movie-budget-revenue-ratings-analysis/blob/c1a1043b2ad7a4b5be82e5dcb0e8bbbd92228f30/CONTRIBUTING.md)** before submitting.

---

## 📄 License

MIT License, see [LICENSE](./LICENSE) for details.

---

<div align="center">

**Built end to end with Python and Pandas**

*If this project added value, consider leaving a ⭐ on the repo, it helps others find it too.*

</div>
