"""Inventory functionality for Villa Ecommerce SDK."""

import pandas as pd
from villa_ecommerce_sdk.base import BaseService


class InventoryService(BaseService):
    """Service for fetching inventory data."""
    
    def get_service_name(self) -> str:
        """Get service name."""
        return "InventoryService"
    
    def get_inventory(self, branch: int = 1000) -> pd.DataFrame:
        """
        Get inventory data for a specific branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            DataFrame containing inventory data
        """
        cache_key = f"inventory/{branch}.json"
        
        # Fetch from API using base service
        data = self._get(
            endpoint=f"/api/inventory2/{branch}",
            cache_key=cache_key
        )
        
        # Process response data
        if isinstance(data, dict):
            # If data is a dict, try to find the list of inventory items
            # Common patterns: data['inventory'], data['data'], data['items'], or data itself
            if 'inventory' in data:
                inventory_list = data['inventory']
            elif 'data' in data:
                inventory_list = data['data']
            elif 'items' in data:
                inventory_list = data['items']
            else:
                # If data is already a list or dict, use it directly
                inventory_list = data if isinstance(data, list) else [data]
        elif isinstance(data, list):
            inventory_list = data
        else:
            inventory_list = [data]
        
        # Convert to DataFrame
        return pd.DataFrame(inventory_list)

