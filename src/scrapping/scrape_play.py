# src/scraping/scrape_play.py
from google_play_scraper import reviews, Sort
import json, time, csv
from datetime import datetime

with open('src/scrapping/app_ids.json') as f:
    apps = json.load(f)

def scrape_app(appId, bank, target=800):
    out = []
    cont_token = None
    while len(out) < target:
        rv, cont_token = reviews(appId, lang='en', country='us', sort=Sort.NEWEST, count=200, continuation_token=cont_token)
        if not rv:
            break
        for r in rv:
            out.append({
                'review': r.get('content',''),
                'rating': r.get('score'),
                'date': r.get('at').strftime('%Y-%m-%d') if r.get('at') else None,
                'bank': bank,
                'source': 'google_play'
            })
        if not cont_token:
            break
        time.sleep(1)  # be polite
    return out[:target]

if __name__ == '__main__':
    for app in apps:
        rows = scrape_app(app['appId'], app['bank'], target=800)
        out_path = f"data/raw/{app['bank']}_reviews_raw.csv"
        keys = ['review','rating','date','bank','source']
        with open(out_path,'w',newline='',encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        print(f"Saved {len(rows)} reviews for {app['bank']} -> {out_path}")
