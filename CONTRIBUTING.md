# Contributing

Thanks for your interest in this project! This is a personal portfolio
project, but contributions, suggestions, and bug reports are welcome.

## How to contribute

1. Fork the repository
2. Create a new branch for your change
   ```
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test that the pipeline still runs end to end (see order below)
5. Commit your changes with a clear message
6. Push to your fork and open a Pull Request

## Project structure / pipeline order

The scripts are meant to be run in this order, since each stage
depends on the output of the one before it:

1. `cleaning.py` - pulls raw data live from the TMDB and OMDB APIs
   via `fetch.py`, cleans it, and writes `<table>_cleaned.csv`
2. `EDA.py` - explores the raw API data and generates plots in
   `Output/eda_plots/`
3. `verification.py` - validates cleaned data, joins movies and
   ratings on `imdb_id`, and builds `Output/master_data/`
4. `visualization.py` - generates charts in `Output/charts/`
5. `insights.py` - generates `Output/reports/insights_report.txt`

## Setting up locally

```
pip install -r requirements.txt
cp .env.example .env
# fill in TMDB_API_KEY and OMDB_API_KEY in .env
python -i cleaning.py
python EDA.py
python -i verification.py
python visualization.py
python insights.py
```

## Reporting issues

If you find a bug or have a suggestion, please open an issue with:
- A clear description of the problem or idea
- Steps to reproduce (for bugs)
- Expected vs actual behavior

## Code style

- Keep new dependencies to a minimum
- Follow the existing pattern of anchoring file paths to the
  script's own location
- Only `fetch.py` should read API keys directly, other scripts get
  raw data by importing `fetch.py`'s functions
