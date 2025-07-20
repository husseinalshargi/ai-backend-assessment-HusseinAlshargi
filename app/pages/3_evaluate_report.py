from pathlib import Path
import streamlit as st
import os

st.set_page_config(page_title="Show Markdown Report", layout="wide")
st.title("Evaluation Report")

markdown_path = Path("benchmark/evaluation_report.md")

st.info("You can generate a new evaluation report from the scheduler page")

if os.path.exists(markdown_path):
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    st.markdown(markdown_content, unsafe_allow_html=True)
else:
    st.warning("No report found. Please generate an evaluation report first.")