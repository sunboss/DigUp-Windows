# DigUp Windows

Windows version of [DigUp](https://github.com/ARahim3/DigUp) - semantic file search.

**Describe it. Dig it up.** Search your files by what's in them, not just filenames.

## Status: MVP

- [x] Text/PDF/DOCX indexing
- [x] Semantic search with embeddings
- [x] Web UI
- [ ] EmbeddingGemma 2 (currently using nomic-embed-text)
- [ ] Image multimodal search
- [ ] Audio/video support
- [ ] System tray + global hotkey
- [ ] Code search

## Usage

1. Download `DigUp-Windows.exe` from Actions artifacts
2. Download `nomic-embed-text-v1.5.Q8_0.gguf` to `%USERPROFILE%\.digup-windows\models\`
3. Run the EXE, open http://127.0.0.1:8765
4. Click "Index Folder" to index your files
5. Search with natural language

## Build

Push to `main` triggers GitHub Actions Windows build.
