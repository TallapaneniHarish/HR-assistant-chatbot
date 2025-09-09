from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Step 1: Create a small employee dataset
employees = [
    {
        "name": "Dr. Sarah Chen",
        "experience": "6 years in Machine Learning",
        "domain": "Healthcare",
        "projects": "Medical Diagnosis Platform (X-ray analysis using computer vision)",
        "skills": "TensorFlow, PyTorch, medical data processing",
        "papers": "3 papers on healthcare AI",
        "availability": "Currently available"
    },
    {
        "name": "Michael Rodriguez",
        "experience": "4 years in Machine Learning",
        "domain": "Healthcare",
        "projects": "Patient Risk Prediction System (ensemble methods)",
        "skills": "Scikit-learn, Pandas, Electronic Health Records",
        "compliance": "HIPAA",
        "availability": "Currently available"
    },
    {
        "name": "Priya Sharma",
        "experience": "5 years in Web Development",
        "domain": "E-commerce",
        "projects": "Online Marketplace",
        "skills": "React, Node.js, MongoDB",
        "availability": "Busy on a current project"
    }
]

# Step 2: Encode employee data
model = SentenceTransformer("all-MiniLM-L6-v2")
employee_texts = [f"{e['name']} - {e['experience']} - {e['domain']} - {e['projects']} - {e['skills']}" for e in employees]
embeddings = model.encode(employee_texts)

# Step 3: Store in FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Step 4: Query
query = "I need someone experienced with machine learning for a healthcare project"
query_embedding = model.encode([query])

# Step 5: Retrieve top 2 candidates
distances, indices = index.search(np.array(query_embedding), k=2)

# Step 6: Generate a simple response
print("🔍 User Query:", query)
print("🤖 RAG Response:\n")

for idx in indices[0]:
    emp = employees[idx]
    print(f"⭐ {emp['name']} - {emp['experience']}, worked on {emp['projects']}. Skills: {emp['skills']}.\n")

