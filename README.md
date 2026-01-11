# AI Travel Planner

A **constraint-aware and explainable travel itinerary planner** built with Python and Streamlit, with controlled and intentional use of LLMs.

This project focuses on **system design and decision-making**, not just generating text with AI.

---

## What This Project Does

The AI Travel Planner helps users plan a **day itinerary** by:

- Taking **user constraints** (time, budget, walking distance)
- Accepting **user-defined activities** (name + category)
- Deterministically selecting and ordering activities
- Explaining **why** the itinerary was chosen
- Narrating **how the day would feel** in natural language

⚠️ Important:  
The AI **does not decide** the itinerary.  
All planning is done using **deterministic logic**.  
LLMs are used **only for explanation and narration**.

---

## Core Design Idea

> **Planning should be deterministic.  
> AI should explain, not decide.**

This project separates responsibilities clearly:

- **Planner** → decides *what* to do  
- **Explainer** → explains *why* the plan makes sense  
- **Narrator** → describes *how* the day feels  
- **UI** → only displays results  

---

## Architecture Overview

```
User Input (Activities + Constraints)
            ↓
    Constraint Engine (hard limits)
            ↓
      Scoring Engine (heuristics)
            ↓
        Planner (deterministic)
            ↓
   Itinerary (fixed structure)
        ↓           ↓
 Explainer        Narrator
  (WHY)            (HOW)
```

---

## Key Features

- Constraint-aware planning (time, budget, distance)
- Heuristic scoring (interest, time fit, distance penalty)
- Deterministic itinerary generation
- Itinerary-level explainability
- Natural language narration (LLM-assisted)
- Clean modular architecture
- Interactive Streamlit UI

---

## Tech Stack

- **Python**
- **Streamlit** (UI)
- **LangChain + Groq** (LLM interface)
- **Docker** (containerization)
- **No database (yet)** — data is generated deterministically

---

## How Activities Are Handled

Users only provide:
- Activity name
- Activity category (e.g., museum, food, nature)

The system assigns:
- Duration
- Estimated cost
- Tags
- Distance (simple proxy)

This avoids noisy user input and keeps planning **predictable and explainable**.

---

## How to Run Locally

### 1️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add environment variables
Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

### 4️⃣ Run the app
```bash
streamlit run app/app.py
```

---

## Deployment

- The application is **Dockerized** for reproducible builds.
- Deployed on **Streamlit Cloud** for simplicity and fast iteration.
- Secrets (API keys) are injected at runtime via Streamlit Cloud’s secrets manager.
- The Docker image remains portable to other platforms (e.g., Kubernetes) if needed.

---

## Project Structure

```
.
├── app/                    # Streamlit app and UI entry point
│   ├── app.py
│   ├── core/               # Planning, scoring, constraints
│   ├── chains/             # Explainer & narrator (LLM usage)
│   ├── config/             # Environment configuration
│   └── utils/
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

---

## What This Project Is NOT

- Not a ChatGPT wrapper  
- Not prompt-only itinerary generation  
- Not full route optimization  

This project prioritizes **clarity, control, and explainability** over unnecessary complexity.
