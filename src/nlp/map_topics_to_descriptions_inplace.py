# src/nlp/map_topics_to_descriptions_inplace.py
import pandas as pd

# Load the CSV with LDA topics
csv_path = 'data/clean/reviews_sentiment_themes_topic.csv'
df = pd.read_csv(csv_path)

# Mapping of topics to descriptive themes per bank
topic_map = {
    "BOA": {
        "topic_1": "App Functionality / Reliability",
        "topic_2": "App Performance & Updates",
        "topic_3": "Banking Service & Money Handling",
        "topic_4": "Mobile Banking Experience / Slowness",
        "topic_5": "Usability / User Complaints"
    },
    "CBE": {
        "topic_1": "Transactions & History",
        "topic_2": "App Speed & Performance",
        "topic_3": "Service & Charges",
        "topic_4": "Ease of Use / User Experience",
        "topic_5": "Digital Payments / Telebirr Integration"
    },
    "Dashen": {
        "topic_1": "App Performance & Reliability",
        "topic_2": "Transactions & Features",
        "topic_3": "User Satisfaction / Positive Feedback",
        "topic_4": "Innovation & New Features",
        "topic_5": "Usability & Accessibility"
    }
}

# Replace topic IDs with descriptive names
def map_theme(row):
    bank = row['bank']
    topic = row['theme_primary']
    return topic_map.get(bank, {}).get(topic, topic)

df['theme_primary'] = df.apply(map_theme, axis=1)

# Overwrite the main CSV
df.to_csv(csv_path, index=False)

