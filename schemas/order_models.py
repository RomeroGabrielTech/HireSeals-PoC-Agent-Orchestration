from typing import Literal
from pydantic import BaseModel, Field

class OrderDetails(BaseModel):
    """
    Representa los detalles de un pedido con validación estricta.
    """
    product_sku: str
    quantity: int = Field(..., gt=0, description="La cantidad debe ser un entero mayor que cero.")
    customer_id: str

class InventoryCheckResult(BaseModel):
    """
    Representa el resultado de una verificación de inventario usando tipos Literales.
    """
    status: Literal['STOCK_OK', 'OUT_OF_STOCK']
    message: str