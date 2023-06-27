# Model Service 🔬
[![Latest Tag](https://img.shields.io/github/tag/remla23-team19/model-service.svg)](https://github.com/remla23-team19/model-service/tags) [![Latest Commit](https://img.shields.io/github/last-commit/remla23-team19/model-service.svg)](https://github.com/remla23-team19/model-service/commits/main) [![Python Version](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-380/)

Wrapper service for the ML model (see [model-training](https://github.com/remla23-team19/model-training)). The service is able to receive a text input and return the sentiment analysis of the text.


#### Example
* Input, POST request to `/sentiment`:
```json
{
    "msg": "I am happy"
}
```

* Output, `JSON` containing a label and score (note: this is dummy data)

```json
{
    "sentiment": {
        "label": "POSITIVE",
        "score": 0.9999998807907104
    }
}
```

For the complete documentation, please visit `/apidocs` when running the service.
If you want to connect to the frontend of this service, please visit [operation](https://github.com/remla23-team19/operation) to launch the complete project with all the components running together.


## Instructions ⚙️

Clone the repository:

```sh
git clone https://github.com/remla23-team19/model-service.git
```

You can either run the webservice locally or in a Docker container. 


### Running the webservice locally

Download [Poetry](https://python-poetry.org):

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Set up the virtual environment (Python 3.8):

```sh
poetry env use python3.8
```

Install the dependencies:

```sh
poetry install
```

> Note: for details, please refer to `pyproject.toml`.

### Running the webservice in a Docker container

Alternatively, you can run it in a **Docker** container by following the instructions below.

* Build the Docker image:
```zsh
docker build -t modelservice .
```

* Run the Docker image:
```zsh
docker run --rm -it -p 8080:8080 modelservice
```
