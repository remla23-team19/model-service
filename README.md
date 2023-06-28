# Model Service 🔬
[![Latest Tag](https://img.shields.io/github/tag/remla23-team19/model-service.svg)](https://github.com/remla23-team19/model-service/tags) [![Latest Commit](https://img.shields.io/github/last-commit/remla23-team19/model-service.svg)](https://github.com/remla23-team19/model-service/commits/main) [![Python Version](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-380/)

Wrapper service for the ML model (see [model-training](https://github.com/remla23-team19/model-training)). The service is able to receive a text input and return the sentiment analysis of the text in the context of restaurant reviews.


#### Example
* Input, POST request to `/sentiment`:
```json
{
    "msg": "Phenomenal food, service and ambiance."
    "version": "1.0.0"
}
```

Here, `msg` is the review to be analyzed and `version` is the version of the model to be used.
The model version is optional, if not specified, the base version will be used.
If the specified version is not available, the base version will be used.

* Output, `JSON` containing a label for the sentiment:

```json
{
    "sentiment": {
        "label": "POSITIVE"
    }
}
```

For the complete documentation, please visit `/apidocs` when running the service.
If you want to connect to the frontend of this service, please visit [operation](https://github.com/remla23-team19/operation) to launch the complete project with all the components running together.
If you want to play with the model without running the webservice, run `model_library.py` as main and you will be able to test the model with your own input (as configured at the bottom of the file).


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
