import os
import pickle
import faiss
import numpy as np
class Retriever:

    def __init__(self):

        self.index = None
        self.chunks = None

        self.store_path = "vector_store"

        self.index_path = os.path.join(
            self.store_path,
            "faiss.index"
        )

        self.meta_path = os.path.join(
            self.store_path,
            "metadata.pkl"
        )

        os.makedirs(self.store_path, exist_ok=True)

    def build_index(self, embeddings, chunks):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        self.chunks = chunks

        self.save_index()

    def save_index(self):

        faiss.write_index(
            self.index,
            self.index_path
        )

        with open(
            self.meta_path,
            "wb"
        ) as f:

            pickle.dump(
                self.chunks,
                f
            )

        print("Faiss index saved successfully.")

    def load_index(self):

        if not os.path.exists(self.index_path):
            raise FileNotFoundError(
                "Faiss index not found. Please ingest the document first."
            )

        self.index = faiss.read_index(
            self.index_path
        )

        with open(
            self.meta_path,
            "rb"
        ) as f:

            self.chunks = pickle.load(f)

        print("Faiss index loaded successfully.")

    def retrieve(
        self,
        query_embedding,
        top_k=4
    ):

        if self.index is None:
            self.load_index()

        distances, indices = self.index.search(
            np.array(
                [query_embedding],
                dtype=np.float32
            ),
            top_k
        )

        return [
            self.chunks[i]
            for i in indices[0]
        ]