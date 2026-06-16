import streamlit as st
from utils.data_loader import load_movies
from models.recommender import MovieRecommender

def init_session():
    if "df" not in st.session_state:
        st.session_state["df"] = load_movies()
    if "recommender" not in st.session_state:
        st.session_state["recommender"] = MovieRecommender(st.session_state["df"])
    if "recommendations" not in st.session_state:
        st.session_state["recommendations"] = None
    if "last_preferences" not in st.session_state:
        st.session_state["last_preferences"] = {}
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "title"
    if "user_ratings" not in st.session_state:
        st.session_state["user_ratings"] = {}
