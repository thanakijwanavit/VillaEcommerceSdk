"""Inventory functionality for Villa Ecommerce SDK."""

import pandas as pd
import requests
from villa_ecommerce_sdk.cache import S3Cache


class InventoryService:
    """Service for fetching inventory data."""
    
    def __init__(self, base_url: str, cache: S3Cache):
        """
        Initialize Inventory Service.
        
        Args:
            base_url: Base URL for Villa API
            cache: S3Cache instance for caching
        """
        self.base_url = base_url.rstrip('/')
        self.cache = cache
    
    def get_inventory(self, branch: int = 1000) -> pd.DataFrame:
        """
        Get inventory data for a specific branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            DataFrame containing inventory data
        """
        cache_key = f"inventory/{branch}.json"
        
        # Try to get from cache first
        cached_data = self.cache.get_cached(cache_key)
        if cached_data is not None:
            return pd.DataFrame(cached_data)
        
        # Fetch from API
        url = f"{self.base_url}/api/inventory2/{branch}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
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
            df = pd.DataFrame(inventory_list)
            
            # Cache the result
            self.cache.set_cached(cache_key, inventory_list)
            
            return df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch inventory: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing inventory: {str(e)}")

