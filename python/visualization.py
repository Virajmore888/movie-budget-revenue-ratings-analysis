# =================================================================
# visualization.py — 5 charts built from insights_subset.csv
# =================================================================
#   python visualization.py
#   >>> run_all_visuals()
# =================================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PATH = os.path.dirname(os.path.abspath(__file__))
SUBSET_PATH = os.path.join(PATH, "Output", "master_data", "insights_subset.csv")
PLOT_DIR = os.path.join(PATH, "Output", "charts")
os.makedirs(PLOT_DIR, exist_ok=True)

sns.set_style("whitegrid")


def load_subset():
    return pd.read_csv(SUBSET_PATH)


def chart_roi_by_genre(df):
    roi_df = df[df["roi"].notna()]
    top = roi_df.groupby("genre_primary")["roi"].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index, hue=top.index, palette="viridis", legend=False)
    plt.title("Average ROI by Genre (Top 10)")
    plt.xlabel("Average ROI (revenue - budget) / budget")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "1_roi_by_genre.png"))
    plt.close()


def chart_imdb_vs_rt(df):
    both = df.dropna(subset=["imdb_rating", "rotten_tomatoes"])
    plt.figure(figsize=(8, 8))
    sns.scatterplot(data=both, x="imdb_rating", y="rotten_tomatoes", alpha=0.5)
    plt.plot([0, 10], [0, 100], "r--", alpha=0.5, label="perfect agreement")
    plt.title("IMDb Rating vs Rotten Tomatoes Score")
    plt.xlabel("IMDb Rating (/10)")
    plt.ylabel("Rotten Tomatoes (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "2_imdb_vs_rotten_tomatoes.png"))
    plt.close()


def chart_budget_vs_revenue(df):
    both = df.dropna(subset=["budget", "revenue"])
    plt.figure(figsize=(9, 7))
    sns.scatterplot(data=both, x="budget", y="revenue", hue="genre_primary",
                     alpha=0.6, legend=False)
    max_val = max(both["budget"].max(), both["revenue"].max())
    plt.plot([0, max_val], [0, max_val], "r--", alpha=0.4, label="break-even")
    plt.title("Budget vs Revenue")
    plt.xlabel("Budget ($)")
    plt.ylabel("Revenue ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "3_budget_vs_revenue.png"))
    plt.close()


def chart_genre_counts(df):
    counts = df["genre_primary"].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index, hue=counts.index, palette="mako", legend=False)
    plt.title("Movie Count by Primary Genre (Top 10)")
    plt.xlabel("Number of Movies")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "4_genre_counts.png"))
    plt.close()


def chart_rating_trend(df):
    yearly = df.dropna(subset=["release_year", "imdb_rating"]).groupby("release_year")["imdb_rating"].mean()
    plt.figure(figsize=(10, 6))
    yearly.plot(marker="o")
    plt.title("Average IMDb Rating by Release Year")
    plt.xlabel("Release Year")
    plt.ylabel("Average IMDb Rating")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "5_rating_trend_by_year.png"))
    plt.close()


def run_all_visuals():
    df = load_subset()
    chart_roi_by_genre(df)
    chart_imdb_vs_rt(df)
    chart_budget_vs_revenue(df)
    chart_genre_counts(df)
    chart_rating_trend(df)
    print(f"5 charts saved -> {PLOT_DIR}/")


if __name__ == "__main__":
    print("Run: python visualization.py  then call run_all_visuals()")
    print(">>> run_all_visuals()")
