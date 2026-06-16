"""Documentation — architecture, workflow, interview Q&A, execution guide."""
import streamlit as st
from components.styles import inject_css, page_header

def render():
    inject_css()
    page_header("Documentation", "Architecture, VS Code setup guide, and interview Q&A.")

    st.markdown('<div style="font-family:Poppins,sans-serif;font-size:1.1rem;font-weight:700;color:#2A235A;margin-bottom:14px">System Architecture</div>', unsafe_allow_html=True)
    arch = [
        ("Data Layer","data/movies.csv","50-movie dataset with 11 features. Loaded via Pandas and cleaned in utils/data_loader.py."),
        ("Feature Engineering","models/recommender.py → _build_feature_matrix()","Genre (6x), director (3x), language (2x), cast, description concatenated into weighted text blobs. TfidfVectorizer with bigrams and 8,000 max features."),
        ("Hard Genre Filter","models/recommender.py → recommend()","Movies with zero genre overlap have cosine score multiplied by 0.05 — ensuring results always match your genre selections."),
        ("Cosine Similarity","sklearn.metrics.pairwise.cosine_similarity","Scale-invariant similarity in [0,1]. Computed in one matrix operation for all 50 movies simultaneously."),
        ("Explanation Engine","models/recommender.py → explain()","Feature-level diff between preferences and the selected movie — matched genres, directors, languages, and keywords."),
        ("Frontend","app.py + pages/ + components/","Streamlit multi-page app with session state persistence. Custom CSS (Space Grotesk + Poppins) provides the Periwinkle/Peach theme. Plotly powers charts."),
    ]
    for title, module, desc in arch:
        st.markdown(f"""
        <div class="card" style="padding:18px 20px;margin-bottom:10px;">
            <div style="font-family:'Space Grotesk';font-size:.88rem;font-weight:700;color:#2A235A;margin-bottom:2px;">{title}</div>
            <div style="font-size:.72rem;font-weight:600;color:#9381FF;margin-bottom:6px;font-style:italic">{module}</div>
            <div style="font-size:.80rem;color:#9B8FCC;line-height:1.65">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:Poppins,sans-serif;font-size:1.1rem;font-weight:700;color:#2A235A;margin-bottom:14px">VS Code Execution Guide</div>', unsafe_allow_html=True)

    steps = [
        ("Open project in VS Code","File → Open Folder → select recommendation_system/"),
        ("Create virtual environment","python -m venv venv\n.\\venv\\Scripts\\activate   (Windows)\nsource venv/bin/activate   (Mac / Linux)"),
        ("Install dependencies","pip install -r requirements.txt"),
        ("Run the app","streamlit run app.py"),
        ("Open in browser","http://localhost:8501 opens automatically"),
    ]
    for i,(title,desc) in enumerate(steps,1):
        lines = desc.split("\n")
        code = "\n".join(lines[1:]) if len(lines)>1 else ""
        st.markdown(f"""
        <div style="display:flex;gap:14px;align-items:flex-start;margin-bottom:12px">
            <div style="min-width:30px;height:30px;background:linear-gradient(135deg,#9381FF,#B8B8FF);border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'Poppins';font-size:.76rem;font-weight:800;color:#fff">{i}</div>
            <div><div style="font-size:.86rem;font-weight:700;color:#2A235A;margin-bottom:3px">{title}</div>
            <div style="font-size:.80rem;color:#9B8FCC">{lines[0]}</div>
            {'<pre style="background:rgba(147,129,255,.07);border:1.5px solid rgba(147,129,255,.14);border-radius:9px;padding:8px 12px;font-size:.76rem;color:#2A235A;margin-top:6px;overflow-x:auto">'+code+'</pre>' if code else ''}
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:Poppins,sans-serif;font-size:1.1rem;font-weight:700;color:#2A235A;margin-bottom:14px">Interview Q&A</div>', unsafe_allow_html=True)
    qa = [
        ("What type of recommendation system did you build and why?","Content-based filtering. It recommends movies by comparing their features against user preferences — without needing data from other users. Works from day one with a single user."),
        ("How does TF-IDF work?","TF measures how often a word appears in a movie's feature string; IDF penalises words appearing across many movies. The result is a sparse matrix where each dimension is a term weighted by its discriminative power."),
        ("Why Cosine Similarity over Euclidean distance?","Cosine similarity measures the angle between vectors rather than magnitude. Since TF-IDF vectors vary in length by text length, Euclidean distance would penalise longer descriptions. Cosine is scale-invariant and always returns [0,1]."),
        ("How do you ensure genre accuracy?","Movies with zero genre overlap with the user's selection have their cosine score multiplied by 0.05 — a 95% penalty that effectively removes them from results while still allowing the engine to surface them if the dataset has no genre matches at all."),
        ("What are the limitations?","Content-based filtering cannot discover serendipitous recommendations outside the selected genres. It also does not learn from user behaviour over time. Collaborative filtering or hybrid methods would address these gaps."),
        ("How would you scale this to millions of movies?","Replace TF-IDF + exact cosine with FAISS or Annoy for approximate nearest-neighbour search. Store embeddings in a vector database (Pinecone, Weaviate). Use Sentence-BERT for richer semantic embeddings."),
    ]
    for q,a in qa:
        with st.expander(q):
            st.markdown(f'<div style="font-size:.84rem;color:#2A235A;line-height:1.7;padding:4px 0">{a}</div>',unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:Poppins,sans-serif;font-size:1.1rem;font-weight:700;color:#2A235A;margin-bottom:14px">Future Improvements</div>', unsafe_allow_html=True)
    improvements = [
        ("Sentence-BERT Embeddings","Replace TF-IDF with transformer embeddings for richer semantic similarity that captures meaning beyond keywords."),
        ("Collaborative Filtering","Build a user-item matrix from ratings and layer a collaborative model on top for personalised discovery."),
        ("Real-Time Feedback Loop","Let users rate recommendations in-app. Re-rank results within the session via Bayesian updates."),
        ("Vector Database","Store pre-computed embeddings in Pinecone or Weaviate for sub-millisecond ANN search at scale."),
        ("A/B Testing","Experiment across algorithms, weighting schemes, and blends to measure which drives best engagement."),
        ("FastAPI Backend","Expose the engine as a REST API — decoupling backend from Streamlit for mobile or third-party integration."),
    ]
    cols = st.columns(2)
    for i,(title,desc) in enumerate(improvements):
        with cols[i%2]:
            st.markdown(f'<div class="card-sm"><div style="font-size:.86rem;font-weight:700;color:#2A235A;margin-bottom:5px">{title}</div><div style="font-size:.78rem;color:#9B8FCC;line-height:1.6">{desc}</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)
