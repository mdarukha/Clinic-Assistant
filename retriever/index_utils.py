import faiss
import pickle

# utility functions for loading and saving indexes and text

def save_index(index, path):
    faiss.write_index(index, path)

def load_index(path):
    return faiss.read_index(path)

def save_passages(passages, path):
    with open(path, 'wb') as f:
        pickle.dump(passages, f)

def load_passages(path):
    with open(path, 'rb') as f:
        return pickle.load(f)