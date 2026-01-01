"""
Example: Using BaseService to create a custom service.

This example demonstrates how to extend BaseService to create
a custom service for the Villa Ecommerce SDK.
"""

from villa_ecommerce_sdk.base import BaseService
from villa_ecommerce_sdk.cache import S3Cache
from typing import Dict, Any, Optional
import pandas as pd


class OrdersService(BaseService):
    """
    Custom service for order management.
    
    This service extends BaseService to provide order-related functionality.
    """
    
    def get_service_name(self) -> str:
        """Return the service name."""
        return "OrdersService"
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get order details by order ID.
        
        Args:
            order_id: Order identifier
            
        Returns:
            Order data as dictionary
        """
        cache_key = f"orders/{order_id}.json"
        return self._get(
            endpoint=f"/api/orders/{order_id}",
            cache_key=cache_key
        )
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            order_data: Order data dictionary containing:
                - customerId: Customer identifier
                - items: List of order items
                - branch: Branch ID
                - etc.
                
        Returns:
            Created order data
        """
        return self._post(
            endpoint="/api/orders/create",
            json_data=order_data,
            headers={"Content-Type": "application/json"}
        )
    
    def update_order_status(
        self,
        order_id: str,
        status: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update order status.
        
        Args:
            order_id: Order identifier
            status: New status (pending, confirmed, shipped, delivered, cancelled)
            notes: Optional status notes
            
        Returns:
            Updated order data
        """
        payload = {
            "orderId": order_id,
            "status": status
        }
        
        if notes:
            payload["notes"] = notes
        
        return self._put(
            endpoint=f"/api/orders/{order_id}/status",
            json_data=payload,
            headers={"Content-Type": "application/json"}
        )
    
    def get_order_history(
        self,
        customer_id: Optional[str] = None,
        branch: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Get order history with optional filters.
        
        Args:
            customer_id: Optional customer ID filter
            branch: Optional branch ID filter
            status: Optional status filter
            limit: Maximum number of records
            
        Returns:
            DataFrame containing order history
        """
        params = {"limit": limit}
        
        if customer_id:
            params["customerId"] = customer_id
        if branch:
            params["branch"] = branch
        if status:
            params["status"] = status
        
        cache_key = f"orders/history/{customer_id or 'all'}.json"
        data = self._get(
            endpoint="/api/orders/history",
            cache_key=cache_key,
            params=params
        )
        
        # Convert to DataFrame
        if isinstance(data, dict):
            if 'orders' in data:
                orders_list = data['orders']
            elif 'data' in data:
                orders_list = data['data']
            else:
                orders_list = [data] if not isinstance(data, list) else data
        elif isinstance(data, list):
            orders_list = data
        else:
            orders_list = [data]
        
        return pd.DataFrame(orders_list)
    
    def cancel_order(self, order_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            order_id: Order identifier
            reason: Optional cancellation reason
            
        Returns:
            Cancellation result
        """
        payload = {"orderId": order_id}
        
        if reason:
            payload["reason"] = reason
        
        return self._post(
            endpoint=f"/api/orders/{order_id}/cancel",
            json_data=payload,
            headers={"Content-Type": "application/json"}
        )


def example_usage():
    """Example usage of the custom OrdersService."""
    
    # Initialize cache (using default bucket)
    cache = S3Cache(bucket_name="villa-ecommerce-sdk-cache")
    
    # Initialize custom service
    orders_service = OrdersService(
        base_url="https://shop.villamarket.com",
        cache=cache
    )
    
    # Get an order
    order = orders_service.get_order(order_id="ORDER-12345")
    print(f"Order Status: {order['status']}")
    print(f"Order Total: {order['total']}")
    
    # Create a new order
    new_order = orders_service.create_order({
        "customerId": "CUST-123",
        "items": [
            {"productId": "PROD-1", "quantity": 2},
            {"productId": "PROD-2", "quantity": 1}
        ],
        "branch": 1000
    })
    print(f"Created Order: {new_order['orderId']}")
    
    # Update order status
    updated = orders_service.update_order_status(
        order_id="ORDER-12345",
        status="confirmed",
        notes="Order confirmed and ready for processing"
    )
    print(f"Order Status Updated: {updated['status']}")
    
    # Get order history
    history = orders_service.get_order_history(
        customer_id="CUST-123",
        limit=50
    )
    print(f"Order History: {len(history)} orders")
    
    # Cancel an order
    cancelled = orders_service.cancel_order(
        order_id="ORDER-12345",
        reason="Customer requested cancellation"
    )
    print(f"Order Cancelled: {cancelled['status']}")


if __name__ == "__main__":
    example_usage()

