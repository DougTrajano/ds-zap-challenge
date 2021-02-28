import streamlit as st

def read_md(path):
    with open(path, 'r') as md_file:
        content = md_file.read()
    return content

def api_page(state):
    md_content = read_md("docs/api.md")
    st.markdown(md_content, unsafe_allow_html=True)
    state.sync()

def app_page(state):
    md_content = read_md("docs/data_app.md")
    st.markdown(md_content, unsafe_allow_html=True)
    state.sync()

def model_page(state):
    st.write("Pending")
    state.sync()

def report_page(state):
    st.write("Pending")
    state.sync()