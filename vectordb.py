import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./vectordb/chroma_db")

def get_or_create_collection(name: str):
    return chroma_client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        input=text
    )
    return response.data[0].embedding

def add_document(collection_name: str, doc_id: str, content: str, metadata: dict = None):
    collection = get_or_create_collection(collection_name)
    embedding = get_embedding(content)
    
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata or {}]
    )
    print(f"Added document '{doc_id}' to collection '{collection_name}'")

def search_documents(collection_name: str, query: str, n_results: int = 5) -> list:
    collection = get_or_create_collection(collection_name)
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results['documents'][0] if results['documents'] else []

# Add sample business documents
if __name__ == "__main__":
    add_document(
        "business_docs",
        "company_policy_001",
        "Purchase orders above $10,000 require CFO approval. All vendors must be on the approved vendor list.",
        {"type": "policy", "department": "procurement"}
    )
    
    add_document(
        "business_docs",
        "finance_policy_001",
        "Monthly financial close happens on the 5th business day. All expenses must be coded correctly.",
        {"type": "policy", "department": "finance"}
    )
    
    print("Sample documents added to vector database!")
