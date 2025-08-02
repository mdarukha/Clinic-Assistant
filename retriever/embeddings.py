from sentence_transformers import SentenceTransformer

# load sentence transformer model for embeddings
def load_embedder(model_name='all-MiniLM-L6-v2'):
    return SentenceTransformer(model_name)

# returns embeddings for a set of text packages
def embed_passages(passages, embedder):
    return embedder.encode(passages, convert_to_tensor=False)