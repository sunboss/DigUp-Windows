"""File indexer - walks folders and builds search index."""
import os
from db import get_db, save_embedding
from extractors import extract_text, should_index
from embeddings import embed_text

def index_folder(folder_path, progress_callback=None):
    """Index all supported files in folder (recursive)."""
    conn = get_db()
    indexed = 0
    skipped = 0

    for root, dirs, files in os.walk(folder_path):
        # Skip hidden folders and common excludes
        dirs[:] = [d for d in dirs if not d.startswith('.')
                   and d not in ('__pycache__', 'node_modules', '.git', 'venv', '.venv')]

        for filename in files:
            path = os.path.join(root, filename)
            if not should_index(path):
                continue

            try:
                mtime = os.path.getmtime(path)
                # Check if already indexed and unchanged
                cur = conn.execute(
                    "SELECT id, mtime FROM files WHERE path = ?", (path,)
                )
                row = cur.fetchone()
                if row and row[1] >= mtime:
                    skipped += 1
                    continue

                # Extract text
                text, file_type = extract_text(path)
                if not text.strip():
                    skipped += 1
                    continue

                # Save file record
                if row:
                    file_id = row[0]
                    conn.execute(
                        "UPDATE files SET mtime=?, file_type=?, text_content=? WHERE id=?",
                        (mtime, file_type, text[:500], file_id)
                    )
                    conn.execute("DELETE FROM embeddings WHERE file_id=?", (file_id,))
                else:
                    cur = conn.execute(
                        "INSERT INTO files (path, mtime, file_type, text_content) VALUES (?, ?, ?, ?)",
                        (path, mtime, file_type, text[:500])
                    )
                    file_id = cur.lastrowid

                # Generate embedding
                embedding = embed_text(text)
                if embedding is not None:
                    save_embedding(conn, file_id, 0, embedding)
                    indexed += 1
                else:
                    skipped += 1

                conn.commit()

                if progress_callback:
                    progress_callback(indexed, skipped, path)

            except Exception as e:
                print(f"Error indexing {path}: {e}")
                skipped += 1

    conn.close()
    return indexed, skipped
