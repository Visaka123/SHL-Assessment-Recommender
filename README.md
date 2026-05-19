# Conversational SHL Assessment Recommender

An engineering-first, production-grade conversational AI assistant built for the SHL Labs AI Intern assignment. This service transitions users from vague hiring intents into a grounded, highly accurate shortlist of SHL individual test solutions through deterministic, state-driven multi-turn dialogue.

##  Live Production Registries
* **Production Base URL:** `https://shl-assessment-recommender-a4ps.onrender.com`
* **Health Check Endpoint (`GET /health`):** `https://shl-assessment-recommender-a4ps.onrender.com/health`
* **Chat Orchestration Engine (`POST /chat`):** `https://shl-assessment-recommender-a4ps.onrender.com/chat`

---

##  Architectural Blueprint & Core Design Choices

This implementation intentionally avoids loose, unpredictable autonomous agent loops (e.g., raw ReAct or LangGraph chains) to prevent token drift, tool hallucinations, and infinite routing loops under strict evaluation limits. 

Instead, the system utilizes a **State-Driven Multi-Action Orchestrator** built on top of an asynchronous FastAPI/Uvicorn server.

### Key Technical Pillars
1. **Stateless Persistence:** Fully complies with the stateless contract. No database or server-side session caching is used; the complete historical chat log is ingested and parsed on every individual micro-turn execution to re-hydrate state context natively.
2. **Structural Decoupling:** Conversational parsing logic is separated from data delivery. The LLM functions strictly as a semantic classifier, while a hard-coded Python data-integrity gate verifies catalog consistency and compiles the final response schema.
3. **Resilient Schema Enforcement:** Every individual execution pathway runs within strict try-except-intercept blocks, guaranteeing that a runtime failure will never break the required JSON format structure.

---

## Context Engineering & Hybrid Retrieval Pipeline

To optimize the **Mean Recall@10** score across public and holdout evaluation traces without introducing hallucinations, the system implements a dual-engine hybrid retrieval stack:

* **Lexical Layer (Rank-BM25):** Handles exact catalog keyword queries, capturing explicit alphanumeric shorthand test identifiers (e.g., `OPQ32r`, `GSA`) and rigid language strings.
* **Dense Semantic Layer (FAISS + MiniLM):** Maps abstract, low-context descriptions (e.g., *"works with stakeholders"*, *"entry-level track"*) to the core behavioral competencies found in the catalog data.
* **Historical Multi-Turn Ingestion (Turn 4 Fix):** Standard dense vectors drop to zero matching scores on closing turns when users say low-context things like *"Perfect, that's what we need"*. This pipeline fixes the dropout by expanding the vector retrieval sweep window on turns $> 1$ across the entire chat text log, keeping indices fully hydrated through session finality.

---

## Edge-Case Mitigations & Behavior Probes Pass-Rate

* **Vague First-Turn Refusal:** If a user inputs low-context vectors on Turn 1 (e.g., *"I need an assessment"*), the system forces a `CLARIFY` state, flushes the recommendations array to empty `[]`, and asks clarifying questions.
* **State Carry-Over Guard:** When a user signals closing satisfaction (*"Looks great, let's ship it"*), the orchestrator triggers the `COMPLETE` state. To prevent the LLM from accidentally wiping the recommendations list on session finality, a local Python regex overlay scrapes the immediate prior assistant message, extracts the existing verified catalog names, and re-attaches them to lock in a perfect **1.0 Recall Fraction**.
* **Hard Catalog Perimeter Firewall:** Every LLM-generated assessment choice must pass through a local dictionary lookup of the scraped catalog data. Unverified or hallucinated items are pruned instantly.

---

##  Tech Stack & Performance Bounds

* **Framework:** FastAPI + Uvicorn (Async thread execution optimized for low memory overhead).
* **Vector Mechanics:** FAISS (CPU-bound local index) + `rank-bm25` (Zero cloud database round-trip latencies).
* **LLM Core:** Llama 3 Ecosystem via Groq API (Sub-second inference delivering replies in $<1.5$ seconds per turn, safely beating the 30-second evaluator timeout limit).

---

## AI Tools Disclosure

AI tools (Gemini 1.5 and Groq/Llama 3) were strictly leveraged for production acceleration rather than autonomous architecture design:
1. **Data Engineering:** Automated the execution of a custom Python regex scraping script to extract raw HTML catalog fields into a structured JSON index.
2. **Stress Testing:** Assisted in writing a local multi-turn replay simulation harness to validate prompt resilience and state stability across the 10 public trace personas prior to live cloud deployment.