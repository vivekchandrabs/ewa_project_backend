from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from bot.documentLoader import load_documents_from_json_file, split_documents

def get_vector_store(data_file_path):
    docs = split_documents(load_documents_from_json_file(data_file_path))
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = FAISS.from_documents(docs, embedding=embeddings)

    return vector_store

def get_retriever(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    return retriever

def load_docs_into_vector_store(docs, vector_store):
    vector_store.add_documents(docs)
    return vector_store