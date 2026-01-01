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
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_from_api(self, mock_get):
        """Test fetching product list from API."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Product 1"},
            {"id": 2, "name": "Product 2"}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        mock_get.assert_called_once()
        cache.set_cached.assert_called_once()
    
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
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_dict_with_products_key(self, mock_get):
        """Test parsing dict response with 'products' key."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "products": [
                {"id": 1, "name": "Product 1"},
                {"id": 2, "name": "Product 2"}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_dict_with_data_key(self, mock_get):
        """Test parsing dict response with 'data' key."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {"id": 1, "name": "Product 1"}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_dict_with_items_key(self, mock_get):
        """Test parsing dict response with 'items' key."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {"id": 1, "name": "Product 1"}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_dict_fallback(self, mock_get):
        """Test parsing dict response fallback."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "Product 1"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_non_list_non_dict(self, mock_get):
        """Test parsing non-list, non-dict response."""
        mock_response = Mock()
        mock_response.json.return_value = "unexpected format"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        result = service.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_request_exception(self, mock_get):
        """Test handling RequestException."""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        
        with pytest.raises(Exception) as exc_info:
            service.get_product_list(branch=1000)
        assert "Failed to fetch product list" in str(exc_info.value)
    
    @patch('villa_ecommerce_sdk.products.requests.get')
    def test_get_product_list_general_exception(self, mock_get):
        """Test handling general exception."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = ProductsService(base_url="https://api.example.com", cache=cache)
        
        with pytest.raises(Exception) as exc_info:
            service.get_product_list(branch=1000)
        assert "Error processing product list" in str(exc_info.value)

