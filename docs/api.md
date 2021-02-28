# API - [FastAPI](https://fastapi.tiangolo.com/)

The model is served with an API powered by [FastAPI](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

<img src="https://camo.githubusercontent.com/86d9ca3437f5034da052cf0fd398299292aab0e4479b58c20f2fc37dd8ccbe05/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d7465616c2e706e67" width="400"/>

---

## API docs

This API has 3 endpoints available.

### `/docs`

Here you will find all the endpoints and how to use them correctly.

![](images/api.png)

### `/health`

Check if API is live.

![](images/api_health.png)

### `/predict`

Predict sales price from an apartment.
 
![](images/api_predict.png)

---

## How to deploy this API?

The API was developed with FastAPI, see more [here](https://fastapi.tiangolo.com/deployment/docker/).

### Build the Docker image

Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).

Build your FastAPI image:

```
docker build . -t ds-zap-challenge
```

### Start the Docker container

Run a container based on your image:

```
docker run -d --name ds-zap-challenge -p 80:80 ds-zap-challenge
```

Now you have an optimized FastAPI server in a Docker container.

You should be able to interact with this API using your Docker host.