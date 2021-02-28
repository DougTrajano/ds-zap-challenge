import streamlit as st

def home_page(state):
    st.title("Phil, o avaliador de imóveis :house: ")
    st.write("""
    O Phil é um modelo de machine learning que avalia todos os dias milhares de imóveis e fornece recomendações de preços, seja para venda ou aluguel, não é incrível?

    Ele é capaz de interpretar e combinar várias informações dos imóveis como **quantidade de quartos, piscina, área útil, etc.**
    
    Também consegue relacionar tudo isso com informações do bairro que são fornecedias pelo IBGE como **renda média da região, indicadores de iluminação pública, etc.**

    
    """)

    st.write("""
    Se quiser vender seu imóvel, ligue para o Phil!

    ![](https://media2.giphy.com/media/wFOC9RazP97i0/giphy.gif)
    """)

    state.sync()