import os
import re
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

RESUME_DIR = "resumes"
VECTOR_DB_DIR = "vector_db"

embeddings = OpenAIEmbeddings()

def load_resumes():
    docs = []
    for file in os.listdir(RESUME_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(RESUME_DIR, file))
            docs.extend(loader.load())
    return docs


def extract_metadata(text):

    name_match = re.search(r"Name[:\- ]+(.*)", text)
    name = name_match.group(1) if name_match else "Unknown"

    skills = re.findall(r"(Python|Java|SQL|Machine Learning|AWS|Docker)", text)

    exp_match = re.search(r"(\d+)\+?\s+years", text.lower())
    experience = int(exp_match.group(1)) if exp_match else 0

    edu_match = re.search(r"(Bachelor|Master|PhD)[^\n]*", text)
    education = edu_match.group(0) if edu_match else ""

    return {
        "name": name,
        "skills": list(set(skills)),
        "experience_years": experience,
        "education": education
    }


def chunk_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_documents(docs)


def build_vector_db():

    docs = load_resumes()
    chunks = chunk_documents(docs)

    processed_docs = []

    for chunk in chunks:

        metadata = extract_metadata(chunk.page_content)

        chunk.metadata.update(metadata)
        processed_docs.append(chunk)

    vectordb = Chroma.from_documents(
        processed_docs,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    vectordb.persist()

    print("Vector DB created successfully")


if __name__ == "__main__":
    build_vector_db()