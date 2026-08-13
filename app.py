# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import subprocess

# app = Flask(__name__)
# CORS(app)

# @app.route('/predict', methods=['POST'])
# def predict():

#     try:
#         data = request.json
#         text = data['text']

#         result = subprocess.check_output(
#             ['python', 'python/predict.py', text],
#             stderr=subprocess.STDOUT
#         ).decode('utf-8').strip()

#         print("Python Output:", result)

#         output = result.split('|')

#         return jsonify({
#             "prediction": output[0],
#             "confidence": output[1],
#             "explanation": output[2]
#         })

#     except Exception as e:
#         print("ERROR:", e)

#         return jsonify({
#             "prediction": "error",
#             "confidence": "0",
#             "explanation": str(e)
#         })

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

# Load model ONCE only
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Clean text
def clean_text(text):

    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    words = text.split()

    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(
                lemmatizer.lemmatize(word)
            )

    return ' '.join(filtered_words)

@app.route('/predict', methods=['POST'])
def predict():

    try:

        data = request.json
        input_text = data['text']

        cleaned_text = clean_text(input_text)

        text_vector = vectorizer.transform([cleaned_text])

        prediction = model.predict(text_vector)[0]

        probability = max(
            model.predict_proba(text_vector)[0]
        ) * 100

        reasons = []

        clickbait_words = [
            "breaking",
            "shocking",
            "miracle",
            "secret",
            "urgent",
            "share",
            "unbelievable"
        ]

        for word in clickbait_words:
            if word in input_text.lower():
                reasons.append(
                    f"Suspicious word detected: {word}"
                )

        if "!!!" in input_text:
            reasons.append(
                "Excessive punctuation detected"
            )

        if input_text.isupper():
            reasons.append(
                "ALL CAPS text detected"
            )

        sentiment = TextBlob(
            input_text
        ).sentiment.polarity

        if sentiment > 0.6 or sentiment < -0.6:
            reasons.append(
                "Highly emotional tone detected"
            )

        if len(reasons) == 0:
            explanation = "Text appears neutral and formal"
        else:
            explanation = "; ".join(reasons)

        return jsonify({
            "prediction": prediction,
            "confidence": round(probability, 2),
            "explanation": explanation
        })

    except Exception as e:

        return jsonify({
            "prediction": "error",
            "confidence": 0,
            "explanation": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)