# Mining and Visualizing Mobile App Reviews

A project focused on scraping, analyzing, and visualizing Google Play Store reviews for Ethiopian banking apps. This includes web scraping, NLP sentiment analysis, thematic extraction, PostgreSQL storage, and data-driven reporting.

# Bank Reviews Database Schema

This project uses **PostgreSQL** to store cleaned and processed review data. The database is named `bank_reviews` and contains two tables: `banks` and `reviews`.

---

## 1. Database Schema

### Banks Table
- `bank_id` (SERIAL, PRIMARY KEY): Unique identifier for each bank.
- `bank_name` (VARCHAR, NOT NULL): Name of the bank.
- `app_name` (VARCHAR, NOT NULL): Name of the mobile app.

### Reviews Table
- `review_id` (SERIAL, PRIMARY KEY): Unique identifier for each review.
- `bank_id` (INT, FOREIGN KEY REFERENCES `banks`): Bank associated with the review.
- `review_text` (TEXT, NOT NULL): Text of the user review.
- `rating` (INT, NOT NULL): Review rating (1–5 stars).
- `review_date` (DATE, NOT NULL): Date of the review.
- `sentiment_label` (VARCHAR): Sentiment label (positive/negative/neutral).
- `sentiment_score` (FLOAT): Numerical sentiment score.
- `theme_primary` (VARCHAR): Primary theme extracted from the review.
- `source` (VARCHAR, NOT NULL): Source of the review (e.g., Google Play).

---

## 2. Example SQL Statements

**Create `banks` table:**
```sql
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    app_name VARCHAR(255) NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INT NOT NULL,
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(50),
    sentiment_score FLOAT,
    theme_primary VARCHAR(255),
    source VARCHAR(100) NOT NULL
);

-- Count reviews per bank
SELECT bank_id, COUNT(*) AS review_count
FROM reviews
GROUP BY bank_id;

-- Average rating per bank
SELECT bank_id, AVG(rating) AS avg_rating
FROM reviews
GROUP BY bank_id;

