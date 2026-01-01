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
    
    @patch('villa_ecommerce_sdk.inventory.requests.get')
    def test_get_inventory_from_api(self, mock_get):
        """Test fetching inventory from API."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "stock": 10},
            {"id": 2, "stock": 20}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        cache = Mock(spec=S3Cache)
        cache.get_cached.return_value = None
        
        service = InventoryService(base_url="https://api.example.com", cache=cache)
        result = service.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        mock_get.assert_called_once()
        cache.set_cached.assert_called_once()
    
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

