"""Analytics Dashboard — full corpus and recommendation charts."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from components.styles import inject_css, page_header, metric_tile

PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,247,255,1)",
    font=dict(family="Space Grotesk,Inter,sans-serif", color="#2A235A", size=11),
    margin=dict(l=0, r=0, t=36, b=0), title_font_size=13,
    title_font_family="Poppins", title_font_color="#2A235A",
)
SCALE = ["#C4C4FF", "#B8B8FF", "#9381FF"]

def render():
    inject_css()
    page_header("Analytics Dashboard", "Data insights across the movie corpus and recommendation outputs.")

    df   = st.session_state["df"]
    recs = st.session_state.get("recommendations")

    # KPI row
    cols = st.columns(5)
    top_g = df["genre"].str.split("|").explode().value_counts().index[0]
    decade_top = str((df["year"] // 10 * 10).value_counts().idxmax()) + "s"
    n_recs = str(len(recs)) if recs is not None else "—"
    stats = [
        ("Total Movies", "50", "in dataset"),
        ("Avg IMDb Rating", f"{df['rating'].mean():.2f}", "out of 10"),
        ("Top Genre", top_g, "most frequent"),
        ("Best Decade", decade_top, "by count"),
        ("Last Recs", n_recs, "from engine"),
    ]
    for col, (label, val, sub) in zip(cols, stats):
        with col:
            metric_tile(label, val, sub)

    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Corpus Analysis</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(df, x="year", y="rating", size="votes",
            hover_name="title", color="rating",
            color_continuous_scale=["#FFEEDD","#B8B8FF","#9381FF"],
            title="Rating vs Year (bubble = vote count)",
            labels={"year":"Release Year","rating":"IMDb Rating"}, size_max=28)
        fig.update_layout(**PL, coloraxis_showscale=False, height=280)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top10 = df.nlargest(10,"rating").copy()
        top10["short"] = top10["title"].str[:22]
        fig2 = px.bar(top10[::-1], x="rating", y="short", orientation="h",
            color="rating", color_continuous_scale=SCALE,
            title="Top 10 Highest Rated",
            labels={"rating":"IMDb Rating","short":""})
        fig2.update_layout(**PL, coloraxis_showscale=False, height=280,
                           yaxis=dict(tickfont=dict(size=10)))
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        top_g_list = df["genre"].str.split("|").explode().value_counts().head(8).index.tolist()
        import pandas as pd
        matrix = pd.DataFrame(0, index=top_g_list, columns=top_g_list)
        for gl in df["genre"].str.split("|"):
            for a in gl:
                for b in gl:
                    if a in top_g_list and b in top_g_list:
                        matrix.loc[a,b] += 1
        fig3 = go.Figure(data=go.Heatmap(z=matrix.values, x=top_g_list, y=top_g_list,
            colorscale=[[0,"rgba(147,129,255,.05)"],[1,"#9381FF"]], showscale=False))
        fig3.update_layout(**PL, title="Genre Co-occurrence Matrix", height=280)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.violin(df, y="runtime", box=True, points="all",
            title="Runtime Distribution (minutes)",
            color_discrete_sequence=["#9381FF"],
            labels={"runtime":"Runtime (min)"})
        fig4.update_layout(**PL, height=280)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Director & Language Insights</div>", unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        dc = df["director"].str.split("|").explode().value_counts().head(10)
        fig5 = px.bar(x=dc.index, y=dc.values, title="Most Frequent Directors",
            labels={"x":"Director","y":"Count"}, color=dc.values,
            color_continuous_scale=SCALE)
        fig5.update_layout(**PL, coloraxis_showscale=False, height=260, xaxis_tickangle=-30)
        fig5.update_traces(marker_line_width=0)
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        lc = df["language"].value_counts().reset_index()
        lc.columns = ["language","count"]
        fig6 = px.pie(lc, names="language", values="count",
            title="Language Split",
            color_discrete_sequence=["#9381FF","#B8B8FF","#FFD8BE","#FFEEDD"])
        fig6.update_layout(**PL, height=260)
        st.plotly_chart(fig6, use_container_width=True)

    # Recommendation analytics
    if recs is not None:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Last Recommendation Session</div>", unsafe_allow_html=True)
        cr1, cr2 = st.columns(2)
        with cr1:
            fig_r1 = px.bar(recs, x="similarity_pct", y="title", orientation="h",
                title="Similarity Scores — Ranked",
                labels={"similarity_pct":"Content Similarity (%)","title":""},
                color="similarity_pct", color_continuous_scale=SCALE)
            fig_r1.update_layout(**PL, coloraxis_showscale=False, height=260,
                                 yaxis=dict(tickfont=dict(size=10)))
            fig_r1.update_traces(marker_line_width=0)
            st.plotly_chart(fig_r1, use_container_width=True)
        with cr2:
            rg = recs["genre"].str.split("|").explode().value_counts()
            fig_r2 = px.pie(values=rg.values, names=rg.index,
                title="Genre Mix in Recommendations", hole=0.5,
                color_discrete_sequence=["#9381FF","#B8B8FF","#FFD8BE","#FFEEDD","#7B6EE8"])
            fig_r2.update_layout(**PL, height=260)
            st.plotly_chart(fig_r2, use_container_width=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:32px;">
            <div style="font-size:.88rem;color:#9B8FCC;">Run the Recommendation Engine to see session analytics here.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)
