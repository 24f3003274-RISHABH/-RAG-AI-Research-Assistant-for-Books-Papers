import sys
import os
import ollama
from utils import (
    load_pdfs,
    split_documents,
    create_vector_store,
    load_vector_store
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Paths for PDFs and FAISS vector store
DATA_PATH = os.path.join(BASE_DIR, "data")
VECTOR_STORE_PATH = os.path.join(BASE_DIR, "vector_store")

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

Use the following context from books and research papers to answer the question accurately.

Format the answer in clean Markdown like ChatGPT:
- Start with a short introduction.
- Use clear headings (##).
- Use bullet points or numbered lists where appropriate.
- Bold important terms using **bold**.
- Add spacing between paragraphs.
- Keep the answer well-structured and easy to read.
- Do not mention "Based on the context provided" unless necessary.

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
def add_new_pdf(pdf_path):
    """
    Add only the newly uploaded PDF to the existing FAISS index.
    This avoids rebuilding the entire database.
    """

    from langchain_community.document_loaders import PyPDFLoader

    print(f"Processing new PDF: {pdf_path}")

    # Load only the new PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split into chunks
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks from new PDF")

    # Load existing FAISS vector store
    vector_store = load_vector_store(VECTOR_STORE_PATH)

    # Add new chunks
    vector_store.add_documents(chunks)

    # Save updated vector store
    vector_store.save_local(VECTOR_STORE_PATH)

    print("New PDF added to FAISS successfully!")
# ---------------------------------------------------------
# Command-line execution
# ---------------------------------------------------------
if __name__ == "__main__":
    # Force UTF-8 encoding for Windows console
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    # If user passes --build, create the FAISS database
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        build_rag()

    # Otherwise, answer the query
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

        result = generate_answer(query)

        # Print only the answer (safe for backend)
        print(result["answer"])
    elif len(sys.argv) > 2 and sys.argv[1] == "--add":
      pdf_path = sys.argv[2]
      add_new_pdf(pdf_path)

    else:
        print("Usage:")
        print("python main.py --build")
        print("python main.py <your question>")