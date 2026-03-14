import streamlit as st
from db.models import init_db

# Initialise DB on first run
init_db()

st.set_page_config(
    page_title="My Journal",
    page_icon="📓",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("📓 My AI Journal")
st.markdown(
    """
    Welcome to your personal AI-powered journal.
    Use the sidebar to navigate between sections.
    """
)

st.sidebar.title("Navigation")
st.sidebar.markdown("---")
st.sidebar.info(
    "**Pages coming in later plans:**\n"
    "- 📝 Log Your Day\n"
    "- 💬 Ask About Your Day\n"
    "- 📊 Insights & Summaries"
)

st.markdown("---")
st.success("✅ App is running. Database connected. Ready to build Plan 2!")
