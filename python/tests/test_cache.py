"""Tests for S3 cache module."""

import pytest
from unittest.mock import Mock, patch
from villa_ecommerce_sdk.cache import S3Cache


class TestS3Cache:
    """Test cases for S3Cache."""
    
    def test_init(self):
        """Test S3Cache initialization."""
        cache = S3Cache(bucket_name="test-bucket", prefix="test-prefix")
        assert cache.bucket_name == "test-bucket"
        assert cache.prefix == "test-prefix"
    
    def test_get_cache_key(self):
        """Test cache key generation."""
        cache = S3Cache(bucket_name="test-bucket")
        key = cache._get_cache_key("products/1000.json")
        assert key == "villa-sdk/products/1000.json"
    
    @patch('villa_ecommerce_sdk.cache.boto3.client')
    def test_get_cached_success(self, mock_boto3):
        """Test successful cache retrieval."""
        mock_s3 = Mock()
        mock_boto3.return_value = mock_s3
        
        mock_response = {
            'Body': Mock()
        }
        mock_response['Body'].read.return_value = b'{"test": "data"}'
        mock_s3.get_object.return_value = mock_response
        
        cache = S3Cache(bucket_name="test-bucket")
        result = cache.get_cached("test-key")
        
        assert result == {"test": "data"}
        mock_s3.get_object.assert_called_once()
    
    @patch('villa_ecommerce_sdk.cache.boto3.client')
    def test_get_cached_not_found(self, mock_boto3):
        """Test cache retrieval when key doesn't exist."""
        mock_s3 = Mock()
        mock_boto3.return_value = mock_s3
        
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Code': 'NoSuchKey'}}
        mock_s3.get_object.side_effect = ClientError(error_response, 'GetObject')
        
        cache = S3Cache(bucket_name="test-bucket")
        result = cache.get_cached("test-key")
        
        assert result is None
    
    @patch('villa_ecommerce_sdk.cache.boto3.client')
    def test_set_cached(self, mock_boto3):
        """Test setting cache."""
        mock_s3 = Mock()
        mock_boto3.return_value = mock_s3
        
        cache = S3Cache(bucket_name="test-bucket")
        cache.set_cached("test-key", {"test": "data"})
        
        mock_s3.put_object.assert_called_once()
        call_args = mock_s3.put_object.call_args
        assert call_args[1]['Bucket'] == "test-bucket"
        assert call_args[1]['Key'] == "villa-sdk/test-key"
    
    @patch('villa_ecommerce_sdk.cache.boto3.client')
    def test_is_cached_true(self, mock_boto3):
        """Test checking if key exists in cache."""
        mock_s3 = Mock()
        mock_boto3.return_value = mock_s3
        
        cache = S3Cache(bucket_name="test-bucket")
        result = cache.is_cached("test-key")
        
        assert result is True
        mock_s3.head_object.assert_called_once()
    
    @patch('villa_ecommerce_sdk.cache.boto3.client')
    def test_is_cached_false(self, mock_boto3):
        """Test checking if key doesn't exist in cache."""
        mock_s3 = Mock()
        mock_boto3.return_value = mock_s3
        
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Code': '404'}}
        mock_s3.head_object.side_effect = ClientError(error_response, 'HeadObject')
        
        cache = S3Cache(bucket_name="test-bucket")
        result = cache.is_cached("test-key")
        
        assert result is False

