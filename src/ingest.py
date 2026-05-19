import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from search import get_collection_name, get_database_url, get_embeddings

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_pdf_path = os.getenv("PDF_PATH", "document.pdf")
PDF_PATH = os.path.join(PROJECT_ROOT, _pdf_path)


def ingest_pdf():
    if not os.path.isfile(PDF_PATH):
        raise FileNotFoundError(f"Caminho do PDF não encontrado: {PDF_PATH}")

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 150)),
    )
    chunks = text_splitter.split_documents(documents)

    PGVector.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=get_collection_name(),
        connection=get_database_url(),
        pre_delete_collection=True,
        use_jsonb=True,
    )

    print(f"Ingestão concluída: {len(chunks)} chunks salvos no banco vetorial.")


if __name__ == "__main__":
    ingest_pdf()
