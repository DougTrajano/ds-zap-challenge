# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing at this moment.

## [1.0.0] - 2021-02-28

### Added

- API Service (powered by [FastAPI](https://fastapi.tiangolo.com/)) to serve the ML model.
- [MLFlow](https://www.mlflow.org/) for machine learning lifecycle.
- Data App (powered by [Streamlit](https://www.streamlit.io/)) for model interaction and presentation.
- `/docs` folder with documentation about each component of this project.
- `/properties` folder with `application.json` to storage application properties.

### Changed

- A new trained machine learning model. See more on [MLflow Tracking UI](https://www.mlflow.org/docs/latest/tracking.html#tracking-ui).
