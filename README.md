# HR Resource Query Chatbot
## Overview
The **HR Resource Query Chatbot** is an AI-powered assistant designed to help HR teams quickly find employees based on skills, experience, and past projects. It combines a **retrieval system** with **template-based natural responses** to provide recommendations in a chat interface. Users can query for developers by technology, experience, or project background, and receive structured, actionable information.

---

## Features
- Search employees by skills, years of experience, and projects.
- Filter by availability.
- AI-style chatbot interface providing human-readable recommendations.
- Backend API using **FastAPI** with interactive Swagger documentation.
- Frontend chat interface using **Streamlit**.
- Simple RAG-like retrieval system using TF–IDF and cosine similarity.

---

## Architecture
**System Overview:**
1. **Frontend (Streamlit)**
   - Chat interface where HR can type queries.
   - Sends user queries to the FastAPI backend.

2. **Backend (FastAPI)**
   - Endpoints:
     - `GET /employees/search`: Search employees by query.
     - `POST /chat`: Returns AI-style recommendation messages.
   - Performs retrieval and augments results using Python logic.

3. **Data Layer**
   - Sample employee dataset (JSON) with fields:
     ```json
  

4. **AI/ML Component**
   - Uses TF–IDF vectorizer + cosine similarity to find relevant employees.
   - Template-based generation to produce readable recommendations.

---

## Setup & Installation
**1. Clone the repository**
``
            

##API Documentation
The HR Finder Chatbot backend exposes the following endpoints via **FastAPI**:

---

### 1️⃣ GET /employees/search
**Description:**  
Search for employees based on skills, experience, or past projects.

**Request Parameters:**  
- `query` (string): The search text describing required skills, experience, or projects.  
- `k` (integer, optional): Number of top matching employees to return (default 5).

## AI Development Process

**AI Coding Assistants Used:**  
- **ChatGPT** – Assisted in writing Python code for FastAPI endpoints, retrieval logic, and template-based responses.  
- **GitHub Copilot** – Suggested boilerplate code for Streamlit frontend, loops, and data handling.  

**How AI Helped in Different Phases:**  
- **Code Generation:** Generated initial FastAPI endpoint skeletons, Streamlit input/output handling, and JSON parsing logic.  
- **Debugging:** Helped identify errors in TF–IDF retrieval, data filtering, and API request/response handling.  
- **Architecture Decisions:** Suggested approaches for RAG-like system, combining retrieval + augmentation + template generation.  
- **Template Design:** Provided examples for readable AI-style recommendation messages.  

**Percentage of AI-assisted vs Hand-written Code:**  
- ~60% of the code was AI-assisted or generated (boilerplate, retrieval logic, templates).  
- ~40% was manually written/adjusted for project-specific logic, integration, and debugging.  

**Interesting AI-generated Solutions or Optimizations:**  
- Multi-constraint candidate filtering (skills + experience + projects).  
- Structured JSON response formatting with notes for readability.  
- Template-based recommendation generation that mimics AI-style answers without using an LLM.  

**Challenges Where AI Couldn’t Help and Were Solved Manually:**  
- Connecting the Streamlit frontend with FastAPI backend correctly.  
- Handling multiple search constraints and combining results accurately.  
- Designing the employees JSON dataset structure for easy retrieval.  
- Implementing optional parameters (`k` for top candidates) in both search and chat endpoints.  
- Debugging issues with local development environment and virtual environments.  

## Technical Decisions

**Backend Framework: FastAPI**  
- Chosen for its **async support**, **automatic Swagger documentation**, and **lightweight Python integration**.  
- Provides easy testing and rapid development for REST APIs.  

**Frontend Framework: Streamlit**  
- Selected for **quick prototyping** and **simple chat-style UI**.  
- Minimal code required to display inputs, buttons, and results interactively.  

**RAG Approach: Simple/Hybrid System**  
- Used **TF–IDF + cosine similarity** for retrieval and **template-based generation** for responses.  
- Chose this over full RAG with LLMs to keep the system **lightweight, fast, and cost-free**.  

**OpenAI vs Open-Source Models:**  
- Decision: Currently **template-based responses** without using OpenAI GPT.  
- Reason: Avoided dependency on cloud API costs, ensured **full privacy**, and simplified deployment.  
- Future plans: Could integrate OpenAI or local LLMs to generate natural language answers.  

**Local LLM (Ollama) vs Cloud API Considerations:**  
- **Local LLM:** Pros – privacy, offline use, no API costs; Cons – may require high compute resources.  
- **Cloud API (OpenAI):** Pros – high-quality natural language generation, scalability; Cons – cost, latency, privacy concerns.  
- Current choice: Template-based local solution, easy to upgrade later to full LLM integration.  

**Performance vs Cost vs Privacy Trade-offs:**  
- **Performance:** Lightweight TF–IDF retrieval ensures fast response times.  
- **Cost:** No paid LLM usage, all components run locally.  
- **Privacy:** Employee data stays local; no cloud data transfer.  
- Decision: Prioritized **cost and privacy** over natural language flexibility.  

## Future Improvements

With more time and resources, the following enhancements could be added:

1. **Full RAG Implementation**  
   - Upgrade from template-based responses to a **retrieval-augmented generation** system using embeddings + vector database + LLM.  
   - This would provide **more natural, flexible AI responses** for complex HR queries.

2. **Authentication and User Roles**  
   - Add **login system** for HR users.  
   - Implement **role-based access control** to manage who can view or edit employee data.

3. **Integration with Real HR Systems**  
   - Connect to **company HR databases or APIs** for live employee data instead of static JSON.

4. **Enhanced Frontend**  
   - Upgrade Streamlit UI to **React or Vue** for a richer, interactive interface.  
   - Add features like **search filters, sorting, and candidate comparison tables**.

5. **Advanced Query Handling**  
   - Support **multi-criteria queries**, e.g., “Find developers with Python + AWS experience who worked on healthcare projects and are available next month.”  
   - Integrate **natural language understanding** for more flexible question parsing.

6. **Analytics Dashboard**  
   - Add visualizations for **skills distribution, project experience, availability statistics**, etc.  

7. **Performance Optimization**  
   - Implement **embedding-based search** for faster and more accurate retrieval when the employee dataset grows large.  

8. **Notifications / Scheduling**  
   - Allow HR to **schedule interviews** or get **automated suggestions** for meetings with available candidates.

## Demo
![Image link](<img width="1704" height="4284" alt="Image" src="https://github.com/user-attachments/assets/71d257c4-d1c4-46f2-bec1-9a5fc60b967b" />)
