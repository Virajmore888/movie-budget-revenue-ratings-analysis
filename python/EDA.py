# =================================================================
# EDA.py — exploratory checks on RAW API data (pre-cleaning)
# =================================================================
# Pulls straight from the APIs via fetch.py, same as cleaning.py does,
# so you can see exactly how messy the raw response is before any
# cleaning happens.
#
#   python -i EDA.py
#   >>> df = run_eda('movies')
#   >>> df = run_eda('ratings', df)   # pass a movies df to look up ratings for
# =================================================================

import os
import matplotlib.pyplot as plt
import seaborn as sns
from fetch import fetch_tmdb_movies, fetch_omdb_ratings

PATH = os.path.dirname(os.path.abspath(__file__))
PLOT_DIR = os.path.join(PATH, "Output", "eda_plots")
os.makedirs(PLOT_DIR, exist_ok=True)

TMDB_PAGES = 5  # smaller sample for a quick EDA pass


def _explore(df, name):
    print(f"\n<----------RAW '{name}' EXPLORATION---------->")
    print(f"Shape: {df.shape}")
    print(f"\nNulls per column:\n{df.isna().sum()}")
    print(f"\nDtypes:\n{df.dtypes}")
    print(f"\nFirst 5 rows:\n{df.head()}")


def run_eda(table, dependency_df=None):
    if table == "movies":
        df = fetch_tmdb_movies(pages=TMDB_PAGES)
        _explore(df, "movies")

        # budget/revenue: how many movies actually report these?
        print(f"\nMovies with budget = 0 (not reported): "
              f"{(df['budget'] == 0).sum()} / {len(df)}")
        print(f"Movies with revenue = 0 (not reported): "
              f"{(df['revenue'] == 0).sum()} / {len(df)}")
        print(f"Movies missing imdb_id entirely: {df['imdb_id'].isna().sum()}")

        plt.figure(figsize=(8, 5))
        sns.histplot(df[df["revenue"] > 0]["revenue"] / 1e6, bins=30)
        plt.title("Raw TMDB — Revenue Distribution (reported only, $M)")
        plt.xlabel("Revenue ($M)")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, "raw_revenue_distribution.png"))
        plt.close()

    elif table == "ratings":
        if dependency_df is None:
            raise ValueError("run_eda('ratings', movies_df) needs a movies df")
        imdb_ids = dependency_df["imdb_id"].dropna().unique().tolist()
        df = fetch_omdb_ratings(imdb_ids)
        _explore(df, "ratings")

        na_counts = (df[["imdb_rating", "metascore", "rotten_tomatoes", "box_office"]]
                     .apply(lambda col: (col == "N/A").sum() if col.dtype == object
                            else col.isna().sum()))
        print(f"\n'N/A' string counts per rating field:\n{na_counts}")

        plt.figure(figsize=(8, 5))
        rt_present = df[df["rotten_tomatoes"] != "N/A"]
        rt_vals = rt_present["rotten_tomatoes"].dropna().astype(str).str.replace("%", "").astype(float)
        sns.histplot(rt_vals, bins=20)
        plt.title("Raw OMDB — Rotten Tomatoes Score Distribution (where available)")
        plt.xlabel("RT Score (%)")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, "raw_rotten_tomatoes_distribution.png"))
        plt.close()

    else:
        raise ValueError(f"Unknown table: {table}")

    print(f"\nPlots saved -> {PLOT_DIR}/")
    return df


if __name__ == "__main__":
    print("Run interactively: python -i EDA.py")
    print(">>> df = run_eda('movies')")
    print(">>> df = run_eda('ratings', df)")
