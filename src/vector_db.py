from chromadb import PersistentClient
from chromadb.utils import embedding_functions


def initialize_vector_db() -> PersistentClient:
    """Initialize and return a persistent Chroma client."""
    try:
        client = PersistentClient(path="./chroma_db")
        return client
    except Exception as e:
        print(f"Failed to initialize Chroma client: {e}")
        raise


def add_to_vector_db(client, collection_name, content):
    try:
        # Explicitly define the embedding function
        embed_model = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"  # Chroma's default
        )
        
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embed_model
        )
        
        # Batch processing
        documents = [page["text"] for page in content]
        metadatas = [{"page": i+1} for i in range(len(content))]
        ids = [f"page_{i+1}" for i in range(len(content))]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        return collection
    except Exception as e:
        print(f"Failed to add data to Chroma: {e}")
        raise

def query_vector_db(collection, query_text, n_results=3, filter_metadata=None):
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=filter_metadata  # Optional metadata filter (e.g., {"page": 1})
        )
        # Simplify the output
        simplified_results = {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0]
        }
        return simplified_results
    except Exception as e:
        print(f"Query failed: {e}")
        raise

