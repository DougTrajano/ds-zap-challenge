import streamlit as st

from app.multi_app import MultiApp
from app.docs import api_page, app_page, model_page
from app.report import report_page
from app.home import home_page
from app.eda import eda_analysis_page, eda_pdreport_page, eda_custom_page
from ds_code.processing.helper_functions import read_json

# Import pages

#from features_selection import *
#from modeling import *
#from reports import *

params = read_json("properties/application.json")

st.set_page_config(page_title=params["streamlit"]["title"],
                   layout=params["streamlit"]["layout"])

app = MultiApp()

app.add_app("Home", home_page)

# Docs
app.add_app("Docs - API", api_page)
app.add_app("Docs - Data App", app_page)
app.add_app("Docs - ML model", model_page)
app.add_app("Docs - Report", report_page)
app.add_app("EDA - Analysis", eda_analysis_page)
app.add_app("EDA - Chart Builder", eda_custom_page)
app.add_app("EDA - Profile Report", eda_pdreport_page)

#app.add_app("Features selection", features_page)
#app.add_app("Modeling", modeling_page)
#app.add_app("Reports", reports_page)

app.run(title=params["streamlit"]["title"],
        disable_menu=params["streamlit"]["disable_menu"])
