import sys
import ollama
from utils import (
    load_pdfs,
    split_documents,
    create_vector_store,
    load_vector_store
)

# Paths for PDFs and FAISS vector store
DATA_PATH = "data"
VECTOR_STORE_PATH = "vector_store"

# ---------------------------------------------------------
# Function: build_rag
# Loads PDFs, splits them into chunks, and creates FAISS index.
# ---------------------------------------------------------
def build_rag():
    print("Loading PDFs...")

    documents = load_pdfs(DATA_PATH)
    print(f"Loaded {len(documents)} pages")

    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    create_vector_store(chunks, VECTOR_STORE_PATH)
    print("FAISS vector store created successfully!")

# ---------------------------------------------------------
# Function: retrieve
# Retrieves top-k relevant chunks for a query.
# ---------------------------------------------------------
def retrieve(query, k=3):
    vector_store = load_vector_store(VECTOR_STORE_PATH)

    # Search for similar chunks
    results = vector_store.similarity_search(query, k=k)

    return results

# ---------------------------------------------------------
# Function: generate_answer
# Uses retrieved chunks + Llama 3 to generate an answer.
# ---------------------------------------------------------
def generate_answer(query):
    docs = retrieve(query)

    # Combine retrieved chunks into context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create the RAG prompt
    prompt = f"""
You are an AI Research Assistant.

Use the following context from books and research papers
to answer the question accurately.

Context:
{context}

Question:
{query}

Answer:
"""

    # Send the prompt to Ollama (Llama 3)
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "answer": response["message"]["content"],
        "references": [doc.page_content[:300] for doc in docs]
    }

# ---------------------------------------------------------
# Command-line execution
# ---------------------------------------------------------
if __name__ == "__main__":
    # Build the FAISS index
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        build_rag()

    # Answer a query
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
        print("python main.py <your question>")