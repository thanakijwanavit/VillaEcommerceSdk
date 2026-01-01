"""Product list functionality for Villa Ecommerce SDK."""

import pandas as pd
from villa_ecommerce_sdk.base import BaseService


class ProductsService(BaseService):
    """Service for fetching product list data."""
    
    def get_service_name(self) -> str:
        """Get service name."""
        return "ProductsService"
    
    def get_product_list(self, branch: int = 1000) -> pd.DataFrame:
        """
        Get product list for a specific branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            DataFrame containing product data
        """
        cache_key = f"products/{branch}.json"
        
        # Fetch from API using base service
        data = self._get(
            endpoint=f"/api/product/productlist/onlineData/{branch}",
            cache_key=cache_key
        )
        
        # Process response data
        if isinstance(data, dict):
            # If data is a dict, try to find the list of products
            # Common patterns: data['products'], data['data'], data['items'], or data itself
            if 'products' in data:
                products_list = data['products']
            elif 'data' in data:
                products_list = data['data']
            elif 'items' in data:
                products_list = data['items']
            else:
                # If data is already a list or dict, use it directly
                products_list = data if isinstance(data, list) else [data]
        elif isinstance(data, list):
            products_list = data
        else:
            products_list = [data]
        
        # Convert to DataFrame
        return pd.DataFrame(products_list)

