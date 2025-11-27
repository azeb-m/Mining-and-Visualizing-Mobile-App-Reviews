import pandas as pd
from dateutil.parser import parse
import glob

files = glob.glob('data/raw/*_reviews_raw.csv')
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# drop empty or null review text
df['review'] = df['review'].astype(str).str.strip()
df = df[df['review'] != '']

# remove exact duplicates
df = df.drop_duplicates(subset=['review'])

# normalize date
def norm_date(x):
    try:
        return parse(str(x)).date().isoformat()
    except:
        return None

if 'date' in df.columns:
    df['date'] = df['date'].apply(norm_date)

# Basic cleanup: lowercasing and trim
df['review_clean'] = df['review'].str.replace(r'\s+',' ', regex=True).str.strip().str.lower()

# Save cleaned
df.to_csv('data/clean/reviews_clean.csv', index=False)
print('Cleaned total:', len(df))
