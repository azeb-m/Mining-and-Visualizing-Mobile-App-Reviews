# src/nlp/sentiment.py

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
import nltk
import math
import os

# ----------------------------------------------------------------------
# Ensure VADER lexicon is available
# ----------------------------------------------------------------------
nltk.download('vader_lexicon')

# ----------------------------------------------------------------------
# Load cleaned reviews
# ----------------------------------------------------------------------
input_path = 'data/clean/reviews_clean.csv'
output_path = 'data/clean/reviews_sentiment.csv'

if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input file not found: {input_path}")

df = pd.read_csv(input_path)

# Ensure text column exists
if 'review_clean' not in df.columns:
    raise ValueError("Column 'review_clean' is missing in the dataset")

# ----------------------------------------------------------------------
# 1. VADER Sentiment Analysis
# ----------------------------------------------------------------------
print("Running VADER sentiment...")

sia = SentimentIntensityAnalyzer()

df['vader_compound'] = df['review_clean'].apply(
    lambda t: sia.polarity_scores(str(t))['compound']
)

def label_v(x):
    if x >= 0.05:
        return 'positive'
    if x <= -0.05:
        return 'negative'
    return 'neutral'

df['sentiment_vader'] = df['vader_compound'].apply(label_v)

print("✓ VADER complete.")

# ----------------------------------------------------------------------
# 2. DistilBERT Sentiment Analysis
# ----------------------------------------------------------------------
print("Loading DistilBERT model...")

clf = pipeline(
    'sentiment-analysis',
    model='distilbert-base-uncased-finetuned-sst-2-english',
    device=-1    # CPU (change to 0 if you have GPU)
)

print("Running DistilBERT sentiment (batched)...")

texts = df['review_clean'].astype(str).tolist()
batch_results = []
batch_size = 32

for i in range(0, len(texts), batch_size):
    batch = texts[i:i + batch_size]
    results = clf(batch)
    batch_results.extend(results)

# Extract labels & scores
df['sent_label'] = [r['label'].lower() for r in batch_results]
df['sent_score'] = [r['score'] for r in batch_results]

print("✓ Transformer sentiment complete.")

# ----------------------------------------------------------------------
# Save result
# ----------------------------------------------------------------------
df.to_csv(output_path, index=False)
print(f"Saved sentiment file: {output_path}")
