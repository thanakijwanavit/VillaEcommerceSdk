"""Tests for InventoryService."""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from villa_ecommerce_sdk.inventory import InventoryService
from villa_ecommerce_sdk.cache import S3Cache


class TestInventoryService:
    """Test cases for InventoryService."""
    
    def test_init(self):
        """Test InventoryService initialization."""
        cache = Mock(spec=S3Cache)
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        assert service.base_url == "https://api.example.com"
        assert service.cache == cache
    
    def test_get_inventory_from_api(self):
        """Test fetching inventory from API."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value=[
            {"id": 1, "stock": 10},
            {"id": 2, "stock": 20}
        ])
        
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        service._get.assert_called_once()
    
    def test_get_inventory_from_cache(self):
        """Test fetching inventory from cache."""
        cached_data = [
            {"id": 1, "stock": 10},
            {"id": 2, "stock": 20}
        ]
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = cached_data
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        cache.get_cached.assert_called_once_with("inventory/1000.json")
    
    def test_get_inventory_dict_with_inventory_key(self):
        """Test parsing dict response with 'inventory' key."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "inventory": [
                {"id": 1, "stock": 10},
                {"id": 2, "stock": 20}
            ]
        })
        
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    def test_get_inventory_dict_with_data_key(self):
        """Test parsing dict response with 'data' key."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "data": [
                {"id": 1, "stock": 10}
            ]
        })
        
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    def test_get_inventory_dict_with_items_key(self):
        """Test parsing dict response with 'items' key."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "items": [
                {"id": 1, "stock": 10}
            ]
        })
        
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
    
    def test_get_inventory_dict_fallback(self):
        """Test parsing dict response fallback."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value={
            "id": 1,
            "stock": 10
        })
        
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_inventory_non_list_non_dict(self):
        """Test parsing non-list, non-dict response."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(return_value="unexpected format")
        
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_inventory_request_exception(self):
        """Test handling RequestException."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(side_effect=Exception("Network error"))
        
        with pytest.raises(Exception):
            service.get_inventory(branch=1000)
    
    def test_get_inventory_general_exception(self):
        """Test handling general exception."""
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        service._get = Mock(side_effect=ValueError("Invalid JSON"))
        
        with pytest.raises(Exception):
            service.get_inventory(branch=1000)

