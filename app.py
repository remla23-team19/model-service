from flasgger import Swagger
from flask import Flask, jsonify, request

import model_library as modellib

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/sentiment", methods=["POST"])
def predict():
    """
    Make a prediction of the sentiment of a message.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: Message to be classified
          required: True
          schema:
            type: object
            required:
              - msg
            properties:
                msg:
                    type: string
                    example: I am happy
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            sentiment:
              type: object
              properties:
                label:
                  type: string
                  enum: ['POSITIVE', 'NEGATIVE']
                  description: Predicted sentiment label
                  example: 'POSITIVE'
                score:
                  type: number
                  format: float
                  minimum: 0
                  maximum: 1
                  description: Prediction confidence score
                  example: 0.9999998807907104
    """
    data = request.get_json()
    msg = data.get("msg")
    version = data.get("version") if "version" in data and modellib.verify_version(data.get("version")) and data.get("version") in modellib.get_available_models() else "base"

    sentiment = modellib.predict_sentiment(msg, version)
    response = jsonify({"sentiment": {
        "label": modellib.PREDICTION_MAP[sentiment],
        "score": 1.0
    }})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/versions", methods=["GET"])
def get_available_versions():
    """
    Get available model versions.
    ---
    responses:
      200:
        description: List of available model versions
        schema:
          type: array
          items:
            type: string
            description: Model version
            example: v1.0.1
    """
    available_versions = modellib.get_available_models()
    response = jsonify(available_versions)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


app.run(host="0.0.0.0", port=8080, debug=True)
