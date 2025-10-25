# 🚀 HireSeals-PoC-Agent-Orchestration: Agente de Pedidos B2B Fiable
Creé este PoC inmediatamente después de la entrevista para validar mi skillset con su stack exacto

Este repositorio contiene una Prueba de Concepto (PoC) que demuestra la arquitectura necesaria para automatizar flujos de trabajo de negocio críticos, como la **toma de pedidos y la cotización**, en entornos de mayoristas y distribuidores.

El enfoque está en la **fiabilidad, la escalabilidad y la validación de datos (Pydantic)**, esenciales para la integración con sistemas ERP de alto riesgo.

---

## 🎯 Desafío de Negocio Abordado

En el sector B2B, un agente de IA debe gestionar lógica compleja y no puede permitirse errores en datos sensibles (SKU, precios). Este PoC modela un agente que:

1.  Extrae los detalles de un pedido de lenguaje natural.
2.  Valida que los datos sean correctos y consistentes.
3.  Maneja la lógica de negocio (ej. ¿Hay inventario? ¿El precio es válido?) mediante un flujo condicional.

## 🛠️ Stack Tecnológico Senior

| Tecnología | Rol en la Arquitectura de HireSeals.ai |
| :--- | :--- |
| **LangGraph** | **Orquestación y Control de Flujo:** Utiliza un `StateGraph` y **Conditional Edges** para gestionar reintentos, validación y la lógica de negocio. Esto simula la toma de decisiones humana. |
| **Pydantic** | **Fiabilidad y Validación Crítica:** Define los esquemas de datos (*Structured Output*) para garantizar que el LLM solo genere datos limpios y tipados, listos para un sistema ERP. |
| **FastAPI** | **Escalabilidad de Backend:** Proporciona un *endpoint* REST de alto rendimiento para exponer el agente de IA como un microservicio, facilitando la integración en cualquier infraestructura existente. |
| **Algoritmos y Estructuras** | La lógica de consulta de stock está optimizada (simulada) para demostrar el conocimiento de **Algoritmos de Grafos** y la eficiencia en la búsqueda de datos (relevante a mi experiencia en Neo4j/Memgraph). |

---

## 🧠 Arquitectura del Flujo (LangGraph)

El grafo está diseñado para asegurar que no se cometa ningún error costoso:

1.  **`extract_details` (LLM Node):** Utiliza un `Pydantic Schema` (definido en `schemas.py`) para extraer el `SKU` y la `quantity` del cliente.
2.  **`check_inventory` (Tool Node):** Simula la llamada a la base de datos de inventario. Devuelve **"STOCK_OK"** o **"STOCK_ERROR"**.
3.  **`conditional_router` (Edge):**
    * Si es **"STOCK_OK"**, el flujo va a `generate_quote`.
    * Si es **"STOCK_ERROR"**, el flujo va al nodo `request_human_intervention`, documentando el error antes de fallar (Human-in-the-Loop).

## 🚀 Cómo Ejecutar el PoC

1.  **Clonar:** `git clone https://www.youtube.com/watch?v=GtN6N11qSgA`
2.  **Entorno:** `python -m venv venv` y `source venv/bin/activate`
3.  **Instalar:** `pip install -r requirements.txt`
4.  **Configurar LLM:** Crea un archivo `.env` y define tu clave de API (ej., `OPENAI_API_KEY=...`).
5.  **Ejecutar:** [Instrucción simple para correr `main.py` o el servidor FastAPI con `uvicorn main:app --reload`].

---

*Desarrollado por Gabriel Romero Canelón como demostración de experiencia en arquitectura de agentes.*
