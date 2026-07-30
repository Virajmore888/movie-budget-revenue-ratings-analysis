# =================================================================
# cleaning.py — reads raw data straight from the APIs (via fetch.py),
# cleans it, saves <table>_cleaned.csv
# =================================================================
# Run interactively:
#
#   python -i cleaning.py
#   >>> movies_df  = run_cleaning('movies')
#   >>> ratings_df = run_cleaning('ratings', movies_df)
# =================================================================

import os
import numpy as np
import pandas as pd
from fetch import fetch_tmdb_movies, fetch_omdb_ratings

PATH = os.path.dirname(os.path.abspath(__file__))
CLEANED_DIR = os.path.join(PATH, "Output", "cleaned_data")
os.makedirs(CLEANED_DIR, exist_ok=True)

# How many TMDB pages to pull (20 movies/page). Kept small by default
# so a first run finishes quickly — raise this for a bigger dataset.
TMDB_PAGES = 10


def _clean_movies(df):
    df = df.copy()

    # Drop movies TMDB couldn't return an imdb_id for — nothing to join later
    df = df.dropna(subset=["imdb_id"])
    df = df[df["imdb_id"] != ""]

    # Duplicates can slip in across pages (TMDB pagination overlap on re-sorts)
    df = df.drop_duplicates(subset="tmdb_id")

    # release_date -> proper datetime, pull out year separately
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year

    # genres/production_companies come back as Python lists — flatten to strings
    df["genres"] = df["genres"].apply(lambda g: ", ".join(g) if isinstance(g, list) else "")
    df["genre_primary"] = df["genres"].apply(lambda g: g.split(",")[0].strip() if g else "Unknown")
    df["production_companies"] = df["production_companies"].apply(
        lambda c: ", ".join(c) if isinstance(c, list) else ""
    )

    # budget/revenue of 0 means "not reported by TMDB", not "movie made $0"
    # flag it first, then null out the same rows via .loc[] so the
    # "which rows changed" condition is explicit and reusable
    df["budget_reported"] = df["budget"] > 0
    df["revenue_reported"] = df["revenue"] > 0
    df.loc[~df["budget_reported"], "budget"] = np.nan
    df.loc[~df["revenue_reported"], "revenue"] = np.nan

    # ROI only makes sense where both are actually reported
    df["roi"] = np.where(
        df["budget_reported"] & df["revenue_reported"],
        (df["revenue"] - df["budget"]) / df["budget"],
        np.nan,
    )

    df["runtime"] = df["runtime"].replace(0, np.nan)

    return df.reset_index(drop=True)


def _clean_ratings(df):
    df = df.copy()
    df = df.drop_duplicates(subset="imdb_id")

    # OMDB sends "N/A" as a literal string for missing numeric fields —
    # this is the main real-world messiness on this side of the join
    na_like = {"N/A", "", None}
    for col in ["imdb_rating", "metascore", "box_office", "imdb_votes"]:
        df[col] = df[col].apply(lambda v: np.nan if v in na_like else v)

    df["imdb_rating"] = pd.to_numeric(df["imdb_rating"], errors="coerce")
    df["metascore"] = pd.to_numeric(df["metascore"], errors="coerce")
    df["imdb_votes"] = (
        df["imdb_votes"].astype(str).str.replace(",", "", regex=False)
    )
    df["imdb_votes"] = pd.to_numeric(df["imdb_votes"], errors="coerce")

    # rotten_tomatoes comes as "83%" (string) or "N/A" — strip to a number
    df["rotten_tomatoes"] = df["rotten_tomatoes"].apply(
        lambda v: np.nan if v in na_like else float(str(v).replace("%", ""))
    )

    # box_office comes as "$389,804,217" (string) or "N/A"
    df["box_office"] = df["box_office"].apply(
        lambda v: np.nan if v in na_like
        else float(str(v).replace("$", "").replace(",", ""))
    )

    return df.reset_index(drop=True)


def run_cleaning(table, dependency_df=None):
    """
    table: 'movies' or 'ratings'
    dependency_df: for 'ratings', pass the cleaned movies_df so we know
                   which imdb_ids to look up on OMDB.
    """
    if table == "movies":
        raw = fetch_tmdb_movies(pages=TMDB_PAGES)
        print(f"Raw TMDB pull: {len(raw)} movies")
        cleaned = _clean_movies(raw)
        print(f"After cleaning: {len(cleaned)} movies "
              f"({cleaned['budget_reported'].sum()} with budget, "
              f"{cleaned['revenue_reported'].sum()} with revenue)")

    elif table == "ratings":
        if dependency_df is None:
            raise ValueError("run_cleaning('ratings', ...) needs the cleaned movies_df")
        imdb_ids = dependency_df["imdb_id"].dropna().unique().tolist()
        raw = fetch_omdb_ratings(imdb_ids)
        print(f"Raw OMDB pull: {len(raw)} / {len(imdb_ids)} imdb_ids matched")
        cleaned = _clean_ratings(raw)
        na_count = cleaned["rotten_tomatoes"].isna().sum()
        print(f"After cleaning: {len(cleaned)} ratings "
              f"({na_count} missing Rotten Tomatoes score)")

    else:
        raise ValueError(f"Unknown table: {table}")

    out_path = os.path.join(CLEANED_DIR, f"{table}_cleaned.csv")
    cleaned.to_csv(out_path, index=False)
    print(f"Saved -> {out_path}")
    return cleaned


if __name__ == "__main__":
    print("Run interactively: python -i cleaning.py")
    print(">>> movies_df = run_cleaning('movies')")
    print(">>> ratings_df = run_cleaning('ratings', movies_df)")
