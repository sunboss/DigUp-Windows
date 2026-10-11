"""Embedding generation using llama.cpp with EmbeddingGemma."""
import os

MODEL_DIR = os.path.join(os.path.expanduser("~"), ".digup-windows", "models")
# Model will be downloaded on first run
# Using a smaller embedding model for MVP (nomic-embed-text)
# TODO: Switch to EmbeddingGemma 2 when available in GGUF

_model = None

def get_model():
    global _model
    if _model is None:
        try:
            from llama_cpp import Llama
            model_path = os.path.join(MODEL_DIR, "nomic-embed-text-v1.5.Q8_0.gguf")
            if not os.path.exists(model_path):
                print(f"Model not found at {model_path}")
                print("Please download nomic-embed-text-v1.5.Q8_0.gguf to the models folder")
                return None
            _model = Llama(
                model_path=model_path,
                embedding=True,
                n_ctx=2048,
                verbose=False
            )
        except Exception as e:
            print(f"Failed to load model: {e}")
            return None
    return _model

def embed_text(text):
    """Generate embedding for text. Returns numpy array or None."""
    model = get_model()
    if model is None:
        return None
    # Truncate to avoid context overflow
    text = text[:2000]
    embedding = model.embed(text)
    return embedding
