"""Tests for VillaClient."""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from villa_ecommerce_sdk.client import VillaClient


class TestVillaClient:
    """Test cases for VillaClient."""
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_init(self, mock_cache, mock_inventory, mock_products):
        """Test VillaClient initialization."""
        client = VillaClient(s3_bucket="test-bucket")
        assert client.base_url == "https://shop.villamarket.com"
        assert client.s3_bucket == "test-bucket"
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_get_product_list(self, mock_cache, mock_inventory, mock_products):
        """Test get_product_list method."""
        mock_products_instance = Mock()
        mock_products_instance.get_product_list.return_value = pd.DataFrame({"id": [1, 2]})
        mock_products.return_value = mock_products_instance
        
        client = VillaClient(s3_bucket="test-bucket")
        result = client.get_product_list(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        mock_products_instance.get_product_list.assert_called_once_with(branch=1000)
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_get_inventory(self, mock_cache, mock_inventory, mock_products):
        """Test get_inventory method."""
        mock_inventory_instance = Mock()
        mock_inventory_instance.get_inventory.return_value = pd.DataFrame({"id": [1, 2]})
        mock_inventory.return_value = mock_inventory_instance
        
        client = VillaClient(s3_bucket="test-bucket")
        result = client.get_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        mock_inventory_instance.get_inventory.assert_called_once_with(branch=1000)
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_filter_dataframe(self, mock_cache, mock_inventory, mock_products):
        """Test filter_dataframe method."""
        client = VillaClient(s3_bucket="test-bucket")
        
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "category": ["electronics", "food", "electronics"],
            "price": [100, 50, 200]
        })
        
        # Test exact match filter
        filtered = client.filter_dataframe(df, {"category": "electronics"})
        assert len(filtered) == 2
        assert all(filtered["category"] == "electronics")
        
        # Test numeric comparison
        filtered = client.filter_dataframe(df, {"price": {"gt": 75}})
        assert len(filtered) == 2
        
        # Test list filter
        filtered = client.filter_dataframe(df, {"category": ["electronics", "food"]})
        assert len(filtered) == 3
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_get_products_with_inventory(self, mock_cache, mock_inventory, mock_products):
        """Test get_products_with_inventory method."""
        mock_products_instance = Mock()
        mock_products_instance.get_product_list.return_value = pd.DataFrame({
            "id": [1, 2],
            "name": ["Product 1", "Product 2"]
        })
        mock_products.return_value = mock_products_instance
        
        mock_inventory_instance = Mock()
        mock_inventory_instance.get_inventory.return_value = pd.DataFrame({
            "id": [1, 2],
            "stock": [10, 20]
        })
        mock_inventory.return_value = mock_inventory_instance
        
        client = VillaClient(s3_bucket="test-bucket")
        result = client.get_products_with_inventory(branch=1000)
        
        assert isinstance(result, pd.DataFrame)
        mock_products_instance.get_product_list.assert_called_once_with(branch=1000)
        mock_inventory_instance.get_inventory.assert_called_once_with(branch=1000)

