

from sentence_transformers import SentenceTransformer

# ---------------------------
# Load model once at startup
# ---------------------------
# (Loading inside functions would be slow)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---------------------------
# Split text into chunks (optional helper)
# ---------------------------
def chunk_text(text: str, max_length: int = 500) -> list[str]:
    """
    Splits long text into smaller chunks so embeddings stay accurate.
    Default chunk size = 500 characters.
    """
    chunks = []
    words = text.split()
    current = []

    for word in words:
        # Add words until the chunk gets too long
        if sum(len(w) for w in current) + len(word) < max_length:
            current.append(word)
        else:
            chunks.append(" ".join(current))
            current = [word]
    if current:
        chunks.append(" ".join(current))

    return chunks

# ---------------------------
# Main embedding function
# ---------------------------
def get_embeddings(text: str, source: str = "unknown") -> list[dict]:
    """
    Convert text (string) into embeddings.
    Returns a list of { "embedding": vector, "text": chunk, "source": source }
    """

    chunks = chunk_text(text)

    # Generate embeddings for all chunks
    vectors = model.encode(chunks, convert_to_numpy=True)

    # Wrap into list of dicts for easier handling in Qdrant
    results = []
    for i, vec in enumerate(vectors):
        results.append({
            "id": f"{source}_{i}",   # unique ID (source+index)
            "embedding": vec.tolist(),
            "text": chunks[i],
            "source": source
        })

    return results
