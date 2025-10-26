# 🚀 HireSeals-PoC-Agent-Orchestration: Reliable B2B Order Agent
I created this PoC immediately after the interview to validate my skillset with your exact stack.

This repository contains a Proof-of-Concept (PoC) demonstrating the necessary architecture to automate critical business workflows, such as **order taking and quoting**, in wholesaler and distributor environments.

The focus is on **reliability, scalability, and data validation (Pydantic)**, which are essential for integration with high-risk ERP systems.

---

## 🎯 Business Challenge Addressed

In the B2B sector, an AI agent must manage complex logic and cannot afford errors in sensitive data (SKU, prices). This PoC models an agent that:

1.  Extracts order details from natural language.
2.  Validates that the data is correct and consistent.
3.  Manages business logic (e.g., Is there inventory? Is the price valid?) using a conditional flow.

## 🛠️ Senior Technology Stack

| Technology | Role in the HireSeals.ai Architecture |
| :--- | :--- |
| **LangGraph** | **Orchestration and Flow Control:** Uses a `StateGraph` and **Conditional Edges** to manage retries, validation, and business logic. This simulates human decision-making. |
| **Pydantic** | **Reliability and Critical Validation:** Defines data schemas (*Structured Output*) to guarantee the LLM only generates clean, typed data, ready for an ERP system. |
| **FastAPI** | **Backend Scalability:** Provides a high-performance REST *endpoint* to expose the AI agent as a microservice, facilitating integration into any existing infrastructure. |
| **Algorithms and Structures** | The stock lookup logic is optimized (simulated) to demonstrate knowledge of **Graph Algorithms** and efficiency in data searching (relevant to my experience in Neo4j/Memgraph). |

---

## 🧠 LangGraph Flow Architecture

The graph is designed to ensure no costly error occurs:

1.  **`extract_details` (LLM Node):** Uses a `Pydantic Schema` (defined in `schemas.py`) to extract the client's `SKU` and `quantity`.
2.  **`check_inventory` (Tool Node):** Simulates the call to the inventory database. Returns **"STOCK_OK"** or **"STOCK_ERROR"**.
3.  **`conditional_router` (Edge):**
    * If it is **"STOCK_OK"**, the flow goes to `generate_quote`.
    * If it is **"STOCK_ERROR"**, the flow goes to the `request_human_intervention` node, documenting the error before failing (Human-in-the-Loop).

## 🚀 How to Run the PoC

1.  **Clone:** `git clone [YOUR_REPOSITORY_URL_HERE]`
2.  **Environment:** `python -m venv venv` and `source venv/bin/activate`
3.  **Install:** `pip install -r requirements.txt`
4.  **Configure LLM:** Create a `.env` file and define your API key (e.g., `GOOGLE_API_KEY=...`).
5.  **Execute:** [Simple instruction to run `main.py` or the FastAPI server with `uvicorn main:app --reload`].
---

*Desarrollado por Gabriel Romero Canelón como demostración de experiencia en arquitectura de agentes.*
