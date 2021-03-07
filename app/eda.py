import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache
def load_df(path):
    return pd.read_feather(path)

def eda_pdreport_page(state):
    from pandas_profiling import ProfileReport
    from streamlit_pandas_profiling import st_profile_report

    st.title(":bar_chart: EDA - Profile Report")

    df_train = pd.read_feather("data/processed/train.feather")

    profile = ProfileReport(df_train,
                            title="ds-zap-challenge - Train dataset",
                            dark_mode=True, minimal=True)

    st_profile_report(profile)

    state.sync()


def eda_custom_page(state):
    st.title(":bar_chart: EDA - Chart Builder")

    df_train = load_df("data/processed/train.feather")

    # Prep columns
    cols = df_train.columns.tolist()

    # Filte invalid_cols
    invalid_cols = ['id']
    cols = [col for col in cols if col not in invalid_cols]

    cols.sort()

    col1, col2 = st.beta_columns(2)

    x = col1.selectbox('X', cols, index=cols.index('price'))
    y = col2.selectbox('Y', cols, index=cols.index('price'))

    color = col1.selectbox('Color', [None]+cols)
    
    min_price = int(df_train['price'].min())
    max_price = int(df_train['price'].max())

    prices = col2.slider('Price range', min_value=min_price,
                         max_value=max_price,
                         value=(min_price, max_price))

    df_train = df_train[(df_train['price'] >= prices[0]) &
                        (df_train['price'] <= prices[1])]

    fig_title = 'Scatter Plot'
    fig = px.scatter(df_train, x=x, y=y, color=color, title=fig_title)
    st.plotly_chart(fig, use_container_width=True)

    state.sync()


def eda_analysis_page(state):
    st.title(":bar_chart: EDA - Analysis")
    st.write("On this page you will find some interesting charts that were created on the Chart Builder page.")

    # Load training dataset
    df_train = load_df("data/processed/train.feather")

    st.header("Price's outliers")
    st.write("The first thing that I identifed is that there are some outliers in the price variable.")
    fig = px.scatter(df_train, x='price', y='price',
                     color=None, title="Identifying price's outliers")

    st.plotly_chart(fig, use_container_width=True)

    st.write("I will remove the property that costs 74.2 million.")

    # Filter dataset
    df_train = df_train[df_train['price'] <= 30000000]

    st.header("IBGE Census Data - High salary rate")
    st.write("""
    As mentioned earlier, I added IBGE census data to the dataset.

    I created a variable called `high_salary_rate` that is based on the proportion of rich people identified over all reported incomes.
    """)

    fig = px.scatter(df_train, x='price', y='high_salary_rate',
                     color=None, title="High salary rate vs Price")
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    It's possible to see that there's a rise in the price for real estate in neighborhoods with a high concentration of people with high salaries.
    """)

    st.header('Rented properties')

    st.write("""
    Another interesting view is in the distribution of properties identified as rented.

    See that more expensive properties tend to have less rented properties in the neighborhood.
    """)

    fig = px.scatter(df_train, x='price', y='ident_logradouro_alugados',
                     color=None, title="Rented properties vs Price")
    st.plotly_chart(fig, use_container_width=True)

    st.header("High Salary vs Low/Middle Salary")

    st.write("""
    
    """)

    col1, col2 = st.beta_columns(2)
    fig = px.scatter(df_train, x='price', y='renda_nom_dom_sal_alto2',
                     color=None, title="High salaries")
    col1.plotly_chart(fig, use_container_width=True)

    col1.markdown("""
    See that properties identified with a high proportion of middle incomes have a lower price than properties with less concentration of them.
    """)
    fig = px.scatter(df_train, x='price', y='renda_nom_dom_sal_medio1',
                     color=None, title="Middle salaries")
    col2.plotly_chart(fig, use_container_width=True)

    col2.info("This behavior occurs with the other low and medium incomes.")

    state.sync()