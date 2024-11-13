from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents_from_json_file(file_path: str):
    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.[]',
        text_content=False
    )
    docs = loader.load()
    return docs

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=0
    )

    doc_splits = text_splitter.split_documents(docs)

    return doc_splits