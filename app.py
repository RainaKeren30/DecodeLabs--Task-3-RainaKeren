import streamlit as st

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.session import init_session
init_session()

page = st.session_state.get("current_page", "title")

if page == "title":
    from pages.title import render
    render()
else:
    from components.sidebar import render_sidebar
    render_sidebar()
    if page == "dashboard":
        from pages.dashboard import render; render()
    elif page == "home":
        from pages.home import render; render()
    elif page == "dataset":
        from pages.dataset import render; render()
    elif page == "engine":
        from pages.engine import render; render()
    elif page == "explain":
        from pages.explain import render; render()
    elif page == "analytics":
        from pages.analytics import render; render()
    elif page == "docs":
        from pages.docs import render; render()
