"""Landing / Project Overview page."""
import streamlit as st
from components.styles import inject_css, page_header

def render():
    inject_css()
    page_header("Project Overview", "How CineMatch AI works — algorithm, architecture, and feature breakdown.")

    st.markdown("""
    <div style="font-family:'Poppins',sans-serif;font-size:1.15rem;font-weight:700;color:#2A235A;margin-bottom:18px;">What this system does</div>
    """, unsafe_allow_html=True)

    features = [
        ("Content-Based Filtering", "Builds a weighted TF-IDF feature matrix from genre, director, cast, language and description for every movie in the dataset."),
        ("Cosine Similarity", "Measures the angular distance between your preference vector and each movie vector to produce a precise relevance score in [0,1]."),
        ("Hard Genre Filtering", "Movies that share zero genres with your selection are penalised 95% — ensuring results are always relevant to what you asked for."),
        ("Explainable Results", "Every recommendation includes a plain-English breakdown of the exact features that drove the match."),
        ("Interactive Filters", "Slice by genre, language, director, decade, and minimum rating before running the engine."),
        ("Analytics Dashboard", "Visualise genre distributions, rating trends, similarity scores, and recommendation patterns across the corpus."),
    ]
    cols = st.columns(2)
    for i, (title, desc) in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card-sm" style="min-height:100px;">
                <div style="font-family:'Space Grotesk';font-size:.88rem;font-weight:700;color:#2A235A;margin-bottom:6px;">{title}</div>
                <div style="font-size:.80rem;color:#9B8FCC;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Poppins',sans-serif;font-size:1.15rem;font-weight:700;color:#2A235A;margin-bottom:18px;">How the algorithm works</div>""", unsafe_allow_html=True)

    steps = [
        ("Build Feature Text", "Each movie's genre (6x), director (3x), language (2x), cast, and description are concatenated into one weighted text string per movie."),
        ("TF-IDF Encoding", "Scikit-learn's TfidfVectorizer encodes the corpus into a sparse 8,000-feature matrix. Bigrams enabled; English stop-words removed."),
        ("Preference Vector", "Your genres, directors, and keywords are encoded into the same TF-IDF space — genre carries 8x weight, director 4x, language 3x."),
        ("Hard Genre Filter", "Movies sharing zero genres with your selection have their cosine score multiplied by 0.05, effectively removing them from results."),
        ("Cosine Similarity", "cos θ = (A·B)/(‖A‖‖B‖) — scale-invariant similarity computed in one matrix operation across all 50 movies."),
        ("Popularity Blend", "A 10% popularity signal (0.6×rating + 0.4×votes, both normalised) is added to prevent obscure zero-vote results from surfacing."),
    ]
    for n, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="card" style="display:flex;gap:16px;align-items:flex-start;padding:18px 20px;">
            <div style="min-width:36px;height:36px;background:linear-gradient(135deg,#9381FF,#B8B8FF);border-radius:10px;display:flex;align-items:center;justify-content:center;font-family:'Poppins';font-size:.88rem;font-weight:800;color:#fff">{n}</div>
            <div><div style="font-family:'Space Grotesk';font-size:.88rem;font-weight:700;color:#2A235A;margin-bottom:4px;">{title}</div>
            <div style="font-size:.80rem;color:#9B8FCC;line-height:1.6;">{desc}</div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)
