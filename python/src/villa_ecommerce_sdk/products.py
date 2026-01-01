"""Product list functionality for Villa Ecommerce SDK."""

import pandas as pd
import requests
from villa_ecommerce_sdk.cache import S3Cache


class ProductsService:
    """Service for fetching product list data."""
    
    def __init__(self, base_url: str, cache: S3Cache):
        """
        Initialize Products Service.
        
        Args:
            base_url: Base URL for Villa API
            cache: S3Cache instance for caching
        """
        self.base_url = base_url.rstrip('/')
        self.cache = cache
    
    def get_product_list(self, branch: int = 1000) -> pd.DataFrame:
        """
        Get product list for a specific branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            DataFrame containing product data
        """
        cache_key = f"products/{branch}.json"
        
        # Try to get from cache first
        cached_data = self.cache.get_cached(cache_key)
        if cached_data is not None:
            return pd.DataFrame(cached_data)
        
        # Fetch from API
        url = f"{self.base_url}/api/product/productlist/onlineData/{branch}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
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
            df = pd.DataFrame(products_list)
            
            # Cache the result
            self.cache.set_cached(cache_key, products_list)
            
            return df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch product list: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing product list: {str(e)}")

