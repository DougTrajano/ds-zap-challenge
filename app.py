import streamlit as st
import pandas as pd
import numpy as np

from app.multi_app import MultiApp
from app.home import *
from app.features_selection import *
from app.modeling import *
from app.reports import *

st.set_page_config(page_title="Phil, o avaliador de imóveis",
                        page_icon="https://assets.zap.com.br/assets/v5.71.0/32x32.png")

app = MultiApp()

app.add_app("Home", home_page)
app.add_app("Features selection", features_page)
app.add_app("Modeling", modeling_page)
app.add_app("Reports", reports_page)

app.run()
