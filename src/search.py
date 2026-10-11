"""Semantic search over indexed files."""
import numpy as np
from db import get_db, get_all_embeddings
from embeddings import embed_text

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

def search(query, top_k=20):
    """Search indexed files by semantic similarity to query."""
    query_emb = embed_text(query)
    if query_emb is None:
        return []

    query_emb = np.array(query_emb, dtype=np.float32)
    conn = get_db()
    all_embs = get_all_embeddings(conn)
    conn.close()

    scored = []
    for path, chunk_idx, emb, text in all_embs:
        score = cosine_similarity(query_emb, emb)
        # Boost exact keyword matches
        query_lower = query.lower()
        text_lower = (text or "").lower()
        if query_lower in text_lower:
            score += 0.1
        scored.append((score, path, text))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [
        {"path": path, "score": float(score), "preview": (text or "")[:200]}
        for score, path, text in scored[:top_k]
    ]
