# =================================================================
# verification.py — re-checks cleaned CSVs, joins movies + ratings
# into master_table.csv, then builds insights_subset.csv
# =================================================================
#   python -i verification.py
#   >>> movies_df  = run_verification('movies')
#   >>> ratings_df = run_verification('ratings')
#   >>> finalize_pipeline()
# =================================================================

import os
import pandas as pd

PATH = os.path.dirname(os.path.abspath(__file__))
CLEANED_DIR = os.path.join(PATH, "Output", "cleaned_data")
MASTER_DIR = os.path.join(PATH, "Output", "master_data")
os.makedirs(MASTER_DIR, exist_ok=True)

_verified = {}


def _verify_movies(df):
    checks = {
        "no duplicate tmdb_id": df["tmdb_id"].is_unique,
        "no null imdb_id": df["imdb_id"].notna().all(),
        "release_year in sane range": df["release_year"].between(1900, 2027).all(),
        "roi only set where both budget & revenue reported":
            (df.loc[df["roi"].notna(), "budget_reported"] &
             df.loc[df["roi"].notna(), "revenue_reported"]).all(),
    }
    return checks


def _verify_ratings(df):
    checks = {
        "no duplicate imdb_id": df["imdb_id"].is_unique,
        "imdb_rating in 0-10 range": df["imdb_rating"].dropna().between(0, 10).all(),
        "rotten_tomatoes in 0-100 range": df["rotten_tomatoes"].dropna().between(0, 100).all(),
        "no leftover 'N/A' strings": not (df.astype(str) == "N/A").any().any(),
    }
    return checks


def run_verification(table):
    path = os.path.join(CLEANED_DIR, f"{table}_cleaned.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found — run cleaning.py first")

    df = pd.read_csv(path)

    if table == "movies":
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        checks = _verify_movies(df)
    elif table == "ratings":
        checks = _verify_ratings(df)
    else:
        raise ValueError(f"Unknown table: {table}")

    print(f"\n<----------VERIFYING '{table}'---------->")
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        all_passed = all_passed and passed

    if not all_passed:
        print(f"⚠️  '{table}' failed one or more checks — fix in cleaning.py before finalizing")
    else:
        print(f"'{table}' passed all checks ({len(df)} rows)")

    _verified[table] = df
    return df


def finalize_pipeline():
    required = ["movies", "ratings"]
    missing = [t for t in required if t not in _verified]
    if missing:
        print(f"❌ Cannot finalize — run_verification() not yet called for: {missing}")
        return

    movies = _verified["movies"]
    ratings = _verified["ratings"]

    # The actual join — this is the core of the project
    master = movies.merge(ratings, on="imdb_id", how="left", suffixes=("", "_omdb"))
    match_rate = ratings["imdb_id"].isin(movies["imdb_id"]).sum() / max(len(movies), 1) * 100
    print(f"\nJoin coverage: {master['imdb_rating'].notna().sum()} / {len(master)} "
          f"movies matched to an OMDB rating ({match_rate:.1f}%)")

    master_path = os.path.join(MASTER_DIR, "master_table.csv")
    master.to_csv(master_path, index=False)
    print(f"Saved -> {master_path}")

    # Subset used downstream by visualization.py / insights.py
    subset_cols = [
        "title", "release_year", "genre_primary", "runtime",
        "budget", "revenue", "roi", "budget_reported", "revenue_reported",
        "popularity", "tmdb_vote_average", "tmdb_vote_count",
        "imdb_rating", "imdb_votes", "rotten_tomatoes", "metascore", "box_office",
    ]
    subset = master[[c for c in subset_cols if c in master.columns]]
    subset_path = os.path.join(MASTER_DIR, "insights_subset.csv")
    subset.to_csv(subset_path, index=False)
    print(f"Saved -> {subset_path}")

    return master


if __name__ == "__main__":
    print("Run interactively: python -i verification.py")
    print(">>> movies_df = run_verification('movies')")
    print(">>> ratings_df = run_verification('ratings')")
    print(">>> finalize_pipeline()")
