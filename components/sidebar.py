"""
Sidebar navigation — matches Periwinkle/Peach palette.
"""

import streamlit as st

NAV_ITEMS = [
    ("Dashboard",             "dashboard"),
    ("Project Overview",      "home"),
    ("Dataset Explorer",      "dataset"),
    ("Recommendation Engine", "engine"),
    ("Explanation View",      "explain"),
    ("Analytics",             "analytics"),
    ("Documentation",         "docs"),
]


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Poppins:wght@700;800&display=swap');
            [data-testid="stSidebar"] {
                background: rgba(248,247,255,0.96) !important;
                border-right: 1.5px solid rgba(147,129,255,0.14) !important;
                box-shadow: 4px 0 28px rgba(147,129,255,0.08) !important;
            }
            [data-testid="stSidebar"] .stButton > button {
                background: transparent !important;
                color: #5B4FA8 !important;
                border: none !important;
                border-radius: 10px !important;
                font-family: 'Space Grotesk', sans-serif !important;
                font-size: 0.84rem !important;
                font-weight: 500 !important;
                padding: 8px 14px !important;
                box-shadow: none !important;
                text-align: left !important;
                justify-content: flex-start !important;
                transition: all 0.2s ease !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background: rgba(147,129,255,0.10) !important;
                color: #2A235A !important;
                transform: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="padding:12px 4px 20px;">
                <div style="
                    font-family:'Poppins',sans-serif;
                    font-size:1.25rem;font-weight:800;
                    background:linear-gradient(135deg,#9381FF,#B8B8FF 60%,#FFD8BE);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;letter-spacing:-0.4px;line-height:1.2;
                ">CineMatch AI</div>
                <div style="font-size:0.68rem;color:#9B8FCC;font-weight:600;
                            margin-top:3px;letter-spacing:0.06em;text-transform:uppercase;">
                    Recommendation System
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="font-size:0.65rem;color:#9B8FCC;font-weight:700;
                        text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;padding-left:4px;">
                Navigation
            </div>
            """,
            unsafe_allow_html=True,
        )

        current = st.session_state.get("current_page", "title")
        for label, key in NAV_ITEMS:
            active = current == key
            if active:
                st.markdown(
                    f"""
                    <div style="
                        background:linear-gradient(90deg,rgba(147,129,255,0.16),rgba(184,184,255,0.08));
                        border-left:3px solid #9381FF;
                        border-radius:0 10px 10px 0;
                        padding:8px 14px;
                        font-family:'Space Grotesk',sans-serif;
                        font-size:0.84rem;font-weight:700;
                        color:#2A235A;margin-bottom:2px;
                    ">{label}</div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state["current_page"] = key
                    st.rerun()

        st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="
                background:rgba(147,129,255,0.07);
                border:1.5px solid rgba(147,129,255,0.16);
                border-radius:14px;padding:14px 15px;
            ">
                <div style="font-size:0.67rem;color:#9B8FCC;font-weight:700;
                            text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">
                    Tech Stack
                </div>
                <div style="font-size:0.76rem;color:#3D2F8A;line-height:1.85;font-weight:500;">
                    Python · Pandas<br>
                    Scikit-learn · TF-IDF<br>
                    Cosine Similarity<br>
                    Streamlit · Plotly
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
