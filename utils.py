import os
import re
from langchain.document_loaders import PyPDFLoader

RESUME_DIR = "resumes"


def load_resumes():

    documents = []

    for file in os.listdir(RESUME_DIR):

        if file.endswith(".pdf"):

            path = os.path.join(RESUME_DIR, file)

            loader = PyPDFLoader(path)

            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = path

            documents.extend(docs)

    return documents


def extract_name(text):

    match = re.search(r"Name[:\- ]+(.*)", text)

    if match:
        return match.group(1).strip()

    return "Unknown"


def extract_skills(text):

    skill_list = [
        "Python",
        "Java",
        "SQL",
        "Machine Learning",
        "AWS",
        "Docker",
        "Kubernetes",
        "TensorFlow",
        "PyTorch"
    ]

    found = []

    for skill in skill_list:

        if skill.lower() in text.lower():
            found.append(skill)

    return list(set(found))


def extract_experience(text):

    match = re.search(r"(\d+)\+?\s+years", text.lower())

    if match:
        return int(match.group(1))

    return 0


def extract_education(text):

    match = re.search(r"(Bachelor|Master|PhD)[^\n]*", text)

    if match:
        return match.group(0)

    return ""


def extract_metadata(text):

    return {
        "name": extract_name(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience(text),
        "education": extract_education(text)
    }


def extract_required_skills(jd):

    skill_list = [
        "Python",
        "Java",
        "SQL",
        "Machine Learning",
        "AWS",
        "Docker"
    ]

    return [s for s in skill_list if s.lower() in jd.lower()]