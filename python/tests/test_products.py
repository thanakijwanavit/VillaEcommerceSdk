"""Tests for ProductsService."""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from villa_ecommerce_sdk.products import ProductsService
from villa_ecommerce_sdk.cache import S3Cache


class TestProductsService:
    """Test cases for ProductsService."""
    
    def test_init(self):
        """Test ProductsService initialization."""
        cache = Mock(spec=S3Cache)
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        assert service.base_url == "https://api.example.com"
        assert service.cache == cache
    
    def test_get_product_list_from_api(self):
        """Test fetching product list from API."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        
        # Mock the _get method
        service._get = Mock(return_value=[
            {"id": 1, "name": "Product 1"},
            {"id": 2, "name": "Product 2"}
        ])
        
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        service._get.assert_called_once()
    
    def test_get_product_list_from_cache(self):
        """Test fetching product list from cache."""
        cached_data = [
            {"id": 1, "name": "Product 1"},
            {"id": 2, "name": "Product 2"}
        ]
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = cached_data
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        cache.get_cached.assert_called_once_with("products/1000.json")
    
    def test_get_product_list_dict_with_products_key(self):
        """Test parsing dict response with 'products' key."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "products": [
                {"id": 1, "name": "Product 1"},
                {"id": 2, "name": "Product 2"}
            ]
        })
        
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    def test_get_product_list_dict_with_data_key(self):
        """Test parsing dict response with 'data' key."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "data": [
                {"id": 1, "name": "Product 1"}
            ]
        })
        
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    def test_get_product_list_dict_with_items_key(self):
        """Test parsing dict response with 'items' key."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "items": [
                {"id": 1, "name": "Product 1"}
            ]
        })
        
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    def test_get_product_list_dict_fallback(self):
        """Test parsing dict response fallback."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "id": 1,
            "name": "Product 1"
        })
        
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_product_list_non_list_non_dict(self):
        """Test parsing non-list, non-dict response."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value="unexpected format")
        
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_product_list_request_exception(self):
        """Test handling RequestException."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(side_effect=Exception("Network error"))
        
        with pytest.raises(Exception):
            service.get_product_list(branch=1000)
    
    def test_get_product_list_general_exception(self):
        """Test handling general exception."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(side_effect=ValueError("Invalid JSON"))
        
        with pytest.raises(Exception):
            service.get_product_list(branch=1000)

