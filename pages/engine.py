"""Recommendation Engine page — accurate genre-filtered results."""
import streamlit as st
from components.styles import inject_css, page_header, rec_card, similarity_bar
from utils.data_loader import get_all_genres, get_all_directors, get_all_languages

def render():
    inject_css()
    page_header("Recommendation Engine", "Select your preferences — the engine filters by genre first, then ranks by TF-IDF cosine similarity.")

    df          = st.session_state["df"]
    recommender = st.session_state["recommender"]
    genres      = get_all_genres(df)
    directors   = get_all_directors(df)
    languages   = get_all_languages(df)

    st.markdown("""
    <div class="card" style="margin-bottom:24px;">
        <div style="font-family:'Poppins';font-size:1.05rem;font-weight:700;color:#2A235A;margin-bottom:4px;">Preference Configuration</div>
        <div style="font-size:.82rem;color:#9B8FCC;margin-bottom:18px;">
            Genre selection acts as a <strong style="color:#9381FF">hard filter</strong> — results will only include movies matching at least one of your chosen genres.
            Directors, languages, and keywords add extra weight on top.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        sel_genres = st.multiselect("Preferred Genres", options=genres, default=["Sci-Fi"],
            help="Hard filter — only movies with at least one matching genre appear in results.")
        sel_languages = st.multiselect("Preferred Languages", options=languages, default=["English"])
    with col_b:
        sel_directors = st.multiselect("Preferred Directors (optional)", options=directors, default=[])
        keywords = st.text_input("Keywords / Themes (optional)", placeholder="e.g. space survival heist time")

    col_c, col_d = st.columns(2)
    with col_c:
        top_n = st.slider("Number of recommendations", 3, 15, 8)
    with col_d:
        min_rating = st.slider("Minimum IMDb rating", 0.0, 10.0, 0.0, 0.5)

    run_col, _ = st.columns([1, 3])
    with run_col:
        run = st.button("Run Recommendation Engine", use_container_width=True)

    has_results = st.session_state.get("recommendations") is not None

    if run or has_results:
        if run:
            if not sel_genres and not sel_directors and not sel_languages and not keywords:
                st.warning("Select at least one genre, director, or language before running.")
                return

            preferences = {"genres": sel_genres, "directors": sel_directors,
                           "languages": sel_languages, "keywords": keywords}

            with st.spinner("Computing similarity scores..."):
                df_filtered = df[df["rating"] >= min_rating] if min_rating > 0 else df
                import pandas as pd
                from models.recommender import MovieRecommender
                rec_temp = MovieRecommender(df_filtered) if min_rating > 0 else recommender
                results  = rec_temp.recommend(preferences=preferences, top_n=top_n)
                st.session_state["recommendations"]  = results
                st.session_state["last_preferences"] = preferences

        results     = st.session_state["recommendations"]
        preferences = st.session_state["last_preferences"]

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Active preference summary
        parts = []
        if preferences.get("genres"):    parts.append(f"Genres: {', '.join(preferences['genres'])}")
        if preferences.get("directors"): parts.append(f"Directors: {', '.join(preferences['directors'])}")
        if preferences.get("languages"): parts.append(f"Languages: {', '.join(preferences['languages'])}")
        if preferences.get("keywords"):  parts.append(f"Keywords: {preferences['keywords']}")

        st.markdown(f"""
        <div style="background:rgba(147,129,255,.07);border:1.5px solid rgba(147,129,255,.14);
                    border-radius:14px;padding:14px 18px;margin-bottom:22px;">
            <div style="font-size:.70rem;font-weight:700;color:#9B8FCC;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px;">Active Preferences</div>
            <div style="font-size:.84rem;color:#2A235A;font-weight:500;">{' &nbsp;·&nbsp; '.join(parts)}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-family:'Poppins';font-size:1.1rem;font-weight:700;color:#2A235A;margin-bottom:18px;">
            {len(results)} Results — ranked by content similarity
        </div>""", unsafe_allow_html=True)

        for _, row in results.iterrows():
            rec_card(title=row["title"], year=row["year"], genre=row["genre"],
                     director=row["director"], rating=row["rating"],
                     similarity=row["similarity_pct"], rank=int(row["rank"]),
                     is_top=(int(row["rank"]) == 1))

        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
        if st.button("View detailed explanations"):
            st.session_state["current_page"] = "explain"
            st.rerun()

    st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)
