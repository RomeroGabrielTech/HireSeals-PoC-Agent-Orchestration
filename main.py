import os
import sys
# Añade el directorio raíz al path para asegurar que los módulos locales se encuentren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from schemas.order_models import OrderDetails
from tools.inventory_tools import check_inventory

# Cargar variables de entorno desde .env
load_dotenv()

# 1. Inicialización del LLM
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)


# 2. Definir el estado del grafo
class AgentState(TypedDict):
    order_details: OrderDetails
    inventory_status: str
    messages: Annotated[list, add_messages]

# 3. Definir los nodos del grafo
def inventory_check_node(state: AgentState):
    """
    Nodo que ejecuta la herramienta de verificación de inventario y actualiza el estado.
    """
    order_details = state['order_details']
    result = check_inventory(order_details)
    
    print("---VERIFICACIÓN DE INVENTARIO---")
    print(f"Resultado para SKU {order_details.product_sku}: {result.status}")
    print(f"Mensaje: {result.message}")
    print("---------------------------------")
    
    return {"inventory_status": result.status}

def human_intervention_node(state: AgentState):
    """
    Nodo que simula la intervención humana, potencialmente usando un LLM para generar un borrador de correo.
    """
    print("---INTERVENCIÓN HUMANA REQUERIDA---")
    details = state['order_details']
    prompt = f"""
    El cliente {details.customer_id} intentó pedir {details.quantity} unidades del producto {details.product_sku}, 
    pero está fuera de stock. Por favor, redacta un correo electrónico breve y profesional para notificar al cliente 
    y sugerir que se ponga en contacto con su gestor de cuenta para explorar alternativas.
    """
    
    response = llm.invoke(prompt)
    
    print("Borrador de correo electrónico generado por IA:")
    print(response.content)
    print("------------------------------------")
    return {"messages": [f"Human intervention for {details.product_sku}: out of stock."]}

# 4. Construir el grafo
workflow = StateGraph(AgentState)
workflow.add_node("inventory_check_node", inventory_check_node)
workflow.add_node("human_intervention_node", human_intervention_node)

# 5. Definir el enrutamiento condicional
def route_inventory_check(state: AgentState):
    """
    Dirige el flujo basado en el estado del inventario.
    """
    return "human_intervention_node" if state["inventory_status"] == "OUT_OF_STOCK" else END

# 6. Establecer los puntos de entrada y las transiciones
workflow.set_entry_point("inventory_check_node")
workflow.add_conditional_edges("inventory_check_node", route_inventory_check)
workflow.add_edge("human_intervention_node", END)

# 7. Compilar el grafo
app = workflow.compile()

# --- Simulación de ejecución ---
if __name__ == "__main__":
    print("Ejecutando Caso 1: STOCK_OK")
    inputs_ok = {"order_details": OrderDetails(product_sku="ABC-456", quantity=10, customer_id="CUST-100")}
    for event in app.stream(inputs_ok, {"recursion_limit": 5}):
        print(f"Evento: {event}")
    print("\n" + "="*30 + "\n")

    print("Ejecutando Caso 2: OUT_OF_STOCK")
    inputs_oot = {"order_details": OrderDetails(product_sku="XYZ-789", quantity=5, customer_id="CUST-200")}
    for event in app.stream(inputs_oot, {"recursion_limit": 5}):
        print(f"Evento: {event}")
