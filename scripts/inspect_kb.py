#!/usr/bin/env python3
import sys
import os
import argparse
import json
from dotenv import load_dotenv

load_dotenv()

# Ensure project root is in path
sys.path.append(os.getcwd())

from src.core.knowledge_base import kb

def list_docs(limit=10):
    print(f"\n--- Listing Top {limit} Ingested Documents ---\n")
    if not kb.vector_store:
        print("Knowledge Base is empty.")
        return

    doc_ids = list(kb.vector_store.docstore._dict.keys())
    for doc_id in doc_ids[:limit]:
        doc = kb.vector_store.docstore.search(doc_id)
        print(f"ID/Key: {doc.metadata.get('key', 'N/A')}")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Type:   {doc.metadata.get('type', 'Unknown')}")
        print(f"Content: {doc.page_content[:200]}...")
        print("-" * 50)

def search_kb(query, k=3):
    print(f"\n--- Searching KB for: '{query}' ---\n")
    results = kb.search(query, k=k)
    if not results:
        print("No matches found.")
        return

    for i, doc in enumerate(results):
        print(f"Result #{i+1}")
        print(f"ID/Key: {doc.metadata.get('key', 'N/A')}")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content: {doc.page_content[:300]}...")
        print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="Inspect the Agentic QA Knowledge Base (FAISS)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List recent documents")
    list_parser.add_argument("--limit", type=int, default=10, help="Number of docs to show")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search the KB")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--k", type=int, default=3, help="Number of results")

    args = parser.parse_args()

    if args.command == "list":
        list_docs(args.limit)
    elif args.command == "search":
        search_kb(args.query, args.k)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
