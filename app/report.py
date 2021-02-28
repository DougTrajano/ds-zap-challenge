import streamlit as st

def read_md(path):
    with open(path, 'r') as md_file:
        content = md_file.read()
    return content

def report_page(state):
    report_md = read_md('docs/report.md')
    st.markdown(report_md)

    # Test model
    # Pending

    state.sync()