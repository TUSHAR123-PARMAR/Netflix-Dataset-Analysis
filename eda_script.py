"""
EDA Script: netflix_titles.csv -> cleaned_netflix.csv + saved plots
Run: python eda_script.py
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.dirname(__file__)
DATA_IN = os.path.join(BASE, "data", "netflix_titles.csv")
DATA_OUT = os.path.join(BASE, "data", "cleaned_netflix.csv")
IMAGES_DIR = os.path.join(BASE, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

def load_data(path=DATA_IN):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}. Please place netflix_titles.csv in the data/ folder.")
    df = pd.read_csv(path)
    return df

def clean_data(df):
    # Basic cleaning
    df = df.copy()
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    # Parse dates
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
        df["date_added_year"] = df["date_added"].dt.year
        df["date_added_month"] = df["date_added"].dt.month
    # Fill NaNs where appropriate
    for col in ["director", "cast", "country", "rating"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    # Extract duration numbers
    if "duration" in df.columns:
        df["duration_num"] = df["duration"].str.extract(r"(\d+)").astype(float)
    return df

def basic_plots(df):
    sns.set(style="whitegrid")
    # Movies vs TV Shows
    if "type" in df.columns:
        plt.figure(figsize=(6,4))
        ax = sns.countplot(data=df, x="type")
        ax.set_title("Movies vs TV Shows")
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, "type_count.png"))
        plt.close()
    # Top 10 genres (listed_in may be multi-valued)
    if "listed_in" in df.columns:
        genres = df["listed_in"].dropna().str.split(",").explode().str.strip()
        top_genres = genres.value_counts().nlargest(10)
        plt.figure(figsize=(8,5))
        ax = sns.barplot(x=top_genres.values, y=top_genres.index)
        ax.set_title("Top 10 Genres")
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, "top_genres.png"))
        plt.close()
    # Content added by year
    if "date_added_year" in df.columns:
        counts = df["date_added_year"].value_counts().sort_index()
        plt.figure(figsize=(8,4))
        ax = counts.plot(kind="line", marker="o")
        ax.set_title("Content Added by Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, "added_by_year.png"))
        plt.close()

def save_clean(df, path=DATA_OUT):
    df.to_csv(path, index=False)
    print(f"Saved cleaned dataset to {path}")

def main():
    df = load_data()
    print("Loaded dataset with shape:", df.shape)
    df_clean = clean_data(df)
    print("After cleaning, shape:", df_clean.shape)
    basic_plots(df_clean)
    save_clean(df_clean)

if __name__ == "__main__":
    main()
