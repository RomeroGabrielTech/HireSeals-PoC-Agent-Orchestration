import pytest
import sys
import os

# Añade el directorio raíz al path para asegurar que los módulos locales se encuentren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemas.order_models import OrderDetails, InventoryCheckResult
from tools.inventory_tools import check_inventory

def test_check_inventory_stock_ok():
    """
    Test para validar que el SKU 'ABC-456' devuelve 'STOCK_OK'.
    """
    order = OrderDetails(product_sku="ABC-456", quantity=1, customer_id="CUST-100")
    expected_result = InventoryCheckResult(status='STOCK_OK', message="El producto ABC-456 tiene stock disponible.")
    
    result = check_inventory(order)
    
    assert result.status == expected_result.status
    assert "tiene stock disponible" in result.message

def test_check_inventory_out_of_stock():
    """
    Test para validar que cualquier otro SKU devuelve 'OUT_OF_STOCK'.
    """
    order = OrderDetails(product_sku="XYZ-789", quantity=1, customer_id="CUST-200")
    expected_result = InventoryCheckResult(status='OUT_OF_STOCK', message="El producto XYZ-789 está fuera de stock.")
    
    result = check_inventory(order)
    
    assert result.status == expected_result.status
    assert "está fuera de stock" in result.message

def test_check_inventory_zero_quantity_error():
    """
    Test para verificar que Pydantic previene cantidades iguales o menores a cero.
    """
    with pytest.raises(ValueError):
        OrderDetails(product_sku="ABC-456", quantity=0, customer_id="CUST-300")