import streamlit as st
import pandas as pd
import numpy as np

st.beta_set_page_config(page_title="Phil, o avaliador de imóveis",
                        page_icon="https://assets.zap.com.br/assets/v5.71.0/32x32.png")


class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self, title="Phil (Data App)"):

        st.sidebar.title(title)
        app = st.sidebar.radio(
            'Páginas',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()

        st.sidebar.write(
            "Autor: [Douglas Trajano](https://dougtrajano.github.io/resume/)")
        st.sidebar.subheader("Descrição")
        st.sidebar.write(
            "Este projeto foi desenvolvido para o [Data Science Challenge](https://grupozap.github.io/cultura/challenges/data-science.html) do Grupo ZAP.")

        st.sidebar.subheader("Source code")
        st.sidebar.write(
            "[DougTrajano/ds-zap-challenge](https://github.com/DougTrajano/ds-zap-challenge)")


def main_page():
    st.title("Phil, o avaliador de imóveis :house: ")
    st.write("""
    O Phil é um modelo de inteligência artificial que avalia todos os dias milhares de imóveis e fornece recomendações de preços, seja para venda ou aluguel, não é incrível?

    Ele é capaz de interpretar e combinar várias informações dos imóveis como **quantidade de quartos, piscina, área útil, etc.** Também consegue relacionar tudo isso com informações do bairro que são fornecedias pelo IBGE como **renda média da região, indicadores de iluminação pública, etc.**

    ![](https://i.pinimg.com/600x315/9b/06/f7/9b06f7d612112f97a271efc278afe425.jpg)

    Foram mais de 77 mil anúncios analisados.

    ![](https://media0.giphy.com/media/fcpJebgkQ14UE/giphy.gif)

    Parece muito né? Mas ele conseguiria analisar muito mais. :)
    """)

    st.write("""
    ## O que preciso para ser melhor?

    Preciso aprender mais sobre os imóveis, coletar mais informações do que foi colocado na **descrição do anúncio** e também sobre a região em que ele está localizado, usando os dados do Censo Sensitário do IBGE.

    O IBGE fornece 26 arquivos apenas para a cidade de **São Paulo - SP**, existem muitas variáveis lá que deverão ser extremamente ricas para aprender mais sobre os preços dos imóveis.

    ---

    """)

    st.write("""
    Se quiser vender seu imóvel, ligue para o Phil!

    ![](https://media2.giphy.com/media/wFOC9RazP97i0/giphy.gif)
    """)


def modeling_page():
    with open('../docs/modeling.md') as md_file:
        data = md_file.read()
    st.write(data)


def features_page():
    with open('../docs/features_selection.md') as md_file:
        data = md_file.read()
    st.write(data)
    st.write("## Localizações dos imóveis")
    df = pd.read_feather("../data/processed/geolocations.feather")
    st.map(df)


def reports_page():
    with open('../docs/reports.md') as md_file:
        data = md_file.read()
    st.write(data)

app = MultiApp()

app.add_app("Página inicial", main_page)
app.add_app("Modelagem", modeling_page)
app.add_app("Selação de variáveis", features_page)
app.add_app("Resultados", reports_page)

app.run()
