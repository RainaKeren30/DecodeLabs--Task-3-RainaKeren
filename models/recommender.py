"""
Recommendation Engine — Content-Based Filtering with Cosine Similarity.
Fixed: genre matching is now the dominant signal. A movie that shares NO
genres with the user's selection cannot rank above one that does.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


class MovieRecommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy().reset_index(drop=True)
        self._build_feature_matrix()

    def _build_feature_matrix(self):
        def combine(row):
            # Genre repeated 6x so it dominates the TF-IDF space
            genre_text  = " ".join(row["genre"].replace("|", " ").split()) + " " 
            genre_text  = genre_text * 6
            dir_text    = row["director"].replace("|", " ") + " "
            dir_text    = dir_text * 3
            cast_text   = row["cast"].replace("|", " ")
            lang_text   = row["language"] * 2
            desc_text   = row.get("description", "")
            return f"{genre_text}{dir_text}{cast_text} {lang_text} {desc_text}"

        self.df["features"] = self.df.apply(combine, axis=1)
        self.tfidf = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_features=8000,
        )
        self.tfidf_matrix = self.tfidf.fit_transform(self.df["features"])

        scaler = MinMaxScaler()
        self.df["rating_norm"] = scaler.fit_transform(self.df[["rating"]])
        self.df["votes_norm"]  = scaler.fit_transform(self.df[["votes"]])
        self.df["pop_score"]   = (0.6 * self.df["rating_norm"] + 0.4 * self.df["votes_norm"])

    def _build_preference_vector(self, preferences: dict) -> np.ndarray:
        parts = []
        # Genres: 8x weight — largest signal
        parts.extend(preferences.get("genres", []) * 8)
        # Directors: 4x
        parts.extend(preferences.get("directors", []) * 4)
        # Languages: 3x
        parts.extend(preferences.get("languages", []) * 3)
        # Keywords: 2x
        kw = preferences.get("keywords", "")
        if kw:
            parts.extend(kw.split() * 2)
        query = " ".join(parts) if parts else "movie"
        return self.tfidf.transform([query])

    def recommend(self, preferences: dict, top_n: int = 10,
                  exclude_ids: list = None, blend_popularity: float = 0.10) -> pd.DataFrame:
        pref_genres = [g.strip() for g in preferences.get("genres", [])]
        pref_dirs   = [d.strip() for d in preferences.get("directors", [])]
        pref_langs  = [l.strip() for l in preferences.get("languages", [])]

        pref_vec   = self._build_preference_vector(preferences)
        raw_sim    = cosine_similarity(pref_vec, self.tfidf_matrix).flatten()

        result = self.df.copy()
        result["cosine_score"] = raw_sim

        # ── Hard genre filter when genres are selected ──────────────
        # A movie must share at least ONE genre with the preference list.
        if pref_genres:
            def has_genre(genre_str):
                movie_genres = [g.strip() for g in genre_str.split("|")]
                return any(g in pref_genres for g in movie_genres)
            genre_mask = result["genre"].apply(has_genre)
            # Keep genre matches; non-matches get score heavily penalised
            result.loc[~genre_mask, "cosine_score"] *= 0.05

        # ── Language filter ─────────────────────────────────────────
        if pref_langs:
            lang_mask = result["language"].isin(pref_langs)
            result.loc[~lang_mask, "cosine_score"] *= 0.3

        # ── Genre overlap bonus ─────────────────────────────────────
        if pref_genres:
            def genre_overlap_bonus(genre_str):
                movie_genres = set(g.strip() for g in genre_str.split("|"))
                pref_set     = set(pref_genres)
                overlap      = len(movie_genres & pref_set)
                union        = len(movie_genres | pref_set)
                return (overlap / union) * 0.4 if union else 0.0
            result["genre_bonus"] = result["genre"].apply(genre_overlap_bonus)
        else:
            result["genre_bonus"] = 0.0

        # ── Director bonus ──────────────────────────────────────────
        if pref_dirs:
            def dir_bonus(dir_str):
                return 0.15 if any(d in dir_str for d in pref_dirs) else 0.0
            result["dir_bonus"] = result["director"].apply(dir_bonus)
        else:
            result["dir_bonus"] = 0.0

        # ── Final blended score ─────────────────────────────────────
        result["final_score"] = (
            result["cosine_score"]
            + result["genre_bonus"]
            + result["dir_bonus"]
            + blend_popularity * result["pop_score"]
        )

        if exclude_ids:
            result = result[~result["id"].isin(exclude_ids)]

        result = result.sort_values("final_score", ascending=False).head(top_n)

        # Normalise similarity % to the top result for clean display
        max_score = result["final_score"].max()
        if max_score > 0:
            result["similarity_pct"] = (result["final_score"] / max_score * 100).round(1)
        else:
            result["similarity_pct"] = 0.0

        result["rank"] = range(1, len(result) + 1)
        return result.reset_index(drop=True)

    def explain(self, movie_id: int, preferences: dict) -> dict:
        row = self.df[self.df["id"] == movie_id].iloc[0]
        genres    = set(row["genre"].split("|"))
        directors = set(row["director"].split("|"))
        language  = row["language"]

        pref_genres = set(preferences.get("genres", []))
        pref_dirs   = set(preferences.get("directors", []))
        pref_langs  = set(preferences.get("languages", []))

        matched_genres    = genres & pref_genres
        matched_directors = directors & pref_dirs
        matched_language  = language in pref_langs

        reasons = []
        if matched_genres:
            reasons.append(f"Matches your genre(s): {', '.join(sorted(matched_genres))}")
        if matched_directors:
            reasons.append(f"Directed by your preferred director: {', '.join(matched_directors)}")
        if matched_language:
            reasons.append(f"Available in your preferred language: {language}")

        keywords = preferences.get("keywords", "")
        if keywords:
            kws   = [k.strip().lower() for k in keywords.split()]
            blob  = (row.get("description", "") + " " + row["features"]).lower()
            hits  = [k for k in kws if k in blob]
            if hits:
                reasons.append(f"Contains your themes: {', '.join(hits)}")

        if not reasons:
            reasons.append("Recommended based on overall content similarity to your preferences")

        return {
            "movie": row["title"], "year": row["year"], "rating": row["rating"],
            "genres": list(genres), "director": row["director"],
            "cast": row["cast"].split("|"), "language": language,
            "reasons": reasons, "matched_genres": list(matched_genres),
            "matched_directors": list(matched_directors),
            "matched_language": matched_language,
        }

    def get_genre_distribution(self) -> pd.Series:
        return self.df["genre"].str.split("|").explode().value_counts()

    def get_year_distribution(self) -> pd.Series:
        return self.df["year"].value_counts().sort_index()

    def get_rating_stats(self) -> dict:
        return {
            "mean":   round(self.df["rating"].mean(), 2),
            "median": round(self.df["rating"].median(), 2),
            "min":    round(self.df["rating"].min(), 2),
            "max":    round(self.df["rating"].max(), 2),
            "std":    round(self.df["rating"].std(), 2),
        }
