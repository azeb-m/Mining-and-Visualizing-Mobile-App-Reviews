# # src/nlp/themes.py
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from collections import Counter
# import re

# df = pd.read_csv('data/clean/reviews_sentiment.csv')
# df['text'] = df['review_clean'].astype(str)

# themes_map = {
#   'account_access': ['login','otp','pin','password','biometric','fingerprint','signin','signup'],
#   'transactions': ['transfer','send','receive','payment','deposit','withdraw','transaction','processing','delay','slow','loading'],
#   'crash_bug': ['crash','freeze','bug','error','stop working','hang'],
#   'ui_ux': ['ui','interface','easy to use','navigation','design','buttons'],
#   'support': ['support','customer service','help','call','agent','response']
# }

# # rule-based primary theme assignment
# def assign_theme(text):
#     low = text.lower()
#     counts = {}
#     for theme, kws in themes_map.items():
#         for kw in kws:
#             if kw in low:
#                 counts[theme] = counts.get(theme,0)+1
#     if counts:
#         # pick highest count
#         return sorted(counts.items(), key=lambda x: -x[1])[0][0]
#     return 'other'

# df['theme_primary'] = df['text'].apply(assign_theme)

# # also compute top n-grams per bank using TF-IDF
# def top_ngrams(texts, n=20):
#     vect = TfidfVectorizer(ngram_range=(1,3), stop_words='english', max_features=800)
#     X = vect.fit_transform(texts)
#     sums = X.sum(axis=0)
#     terms = vect.get_feature_names_out()
#     coefs = [(terms[i], sums[0,i]) for i in range(len(terms))]
#     sorted_terms = sorted(coefs, key=lambda x: -x[1])
#     return [t for t,_ in sorted_terms[:n]]

# top_by_bank = {}
# for bank in df['bank'].unique():
#     top_by_bank[bank] = top_ngrams(df[df['bank']==bank]['text'].tolist(), n=25)

# df.to_csv('data/clean/reviews_sentiment_themes.csv', index=False)
# # save top keywords for report
# import json
# with open('reports/top_keywords_by_bank.json','w') as f:
#     json.dump(top_by_bank,f,indent=2)
# print("Themes assigned and keywords extracted.")


# src/nlp/themes_topic_modeling.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import json

# Load data
df = pd.read_csv('data/clean/reviews_sentiment.csv')
df['text'] = df['review_clean'].astype(str)

# --- Topic Modeling with LDA ---
def extract_topics(texts, n_topics=5, n_top_words=10):
    # Convert text to bag-of-words
    vectorizer = CountVectorizer(stop_words='english', max_features=2000)
    X = vectorizer.fit_transform(texts)

    # Fit LDA model
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)

    # Get top words per topic
    terms = vectorizer.get_feature_names_out()
    topics = {}
    for idx, topic in enumerate(lda.components_):
        top_terms = [terms[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics[f"topic_{idx+1}"] = top_terms
    return lda, topics

# Run topic modeling per bank
topics_by_bank = {}
lda_models = {}
for bank in df['bank'].unique():
    texts = df[df['bank'] == bank]['text'].tolist()
    lda_model, topics = extract_topics(texts, n_topics=5, n_top_words=10)
    topics_by_bank[bank] = topics
    lda_models[bank] = lda_model

# Assign dominant topic to each review
def assign_topic(text, vectorizer, lda_model):
    X = vectorizer.transform([text])
    topic_dist = lda_model.transform(X)[0]
    return f"topic_{topic_dist.argmax()+1}"

# For simplicity, use one global vectorizer + LDA model (all banks together)
vectorizer = CountVectorizer(stop_words='english', max_features=2000)
X_all = vectorizer.fit_transform(df['text'])
lda_global = LatentDirichletAllocation(n_components=5, random_state=42)
lda_global.fit(X_all)

df['theme_primary'] = [
    assign_topic(t, vectorizer, lda_global) for t in df['text']
]

# Save enriched reviews
df.to_csv('data/clean/reviews_sentiment_themes_topic.csv', index=False)

# Save discovered topics per bank
with open('reports/topics_by_bank.json', 'w') as f:
    json.dump(topics_by_bank, f, indent=2)

print("Topic modeling complete. Themes discovered and assigned.")
