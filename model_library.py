import os
import pickle
import re
import sys
from typing import List, Union

import joblib
import pandas as pd
import requests

TRAINED_MODELS_REPO: str = "remla23-team19/model-training"

BOW_MODEL_NAME: str = "c1_BoW_Sentiment_Model.pkl"
CLASSIFIER_MODEL_NAME: str = "c2_Classifier_Sentiment_Model"

MODEL_VERSION_PATTERN: str = r"v[0-9]+.[0-9]+.[0-9]+"

MODEL_OUTPUT_PATH: str = os.path.join(os.path.dirname(__file__), "models")
BASE_MODELS_PATH: str = os.path.join(MODEL_OUTPUT_PATH, "base")

PREDICTION_MAP = {0: "NEGATIVE", 1: "POSITIVE"}

base_version: str = "base"
CURR_VERSION = base_version

models_folder = os.path.join(MODEL_OUTPUT_PATH, base_version)
bow_path = os.path.join(models_folder, "bow.pkl")
classifier_path = os.path.join(models_folder, "classifier")

if not os.path.exists(bow_path):
    raise ValueError("BoW model not found for version: " + base_version)
if not os.path.exists(classifier_path):
    raise ValueError("Classifier model not found for version: " + base_version)

# Load models
CURR_CLASSIFIER_MODEL = joblib.load(classifier_path)
with open(bow_path, "rb") as f:
    CURR_BOW_MODEL = pickle.load(f)


def predict_sentiment(review: str, version: str = "base", verbose: bool = False) -> int:
    global CURR_VERSION
    global CURR_BOW_MODEL
    global CURR_CLASSIFIER_MODEL

    if not CURR_VERSION == version:
        models_folder = os.path.join(MODEL_OUTPUT_PATH, __version_format(version))
        bow_path = os.path.join(models_folder, "bow.pkl")
        classifier_path = os.path.join(models_folder, "classifier")

        if not os.path.exists(bow_path) and not os.path.exists(classifier_path):
            _download_models(version)
            if not os.path.exists(bow_path):
                raise ValueError("BoW model could not be installed/found for version: " + version)
            if not os.path.exists(classifier_path):
                raise ValueError("Classifier model could not be installed/found for version: " + version)

        # Load models
        CURR_VERSION = version
        CURR_CLASSIFIER_MODEL = joblib.load(classifier_path)
        with open(bow_path, "rb") as f:
            CURR_BOW_MODEL = pickle.load(f)

    X = CURR_BOW_MODEL.transform([review]).toarray()
    y_pred = CURR_CLASSIFIER_MODEL.predict(X)

    if verbose:
        print(str(y_pred[0]) + " (" + str(PREDICTION_MAP[y_pred[0]]) + ") -> review:", review)

    return y_pred[0]


def _download_models(version: str):
    if not re.match(MODEL_VERSION_PATTERN, version):
        raise ValueError("Invalid model version: " + version)

    bow_url = f"https://github.com/{TRAINED_MODELS_REPO}/releases/download/{version}/{BOW_MODEL_NAME}"
    classifier_url = f"https://github.com/{TRAINED_MODELS_REPO}/releases/download/{version}/{CLASSIFIER_MODEL_NAME}"

    model_version_output_path = os.path.join(
        MODEL_OUTPUT_PATH, __version_format(version)
    )

    if not os.path.exists(model_version_output_path):
        os.makedirs(model_version_output_path)

    bow_output_path = os.path.join(model_version_output_path, "bow.pkl")
    classifier_output_path = os.path.join(model_version_output_path, "classifier")

    if not os.path.exists(bow_output_path):
        print("Downloading BoW model " + version + " from " + bow_url)
        with open(bow_output_path, "wb") as f:
            bow_response = requests.get(bow_url, timeout=25)
            if not bow_response.status_code == 200:
                raise ValueError("BoW model could not be downloaded for version: " + version)
            f.write(bow_response.content)

    if not os.path.exists(classifier_output_path):
        print("Downloading classifier model " + version + " from " + classifier_url)
        with open(classifier_output_path, "wb") as f:
            classifier_response = requests.get(classifier_url, timeout=25)
            if not classifier_response.status_code == 200:
                raise ValueError("Classifier model could not be downloaded for version: " + version)
            f.write(classifier_response.content)

    print("[DATA PHASE COMPLETE]")


def get_available_models() -> List[str]:
    response = requests.get(__get_api_url_tags(TRAINED_MODELS_REPO))
    data = response.json()

    available_versions: List[str] = []

    for item in data:
        version: str = item["ref"].replace("refs/tags/", "")
        if re.match(MODEL_VERSION_PATTERN, version):
            available_versions.append(version)

    return available_versions

def verify_version(version: str) -> bool:
    return re.match(MODEL_VERSION_PATTERN, version)

def __get_api_url_tags(repo):
    return f"https://api.github.com/repos/{repo}/git/refs/tags"


def __version_format(version: str) -> str:
    return version.replace(".", "-")


def __version_unformat(version: str) -> str:
    return version.replace("-", ".")


if __name__ == "__main__":
    print(get_available_models())
    predict_sentiment("The potatoes were like rubber and you could tell they had been made up ahead of time being kept under a warmer.", version="v1.0.1", verbose=True)
    predict_sentiment("The fries were great too.", version="v1.0.1", verbose=True)
