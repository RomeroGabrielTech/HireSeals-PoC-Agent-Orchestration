from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from schemas.order_models import OrderDetails
from tools.inventory_tools import check_inventory

# 1. Definir el estado del grafo con el modelo Pydantic
class AgentState(TypedDict):
    order_details: OrderDetails
    # Permite que el grafo registre el historial de la conversación.
    messages: Annotated[list, add_messages]

# 2. Definir los nodos del grafo
def inventory_check_node(state: AgentState):
    """
    Nodo que ejecuta la herramienta de verificación de inventario.
    """
    order_details = state['order_details']
    result = check_inventory(order_details)
    
    print(f"---VERIFICACIÓN DE INVENTARIO---")
    print(f"Resultado para SKU {order_details.product_sku}: {result.status}")
    print(f"Mensaje: {result.message}")
    print("---------------------------------")
    
    # El estado del inventario se usará para el enrutamiento
    state['inventory_status'] = result.status
    return {
        "messages": [f"Inventory check for {order_details.product_sku}: {result.status}"],
        "inventory_status": result.status
        }
    
def human_intervention_node(state: AgentState):
    """
    Nodo que simula la intervención humana cuando el stock no está disponible.
    """
    print("---INTERVENCIÓN HUMANA REQUERIDA---")
    print("El producto solicitado está fuera of stock. Se requiere acción manual.")
    print("------------------------------------")
    return {"messages": ["Human intervention required: product out of stock."]}

# 3. Construir el grafo
workflow = StateGraph(AgentState)
workflow.add_node("inventory_check_node", inventory_check_node)
workflow.add_node("human_intervention_node", human_intervention_node)

# 4. Definir el enrutamiento condicional
def route_inventory_check(state: AgentState):
    """
    Dirige el flujo basado en el estado del inventario.
    """
    status = state.get("inventory_status")
    if status == "STOCK_OK":
        return END
    else:
        return "human_intervention_node"

# 5. Establecer los puntos de entrada y las transiciones
workflow.set_entry_point("inventory_check_node")
workflow.add_conditional_edges(
    "inventory_check_node",
    route_inventory_check,
    {
        END: END,
        "human_intervention_node": "human_intervention_node",
    },
)
workflow.add_edge("human_intervention_node", END)

# 6. Compilar el grafo
app = workflow.compile()

# --- Simulación de ejecución ---
if __name__ == "__main__":
    # Caso 1: STOCK_OK
    print("Ejecutando Caso 1: STOCK_OK")
    inputs_ok = {"order_details": OrderDetails(product_sku="ABC-456", quantity=10, customer_id="CUST-100")}
    for event in app.stream(inputs_ok, {"recursion_limit": 5}):
        print(event)
    print("\n" + "="*30 + "\n")

    # Caso 2: OUT_OF_STOCK
    print("Ejecutando Caso 2: OUT_OF_STOCK")
    inputs_oot = {"order_details": OrderDetails(product_sku="XYZ-789", quantity=5, customer_id="CUST-200")}
    for event in app.stream(inputs_oot, {"recursion_limit": 5}):
        print(event)