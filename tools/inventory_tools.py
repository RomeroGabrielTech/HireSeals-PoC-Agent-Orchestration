from schemas.order_models import OrderDetails, InventoryCheckResult

def check_inventory(order_details: OrderDetails) -> InventoryCheckResult:
    """
    Simula la verificación del inventario en un sistema ERP.
    """
    if order_details.product_sku == "ABC-456":
        return InventoryCheckResult(
            status='STOCK_OK',
            message=f"El producto {order_details.product_sku} tiene stock disponible."
        )
    else:
        return InventoryCheckResult(
            status='OUT_OF_STOCK',
            message=f"El producto {order_details.product_sku} está fuera de stock."
        )