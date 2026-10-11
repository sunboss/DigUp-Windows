"""SQLite storage for file index and embeddings."""
import sqlite3
import os
import numpy as np

DB_PATH = os.path.join(os.path.expanduser("~"), ".digup-windows", "index.db")

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            mtime REAL,
            file_type TEXT,
            text_content TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            file_id INTEGER,
            chunk_idx INTEGER,
            embedding BLOB,
            FOREIGN KEY (file_id) REFERENCES files (id),
            PRIMARY KEY (file_id, chunk_idx)
        )
    """)
    return conn

def save_embedding(conn, file_id, chunk_idx, embedding):
    blob = np.array(embedding, dtype=np.float32).tobytes()
    conn.execute(
        "INSERT OR REPLACE INTO embeddings (file_id, chunk_idx, embedding) VALUES (?, ?, ?)",
        (file_id, chunk_idx, blob)
    )

def get_all_embeddings(conn):
    cur = conn.execute("""
        SELECT f.path, e.chunk_idx, e.embedding, f.text_content
        FROM embeddings e JOIN files f ON e.file_id = f.id
    """)
    results = []
    for path, chunk_idx, blob, text in cur:
        emb = np.frombuffer(blob, dtype=np.float32)
        results.append((path, chunk_idx, emb, text))
    return results
