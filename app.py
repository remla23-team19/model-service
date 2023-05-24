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
    response = flask.jsonify({"sentiment": _sentiment[0]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run(host="127.0.0.1", port=8080, debug=True)

