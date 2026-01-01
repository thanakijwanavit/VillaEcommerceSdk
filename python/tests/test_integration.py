"""Integration tests for Villa Ecommerce SDK using deployed infrastructure."""

import pytest
import json
import boto3
from botocore.exceptions import ClientError
from villa_ecommerce_sdk import VillaClient
from villa_ecommerce_sdk.cache import S3Cache


# Use the deployed bucket name
DEPLOYED_BUCKET = "villa-ecommerce-sdk-cache"
DEPLOYED_REGION = "ap-southeast-1"


@pytest.fixture
def s3_client():
    """Create S3 client for cleanup operations."""
    return boto3.client('s3', region_name=DEPLOYED_REGION)


@pytest.fixture
def cache():
    """Create S3Cache instance with deployed bucket."""
    return S3Cache(bucket_name=DEPLOYED_BUCKET)


@pytest.fixture
def client():
    """Create VillaClient instance with deployed bucket."""
    return VillaClient(s3_bucket=DEPLOYED_BUCKET)


@pytest.fixture(autouse=True)
def cleanup_test_files(s3_client):
    """Clean up test files after each test."""
    yield
    # Clean up any test files
    try:
        response = s3_client.list_objects_v2(
            Bucket=DEPLOYED_BUCKET,
            Prefix='villa-sdk/test/'
        )
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(
                    Bucket=DEPLOYED_BUCKET,
                    Key=obj['Key']
                )
    except Exception:
        pass


class TestS3CacheIntegration:
    """Integration tests for S3Cache with deployed bucket."""
    
    def test_cache_initialization(self, cache):
        """Test that cache initializes correctly."""
        assert cache.bucket_name == DEPLOYED_BUCKET
        assert cache.prefix == "villa-sdk"
        assert cache.s3_client is not None
    
    def test_cache_set_and_get(self, cache):
        """Test setting and getting cached data."""
        test_key = "test/integration-test.json"
        test_data = {
            "test": "integration",
            "timestamp": "2026-01-01",
            "data": {"key": "value", "number": 123}
        }
        
        # Set cache
        cache.set_cached(test_key, test_data)
        
        # Verify it was written
        assert cache.is_cached(test_key) is True
        
        # Get cache
        retrieved = cache.get_cached(test_key)
        assert retrieved is not None
        assert retrieved["test"] == "integration"
        assert retrieved["data"]["key"] == "value"
        assert retrieved["data"]["number"] == 123
    
    def test_cache_is_cached(self, cache):
        """Test is_cached method."""
        test_key = "test/is-cached-test.json"
        
        # Should not exist initially
        assert cache.is_cached(test_key) is False
        
        # Create it
        cache.set_cached(test_key, {"test": "data"})
        
        # Should exist now
        assert cache.is_cached(test_key) is True
    
    def test_cache_get_nonexistent(self, cache):
        """Test getting non-existent cache key."""
        result = cache.get_cached("test/nonexistent-key.json")
        assert result is None
    
    def test_cache_invalidate(self, cache):
        """Test cache invalidation."""
        test_key = "test/invalidate-test.json"
        test_data = {"test": "invalidate"}
        
        # Set cache
        cache.set_cached(test_key, test_data)
        assert cache.is_cached(test_key) is True
        
        # Invalidate
        cache.invalidate(test_key)
        
        # Should not exist anymore
        assert cache.is_cached(test_key) is False
        assert cache.get_cached(test_key) is None
    
    def test_cache_with_complex_data(self, cache):
        """Test caching complex nested data structures."""
        test_key = "test/complex-data.json"
        complex_data = {
            "products": [
                {"id": 1, "name": "Product 1", "price": 100.50},
                {"id": 2, "name": "Product 2", "price": 200.75}
            ],
            "metadata": {
                "total": 2,
                "timestamp": "2026-01-01T10:00:00Z"
            }
        }
        
        cache.set_cached(test_key, complex_data)
        retrieved = cache.get_cached(test_key)
        
        assert retrieved is not None
        assert len(retrieved["products"]) == 2
        assert retrieved["products"][0]["id"] == 1
        assert retrieved["products"][0]["price"] == 100.50
        assert retrieved["metadata"]["total"] == 2


class TestVillaClientIntegration:
    """Integration tests for VillaClient with deployed infrastructure."""
    
    def test_client_initialization(self, client):
        """Test VillaClient initialization."""
        assert client.s3_bucket == DEPLOYED_BUCKET
        assert client.base_url == "https://shop.villamarket.com"
        assert client.cache is not None
        assert client.cache.bucket_name == DEPLOYED_BUCKET
    
    def test_client_cache_access(self, client):
        """Test that client can access cache."""
        test_key = "test/client-cache-test.json"
        test_data = {"client": "test", "value": 42}
        
        # Use client's cache
        client.cache.set_cached(test_key, test_data)
        
        # Verify
        assert client.cache.is_cached(test_key) is True
        retrieved = client.cache.get_cached(test_key)
        assert retrieved["value"] == 42
    
    def test_client_custom_base_url(self):
        """Test VillaClient with custom base URL."""
        custom_url = "https://custom.villamarket.com"
        client = VillaClient(s3_bucket=DEPLOYED_BUCKET, base_url=custom_url)
        assert client.base_url == custom_url


class TestS3BucketAccess:
    """Test direct S3 bucket access and permissions."""
    
    def test_bucket_exists(self, s3_client):
        """Test that bucket exists and is accessible."""
        try:
            s3_client.head_bucket(Bucket=DEPLOYED_BUCKET)
            assert True
        except ClientError:
            pytest.fail("Bucket does not exist or is not accessible")
    
    def test_bucket_write_permission(self, s3_client):
        """Test write permission to bucket."""
        test_key = "villa-sdk/test/write-permission-test.txt"
        test_content = b"test content"
        
        try:
            s3_client.put_object(
                Bucket=DEPLOYED_BUCKET,
                Key=test_key,
                Body=test_content
            )
            assert True
        except ClientError as e:
            pytest.fail(f"Write permission failed: {e}")
    
    def test_bucket_read_permission(self, s3_client):
        """Test read permission from bucket."""
        test_key = "villa-sdk/test/read-permission-test.txt"
        test_content = b"test read content"
        
        # Write first
        s3_client.put_object(
            Bucket=DEPLOYED_BUCKET,
            Key=test_key,
            Body=test_content
        )
        
        # Read
        try:
            response = s3_client.get_object(
                Bucket=DEPLOYED_BUCKET,
                Key=test_key
            )
            content = response['Body'].read()
            assert content == test_content
        except ClientError as e:
            pytest.fail(f"Read permission failed: {e}")
    
    def test_bucket_list_permission(self, s3_client):
        """Test list permission for bucket."""
        try:
            response = s3_client.list_objects_v2(
                Bucket=DEPLOYED_BUCKET,
                Prefix='villa-sdk/test/',
                MaxKeys=10
            )
            # Should not raise exception
            assert 'Contents' in response or 'KeyCount' in response
        except ClientError as e:
            pytest.fail(f"List permission failed: {e}")
    
    def test_bucket_delete_permission(self, s3_client):
        """Test delete permission for bucket."""
        test_key = "villa-sdk/test/delete-permission-test.txt"
        
        # Write first
        s3_client.put_object(
            Bucket=DEPLOYED_BUCKET,
            Key=test_key,
            Body=b"test delete"
        )
        
        # Delete
        try:
            s3_client.delete_object(
                Bucket=DEPLOYED_BUCKET,
                Key=test_key
            )
            assert True
        except ClientError as e:
            pytest.fail(f"Delete permission failed: {e}")

