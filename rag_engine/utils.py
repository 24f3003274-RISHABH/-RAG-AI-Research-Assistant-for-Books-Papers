import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# ---------------------------------------------------------
# Function: load_pdfs
# This function loads all PDF files from the data folder.
# ---------------------------------------------------------
def load_pdfs(data_path):
    documents = []

    # Loop through every file in the data folder
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(data_path, file)

            # Load the PDF using PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            # Add all pages to the documents list
            documents.extend(docs)

    return documents

# ---------------------------------------------------------
# Function: split_documents
# Splits large PDF text into smaller chunks.
# ---------------------------------------------------------
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Each chunk will have ~1000 characters
        chunk_overlap=200  # 200 characters overlap for better context
    )

    chunks = text_splitter.split_documents(documents)
    return chunks

# ---------------------------------------------------------
# Function: get_embeddings
# Uses a free HuggingFace embedding model locally.
# ---------------------------------------------------------
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# ---------------------------------------------------------
# Function: create_vector_store
# Creates FAISS vector database from document chunks.
# ---------------------------------------------------------
def create_vector_store(chunks, save_path):
    embeddings = get_embeddings()

    # Convert text chunks into embeddings and store in FAISS
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Save the FAISS index locally
    vector_store.save_local(save_path)

    return vector_store

# ---------------------------------------------------------
# Function: load_vector_store
# Loads the saved FAISS vector database.
# ---------------------------------------------------------
def load_vector_store(save_path):
    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store