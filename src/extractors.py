"""Extract text/content from various file types."""
import os

def extract_text(path):
    """Extract searchable text from a file. Returns (text, file_type)."""
    ext = os.path.splitext(path)[1].lower()

    # Plain text
    if ext in ('.txt', '.md', '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.go', '.rs'):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()[:10000], 'text'
        except:
            return "", 'text'

    # PDF
    if ext == '.pdf':
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            text = ""
            for page in reader.pages[:30]:  # first 30 pages
                text += page.extract_text() or ""
            return text[:10000], 'pdf'
        except:
            return "", 'pdf'

    # Word docs
    if ext in ('.docx', '.doc'):
        try:
            from docx import Document
            doc = Document(path)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text[:10000], 'doc'
        except:
            return "", 'doc'

    # Images - return filename for now (multimodal embedding TODO)
    if ext in ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif'):
        basename = os.path.basename(path)
        return f"Image file: {basename}", 'image'

    return "", 'unknown'

def should_index(path):
    """Check if file should be indexed."""
    ext = os.path.splitext(path)[1].lower()
    return ext in (
        '.txt', '.md', '.pdf', '.docx', '.doc',
        '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.go', '.rs',
        '.jpg', '.jpeg', '.png', '.bmp', '.webp'
    )
