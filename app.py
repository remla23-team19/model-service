from flask import Flask, request
from flasgger import Swagger
from transformers import pipeline

app = Flask(__name__)
swagger = Swagger(app)
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/sentiment/', methods=['POST'])
def predict():
    msg = request.get_json().get('msg')
    _sentiment = sentiment_pipeline(msg)

    return {"sentiment": _sentiment[0]}

app.run(host="0.0.0.0", port=8080, debug=True)

