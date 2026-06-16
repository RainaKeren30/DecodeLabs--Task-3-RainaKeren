"""Dashboard — command centre, second page after title."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from components.styles import inject_css

PL = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(248,247,255,1)",
          font=dict(family="Space Grotesk,Inter,sans-serif",color="#2A235A",size=11),
          margin=dict(l=0,r=0,t=36,b=0),title_font_size=13,
          title_font_family="Poppins",title_font_color="#2A235A",showlegend=False)

def render():
    inject_css()
    st.markdown("""
    <style>
    .dash-hero{background:linear-gradient(135deg,#9381FF 0%,#B8B8FF 55%,#FFD8BE 100%);border-radius:22px;padding:38px 44px 34px;margin-bottom:24px;position:relative;overflow:hidden;box-shadow:0 14px 44px rgba(147,129,255,.26)}
    .dash-hero::before{content:'';position:absolute;top:-60px;right:-60px;width:240px;height:240px;background:rgba(255,255,255,.09);border-radius:50%}
    .dash-hero h1{font-family:'Poppins',sans-serif;font-size:1.9rem;font-weight:800;color:#2A235A;letter-spacing:-.5px;margin-bottom:5px;position:relative;z-index:1}
    .dash-hero p{font-family:'Inter',sans-serif;font-size:.92rem;color:rgba(42,35,90,.72);position:relative;z-index:1}
    .kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}
    .kpi-tile{background:#fff;border:1.5px solid rgba(147,129,255,.13);border-radius:18px;padding:20px 18px 16px;box-shadow:0 3px 14px rgba(147,129,255,.08);position:relative;overflow:hidden}
    .kpi-tile::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#9381FF,#B8B8FF,#FFD8BE);border-radius:0 0 18px 18px}
    .kpi-num{font-family:'Poppins',sans-serif;font-size:2rem;font-weight:800;color:#2A235A;line-height:1;margin-bottom:4px}
    .kpi-lbl{font-size:.68rem;font-weight:700;color:#9B8FCC;text-transform:uppercase;letter-spacing:.08em}
    .kpi-sub{font-size:.70rem;color:#22c55e;font-weight:600;margin-top:5px}
    .lg{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px}
    .lc{background:#fff;border:1.5px solid rgba(147,129,255,.13);border-radius:16px;padding:18px 16px;box-shadow:0 2px 10px rgba(147,129,255,.07);transition:all .25s}
    .lc:hover{box-shadow:0 8px 26px rgba(147,129,255,.16);transform:translateY(-2px);border-color:rgba(147,129,255,.26)}
    .lt{font-family:'Space Grotesk';font-size:.88rem;font-weight:700;color:#2A235A;margin-bottom:4px}
    .ld{font-size:.76rem;color:#9B8FCC;line-height:1.5}
    .la{font-size:.72rem;font-weight:700;color:#9381FF;margin-top:8px;display:block}
    .sec-head{font-family:'Poppins',sans-serif;font-size:1rem;font-weight:700;color:#2A235A;margin-bottom:14px}
    .mr{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid rgba(147,129,255,.08)}
    .mr:last-child{border-bottom:none}
    .mrk{font-family:'Poppins',sans-serif;font-size:.9rem;font-weight:800;color:rgba(147,129,255,.25);min-width:24px;text-align:center}
    .mn{font-size:.82rem;font-weight:700;color:#2A235A}
    .mm{font-size:.70rem;color:#9B8FCC;margin-top:1px}
    .mrt{font-family:'Poppins',sans-serif;font-size:.82rem;font-weight:800;color:#2A235A}
    .star{color:#FFB07A}
    .algo-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .algo-step{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1.5px solid rgba(147,129,255,.10);border-radius:13px;padding:14px 16px;box-shadow:0 2px 10px rgba(147,129,255,.06)}
    .algo-n{min-width:32px;height:32px;background:linear-gradient(135deg,#9381FF,#B8B8FF);border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'Poppins';font-size:.78rem;font-weight:800;color:#fff}
    .algo-t{font-size:.84rem;font-weight:700;color:#2A235A;margin-bottom:3px}
    .algo-d{font-size:.76rem;color:#9B8FCC;line-height:1.55}
    </style>
    """, unsafe_allow_html=True)

    df   = st.session_state["df"]
    recs = st.session_state.get("recommendations")

    st.markdown("""
    <div class="dash-hero">
        <h1>CineMatch AI — Dashboard</h1>
        <p>Overview of the dataset, algorithm pipeline, and quick navigation to every module.</p>
    </div>""", unsafe_allow_html=True)

    avg_r    = df["rating"].mean()
    top_g    = df["genre"].str.split("|").explode().value_counts().index[0]
    n_dirs   = df["director"].str.split("|").explode().nunique()
    recs_lbl = str(len(recs)) if recs is not None else "Ready"

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-tile"><div class="kpi-num">50</div><div class="kpi-lbl">Movies in Dataset</div><div class="kpi-sub">11 features each</div></div>
        <div class="kpi-tile"><div class="kpi-num">{avg_r:.1f}</div><div class="kpi-lbl">Avg IMDb Rating</div><div class="kpi-sub">Range 7.3 — 9.3</div></div>
        <div class="kpi-tile"><div class="kpi-num">{n_dirs}</div><div class="kpi-lbl">Unique Directors</div><div class="kpi-sub">Top genre: {top_g}</div></div>
        <div class="kpi-tile"><div class="kpi-num">{recs_lbl}</div><div class="kpi-lbl">Last Recommendations</div><div class="kpi-sub">TF-IDF · Cosine</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Quick Navigation</div>', unsafe_allow_html=True)
    items = [
        ("dataset","Dataset Explorer","Browse and filter the full 50-movie corpus."),
        ("engine","Recommendation Engine","Run the genre-filtered cosine similarity engine."),
        ("explain","Explanation View","Feature-level breakdown of every recommendation."),
        ("analytics","Analytics","Deep-dive corpus and recommendation charts."),
        ("home","Project Overview","Algorithm walkthrough and architecture."),
        ("docs","Documentation","Setup guide and interview Q&A."),
    ]
    cols = st.columns(3)
    for i,(key,title,desc) in enumerate(items):
        with cols[i%3]:
            st.markdown(f'<div class="lc"><div class="lt">{title}</div><div class="ld">{desc}</div></div>',unsafe_allow_html=True)
            if st.button(f"Open", key=f"dn_{key}", use_container_width=True):
                st.session_state["current_page"] = key
                st.rerun()

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    left, right = st.columns([1,1.1])

    with left:
        st.markdown('<div class="sec-head">Top 8 Rated Movies</div>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="padding:16px 18px">', unsafe_allow_html=True)
        top8 = df.nlargest(8,"rating")[["title","year","rating","genre"]].reset_index(drop=True)
        for idx, row in top8.iterrows():
            g = row["genre"].split("|")[0]
            st.markdown(f'<div class="mr"><div class="mrk">#{idx+1}</div><div style="flex:1"><div class="mn">{row["title"]}</div><div class="mm">{row["year"]} · {g}</div></div><div class="mrt"><span class="star">★</span> {row["rating"]}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="sec-head">Genre Distribution</div>', unsafe_allow_html=True)
        gc = df["genre"].str.split("|").explode().value_counts().head(12)
        fig = px.bar(x=gc.values,y=gc.index,orientation="h",
                     color=gc.values,color_continuous_scale=["#C4C4FF","#9381FF"],
                     labels={"x":"Count","y":""})
        fig.update_layout(**PL,coloraxis_showscale=False,height=300,
                          yaxis=dict(tickfont=dict(size=10)))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.histogram(df,x="rating",nbins=14,color_discrete_sequence=["#B8B8FF"],
                            labels={"rating":"IMDb Rating","count":"Count"})
        fig2.update_layout(**PL,title="Rating Distribution",height=160)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">Algorithm Pipeline</div>', unsafe_allow_html=True)
    steps = [
        ("Feature Engineering","Genre (6x), director (3x), language (2x), cast & description — weighted text blob per movie."),
        ("TF-IDF Vectorisation","8,000-feature sparse matrix with bigrams; English stop-words removed."),
        ("Hard Genre Filter","Movies with zero genre overlap are penalised 95% — guaranteeing relevant results."),
        ("Preference Vector","User selections encoded into the same TF-IDF space as a query vector."),
        ("Cosine Similarity","cos θ = (A·B)/(‖A‖‖B‖) in [0,1] — one matrix op across all movies."),
        ("Rank & Explain","Feature-diff produces natural-language reasons for every recommendation."),
    ]
    ca, cb = st.columns(2)
    for i,(t,d) in enumerate(steps):
        with (ca if i%2==0 else cb):
            st.markdown(f'<div class="algo-step"><div class="algo-n">{i+1}</div><div><div class="algo-t">{t}</div><div class="algo-d">{d}</div></div></div>',unsafe_allow_html=True)

    # Decade chart
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">Movies by Decade</div>', unsafe_allow_html=True)
    ddf = df.copy()
    ddf["decade"] = (ddf["year"]//10*10).astype(str)+"s"
    dc  = ddf["decade"].value_counts().sort_index()
    ar  = ddf.groupby("decade")["rating"].mean().reindex(dc.index)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=dc.index,y=dc.values,marker_color="#9381FF",marker_line_width=0,name="Count"))
    fig3.add_trace(go.Scatter(x=ar.index,y=ar.values,yaxis="y2",line=dict(color="#FFB07A",width=2.5),
                              mode="lines+markers",marker=dict(size=7,color="#FFB07A"),name="Avg Rating"))
    fig3.update_layout(**PL,height=200,showlegend=True,
                       legend=dict(orientation="h",x=0.7,y=1.18),
                       yaxis=dict(title="Count"),
                       yaxis2=dict(title="Avg Rating",overlaying="y",side="right",range=[7,10]))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("<div style='margin-bottom:48px'></div>", unsafe_allow_html=True)
