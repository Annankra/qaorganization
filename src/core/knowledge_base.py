import os
import logging
from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("KnowledgeBase")

class KnowledgeBase:
    """RAG implementation for grounding agents with requirements and history."""
    
    def __init__(self, index_path: Optional[str] = None):
        self.index_path = index_path or os.getenv("KB_DIR", "data/faiss_index")
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        
        if os.path.exists(self.index_path):
            self.vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            logger.info(f"Loaded existing index from {self.index_path}")

    def add_documents(self, documents: List[Document]):
        """Adds documents to the vector store."""
        if self.vector_store:
            self.vector_store.add_documents(documents)
        else:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        
        self.vector_store.save_local(self.index_path)
        logger.info(f"Saved index with {len(documents)} new documents to {self.index_path}")

    def search(self, query: str, k: int = 4) -> List[Document]:
        """Searches for relevant documents."""
        if not self.vector_store:
            logger.warning("Vector store not initialized. Returning empty results.")
            return []
        
        return self.vector_store.similarity_search(query, k=k)

    def ingest_directory(self, directory_path: str):
        """Indexes all text files in a directory."""
        docs = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt") or filename.endswith(".md"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, "r") as f:
                    content = f.read()
                    docs.append(Document(page_content=content, metadata={"source": filename}))
        
        if docs:
            self.add_documents(docs)

# Singleton initialization
kb = KnowledgeBase()
