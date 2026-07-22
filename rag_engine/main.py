import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from utils import (
    load_pdfs,
    split_documents,
    create_vector_store,
    load_vector_store
)

# Load environment variables from .env
load_dotenv()

# Paths
DATA_PATH = "data"
VECTOR_STORE_PATH = "vector_store"

# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Build the FAISS vector database
def build_rag():
    print("Loading PDFs...")

    # Load all PDFs
    documents = load_pdfs(DATA_PATH)

    print(f"Loaded {len(documents)} pages")

    # Split into chunks
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Create and save FAISS vector store
    create_vector_store(chunks, VECTOR_STORE_PATH)

    print("FAISS vector store created successfully!")

# Retrieve top-k relevant chunks
def retrieve(query, k=3):
    # Load vector store
    vector_store = load_vector_store(VECTOR_STORE_PATH)

    # Search for similar chunks
    results = vector_store.similarity_search(query, k=k)

    return results

# Generate answer using retrieved chunks
def generate_answer(query):
    # Retrieve relevant chunks
    docs = retrieve(query)

    # Combine retrieved text
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create RAG prompt
    prompt = f"""
You are an AI Research Assistant.

Use the following context from books and research papers to answer the question accurately.

Context:
{context}

Question:
{query}

Answer:
"""

    # Send prompt to LLM
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "references": [doc.page_content[:300] for doc in docs]
    }

# Command-line execution
if __name__ == "__main__":
    # If user passes --build, create the FAISS database
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        build_rag()

    # Otherwise, answer the query
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

        result = generate_answer(query)

        print("\nAnswer:\n")
        print(result["answer"])

        print("\nReferences:\n")
        for ref in result["references"]:
            print("-", ref)

    else:
        print("Usage:")
        print("python main.py --build")
        print("python main.py explain datatypes in c library")