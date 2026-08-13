import sys
import pickle
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# nltk.download('stopwords')
# nltk.download('wordnet')

# Load model and vectorizer
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
            filtered_words.append(lemmatizer.lemmatize(word))

    return ' '.join(filtered_words)

# Get input
input_text = " ".join(sys.argv[1:])
cleaned_text = clean_text(input_text)

# Transform text
text_vector = vectorizer.transform([cleaned_text])

# Predict
prediction = model.predict(text_vector)[0]
probability = max(model.predict_proba(text_vector)[0]) * 100

# Explanation system
reasons = []

# Clickbait words
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
        reasons.append(f"Suspicious word detected: {word}")

# Excess punctuation
if "!!!" in input_text:
    reasons.append("Excessive punctuation detected")

# Capital letters
if input_text.isupper():
    reasons.append("ALL CAPS text detected")

# Sentiment analysis
sentiment = TextBlob(input_text).sentiment.polarity

if sentiment > 0.6 or sentiment < -0.6:
    reasons.append("Highly emotional tone detected")

# Final explanation
if len(reasons) == 0:
    explanation = "Text appears neutral and formal"
else:
    explanation = "; ".join(reasons)

# Output
print(prediction + "|" + str(round(probability, 2)) + "|" + explanation)