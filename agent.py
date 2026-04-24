import feedparser
import sqlite3
import hashlib
import os
import json
import time
from datetime import datetime

import google.generativeai as genai

# --- Configuration ---
DB_PATH = os.path.join("data", "articles.db")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")  # fast, capable model

# --- Curated RSS Feeds ---
FEEDS = [
    "https://www.cisa.gov/cybersecurity-advisories/feed",
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.reuters.com/reuters/worldNews",
    # Add more as you like (ensure they are RSS/Atom)
]

# --- Database Init ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            link TEXT,
            source TEXT,
            published TEXT,
            summary TEXT,
            threat_level TEXT,
            entities TEXT,
            geopolitical_impact TEXT,
            raw_text TEXT,
            processed_date TEXT
        )"""
    )
    conn.commit()
    conn.close()

def get_article_id(link):
    return hashlib.md5(link.encode()).hexdigest()

def article_exists(article_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM articles WHERE id=?", (article_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

# --- AI Analysis ---
import time
from google.api_core import exceptions as google_exceptions

def analyze_with_gemini(title, raw_text, max_retries=3):
    prompt = f"""..."""  # keep your existing prompt

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            # clean fences as before ...
            return json.loads(text)
        except google_exceptions.ResourceExhausted as e:
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt  # 1, 2, 4 seconds
                print(f"Rate limit hit, sleeping {sleep_time}s...")
                time.sleep(sleep_time)
            else:
                print("Rate limit exceeded after retries, storing raw article only.")
                return {
                    "summary": "Analysis not available – rate limited. Read original article.",
                    "threat_level": "Info",
                    "entities": [],
                    "geopolitical_impact": "None",
                }
        except Exception as e:
            print(f"Gemini error: {e}")
            return {
                "summary": "Analysis failed",
                "threat_level": "Info",
                "entities": [],
                "geopolitical_impact": "None",
            }
# --- Main Feed Fetcher ---
def fetch_and_process():
    conn = sqlite3.connect(DB_PATH)
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            source = feed.feed.get("title", url)
            for entry in feed.entries:
                link = entry.link
                article_id = get_article_id(link)
                if article_exists(article_id):
                    continue

                title = entry.title
                published = entry.get(
                    "published", entry.get("updated", str(datetime.now()))
                )
                # Use description or full content if available
                raw_text = entry.get("description", "") or (
                    entry.get("content", [{}])[0].get("value", "")
                )

                analysis = analyze_with_gemini(title, raw_text)

                c = conn.cursor()
                c.execute(
                    """INSERT OR IGNORE INTO articles
                    (id, title, link, source, published, summary,
                     threat_level, entities, geopolitical_impact,
                     raw_text, processed_date)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        article_id,
                        title,
                        link,
                        source,
                        published,
                        analysis["summary"],
                        analysis["threat_level"],
                        json.dumps(analysis.get("entities", [])),
                        analysis.get("geopolitical_impact", "None"),
                        raw_text[:2000],
                        str(datetime.now()),
                    ),
                )
                conn.commit()
                time.sleep(1)  # polite rate limiting
        except Exception as e:
            print(f"Error processing feed {url}: {e}")
    conn.close()

if __name__ == "__main__":
    init_db()
    fetch_and_process()
