import sqlite3
from datetime import datetime

DB_PATH = "ott_analytics.db"


def init_db():
    """Creates the SQLite database table if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS launches (
            show_title TEXT PRIMARY KEY,
            article_volume INTEGER,
            publisher_count INTEGER,
            net_sentiment REAL,
            positive_hype_pct REAL,
            timestamp TEXT
        )
    """
    )

    conn.commit()
    conn.close()


def save_launch_metrics(
    show_title: str,
    article_volume: int,
    publisher_count: int,
    net_sentiment: float,
    positive_hype_pct: float,
):
    """Saves or updates search analytics in SQLite."""
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT OR REPLACE INTO launches (
            show_title, article_volume, publisher_count, net_sentiment, positive_hype_pct, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            show_title,
            article_volume,
            publisher_count,
            net_sentiment,
            positive_hype_pct,
            now_str,
        ),
    )

    conn.commit()
    conn.close()


def fetch_all_launches():
    """Retrieves all historical saved show searches for dashboard comparison."""
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT show_title, article_volume, publisher_count, net_sentiment, positive_hype_pct, timestamp FROM launches ORDER BY timestamp DESC"
    )
    rows = cursor.fetchall()

    conn.close()
    return rows