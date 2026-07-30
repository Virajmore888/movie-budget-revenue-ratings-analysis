# =================================================================
# insights.py — 8 movie-economics questions, answered from
# insights_subset.csv (built by finalize_pipeline() in verification.py)
# =================================================================
#   python insights.py
# =================================================================

import os
import numpy as np
import pandas as pd

PATH = os.path.dirname(os.path.abspath(__file__))
SUBSET_PATH = os.path.join(PATH, "Output", "master_data", "insights_subset.csv")
REPORT_DIR = os.path.join(PATH, "Output", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)


def load_subset():
    if not os.path.exists(SUBSET_PATH):
        raise FileNotFoundError(
            "insights_subset.csv not found — run finalize_pipeline() in "
            "verification.py first"
        )
    return pd.read_csv(SUBSET_PATH)


def generate_insights(df):
    lines = []

    def report(question, answer):
        lines.append(f"Q: {question}\nA: {answer}\n")
        print(f"Q: {question}\nA: {answer}\n")

    # 1. Highest ROI genre
    roi_df = df[df["roi"].notna()]
    genre_roi = roi_df.groupby("genre_primary")["roi"].mean().sort_values(ascending=False)
    report(
        "Which genre has the best average ROI (revenue vs budget)?",
        f"{genre_roi.index[0]} leads with an average ROI of {genre_roi.iloc[0]:.1f}x "
        f"(based on {roi_df.groupby('genre_primary').size()[genre_roi.index[0]]} movies "
        f"with both budget & revenue reported)."
    )

    # 2. IMDb vs Rotten Tomatoes agreement
    both = df.dropna(subset=["imdb_rating", "rotten_tomatoes"])
    corr = both["imdb_rating"].corr(both["rotten_tomatoes"])
    report(
        "How closely do IMDb ratings and Rotten Tomatoes scores agree?",
        f"Correlation of {corr:.2f} across {len(both)} movies with both scores — "
        f"{'fairly aligned' if corr > 0.6 else 'noticeably divergent'}."
    )

    # 3. Biggest critic/audience gap
    both["gap"] = (both["imdb_rating"] * 10) - both["rotten_tomatoes"]
    biggest_gap = both.loc[both["gap"].abs().idxmax()]
    report(
        "Which movie has the biggest gap between IMDb and Rotten Tomatoes?",
        f"'{biggest_gap['title']}' — IMDb {biggest_gap['imdb_rating']}/10 vs "
        f"RT {biggest_gap['rotten_tomatoes']:.0f}%."
    )

    # 4. Budget vs quality
    budget_rating = df.dropna(subset=["budget", "imdb_rating"])
    corr_br = budget_rating["budget"].corr(budget_rating["imdb_rating"])
    report(
        "Does a bigger budget mean a better-rated movie?",
        f"Correlation between budget and IMDb rating is {corr_br:.2f} — "
        f"{'weak/no relationship' if abs(corr_br) < 0.3 else 'moderate relationship'}."
    )

    # 5. Data coverage — how much budget/revenue data actually exists
    report(
        "What share of movies have usable budget & revenue data?",
        f"{df['budget_reported'].sum()} / {len(df)} movies report budget "
        f"({df['budget_reported'].mean()*100:.1f}%); "
        f"{df['revenue_reported'].sum()} / {len(df)} report revenue "
        f"({df['revenue_reported'].mean()*100:.1f}%)."
    )

    # 6. Most popular genre by count
    genre_counts = df["genre_primary"].value_counts()
    report(
        "Which genre appears most often in this dataset?",
        f"{genre_counts.index[0]} ({genre_counts.iloc[0]} movies), "
        f"followed by {genre_counts.index[1]} ({genre_counts.iloc[1]})."
    )

    # 7. Year-over-year average rating trend
    yearly = df.dropna(subset=["release_year", "imdb_rating"]).groupby("release_year")["imdb_rating"].mean()
    report(
        "Has average IMDb rating trended up or down across release years?",
        f"From {int(yearly.index.min())} to {int(yearly.index.max())}, average IMDb "
        f"rating went from {yearly.iloc[0]:.2f} to {yearly.iloc[-1]:.2f}."
    )

    # 8. Best value-for-money movie (rating per $M budget)
    vfm = df.dropna(subset=["budget", "imdb_rating"]).copy()
    vfm = vfm[vfm["budget"] > 0]
    vfm["rating_per_million"] = vfm["imdb_rating"] / (vfm["budget"] / 1e6)
    best_value = vfm.loc[vfm["rating_per_million"].idxmax()]
    report(
        "Which movie delivered the best rating-per-dollar-of-budget?",
        f"'{best_value['title']}' — IMDb {best_value['imdb_rating']}/10 on a "
        f"${best_value['budget']/1e6:.1f}M budget."
    )

    return "\n".join(lines)


if __name__ == "__main__":
    df = load_subset()
    report_text = generate_insights(df)
    out_path = os.path.join(REPORT_DIR, "insights_report.txt")
    with open(out_path, "w") as f:
        f.write(report_text)
    print(f"\nSaved -> {out_path}")
