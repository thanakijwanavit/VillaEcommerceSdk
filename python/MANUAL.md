# Villa Ecommerce SDK - Python Manual

Complete guide to using the Villa Ecommerce Python SDK for integrating with Villa Market's ecommerce platform.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Core Concepts](#core-concepts)
6. [Working with Products](#working-with-products)
7. [Working with Inventory](#working-with-inventory)
8. [Payment Processing](#payment-processing)
9. [Data Filtering](#data-filtering)
10. [Caching](#caching)
11. [Advanced Usage](#advanced-usage)
12. [Error Handling](#error-handling)
13. [Best Practices](#best-practices)
14. [Extending the SDK](#extending-the-sdk)
15. [Troubleshooting](#troubleshooting)
16. [API Reference](#api-reference)

---

## Introduction

The Villa Ecommerce SDK for Python provides a simple and powerful interface for connecting third-party applications to Villa Market's ecommerce engine. Villa Market is a supermarket chain that allows third parties to integrate with their platform to access product catalogs, inventory data, and payment processing.

### Key Features

- **Product Management**: Fetch product catalogs, search, and filter products
- **Inventory Tracking**: Real-time inventory data for all branches
- **Payment Processing**: Create payments, process refunds, and manage payment history
- **S3 Caching**: Automatic caching of API responses for improved performance
- **Pandas Integration**: All data returned as pandas DataFrames for easy manipulation
- **Extensible Architecture**: Base class for creating custom services

### Requirements

- Python 3.12 or higher
- AWS account with S3 access
- AWS credentials configured

---

## Installation

### Install from PyPI

```bash
pip install villa-ecommerce-sdk
```

### Install from Source

```bash
git clone https://github.com/your-org/VillaEcommerceSdk.git
cd VillaEcommerceSdk/python
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The SDK requires:
- `pandas >= 1.5.0`
- `requests >= 2.28.0`
- `boto3 >= 1.26.0`
- `python-dateutil >= 2.8.0`

---

## Quick Start

### Basic Example

```python
from villa_ecommerce_sdk import VillaClient

# Initialize client (uses default bucket: villa-ecommerce-sdk-cache)
client = VillaClient()

# Get products for branch 1000
products = client.get_product_list(branch=1000)
print(f"Found {len(products)} products")
print(products.head())

# Get inventory
inventory = client.get_inventory(branch=1000)
print(f"Inventory items: {len(inventory)}")

# Get merged products and inventory
merged = client.get_products_with_inventory(branch=1000)
print(f"Merged data: {len(merged)} rows")
```

### Custom Configuration

```python
# Use custom S3 bucket
client = VillaClient(s3_bucket="my-custom-bucket")

# Use custom API base URL
client = VillaClient(
    s3_bucket="villa-ecommerce-sdk-cache",
    base_url="https://custom-api.example.com"
)
```

---

## Configuration

### AWS Credentials Setup

The SDK uses boto3 for S3 access. Configure your AWS credentials using one of these methods:

#### Option 1: AWS Credentials File

Create `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = ap-southeast-1
```

#### Option 2: Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=ap-southeast-1
```

#### Option 3: IAM Role (for EC2/Lambda)

Attach an IAM policy with S3 access to your role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::villa-ecommerce-sdk-cache/*",
        "arn:aws:s3:::villa-ecommerce-sdk-cache"
      ]
    }
  ]
}
```

### S3 Bucket Setup

The SDK requires an S3 bucket for caching. You can:

1. **Use the default bucket**: `villa-ecommerce-sdk-cache` (if deployed)
2. **Deploy your own bucket** using the included SAM template:

```bash
cd python
sam build
sam deploy --guided
```

3. **Use an existing bucket**: Just pass the bucket name when initializing the client

---

## Core Concepts

### Architecture

The SDK follows a service-oriented architecture:

```
VillaClient (Main Client)
├── ProductsService (extends BaseService)
├── InventoryService (extends BaseService)
└── PaymentService (extends BaseService)
```

### Data Flow

1. **Request**: Client method called (e.g., `get_product_list()`)
2. **Cache Check**: SDK checks S3 cache first
3. **API Call**: If not cached, makes API request
4. **Cache Store**: Successful responses are cached
5. **Data Processing**: Response converted to pandas DataFrame
6. **Return**: DataFrame returned to caller

### Service Pattern

All services extend `BaseService`, which provides:
- HTTP request handling (GET, POST, PUT, DELETE)
- Automatic caching integration
- Error handling
- Consistent API patterns

---

## Working with Products

### Get Product List

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient()

# Get all products for a branch
products = client.get_product_list(branch=1000)

# Display basic information
print(f"Total products: {len(products)}")
print(f"Columns: {list(products.columns)}")
print(products.head())

# Get products for different branch
products_branch_1001 = client.get_product_list(branch=1001)
```

### Product Data Structure

The product DataFrame typically contains columns like:
- `id` or `product_id`: Product identifier
- `name`: Product name
- `category`: Product category
- `price`: Product price
- `description`: Product description
- `image_url`: Product image URL
- Other product-specific fields

### Filter Products

```python
# Filter by category
electronics = client.filter_dataframe(
    products,
    {"category": "electronics"}
)

# Filter by price range
affordable = client.filter_dataframe(
    products,
    {"price": {"gte": 10, "lte": 100}}
)

# Multiple filters (AND condition)
filtered = client.filter_dataframe(
    products,
    {
        "category": "electronics",
        "price": {"gt": 50},
        "available": True
    }
)
```

### Product Analysis

```python
import pandas as pd

products = client.get_product_list(branch=1000)

# Basic statistics
if 'price' in products.columns:
    print(f"Average price: {products['price'].mean():.2f}")
    print(f"Max price: {products['price'].max():.2f}")
    print(f"Min price: {products['price'].min():.2f}")

# Category distribution
if 'category' in products.columns:
    category_counts = products['category'].value_counts()
    print("\nProducts by category:")
    print(category_counts)

# Export to CSV
products.to_csv('products.csv', index=False)

# Export to Excel
products.to_excel('products.xlsx', index=False)
```

---

## Working with Inventory

### Get Inventory Data

```python
client = VillaClient()

# Get inventory for a branch
inventory = client.get_inventory(branch=1000)

print(f"Inventory items: {len(inventory)}")
print(inventory.head())
```

### Inventory Data Structure

The inventory DataFrame typically contains:
- `product_id`: Product identifier
- `stock` or `quantity`: Available stock
- `branch`: Branch ID
- `last_updated`: Last update timestamp
- Other inventory-specific fields

### Check Stock Levels

```python
# Find low stock items
low_stock = client.filter_dataframe(
    inventory,
    {"stock": {"lt": 10}}
)

print(f"Low stock items: {len(low_stock)}")
print(low_stock[['product_id', 'stock']])

# Find out of stock items
out_of_stock = client.filter_dataframe(
    inventory,
    {"stock": {"eq": 0}}
)

# Find well-stocked items
well_stocked = client.filter_dataframe(
    inventory,
    {"stock": {"gte": 50}}
)
```

### Inventory Analysis

```python
import pandas as pd

# Get products and inventory
products = client.get_product_list(branch=1000)
inventory = client.get_inventory(branch=1000)

# Merge to calculate total inventory value
merged = pd.merge(
    products,
    inventory,
    left_on='id',
    right_on='product_id',
    how='inner'
)

# Calculate total value
if 'price' in merged.columns and 'stock' in merged.columns:
    merged['total_value'] = merged['price'] * merged['stock']
    total_value = merged['total_value'].sum()
    print(f"Total inventory value: {total_value:,.2f} THB")
```

### Get Products with Inventory

```python
# Get merged products and inventory in one call
merged = client.get_products_with_inventory(branch=1000)

# Filter for in-stock items only
in_stock = client.filter_dataframe(
    merged,
    {"stock": {"gt": 0}}
)

# Filter for affordable in-stock items
affordable_in_stock = client.get_products_with_inventory(
    branch=1000,
    filters={
        "stock": {"gt": 0},
        "price": {"lte": 100}
    }
)
```

---

## Payment Processing

### Create Payment

```python
client = VillaClient()

# Basic payment
payment = client.create_payment(
    order_id="ORDER-12345",
    amount=2500.00,
    currency="THB",
    payment_method="credit_card"
)

print(f"Payment ID: {payment['paymentId']}")
print(f"Status: {payment['status']}")
```

### Payment with Customer Info

```python
payment = client.create_payment(
    order_id="ORDER-12345",
    amount=2500.00,
    currency="THB",
    payment_method="credit_card",
    customer_info={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+66123456789"
    },
    metadata={
        "source": "website",
        "campaign": "summer_sale"
    }
)
```

### Get Payment Status

```python
# Check payment status
status = client.get_payment_status(payment_id="PAY-12345")
print(f"Payment Status: {status['status']}")
print(f"Amount: {status['amount']} {status['currency']}")
```

### Payment History

```python
# Get all payments
all_payments = client.get_payment_history()
print(f"Total payments: {len(all_payments)}")

# Filter by order
order_payments = client.get_payment_history(order_id="ORDER-12345")

# Filter by date range
recent_payments = client.get_payment_history(
    start_date="2024-01-01",
    end_date="2024-01-31",
    limit=100
)

# Filter by customer
customer_payments = client.get_payment_history(
    customer_id="CUST-12345"
)

# Analyze payment data
if len(all_payments) > 0 and 'amount' in all_payments.columns:
    print(f"Total revenue: {all_payments['amount'].sum():,.2f}")
    print(f"Average payment: {all_payments['amount'].mean():,.2f}")
    print(f"Max payment: {all_payments['amount'].max():,.2f}")
```

### Process Refund

```python
# Full refund
refund = client.process_refund(
    payment_id="PAY-12345",
    reason="Customer requested refund"
)

# Partial refund
partial_refund = client.process_refund(
    payment_id="PAY-12345",
    amount=500.00,
    reason="Partial refund for damaged item"
)

print(f"Refund ID: {refund['refundId']}")
print(f"Refund Status: {refund['status']}")
```

### Get Refund Status

```python
refund_status = client.get_refund_status(refund_id="REF-12345")
print(f"Refund Status: {refund_status['status']}")
print(f"Refund Amount: {refund_status['amount']}")
```

### Available Payment Methods

```python
# Get available payment methods for a branch
methods = client.get_available_payment_methods(branch=1000)

for method in methods:
    print(f"{method['name']}: {method['type']}")
    print(f"  Enabled: {method['enabled']}")
    if 'fees' in method:
        print(f"  Fees: {method['fees']}")
```

### Verify Payment

```python
# Verify payment matches order
verification = client.verify_payment(
    payment_id="PAY-12345",
    order_id="ORDER-12345"
)

if verification['verified']:
    print("Payment verified successfully")
else:
    print(f"Verification failed: {verification['reason']}")
```

---

## Data Filtering

The SDK provides powerful filtering capabilities for DataFrames.

### Exact Match

```python
# Filter by exact value
filters = {"category": "electronics"}
filtered = client.filter_dataframe(df, filters)
```

### Comparison Operators

```python
# Greater than
filters = {"price": {"gt": 100}}

# Less than
filters = {"price": {"lt": 50}}

# Greater than or equal
filters = {"price": {"gte": 100}}

# Less than or equal
filters = {"price": {"lte": 200}}

# Equal
filters = {"price": {"eq": 150}}

# Multiple comparisons
filters = {"price": {"gte": 10, "lte": 100}}
```

### Multiple Values (OR condition)

```python
# Match any value in list
filters = {"category": ["electronics", "food", "clothing"]}
```

### Multiple Filters (AND condition)

```python
# All conditions must match
filters = {
    "category": "electronics",
    "price": {"gt": 100},
    "in_stock": True,
    "available": True
}
```

### Complex Filtering Examples

```python
# Products between $10-$100 in electronics category
filters = {
    "category": "electronics",
    "price": {"gte": 10, "lte": 100}
}

# Low stock items in multiple categories
filters = {
    "category": ["electronics", "food"],
    "stock": {"lt": 10}
}

# Available products with price range
filters = {
    "available": True,
    "price": {"gte": 20, "lte": 500},
    "stock": {"gt": 0}
}
```

---

## Caching

The SDK automatically caches API responses in S3 to improve performance and reduce API calls.

### How Caching Works

1. **GET requests** are automatically cached
2. **POST/PUT/DELETE requests** are not cached
3. Cache is checked **before** making API calls
4. Successful responses are **automatically stored** in cache

### Cache Keys

Cache keys follow this pattern:
- Products: `villa-sdk/products/{branch}.json`
- Inventory: `villa-sdk/inventory/{branch}.json`
- Payments: `villa-sdk/payments/{payment_id}.json`

### Manual Cache Management

```python
client = VillaClient()

# Check if data is cached
is_cached = client.cache.is_cached("products/1000.json")

# Get cached data directly
cached_data = client.cache.get_cached("products/1000.json")

# Invalidate cache
client.cache.invalidate("products/1000.json")

# Force fresh data fetch
client.cache.invalidate("products/1000.json")
products = client.get_product_list(branch=1000)
```

### Cache Best Practices

```python
# Good: Let SDK handle caching automatically
products = client.get_product_list(branch=1000)  # Cached automatically

# Good: Invalidate cache when data might have changed
client.cache.invalidate("products/1000.json")
products = client.get_product_list(branch=1000)  # Fresh data

# Good: Check cache before expensive operations
if client.cache.is_cached("products/1000.json"):
    print("Using cached data")
else:
    print("Fetching fresh data")
```

### Custom Cache Prefix

```python
from villa_ecommerce_sdk.cache import S3Cache

# Create cache with custom prefix
cache = S3Cache(
    bucket_name="my-bucket",
    prefix="my-custom-prefix"
)

client = VillaClient(s3_bucket="my-bucket")
# Cache will use "my-custom-prefix" prefix
```

---

## Advanced Usage

### Batch Operations

```python
# Process multiple branches
branches = [1000, 1001, 1002]
all_products = []

for branch in branches:
    products = client.get_product_list(branch=branch)
    products['branch'] = branch
    all_products.append(products)

combined = pd.concat(all_products, ignore_index=True)
print(f"Total products across all branches: {len(combined)}")
```

### Batch Payments

```python
# Process multiple payments
orders = [
    {"order_id": "ORDER-1", "amount": 1000.00},
    {"order_id": "ORDER-2", "amount": 2000.00},
    {"order_id": "ORDER-3", "amount": 1500.00}
]

payments = []
for order in orders:
    try:
        payment = client.create_payment(
            order_id=order["order_id"],
            amount=order["amount"]
        )
        payments.append(payment)
    except Exception as e:
        print(f"Failed to create payment for {order['order_id']}: {e}")

print(f"Successfully created {len(payments)} payments")
```

### Data Export

```python
import pandas as pd
import json

# Export to CSV
products = client.get_product_list(branch=1000)
products.to_csv('products.csv', index=False)

# Export to Excel
inventory = client.get_inventory(branch=1000)
inventory.to_excel('inventory.xlsx', index=False)

# Export to JSON
payment_history = client.get_payment_history()
payment_history.to_json('payments.json', orient='records', indent=2)

# Export to Parquet (efficient for large datasets)
products.to_parquet('products.parquet', index=False)
```

### Custom Headers

You can extend services to add custom headers:

```python
from villa_ecommerce_sdk.payments import PaymentService
import uuid

class CustomPaymentService(PaymentService):
    def create_payment(self, order_id, amount, **kwargs):
        headers = {
            "X-API-Key": "your-api-key",
            "X-Request-ID": str(uuid.uuid4())
        }
        return super()._post(
            endpoint="/api/payment/create",
            json_data={
                "orderId": order_id,
                "amount": amount,
                **kwargs
            },
            headers=headers
        )
```

### Retry Logic

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# Use retry decorator
@retry_on_failure(max_retries=3, delay=2)
def get_products_with_retry(client, branch):
    return client.get_product_list(branch=branch)

products = get_products_with_retry(client, 1000)
```

---

## Error Handling

### Common Exceptions

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient()

try:
    products = client.get_product_list(branch=1000)
except Exception as e:
    if "Failed to fetch" in str(e):
        print("Network or API error")
    elif "Error processing" in str(e):
        print("Data processing error")
    else:
        print(f"Unexpected error: {e}")
```

### Payment Error Handling

```python
try:
    payment = client.create_payment(
        order_id="ORDER-123",
        amount=1000.00
    )
except Exception as e:
    print(f"Payment creation failed: {e}")
    # Handle error (retry, log, notify, etc.)
```

### Safe Data Fetching

```python
def safe_get_products(client, branch):
    try:
        return client.get_product_list(branch=branch)
    except Exception as e:
        print(f"Error fetching products: {e}")
        # Return empty DataFrame or cached data
        return pd.DataFrame()

products = safe_get_products(client, 1000)
```

### Error Recovery

```python
def get_products_with_fallback(client, branch):
    try:
        # Try to get fresh data
        return client.get_product_list(branch=branch)
    except Exception:
        # Fallback to cache
        cached = client.cache.get_cached(f"products/{branch}.json")
        if cached:
            return pd.DataFrame(cached)
        # Last resort: empty DataFrame
        return pd.DataFrame()

products = get_products_with_fallback(client, 1000)
```

---

## Best Practices

### 1. Reuse Client Instance

```python
# Good: Create once, reuse many times
client = VillaClient()
products = client.get_product_list(branch=1000)
inventory = client.get_inventory(branch=1000)
payments = client.get_payment_history()

# Bad: Creating new client for each operation
products = VillaClient().get_product_list(branch=1000)
inventory = VillaClient().get_inventory(branch=1000)
```

### 2. Use Caching Effectively

```python
# The SDK automatically caches GET requests
products = client.get_product_list(branch=1000)  # API call + cache
products = client.get_product_list(branch=1000)  # From cache

# Invalidate cache when data might have changed
client.cache.invalidate("products/1000.json")
```

### 3. Handle Errors Gracefully

```python
def safe_get_products(client, branch):
    try:
        return client.get_product_list(branch=branch)
    except Exception as e:
        print(f"Error fetching products: {e}")
        return pd.DataFrame()
```

### 4. Use Type Hints

```python
from typing import Optional, Dict, Any
import pandas as pd

def process_products(
    client: VillaClient,
    branch: int = 1000,
    filters: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    products = client.get_product_list(branch=branch)
    if filters:
        return client.filter_dataframe(products, filters)
    return products
```

### 5. Batch Operations Efficiently

```python
# Process multiple branches efficiently
branches = [1000, 1001, 1002]
all_products = []

for branch in branches:
    products = client.get_product_list(branch=branch)
    products['branch'] = branch
    all_products.append(products)

combined = pd.concat(all_products, ignore_index=True)
```

### 6. Validate Data Before Processing

```python
products = client.get_product_list(branch=1000)

# Check if required columns exist
required_columns = ['id', 'name', 'price']
missing = [col for col in required_columns if col not in products.columns]

if missing:
    print(f"Warning: Missing columns: {missing}")
else:
    # Process data safely
    total_value = products['price'].sum()
```

---

## Extending the SDK

### Creating a Custom Service

```python
from villa_ecommerce_sdk.base import BaseService
import pandas as pd
from typing import Dict, Any

class OrdersService(BaseService):
    """Service for order management."""
    
    def get_service_name(self) -> str:
        return "OrdersService"
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order by ID."""
        cache_key = f"orders/{order_id}.json"
        return self._get(
            endpoint=f"/api/orders/{order_id}",
            cache_key=cache_key
        )
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order."""
        return self._post(
            endpoint="/api/orders/create",
            json_data=order_data
        )
    
    def get_orders(self, branch: int = 1000) -> pd.DataFrame:
        """Get all orders for a branch."""
        cache_key = f"orders/{branch}.json"
        data = self._get(
            endpoint=f"/api/orders/{branch}",
            cache_key=cache_key
        )
        
        if isinstance(data, dict):
            if 'orders' in data:
                orders_list = data['orders']
            elif 'data' in data:
                orders_list = data['data']
            else:
                orders_list = [data] if not isinstance(data, list) else data
        else:
            orders_list = data if isinstance(data, list) else [data]
        
        return pd.DataFrame(orders_list)
```

### Using Custom Service

```python
from villa_ecommerce_sdk.cache import S3Cache
from orders_service import OrdersService

# Initialize cache
cache = S3Cache(bucket_name="villa-ecommerce-sdk-cache")

# Initialize custom service
orders_service = OrdersService(
    base_url="https://shop.villamarket.com",
    cache=cache
)

# Use the service
order = orders_service.get_order(order_id="ORDER-123")
orders = orders_service.get_orders(branch=1000)
```

### Adding Custom Service to Client

```python
# In client.py __init__ method
from villa_ecommerce_sdk.orders import OrdersService

self.orders_service = OrdersService(base_url=base_url, cache=self.cache)

# Add convenience methods
def get_order(self, order_id: str) -> Dict[str, Any]:
    return self.orders_service.get_order(order_id=order_id)
```

### Custom Caching Strategy

```python
from villa_ecommerce_sdk.cache import S3Cache
from typing import Optional
from datetime import datetime, timedelta

class TTLCache(S3Cache):
    """Custom cache with TTL support."""
    
    def __init__(self, bucket_name: str, prefix: str = "villa-sdk", ttl_hours: int = 24):
        super().__init__(bucket_name, prefix)
        self.ttl_hours = ttl_hours
    
    def get_cached(self, key: str) -> Optional[dict]:
        data = super().get_cached(key)
        if data and self._is_expired(data):
            self.invalidate(key)
            return None
        return data
    
    def set_cached(self, key: str, data: dict) -> None:
        # Add timestamp to data
        data['_cached_at'] = datetime.now().isoformat()
        super().set_cached(key, data)
    
    def _is_expired(self, data: dict) -> bool:
        if '_cached_at' not in data:
            return True
        
        cached_at = datetime.fromisoformat(data['_cached_at'])
        expiry = cached_at + timedelta(hours=self.ttl_hours)
        return datetime.now() > expiry
```

---

## Troubleshooting

### Common Issues

#### Issue: "No module named 'villa_ecommerce_sdk'"

**Solution:** Install the package:
```bash
pip install villa-ecommerce-sdk
```

Or install from source:
```bash
cd python
pip install -e .
```

#### Issue: "AccessDenied" when accessing S3

**Solution:** 
1. Check AWS credentials are configured correctly
2. Verify IAM permissions include S3 access
3. Ensure bucket exists and is accessible
4. Check bucket name is correct

#### Issue: "Failed to fetch product list"

**Solution:**
- Check your internet connection
- Verify the API endpoint is accessible
- Check if the branch ID is valid
- Review error message for specific details

#### Issue: Cache not working

**Solution:**
- Verify S3 bucket exists and is accessible
- Check AWS credentials are configured
- Ensure IAM permissions are correct
- Verify cache key format is correct

#### Issue: DataFrame is empty

**Solution:**
- Check API response structure
- Verify branch ID is valid
- Check if filters are too restrictive
- Review API response format

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# SDK will log all requests and responses
client = VillaClient()
```

### Verify Setup

```python
from villa_ecommerce_sdk import VillaClient
import boto3

# Test AWS credentials
try:
    s3 = boto3.client('s3')
    s3.list_buckets()
    print("✓ AWS credentials working")
except Exception as e:
    print(f"✗ AWS credentials error: {e}")

# Test SDK
try:
    client = VillaClient()
    print("✓ SDK initialized")
except Exception as e:
    print(f"✗ SDK initialization error: {e}")

# Test cache
try:
    is_cached = client.cache.is_cached("test.json")
    print("✓ Cache access working")
except Exception as e:
    print(f"✗ Cache access error: {e}")
```

---

## API Reference

### VillaClient

Main client class for interacting with Villa Market APIs.

#### `__init__(s3_bucket: Optional[str] = None, base_url: str = "https://shop.villamarket.com")`

Initialize the Villa API client.

**Parameters:**
- `s3_bucket` (str, optional): Name of the S3 bucket to use for caching. Defaults to `villa-ecommerce-sdk-cache`
- `base_url` (str, optional): Base URL for Villa API. Defaults to `https://shop.villamarket.com`

#### `get_product_list(branch: int = 1000) -> pd.DataFrame`

Get product list for a specific branch.

**Parameters:**
- `branch` (int, optional): Branch ID. Defaults to 1000

**Returns:**
- `pd.DataFrame`: DataFrame containing product data

#### `get_inventory(branch: int = 1000) -> pd.DataFrame`

Get inventory data for a specific branch.

**Parameters:**
- `branch` (int, optional): Branch ID. Defaults to 1000

**Returns:**
- `pd.DataFrame`: DataFrame containing inventory data

#### `get_products_with_inventory(branch: int = 1000, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame`

Get merged products and inventory data with optional filtering.

**Parameters:**
- `branch` (int, optional): Branch ID. Defaults to 1000
- `filters` (dict, optional): Dictionary of filters to apply

**Returns:**
- `pd.DataFrame`: Merged and filtered DataFrame

#### `filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame`

Filter a DataFrame based on provided criteria.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to filter
- `filters` (dict): Dictionary of filter criteria

**Returns:**
- `pd.DataFrame`: Filtered DataFrame

#### Payment Methods

- `create_payment(order_id, amount, currency="THB", payment_method="credit_card", ...) -> Dict[str, Any]`
- `get_payment_status(payment_id) -> Dict[str, Any]`
- `get_payment_history(order_id=None, customer_id=None, start_date=None, end_date=None, limit=100) -> pd.DataFrame`
- `process_refund(payment_id, amount=None, reason=None) -> Dict[str, Any]`
- `get_refund_status(refund_id) -> Dict[str, Any]`
- `get_available_payment_methods(branch=1000) -> list`
- `verify_payment(payment_id, order_id) -> Dict[str, Any]`

### BaseService

Base class for all SDK services.

#### Methods

- `_get(endpoint, cache_key=None, params=None) -> Dict[str, Any]`
- `_post(endpoint, json_data=None, headers=None) -> Dict[str, Any]`
- `_put(endpoint, json_data=None, headers=None) -> Dict[str, Any]`
- `_delete(endpoint, headers=None) -> Dict[str, Any]`
- `get_service_name() -> str` (abstract)

### S3Cache

S3-based cache for storing API responses.

#### Methods

- `get_cached(key) -> Optional[dict]`
- `set_cached(key, data) -> None`
- `is_cached(key) -> bool`
- `invalidate(key) -> None`

---

## Complete Example: E-commerce Integration

```python
from villa_ecommerce_sdk import VillaClient
import pandas as pd

# Initialize client
client = VillaClient()

# 1. Get available products
products = client.get_products_with_inventory(
    branch=1000,
    filters={"stock": {"gt": 0}, "price": {"lte": 500}}
)

# 2. Display products to customer
print("Available Products:")
for _, product in products.head(10).iterrows():
    print(f"{product['name']}: {product['price']} THB (Stock: {product['stock']})")

# 3. Customer selects products (simulated)
selected_items = [
    {"product_id": "123", "quantity": 2},
    {"product_id": "456", "quantity": 1}
]

# 4. Calculate total
total = 0
for item in selected_items:
    product = products[products['id'] == item['product_id']].iloc[0]
    total += product['price'] * item['quantity']

print(f"\nTotal: {total} THB")

# 5. Create payment
order_id = f"ORDER-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
payment = client.create_payment(
    order_id=order_id,
    amount=total,
    currency="THB",
    payment_method="credit_card",
    customer_info={
        "name": "John Doe",
        "email": "john@example.com"
    }
)

print(f"\nPayment Created:")
print(f"  Payment ID: {payment['paymentId']}")
print(f"  Status: {payment['status']}")

# 6. Verify payment
verification = client.verify_payment(
    payment_id=payment['paymentId'],
    order_id=order_id
)

if verification['verified']:
    print("\nPayment verified! Order confirmed.")
else:
    print(f"\nPayment verification failed: {verification['reason']}")

# 7. Get payment history
recent_payments = client.get_payment_history(limit=10)
print(f"\nRecent Payments: {len(recent_payments)}")
```

---

## Support and Resources

- **Documentation**: See `/docs` directory
- **API Reference**: See `/docs/api/python.md`
- **Examples**: See `/docs/examples/python/` directory
- **Issues**: Report on GitHub

---

## License

MIT License

---

**Last Updated**: 2024
