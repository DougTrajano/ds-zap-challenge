import streamlit as st

def api_page(state):
    st.title("API - [FastAPI](https://fastapi.tiangolo.com/)")
    st.markdown("""
    The model is served with an API powered by [FastAPI](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
    """)
    st.image("docs/images/fastapi.png", width=400)
    
    st.header("API docs")
    st.write("This API has 3 endpoints available.")
    
    st.subheader("`/docs`")
    st.write("Here you will find all the endpoints and how to use them correctly.")
    st.image("docs/images/api.png", use_column_width=True)

    st.subheader("`/health`")
    st.write("Check if API is live.")
    st.image("docs/images/api_health.png", use_column_width=True)

    st.subheader("`/predict`")
    st.write("Predict sales price from an apartment.")
    st.image("docs/images/api_predict.png", use_column_width=True)

    st.header("How to deploy this API?")
    st.write("The API was developed with FastAPI, see more [here](https://fastapi.tiangolo.com/deployment/docker/).")

    st.subheader("Build the Docker image")
    st.write("Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).")
    st.write("Build your FastAPI image:")
    st.code("docker build . -t ds-zap-challenge")

    st.subheader("Start the Docker container")
    st.write("Run a container based on your image:")
    st.code("docker run -d --name ds-zap-challenge -p 80:80 ds-zap-challenge")
    st.write("Now you have an optimized FastAPI server in a Docker container.")
    st.write("You should be able to interact with this API using your Docker host.")

    state.sync()

def app_page(state):
    st.title("Data App - [Streamlit](https://www.streamlit.io/)")
    st.write("We have a data app available for this project.")
    st.write("This was created with [Streamlit](https://www.streamlit.io/). The fastest way to build and share data apps.")
    st.image("docs/images/streamlit.png", width=400)

    st.subheader("How to see this Data App?")
    st.markdown("[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dougtrajano/ds-zap-challenge/main/app.py)")

    st.subheader("How to run it locally?")

    st.write("Install Python requirements.")
    st.code("pip install -r requirements.txt")

    st.write("Run Streamlit App")
    st.code("streamlit run app/main.py")

    st.write("Open one of URLs printed on console by Streamlit.")
    st.image("docs/images/streamlit_urls.png")
    state.sync()

def model_page(state):
    st.title("Machine Learning Model - [MLflow](https://www.mlflow.org/)")
    st.write("The last model (a XGBoost Regressor) was trained on **February 27 | 2021**.")

    st.header("Scores")
    st.markdown("""
    | Metric | Score |
    | - | - |
    | R2 Score (cross-validation)| 0.8253 |
    | R2 Score (test set) | 0.8464 |
    """)

    st.header("Hyperparameters")
    st.markdown("""
    | Hyperparameter | Value |
    | - | - |
    | objective | "reg:squarederror" |
    | base_score | 0.5 |
    | booster | "dart" |
    | colsample_bylevel | 0.45089899886494966 |
    | colsample_bynode | 1.0 |
    | colsample_bytree | 0.8070554145088148 |
    | gamma | 0 |
    | gpu_id | -1 |
    | importance_type | "gain" |
    | interaction_constraints | "" |
    | learning_rate | 0.1696738106834926 |
    | max_delta_step | 0 |
    | max_depth | 5 |
    | min_child_weight | 1 |
    | missing | nan |
    | monotone_constraints | "()" |
    | n_estimators | 1000 |
    | n_jobs | 0 |
    | num_parallel_tree | 1 |
    | random_state | 1993 |
    | reg_alpha | 0.21974995218922627 |
    | reg_lambda | 1.2579087520356529 |
    | scale_pos_weight | 1 |
    | subsample | 1.0 |
    | tree_method | "exact" |
    | validate_parameters | 1 |
    | verbosity | None |
    """)

    st.header("Machine Learning Lifecycle")

    st.write("[MLflow](https://www.mlflow.org/) is an open source platform for the machine learning lifecycle.")

    st.image("docs/images/mlflow_detailed.png", use_column_width=True)

    st.subheader("Tracking experiments")
    st.write("The model(s) trained in this project was tracked with mlflow API.")
    st.write("The files involve with MLflow are in `/mlruns` folder.")

    st.subheader("Viewing the Tracking UI")
    st.write("You can see all experiments in MLflow Tracking UI, just type this command in the terminal of the project directory.")
    st.code("mlflow ui")

    state.sync()

def report_page(state):
    st.write("Pending")
    state.sync()