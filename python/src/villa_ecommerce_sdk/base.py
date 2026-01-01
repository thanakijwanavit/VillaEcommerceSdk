"""Base class for Villa Ecommerce SDK services."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import requests
from villa_ecommerce_sdk.cache import S3Cache


class BaseService(ABC):
    """Base class for all Villa SDK services."""
    
    def __init__(self, base_url: str, cache: Optional[S3Cache] = None):
        """
        Initialize base service.
        
        Args:
            base_url: Base URL for Villa API
            cache: Optional S3Cache instance for caching
        """
        self.base_url = base_url.rstrip('/')
        self.cache = cache
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        cache_key: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Make HTTP request with caching support.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (relative to base_url)
            cache_key: Optional cache key for GET requests
            params: Optional query parameters
            json_data: Optional JSON body for POST/PUT requests
            headers: Optional HTTP headers
            timeout: Request timeout in seconds
            
        Returns:
            Response data as dictionary
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        # Check cache for GET requests
        if method.upper() == 'GET' and cache_key and self.cache:
            cached_data = self.cache.get_cached(cache_key)
            if cached_data is not None:
                return cached_data
        
        # Prepare request
        request_kwargs = {
            'timeout': timeout,
            'headers': headers or {}
        }
        
        if params:
            request_kwargs['params'] = params
        if json_data:
            request_kwargs['json'] = json_data
        
        try:
            # Make request
            response = requests.request(method, url, **request_kwargs)
            response.raise_for_status()
            data = response.json()
            
            # Cache GET responses
            if method.upper() == 'GET' and cache_key and self.cache:
                self.cache.set_cached(cache_key, data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to {method} {endpoint}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing response from {endpoint}: {str(e)}")
    
    def _get(self, endpoint: str, cache_key: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request.
        
        Args:
            endpoint: API endpoint
            cache_key: Optional cache key
            params: Optional query parameters
            
        Returns:
            Response data
        """
        return self._make_request('GET', endpoint, cache_key=cache_key, params=params)
    
    def _post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make POST request.
        
        Args:
            endpoint: API endpoint
            json_data: Optional JSON body
            headers: Optional HTTP headers
            
        Returns:
            Response data
        """
        return self._make_request('POST', endpoint, json_data=json_data, headers=headers)
    
    def _put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make PUT request.
        
        Args:
            endpoint: API endpoint
            json_data: Optional JSON body
            headers: Optional HTTP headers
            
        Returns:
            Response data
        """
        return self._make_request('PUT', endpoint, json_data=json_data, headers=headers)
    
    def _delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Optional HTTP headers
            
        Returns:
            Response data
        """
        return self._make_request('DELETE', endpoint, headers=headers)
    
    @abstractmethod
    def get_service_name(self) -> str:
        """
        Get service name for logging/debugging.
        
        Returns:
            Service name string
        """
        pass

