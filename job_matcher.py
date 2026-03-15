from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import json
import re

VECTOR_DB_DIR = "vector_db"

embeddings = OpenAIEmbeddings()

vectordb = Chroma(
    persist_directory=VECTOR_DB_DIR,
    embedding_function=embeddings
)


def extract_required_skills(jd):

    skills = ["Python", "Machine Learning", "SQL", "AWS", "Docker"]

    return [s for s in skills if s.lower() in jd.lower()]


def semantic_search(jd, k=10):

    results = vectordb.similarity_search_with_score(jd, k=k)

    return results


def compute_match_score(similarity_score, matched_skills):

    semantic_score = (1 - similarity_score) * 70

    skill_score = len(matched_skills) * 10

    total = min(100, semantic_score + skill_score)

    return int(total)


def job_match(jd):

    required_skills = extract_required_skills(jd)

    results = semantic_search(jd)

    matches = []

    for doc, score in results:

        candidate = doc.metadata.get("name", "Unknown")
        resume_path = doc.metadata.get("source", "")

        candidate_skills = doc.metadata.get("skills", [])

        matched_skills = list(set(required_skills) & set(candidate_skills))

        match_score = compute_match_score(score, matched_skills)

        reasoning = f"Matched skills: {matched_skills}. Semantic similarity considered."

        matches.append({
            "candidate_name": candidate,
            "resume_path": resume_path,
            "match_score": match_score,
            "matched_skills": matched_skills,
            "relevant_excerpts": [doc.page_content[:200]],
            "reasoning": reasoning
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)

    return matches[:10]


if __name__ == "__main__":

    jd = input("Enter Job Description:\n")

    matches = job_match(jd)

    output = {
        "job_description": jd,
        "top_matches": matches
    }

    print(json.dumps(output, indent=2))