import streamlit as st

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