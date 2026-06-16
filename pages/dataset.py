"""Dataset Explorer — browse, filter, and inspect the movie corpus."""
import streamlit as st
import plotly.express as px
from components.styles import inject_css, page_header, metric_tile
from utils.data_loader import get_all_genres, get_all_languages, filter_movies

PL = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,247,255,1)",
          font=dict(family="Space Grotesk,Inter,sans-serif", color="#2A235A", size=11),
          margin=dict(l=0,r=0,t=36,b=0), title_font_size=13,
          title_font_family="Poppins", title_font_color="#2A235A")
SCALE = ["#C4C4FF","#B8B8FF","#9381FF"]

def render():
    inject_css()
    page_header("Dataset Explorer", "Browse and filter the 50-movie corpus powering the recommendation engine.")

    df       = st.session_state["df"]
    genres   = get_all_genres(df)
    languages = get_all_languages(df)

    st.markdown("<div class='section-label'>Filter Dataset</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: sel_genre = st.selectbox("Genre", ["All"] + genres)
    with col2: sel_lang  = st.selectbox("Language", ["All"] + languages)
    with col3: year_range = st.slider("Year range", int(df["year"].min()), int(df["year"].max()), (int(df["year"].min()), int(df["year"].max())))
    with col4: min_rating = st.slider("Min rating", 0.0, 10.0, 0.0, 0.1)

    filtered = filter_movies(df,
        genre=None if sel_genre=="All" else sel_genre,
        language=None if sel_lang=="All" else sel_lang,
        min_year=year_range[0], max_year=year_range[1], min_rating=min_rating)

    st.markdown("<div style='margin-top:22px'></div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for col, (label, val, sub) in zip(cols, [
        ("Total Movies", str(len(filtered)), "in filtered view"),
        ("Avg Rating", f"{filtered['rating'].mean():.1f}", "out of 10"),
        ("Genres Covered", str(filtered['genre'].str.split('|').explode().nunique()), "unique genres"),
        ("Avg Runtime", f"{filtered['runtime'].mean():.0f} min", "per movie"),
    ]):
        with col: metric_tile(label, val, sub)

    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Visual Overview</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        gc = filtered["genre"].str.split("|").explode().value_counts().head(12)
        fig = px.bar(x=gc.values, y=gc.index, orientation="h", title="Genre Distribution",
            color=gc.values, color_continuous_scale=SCALE, labels={"x":"Count","y":""})
        fig.update_layout(**PL, coloraxis_showscale=False, height=280, yaxis=dict(tickfont=dict(size=10)))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.histogram(filtered, x="rating", nbins=15, title="Rating Distribution",
            color_discrete_sequence=["#9381FF"], labels={"rating":"IMDb Rating","count":"Count"})
        fig2.update_layout(**PL, height=280)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        yc = filtered["year"].value_counts().sort_index()
        fig3 = px.area(x=yc.index, y=yc.values, title="Movies by Year",
            labels={"x":"Year","y":"Movies"}, color_discrete_sequence=["#9381FF"])
        fig3.update_traces(fill="tozeroy", fillcolor="rgba(147,129,255,.10)")
        fig3.update_layout(**PL, height=220)
        st.plotly_chart(fig3, use_container_width=True)
    with c4:
        lc = filtered["language"].value_counts()
        fig4 = px.pie(values=lc.values, names=lc.index, title="Language Split", hole=0.5,
            color_discrete_sequence=["#9381FF","#B8B8FF","#FFD8BE","#FFEEDD"])
        fig4.update_layout(**PL, height=220)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Movie Cards</div>", unsafe_allow_html=True)

    rows = [filtered.iloc[i:i+2] for i in range(0, len(filtered), 2)]
    for row in rows:
        cols = st.columns(2)
        for col, (_, movie) in zip(cols, row.iterrows()):
            with col:
                genres_display = " · ".join(movie["genre"].split("|")[:3])
                st.markdown(f"""
                <div class="card-sm">
                    <div style="font-family:'Space Grotesk';font-size:.92rem;font-weight:700;color:#2A235A;margin-bottom:3px">{movie['title']}</div>
                    <div style="font-size:.72rem;color:#9B8FCC;margin-bottom:7px">{movie['year']} &nbsp;·&nbsp; {genres_display}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span style="font-size:.80rem;color:#9B8FCC"><span style="color:#FFB07A;font-weight:700">★</span> {movie['rating']} &nbsp;·&nbsp; {movie['runtime']} min</span>
                        <span style="font-size:.72rem;color:#9B8FCC">{movie['language']}</span>
                    </div>
                    <div style="font-size:.73rem;color:#9B8FCC;margin-top:7px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{str(movie.get('description',''))[:120]}...</div>
                </div>""", unsafe_allow_html=True)

    with st.expander("View raw data table"):
        display_cols = ["id","title","genre","director","year","rating","votes","runtime","language"]
        st.dataframe(filtered[display_cols].rename(columns=str.title), use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)
