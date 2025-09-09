# search_engine.py

from typing import List, Dict, Any, Optional
import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# local import
from employees_data import employees

# Build a canonical skill list from the dataset
def build_skill_set(employees_list):
    skills = set()
    for e in employees_list:
        for s in e.get("skills", []):
            skills.add(s.lower())
    return skills

SKILLS_SET = build_skill_set(employees)

def profile_to_text(emp: Dict[str, Any]) -> str:
    # combine name, skills, projects and notes to single text for semantic matching
    skills = " ".join(emp.get("skills", []))
    projects = " ".join(emp.get("projects", []))
    notes = emp.get("notes", "")
    text = f"{emp.get('name','')} {skills} {projects} {notes} experience:{emp.get('experience_years',0)} availability:{emp.get('availability','')}"
    return text

class EmployeeSearch:
    def __init__(self, employees_list: List[Dict[str, Any]]):
        self.employees = employees_list
        self.docs = [profile_to_text(e) for e in self.employees]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), min_df=1)
        self.doc_embeddings = self.vectorizer.fit_transform(self.docs)

    def query_to_skills_and_min_exp(self, query: str) -> Dict[str, Any]:
        # Extract explicit skills mentioned (from known skill list)
        q_lower = query.lower()
        found_skills = set()
        for s in SKILLS_SET:
            if re.search(r'\b' + re.escape(s) + r'\b', q_lower):
                found_skills.add(s)

        # Extract experience like "3+ years" or "3 years"
        exp_match = re.search(r'(\d+)\s*\+?\s*years?', q_lower)
        min_exp = int(exp_match.group(1)) if exp_match else None

        # availability keywords
        wants_available = bool(re.search(r'\bavailable\b|\bimmediate\b|\bopen\b', q_lower))

        return {"skills": list(found_skills), "min_experience": min_exp, "wants_available": wants_available}

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # vectorize query and compute cosine similarity
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.doc_embeddings).flatten()
        ranked_idx = np.argsort(-sims)[:top_k]
        results = []
        for i in ranked_idx:
            results.append({"employee": self.employees[i], "score": float(sims[i])})
        return results

    def filter_by_parsed(self, candidates: List[Dict[str, Any]], parsed: Dict[str, Any]) -> List[Dict[str, Any]]:
        filtered = []
        for item in candidates:
            emp = item["employee"]
            score = item["score"]
            # skill filter (if user asked for specific skill words)
            skills_lower = [s.lower() for s in emp.get("skills", [])]
            skill_ok = True
            if parsed["skills"]:
                for s in parsed["skills"]:
                    if s not in skills_lower:
                        skill_ok = False
                        break
            # experience filter
            exp_ok = True
            if parsed["min_experience"] is not None:
                if emp.get("experience_years", 0) < parsed["min_experience"]:
                    exp_ok = False
            # availability filter
            avail_ok = True
            if parsed["wants_available"]:
                avail_ok = emp.get("availability","").lower() == "available"
            if skill_ok and exp_ok and avail_ok:
                filtered.append(item)
        return filtered

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        parsed = self.query_to_skills_and_min_exp(query)
        # Stage 1: semantic retrieval (get larger candidate set)
        candidates = self.semantic_search(query, top_k=max(10, k*2))
        # Stage 2: filtering by explicit parsed constraints
        filtered = self.filter_by_parsed(candidates, parsed)
        # If filtering removes too many, fallback to top semantic candidates
        if len(filtered) < k:
            # merge filtered with top semantic (but keep uniqueness)
            ids = set([f["employee"]["id"] for f in filtered])
            for c in candidates:
                if c["employee"]["id"] not in ids:
                    filtered.append(c)
                    ids.add(c["employee"]["id"])
                if len(filtered) >= k:
                    break
        # Sort by score and return top k
        filtered = sorted(filtered, key=lambda x: -x["score"])
        return filtered[:k]

    def generate_response(self, query: str, candidates: List[Dict[str, Any]]) -> str:
        # Simple templated generation. You can plug an LLM here.
        if not candidates:
            return "I couldn't find matching employees for your query. Try relaxing constraints or mentioning specific skills."

        lines = []
        header = f"Based on your request: \"{query}\", here are the top {len(candidates)} candidates I found:\n"
        lines.append(header)
        for item in candidates:
            emp = item["employee"]
            score = item.get("score", 0)
            lines.append(f"**{emp['name']}** — {emp['experience_years']} years experience. Availability: {emp['availability']}.")
            lines.append(f"Skills: {', '.join(emp.get('skills', []))}.")
            lines.append(f"Notable projects: {', '.join(emp.get('projects', []))}.")
            # small reasoning sentence about why matched (score)
            lines.append(f"Why recommended: semantic match score {score:.2f}.")
            lines.append("")  # blank line
        # call to action
        lines.append("Would you like deeper details on any of these candidates (e.g., full CV, contact info, or availability for interview)?")
        return "\n".join(lines)


# Singleton search object (reuse model)
_default_searcher = EmployeeSearch(employees)

def get_searcher():
    return _default_searcher
