import faiss
import argparse
from retriever.embeddings import load_embedder, embed_passages
from retriever.index_utils import save_index, save_passages

# splits file into different paragraph chunks
def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    passages = [p.strip() for p in content.split('\n\n') if p.strip()]
    return passages

# builds FAISS index from text corpus file
def build_and_save_index(corpus_path, output_prefix):
    passages = load_corpus(corpus_path)
    embedder = load_embedder()
    embeddings = embed_passages(passages, embedder)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    save_index(index, f"{output_prefix}.index")
    save_passages(passages, f"{output_prefix}_corpus.pkl")
    print(f"[✓] Saved index to {output_prefix}.index")
    print(f"[✓] Saved corpus to {output_prefix}_corpus.pkl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True, help="Path to .txt corpus file")
    parser.add_argument("--out", required=True, help="Output prefix for index files")
    args = parser.parse_args()

    build_and_save_index(args.corpus, args.out)