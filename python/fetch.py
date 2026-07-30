# =================================================================
# fetch.py — API connection layer (TMDB + OMDB)
# =================================================================
# This module ONLY talks to the two APIs. It does not clean or save
# anything — cleaning.py and EDA.py import these functions and read
# raw API data directly.
# =================================================================

import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

TMDB_BASE = "https://api.themoviedb.org/3"
OMDB_BASE = "https://www.omdbapi.com/"

# Check keys are present, fail early with a clear message
_missing = [name for name, val in
            [("TMDB_API_KEY", TMDB_API_KEY), ("OMDB_API_KEY", OMDB_API_KEY)]
            if not val]
if _missing:
    raise ValueError(f"Missing values in .env: {_missing}")


# -----------------------------------------------------------------
# TMDB — raw movie list ("movies" table)
# -----------------------------------------------------------------
def fetch_tmdb_movies(pages=10, sort_by="revenue.desc"):
    """
    Pulls `pages` pages (20 movies/page) from TMDB's /discover/movie
    endpoint, then makes a SECOND call per movie to /movie/{id} to get
    budget, revenue, and imdb_id — the discover/list endpoint does NOT
    return these fields, only the details endpoint does.

    Returns a raw (uncleaned) DataFrame — one row per movie.
    """
    rows = []
    for page in range(1, pages + 1):
        resp = requests.get(f"{TMDB_BASE}/discover/movie", params={
            "api_key": TMDB_API_KEY,
            "sort_by": sort_by,
            "page": page,
            "include_adult": "false",
        })
        resp.raise_for_status()
        results = resp.json().get("results", [])

        for movie in results:
            detail = requests.get(f"{TMDB_BASE}/movie/{movie['id']}", params={
                "api_key": TMDB_API_KEY
            })
            if detail.status_code != 200:
                continue  # skip movies TMDB can't return details for
            d = detail.json()

            rows.append({
                "tmdb_id": d.get("id"),
                "imdb_id": d.get("imdb_id"),          # needed to join with OMDB
                "title": d.get("title"),
                "release_date": d.get("release_date"),
                "genres": [g["name"] for g in d.get("genres", [])],  # list, not flat yet
                "budget": d.get("budget"),             # often 0 — not reported
                "revenue": d.get("revenue"),            # often 0 — not reported
                "runtime": d.get("runtime"),
                "original_language": d.get("original_language"),
                "production_companies": [c["name"] for c in d.get("production_companies", [])],
                "popularity": d.get("popularity"),
                "tmdb_vote_average": d.get("vote_average"),
                "tmdb_vote_count": d.get("vote_count"),
            })
            time.sleep(0.02)  # stay well under TMDB's ~40 req/sec soft limit

    return pd.DataFrame(rows)


# -----------------------------------------------------------------
# OMDB — raw ratings lookup ("ratings" table), one call per imdb_id
# -----------------------------------------------------------------
def fetch_omdb_ratings(imdb_ids):
    """
    Given a list of imdb_ids, queries OMDB for each and returns a raw
    DataFrame of ratings/box-office data. OMDB returns "N/A" (a string,
    not a real null) for any field it doesn't have — that gets handled
    in cleaning.py, not here, since this function's job is only to
    fetch what the API actually sends back.
    """
    rows = []
    for imdb_id in imdb_ids:
        if not imdb_id:
            continue
        resp = requests.get(OMDB_BASE, params={
            "i": imdb_id,
            "apikey": OMDB_API_KEY,
            "tomatoes": "true",
        })
        if resp.status_code != 200:
            continue
        d = resp.json()
        if d.get("Response") != "True":
            continue  # OMDB has no record for this imdb_id

        rt_rating = "N/A"
        for r in d.get("Ratings", []):
            if r.get("Source") == "Rotten Tomatoes":
                rt_rating = r.get("Value")

        rows.append({
            "imdb_id": d.get("imdbID"),
            "imdb_rating": d.get("imdbRating"),        # string, "N/A" possible
            "imdb_votes": d.get("imdbVotes"),           # string with commas, "N/A" possible
            "metascore": d.get("Metascore"),            # string, "N/A" possible
            "rotten_tomatoes": rt_rating,                # string like "83%" or "N/A"
            "rated": d.get("Rated"),
            "box_office": d.get("BoxOffice"),            # string like "$389,804,217" or "N/A"
            "awards": d.get("Awards"),
        })
        time.sleep(0.05)  # OMDB free tier: 1,000 req/day, be gentle

    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Quick smoke test — confirms both keys work before running the full pipeline
    test_movies = fetch_tmdb_movies(pages=1)
    print(f"✅ TMDB OK — pulled {len(test_movies)} movies")
    test_ratings = fetch_omdb_ratings(test_movies["imdb_id"].dropna().head(3).tolist())
    print(f"✅ OMDB OK — pulled {len(test_ratings)} ratings")
