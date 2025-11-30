# src/nlp/map_topics_to_descriptions_inplace_debug.py
import pandas as pd
from datetime import datetime

# Load the CSV with LDA topics
csv_path = 'data/clean/reviews_sentiment_themes_topic.csv'
print(f"Loading CSV from: {csv_path}")

df = pd.read_csv(csv_path)
print(f"Original data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Show sample of original themes
print("\nSample of original themes:")
print(df[['bank', 'theme_primary']].head(10))

# Enhanced mapping of topics to descriptive themes per bank
topic_map = {
    "BOA": {
        "topic_1": "App Functionality ",
        "topic_2": "Features & Update Requests", 
        "topic_3": "Core Service satisfaction",
        "topic_4": "Performance ",
        "topic_5": "Usability & App Comparison"
    },
    "CBE": {
        "topic_1": "Transaction ",
        "topic_2": "Banking Efficiency & Speed",
        "topic_3": "Service Charges ",
        "topic_4": "Accessibility & Ease of Use",
        "topic_5": "Innovation & Integration"
    },
    "Dashen": {
        "topic_1": "Overall Excellence in Mobile Banking",
        "topic_2": "Smooth Operation",
        "topic_3": "User Satisfaction",
        "topic_4": "Pioneering Innovation in Ethiopian Banking",
        "topic_5": "Fast & User-Friendly Banking Experience"
    }
}

# Replace topic IDs with descriptive names
def map_theme(row):
    bank = row['bank']
    topic = row['theme_primary']
    new_theme = topic_map.get(bank, {}).get(topic, topic)
    return new_theme

print(f"\nMapping themes...")
df['theme_primary'] = df.apply(map_theme, axis=1)

# Show sample of new themes
print("\nSample of new themes:")
print(df[['bank', 'theme_primary']].head(10))

# Check if any themes weren't mapped
unmapped = df[df['theme_primary'].str.startswith('topic_')]
print(f"\nUnmapped themes count: {len(unmapped)}")

# Save with timestamp to verify
output_path = 'data/clean/reviews_sentiment_themes_topic.csv'
print(f"\nSaving to: {output_path}")
df.to_csv(output_path, index=False)

print(f"Debug completed at {datetime.now()}")