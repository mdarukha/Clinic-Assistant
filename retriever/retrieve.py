from retriever.embeddings import load_embedder, embed_passages
from retriever.index_utils import load_index, load_passages

# retrieve top_k passages given a query
def retrieve_top_k(query, index_path, corpus_path, k=1):
    embedder = load_embedder()
    query_vec = embed_passages([query], embedder)

    index = load_index(index_path)
    passages = load_passages(corpus_path)

    distances, indices = index.search(query_vec, k)
    return [passages[i] for i in indices[0]]