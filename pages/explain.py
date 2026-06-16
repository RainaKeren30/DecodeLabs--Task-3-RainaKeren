"""Explanation View — deep-dive into why each recommendation appeared."""
import streamlit as st
from components.styles import inject_css, page_header, similarity_bar

def render():
    inject_css()
    page_header("Recommendation Explanations", "Transparent feature-level breakdown of every recommendation.")

    if st.session_state.get("recommendations") is None:
        st.markdown("""
        <div class="card" style="text-align:center;padding:48px 32px;">
            <div style="font-family:'Poppins';font-size:1.05rem;font-weight:700;color:#2A235A;margin-bottom:8px;">No Recommendations Yet</div>
            <div style="font-size:.84rem;color:#9B8FCC;">Run the Recommendation Engine first to see explanations here.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Go to Engine"):
            st.session_state["current_page"] = "engine"
            st.rerun()
        return

    results     = st.session_state["recommendations"]
    preferences = st.session_state["last_preferences"]
    recommender = st.session_state["recommender"]

    pref_genres = set(preferences.get("genres", []))
    pref_dirs   = set(preferences.get("directors", []))
    pref_langs  = set(preferences.get("languages", []))

    # Preference profile strip
    st.markdown("<div style='font-family:Poppins,sans-serif;font-size:1.05rem;font-weight:700;color:#2A235A;margin-bottom:16px'>Your Preference Profile</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        badges = " ".join([f'<span class="badge badge-primary">{g}</span>' for g in pref_genres]) or "—"
        st.markdown(f'<div class="card-sm"><div class="section-label">Genres</div><div style="display:flex;flex-wrap:wrap;gap:5px">{badges}</div></div>', unsafe_allow_html=True)
    with col2:
        dbadges = " ".join([f'<span class="badge badge-purple">{d}</span>' for d in pref_dirs]) or "—"
        st.markdown(f'<div class="card-sm"><div class="section-label">Directors</div><div style="display:flex;flex-wrap:wrap;gap:5px">{dbadges}</div></div>', unsafe_allow_html=True)
    with col3:
        lbadges = " ".join([f'<span class="badge badge-green">{l}</span>' for l in pref_langs]) or "—"
        kw = preferences.get("keywords","")
        st.markdown(f'<div class="card-sm"><div class="section-label">Languages & Keywords</div><div style="display:flex;flex-wrap:wrap;gap:5px">{lbadges}</div>{"<div style=font-size:.76rem;color:#9B8FCC;margin-top:6px>Keywords: "+kw+"</div>" if kw else ""}</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Poppins,sans-serif;font-size:1.05rem;font-weight:700;color:#2A235A;margin-bottom:16px'>Match Analysis by Movie</div>", unsafe_allow_html=True)

    for _, row in results.iterrows():
        movie_id = int(row["id"])
        exp      = recommender.explain(movie_id, preferences)
        sim      = row["similarity_pct"]
        rank     = int(row["rank"])
        is_top   = rank == 1

        movie_genres   = set(row["genre"].split("|"))
        genre_overlap  = len(movie_genres & pref_genres)
        genre_union    = len(movie_genres | pref_genres) if (movie_genres | pref_genres) else 1
        genre_jaccard  = round(genre_overlap / genre_union * 100, 1)
        director_match = any(d in row["director"] for d in pref_dirs)
        lang_match     = row["language"] in pref_langs

        with st.expander(
            f"{'[Top Pick] ' if is_top else ''}#{rank} — {row['title']} ({row['year']})   |   Similarity: {sim:.1f}%",
            expanded=(rank <= 3)
        ):
            left, right = st.columns([1.5, 1])
            with left:
                st.markdown(f"""
                <div style="font-size:.76rem;color:#9B8FCC;margin-bottom:12px;line-height:1.6">
                    <strong style="color:#2A235A">{row['title']}</strong> ({row['year']}) &nbsp;·&nbsp;
                    Directed by {row['director']} &nbsp;·&nbsp;
                    <span style="color:#FFB07A">★</span> {row['rating']} &nbsp;·&nbsp; {row['runtime']} min
                </div>""", unsafe_allow_html=True)

                st.markdown("<div style='font-size:.70rem;font-weight:700;color:#9B8FCC;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px'>Similarity Breakdown</div>", unsafe_allow_html=True)
                similarity_bar("Overall Content Similarity", sim)
                similarity_bar("Genre Jaccard Overlap", genre_jaccard)
                similarity_bar("Director Match", 100 if director_match else 0)
                similarity_bar("Language Match", 100 if lang_match else 0)
                similarity_bar("Popularity Score", round(row.get("pop_score", 0) * 100, 1))

                st.markdown("<div style='margin-top:14px;font-size:.70rem;font-weight:700;color:#9B8FCC;text-transform:uppercase;letter-spacing:.08em;margin-bottom:7px'>Why it was recommended</div>", unsafe_allow_html=True)
                for reason in exp["reasons"]:
                    st.markdown(f"""
                    <div style="display:flex;align-items:flex-start;gap:7px;margin-bottom:5px">
                        <div style="min-width:5px;height:5px;background:linear-gradient(135deg,#9381FF,#B8B8FF);border-radius:50%;margin-top:5px;flex-shrink:0"></div>
                        <div style="font-size:.82rem;color:#2A235A;line-height:1.55">{reason}</div>
                    </div>""", unsafe_allow_html=True)

            with right:
                st.markdown("<div style='font-size:.70rem;font-weight:700;color:#9B8FCC;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px'>Feature Comparison</div>", unsafe_allow_html=True)
                for feat, mv, uv in [
                    ("Genres",   ", ".join(movie_genres), ", ".join(pref_genres) if pref_genres else "Any"),
                    ("Director", row["director"],         ", ".join(pref_dirs)   if pref_dirs   else "Any"),
                    ("Language", row["language"],         ", ".join(pref_langs)  if pref_langs  else "Any"),
                    ("Rating",   str(row["rating"]),      "—"),
                    ("Year",     str(row["year"]),         "—"),
                ]:
                    st.markdown(f"""
                    <div style="background:rgba(248,247,255,.8);border-radius:9px;padding:9px 11px;margin-bottom:5px">
                        <div style="font-size:.67rem;font-weight:700;color:#9B8FCC;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px">{feat}</div>
                        <div style="font-size:.78rem;color:#2A235A;font-weight:600;margin-bottom:1px">{str(mv)[:50]}</div>
                        <div style="font-size:.70rem;color:#9B8FCC">You wanted: {str(uv)[:40]}</div>
                    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)
