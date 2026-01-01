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
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_get_products_with_inventory_with_filters(self, mock_cache, mock_inventory, mock_products):
        """Test get_products_with_inventory with filters."""
        mock_products_instance = Mock()
        mock_products_instance.get_product_list.return_value = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Product 1", "Product 2", "Product 3"],
            "category": ["A", "B", "A"]
        })
        mock_products.return_value = mock_products_instance
        
        mock_inventory_instance = Mock()
        mock_inventory_instance.get_inventory.return_value = pd.DataFrame({
            "id": [1, 2, 3],
            "stock": [10, 20, 30]
        })
        mock_inventory.return_value = mock_inventory_instance
        
        client = VillaClient(s3_bucket="test-bucket")
        filters = {"category": "A"}
        result = client.get_products_with_inventory(branch=1000, filters=filters)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2  # Filtered to category A
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_filter_dataframe_column_not_exists(self, mock_cache, mock_inventory, mock_products):
        """Test filter_dataframe with column that doesn't exist."""
        client = VillaClient(s3_bucket="test-bucket")
        
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "price": [100, 50, 200]
        })
        
        # Filter with non-existent column
        filtered = client.filter_dataframe(df, {"nonexistent": "value"})
        assert len(filtered) == 3  # Should return all rows
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_filter_dataframe_comparison_operators(self, mock_cache, mock_inventory, mock_products):
        """Test filter_dataframe with all comparison operators."""
        client = VillaClient(s3_bucket="test-bucket")
        
        df = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "price": [100, 150, 200, 250, 300]
        })
        
        # Test gte (greater than or equal)
        filtered = client.filter_dataframe(df, {"price": {"gte": 200}})
        assert len(filtered) == 3
        
        # Test lte (less than or equal)
        filtered = client.filter_dataframe(df, {"price": {"lte": 150}})
        assert len(filtered) == 2
        
        # Test eq (equals)
        filtered = client.filter_dataframe(df, {"price": {"eq": 200}})
        assert len(filtered) == 1
        
        # Test lt (less than) - this should hit line 154
        filtered = client.filter_dataframe(df, {"price": {"lt": 200}})
        assert len(filtered) == 2
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_merge_dataframes_no_common_key(self, mock_cache, mock_inventory, mock_products):
        """Test _merge_dataframes when no common key exists."""
        client = VillaClient(s3_bucket="test-bucket")
        
        products_df = pd.DataFrame({
            "product_id": [1, 2],
            "name": ["A", "B"]
        })
        
        inventory_df = pd.DataFrame({
            "inventory_id": [1, 2],
            "stock": [10, 20]
        })
        
        # No common key - should use fallback
        merged = client._merge_dataframes(products_df, inventory_df)
        assert isinstance(merged, pd.DataFrame)
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_merge_dataframes_same_length_fallback(self, mock_cache, mock_inventory, mock_products):
        """Test _merge_dataframes fallback when same length but no common key."""
        client = VillaClient(s3_bucket="test-bucket")
        
        products_df = pd.DataFrame({
            "name": ["A", "B"],
            "price": [100, 200]
        })
        
        inventory_df = pd.DataFrame({
            "stock": [10, 20],
            "location": ["X", "Y"]
        })
        
        # Same length, no common key - should concat
        merged = client._merge_dataframes(products_df, inventory_df)
        assert isinstance(merged, pd.DataFrame)
        assert len(merged) == 2
    
    @patch('villa_ecommerce_sdk.products.ProductsService')
    @patch('villa_ecommerce_sdk.inventory.InventoryService')
    @patch('villa_ecommerce_sdk.cache.S3Cache')
    def test_merge_dataframes_different_length_fallback(self, mock_cache, mock_inventory, mock_products):
        """Test _merge_dataframes fallback when different length."""
        client = VillaClient(s3_bucket="test-bucket")
        
        products_df = pd.DataFrame({
            "name": ["A", "B", "C"],
            "price": [100, 200, 300]
        })
        
        inventory_df = pd.DataFrame({
            "stock": [10, 20],
            "location": ["X", "Y"]
        })
        
        # Different length - should return products copy
        merged = client._merge_dataframes(products_df, inventory_df)
        assert isinstance(merged, pd.DataFrame)
        assert len(merged) == 3

