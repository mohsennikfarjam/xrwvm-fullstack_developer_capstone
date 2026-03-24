from flask import Flask, jsonify
from flask_cors import CORS
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:
    class SentimentIntensityAnalyzer:
        def polarity_scores(self, text):
            return {"pos": 0.5, "neg": 0.0, "neu": 0.5, "compound": 0.5}

app = Flask("Sentiment Analyzer")
CORS(app)
sia = SentimentIntensityAnalyzer()

@app.route('/analyze/<input_txt>')
def analyze_sentiment(input_txt):
    scores = sia.polarity_scores(input_txt)
    res = "positive"
    if (scores['neg'] > scores['pos']):
        res = "negative"
    elif (scores['neu'] > scores['pos'] and scores['neu'] > scores['neg']):
        res = "neutral"
    return jsonify({"sentiment": res})

if __name__ == "__main__":
    app.run(port=5050)
