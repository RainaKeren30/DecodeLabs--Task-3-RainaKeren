"""
Data utilities — load and preprocess the movie dataset.
"""

import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "movies.csv")


def load_movies() -> pd.DataFrame:
    """Load and clean the movies CSV."""
    df = pd.read_csv(DATA_PATH)

    # Normalise text fields
    for col in ["genre", "director", "cast", "language", "description"]:
        df[col] = df[col].fillna("").str.strip()

    df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    df["runtime"] = pd.to_numeric(df["runtime"], errors="coerce").fillna(0).astype(int)

    return df


def get_all_genres(df: pd.DataFrame) -> list:
    genres = set()
    for g in df["genre"].str.split("|"):
        genres.update(g)
    return sorted(genres)


def get_all_directors(df: pd.DataFrame) -> list:
    directors = set()
    for d in df["director"].str.split("|"):
        directors.update(d)
    return sorted(directors)


def get_all_languages(df: pd.DataFrame) -> list:
    return sorted(df["language"].unique().tolist())


def filter_movies(df: pd.DataFrame, genre=None, min_year=None, max_year=None,
                  min_rating=None, language=None) -> pd.DataFrame:
    result = df.copy()
    if genre:
        result = result[result["genre"].str.contains(genre, case=False, na=False)]
    if min_year:
        result = result[result["year"] >= min_year]
    if max_year:
        result = result[result["year"] <= max_year]
    if min_rating:
        result = result[result["rating"] >= min_rating]
    if language:
        result = result[result["language"] == language]
    return result
