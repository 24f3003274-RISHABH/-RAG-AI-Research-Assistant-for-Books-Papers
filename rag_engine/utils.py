import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load all PDFs from the data folder
def load_pdfs(data_path):
    documents = []

    # Loop through all files in the data folder
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(data_path, file)

            # Load PDF pages
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            documents.extend(docs)

    return documents

# Split documents into smaller chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Maximum size of each chunk
        chunk_overlap=200  # Overlap between chunks for better context
    )

    chunks = text_splitter.split_documents(documents)
    return chunks

# Create embeddings and save them into FAISS
def create_vector_store(chunks, save_path):
    # OpenAI embedding model converts text into vectors
    embeddings = OpenAIEmbeddings()

    # Create FAISS vector database
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Save FAISS index locally
    vector_store.save_local(save_path)

    return vector_store

# Load existing FAISS vector database
def load_vector_store(save_path):
    embeddings = OpenAIEmbeddings()

    # Load FAISS index
    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store 