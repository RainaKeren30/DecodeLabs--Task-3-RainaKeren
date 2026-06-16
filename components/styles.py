"""
Global CSS — Periwinkle / Peach Fuzz palette throughout.
Ghost White #F8F7FF · Antique White #FFEEDD · Peach Fuzz #FFD8BE
Periwinkle #B8B8FF · Soft Periwinkle #9381FF
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&family=Poppins:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F8F7FF !important;
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    color: #1F2430;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]    { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── Page header ── */
.page-header {
    background: linear-gradient(135deg, #9381FF 0%, #B8B8FF 55%, #FFD8BE 100%);
    border-radius: 20px;
    padding: 38px 44px 34px;
    margin-bottom: 28px;
    box-shadow: 0 10px 36px rgba(147,129,255,0.22);
    position: relative; overflow: hidden;
}
.page-header::before {
    content:'';position:absolute;top:-60px;right:-60px;
    width:220px;height:220px;
    background:rgba(255,255,255,0.12);border-radius:50%;
}
.page-header h1 {
    font-family:'Poppins',sans-serif;font-size:1.9rem;font-weight:800;
    color:#2A235A;letter-spacing:-0.5px;margin-bottom:5px;
}
.page-header p {
    font-family:'Inter',sans-serif;font-size:0.92rem;
    color:rgba(42,35,90,0.70);font-weight:400;
}

/* ── Cards ── */
.card {
    background:#FFFFFF;
    border:1.5px solid rgba(147,129,255,0.13);
    border-radius:20px;
    padding:26px 26px 22px;
    box-shadow:0 4px 20px rgba(147,129,255,0.08);
    transition:box-shadow 0.3s ease,transform 0.3s ease;
    margin-bottom:14px;
}
.card:hover {
    box-shadow:0 10px 32px rgba(147,129,255,0.16);
    transform:translateY(-2px);
}
.card-sm {
    background:#FFFFFF;
    border:1.5px solid rgba(147,129,255,0.13);
    border-radius:16px;padding:18px 20px;
    box-shadow:0 2px 14px rgba(147,129,255,0.07);
    transition:box-shadow 0.3s ease,transform 0.25s ease;
    margin-bottom:10px;
}
.card-sm:hover {
    box-shadow:0 8px 24px rgba(147,129,255,0.14);
    transform:translateY(-1px);
}

/* ── Metric tile ── */
.metric-tile {
    background:#FFFFFF;
    border:1.5px solid rgba(147,129,255,0.13);
    border-radius:18px;padding:22px 20px 18px;
    box-shadow:0 3px 16px rgba(147,129,255,0.08);
    text-align:center;
}
.metric-tile .label {
    font-size:0.70rem;font-weight:700;color:#9B8FCC;
    text-transform:uppercase;letter-spacing:0.08em;margin-bottom:7px;
}
.metric-tile .value {
    font-family:'Poppins',sans-serif;font-size:1.9rem;font-weight:800;
    color:#2A235A;line-height:1;
}
.metric-tile .sub { font-size:0.74rem;color:#9B8FCC;margin-top:4px; }

/* ── Similarity bar ── */
.sim-bar-wrap { margin:7px 0 3px; }
.sim-bar-label {
    display:flex;justify-content:space-between;
    font-size:0.74rem;color:#9B8FCC;margin-bottom:4px;
}
.sim-bar-track {
    height:7px;background:rgba(147,129,255,0.13);
    border-radius:99px;overflow:hidden;
}
.sim-bar-fill {
    height:100%;border-radius:99px;
    background:linear-gradient(90deg,#9381FF,#B8B8FF,#FFD8BE);
    transition:width 0.55s cubic-bezier(0.25,0.46,0.45,0.94);
}

/* ── Badges ── */
.badge {
    display:inline-block;font-size:0.68rem;font-weight:700;
    padding:3px 10px;border-radius:99px;
    letter-spacing:0.04em;text-transform:uppercase;
}
.badge-primary { background:rgba(147,129,255,0.13);color:#5B48CC; }
.badge-gold    { background:linear-gradient(90deg,#FFD8BE,#FFEEDD);color:#8B5E3C; }
.badge-green   { background:rgba(34,197,94,0.10);color:#15803D; }
.badge-purple  { background:rgba(184,184,255,0.20);color:#4B3FAA; }

/* ── Recommendation card ── */
.rec-card {
    background:#FFFFFF;
    border:1.5px solid rgba(147,129,255,0.13);
    border-radius:20px;padding:20px 22px;
    box-shadow:0 3px 16px rgba(147,129,255,0.07);
    transition:box-shadow 0.3s ease,transform 0.3s ease;
    position:relative;overflow:hidden;margin-bottom:12px;
}
.rec-card::before {
    content:'';position:absolute;left:0;top:0;bottom:0;
    width:4px;
    background:linear-gradient(180deg,#9381FF,#B8B8FF,#FFD8BE);
    border-radius:4px 0 0 4px;
}
.rec-card:hover {
    box-shadow:0 10px 32px rgba(147,129,255,0.16);
    transform:translateY(-2px);
}
.rec-card.top-pick::before {
    background:linear-gradient(180deg,#FFD8BE,#FFEEDD,#9381FF);
}
.rec-card .rank-num {
    font-family:'Poppins',sans-serif;font-size:1.9rem;font-weight:800;
    color:rgba(147,129,255,0.16);position:absolute;right:18px;top:12px;line-height:1;
}
.rec-card .title {
    font-family:'Poppins',sans-serif;font-size:1rem;font-weight:700;
    color:#2A235A;margin-bottom:4px;
}
.rec-card .meta { font-size:0.78rem;color:#9B8FCC;margin-bottom:8px; }
.rec-card .rating-star { color:#FFB07A;font-weight:700; }

/* ── Section label ── */
.section-label {
    font-size:0.70rem;font-weight:700;text-transform:uppercase;
    letter-spacing:0.10em;color:#9B8FCC;margin-bottom:12px;
}

/* ── Divider ── */
.divider {
    height:1.5px;
    background:linear-gradient(90deg,rgba(147,129,255,0.10),rgba(255,216,190,0.20),rgba(147,129,255,0.10));
    border-radius:99px;margin:22px 0;
}

/* ── Glass panel ── */
.glass {
    background:rgba(248,247,255,0.60);
    backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
    border:1.5px solid rgba(255,255,255,0.70);
    border-radius:20px;
    box-shadow:0 8px 32px rgba(147,129,255,0.12);
    padding:26px;
}

/* ── Streamlit widget overrides ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border:1.5px solid rgba(147,129,255,0.22) !important;
    border-radius:12px !important;background:#FFFFFF !important;
}
.stButton > button {
    background:linear-gradient(135deg,#9381FF,#B8B8FF) !important;
    color:#2A235A !important;border:none !important;
    border-radius:12px !important;
    font-family:'Space Grotesk',sans-serif !important;
    font-weight:700 !important;font-size:0.90rem !important;
    padding:10px 26px !important;
    box-shadow:0 4px 18px rgba(147,129,255,0.30) !important;
    transition:all 0.25s ease !important;
}
.stButton > button:hover {
    box-shadow:0 8px 28px rgba(147,129,255,0.44) !important;
    transform:translateY(-1px) !important;
}
div[data-testid="stMetricValue"] {
    font-family:'Poppins',sans-serif;font-size:1.9rem;
    font-weight:800;color:#2A235A;
}
div[data-testid="stMetricLabel"] {
    font-size:0.70rem;font-weight:700;color:#9B8FCC;
    text-transform:uppercase;letter-spacing:0.07em;
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    import streamlit as st
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            {'<p>' + subtitle + '</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def similarity_bar(label: str, pct: float):
    import streamlit as st
    pct = max(0, min(100, pct))
    st.markdown(
        f"""
        <div class="sim-bar-wrap">
            <div class="sim-bar-label"><span>{label}</span><span>{pct:.1f}%</span></div>
            <div class="sim-bar-track">
                <div class="sim-bar-fill" style="width:{pct}%"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_tile(label: str, value: str, sub: str = ""):
    import streamlit as st
    st.markdown(
        f"""
        <div class="metric-tile">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {'<div class="sub">' + sub + '</div>' if sub else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def rec_card(title: str, year: int, genre: str, director: str, rating: float,
             similarity: float, rank: int, is_top: bool = False):
    import streamlit as st
    badge = '<span class="badge badge-gold">Top Pick</span>' if is_top else f'<span class="badge badge-primary">Rank #{rank}</span>'
    cls = "rec-card top-pick" if is_top else "rec-card"
    genres = " · ".join(genre.split("|")[:3])
    st.markdown(
        f"""
        <div class="{cls}">
            <div class="rank-num">#{rank}</div>
            {badge}
            <div class="title" style="margin-top:8px">{title}</div>
            <div class="meta">{year} &nbsp;·&nbsp; {genres} &nbsp;·&nbsp;
                <span class="rating-star">★</span> {rating}</div>
            <div class="meta" style="margin-bottom:8px">Directed by {director}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    similarity_bar("Content Similarity", similarity)
    st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)
