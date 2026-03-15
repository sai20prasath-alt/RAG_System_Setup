
Resume RAG System – Semantic Job Matching

Overview
This project implements a Retrieval-Augmented Generation (RAG) system to match resumes with job descriptions using semantic search and vector databases.

Traditional resume screening relies on keyword matching, which often misses qualified candidates. This system uses embeddings and vector similarity to find the most relevant candidates for a given job description.

Learning Objectives
- Document chunking and processing
- Embedding generation
- Vector database creation
- Semantic search
- Hybrid search (semantic + keyword)
- Candidate ranking and scoring

Project Architecture
Resumes (PDF)
 → Document Loader
 → Chunking
 → Embedding Generation
 → Vector Database (ChromaDB)
 → Job Description Input
 → Semantic Search
 → Hybrid Skill Matching
 → Ranking & Scoring
 → JSON Output

Project Structure
project/
resumes/
    john_doe.pdf
    jane_smith.pdf
vector_db/
resume_rag.py
job_matcher.py
utils.py
README.md

Components

resume_rag.py
Responsible for building the vector database.

Tasks:
- Load resume PDF files
- Split resumes into chunks
- Extract metadata
- Generate embeddings
- Store embeddings in ChromaDB

utils.py
Contains reusable helper functions used across the project.

Examples:
- Resume loading
- Skill extraction
- Experience extraction
- Education extraction
- Metadata creation
- Required skill detection

job_matcher.py
Implements the job matching engine.

Responsibilities:
- Accept job description input
- Convert JD to embeddings
- Retrieve similar resumes
- Perform hybrid search
- Score candidates
- Generate ranking output

vector_db Folder
This folder stores the persistent vector database created by ChromaDB.

It contains:
- Embedding vectors
- Resume text chunks
- Metadata
- Vector index files

Metadata Extraction Example
Name: John Doe
Skills: Python, Machine Learning
Experience Years: 5
Education: MS Computer Science

Hybrid Search Approach

1. Semantic Search
Vector similarity compares embeddings of job description and resumes.

2. Keyword Skill Matching
Critical skills are matched explicitly such as Python, Machine Learning, AWS.

Candidate Scoring
Score range: 0–100

Formula:
Total Score =
Semantic Similarity (70%)
+ Skill Match Score (30%)

Example:
Semantic Score = 62
Skill Matches = 30
Final Score = 92

Example Output
{
  "candidate_name": "John Doe",
  "match_score": 92,
  "matched_skills": ["Python","Machine Learning"]
}

Installation
pip install langchain chromadb openai pypdf
Optional:
pip install sentence-transformers

Running the Project

Step 1: Build Vector Database
python resume_rag.py

Step 2: Run Job Matching
python job_matcher.py

Example Job Description:
Looking for Python Machine Learning engineer with AWS experience

Example Result:
John Doe — Score: 92
Jane Smith — Score: 78

Benefits
- Faster resume screening
- Semantic candidate matching
- Improved hiring decisions
- Scalable for thousands of resumes

Future Improvements
- LLM-based skill extraction
- Resume summarization
- Cross-encoder reranking
- Web interface for recruiters
- ATS integrations

Conclusion
This project demonstrates how RAG architecture, embeddings, and vector databases can build intelligent recruitment systems capable of semantic resume matching.

