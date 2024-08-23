from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from .load_embedding import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv
import os
import logging

load_dotenv()

PERSIST_DIRECTORY_DB_PATH = os.getenv("PERSIST_DIRECTORY_DB_PATH")
PDF_DATA_PATH = os.getenv("PDF_DATA_PATH")


def load_document():
    document_loader = PyPDFDirectoryLoader(PDF_DATA_PATH)
    document = document_loader.load()
    return document


def chunk_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    text = text_splitter.split_documents(documents)
    return text


def create_chroma_ids(chunks: list[Document]):
    # Creating id for each chunk based on {source}: {page} : {chunk number}

    last_id = None
    current_chunk_id = 0

    for chunk in chunks:
        source = chunk.metadata["source"].split("/")[-1]  # Getting the name of the file
        page = chunk.metadata["page"]  # Getting the page number

        current_id = f"{source}:{page}"

        if current_id == last_id:
            current_chunk_id += 1
        else:
            current_chunk_id = 0

        last_id = current_id

        current_id += f":{current_chunk_id}"
        chunk.metadata["id"] = current_id
    return chunks


def add_documents_to_chroma(chunks_with_ids: list[Document]):
    embedding = get_embedding_function()
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY_DB_PATH, embedding_function=embedding
    )

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        logging.info(f"Adding new documents: {len(new_chunks)}")
    else:
        print("✅ No new documents to add")


def update_chroma():
    documents = load_document()
    chunks = chunk_documents(documents)
    chunks_with_ids = create_chroma_ids(chunks)
    add_documents_to_chroma(chunks_with_ids)


def delete_file_from_chroma(prefix: str):
    embedding = get_embedding_function()
    file_path = f"{PDF_DATA_PATH}/{prefix}"

    try:
        db = Chroma(
            persist_directory=PERSIST_DIRECTORY_DB_PATH, embedding_function=embedding
        )
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        ids_to_remove = [id for id in existing_ids if id.startswith(prefix)]

        if ids_to_remove:
            db._collection.delete(ids=ids_to_remove)
            os.remove(file_path)
            print(f"Deleting file: {file_path}")
            print(
                f"🔥 Deleted documents with ids starting with '{prefix}' -> {len(ids_to_remove)}"
            )
        else:
            logging(f"No documents found with ids starting with '{prefix}'")
    except Exception as e:
        logging.error(f"Error in delete_file_from_chroma: {e}")
        raise


if __name__ == "__main__":
    update_chroma()
