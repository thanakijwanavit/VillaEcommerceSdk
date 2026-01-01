"""S3-based caching implementation for Villa Ecommerce SDK."""

import json
import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


class S3Cache:
    """S3-based cache for storing API responses."""
    
    def __init__(self, bucket_name: str, prefix: str = "villa-sdk"):
        """
        Initialize S3 cache.
        
        Args:
            bucket_name: Name of the S3 bucket to use for caching
            prefix: Prefix for cache keys (default: "villa-sdk")
        """
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.s3_client = boto3.client('s3')
    
    def _get_cache_key(self, key: str) -> str:
        """Generate full cache key with prefix."""
        return f"{self.prefix}/{key}"
    
    def get_cached(self, key: str) -> Optional[dict]:
        """
        Retrieve cached data from S3.
        
        Args:
            key: Cache key (e.g., "products/1000.json")
            
        Returns:
            Cached data as dict, or None if not found or error occurs
        """
        cache_key = self._get_cache_key(key)
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=cache_key
            )
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            # Log error but don't fail - return None to allow fallback
            return None
        except Exception:
            # Any other error - return None to allow fallback
            return None
    
    def set_cached(self, key: str, data: dict) -> None:
        """
        Store data in S3 cache.
        
        Args:
            key: Cache key (e.g., "products/1000.json")
            data: Data to cache (will be JSON serialized)
        """
        cache_key = self._get_cache_key(key)
        try:
            json_data = json.dumps(data, default=str)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=cache_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json'
            )
        except Exception:
            # Log error but don't fail - caching is optional
            pass
    
    def is_cached(self, key: str) -> bool:
        """
        Check if a key exists in cache.
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists, False otherwise
        """
        cache_key = self._get_cache_key(key)
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=cache_key
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            return False
        except Exception:
            return False
    
    def invalidate(self, key: str) -> None:
        """
        Remove cached data from S3.
        
        Args:
            key: Cache key to invalidate
        """
        cache_key = self._get_cache_key(key)
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=cache_key
            )
        except Exception:
            # Log error but don't fail
            pass

