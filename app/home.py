import streamlit as st

def home_page(state):
    st.title(":house: Phil, virtual realtor")

    st.warning("""
    This project shouldn't be used in production environment or for decision making without validating its results.
    
    This project has no support lifecycle and has only learning purposes.""")

    st.subheader("Who is Phil?")
    st.write("Phil is a machine learning model that predicts sales prices for apartments advertised on our webiste.")

    st.subheader("How does he do that?")
    st.write("""
    Phil analyzes a lot of information about the ads and combines this with geographic data, for example, neighborhood average income, street lighting indicators, etc.
    """)

    st.subheader("Phil Dunphy")
    st.write("For all your Real Estate needs.")
    st.markdown("![](https://media2.giphy.com/media/wFOC9RazP97i0/giphy.gif)")

    state.sync()