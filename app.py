from flask import Flask, request
from flask_cors import CORS
from flasgger import Swagger
from transformers import pipeline

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/sentiment', methods=['POST'])
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
    msg = request.get_json().get('msg')
    _sentiment = sentiment_pipeline(msg)

    return {"sentiment": _sentiment[0]}

app.run(host="0.0.0.0", port=8080, debug=True)
