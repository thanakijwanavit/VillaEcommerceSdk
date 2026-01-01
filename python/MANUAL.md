# Villa Ecommerce SDK - Complete Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Architecture Overview](#architecture-overview)
5. [Base Class Usage](#base-class-usage)
6. [Products](#products)
7. [Inventory](#inventory)
8. [Payments](#payments)
9. [Advanced Usage](#advanced-usage)
10. [Error Handling](#error-handling)
11. [Best Practices](#best-practices)
12. [Extending the SDK](#extending-the-sdk)

---

## Introduction

The Villa Ecommerce SDK is a Python library that provides a simple and powerful interface for connecting third-party applications (websites, mobile apps, etc.) to the Villa Market ecommerce engine. Villa Market is a supermarket chain that allows third parties to integrate with their platform to access product catalogs, inventory data, and payment processing.

### Key Features

- **Product Management**: Fetch product catalogs, search, and filter products
- **Inventory Tracking**: Real-time inventory data for all branches
- **Payment Processing**: Create payments, process refunds, and manage payment history
- **S3 Caching**: Automatic caching of API responses for improved performance
- **Pandas Integration**: All data returned as pandas DataFrames for easy manipulation
- **Extensible Architecture**: Base class for creating custom services

---

## Installation

### Prerequisites

- Python 3.8 or higher
- AWS account with S3 bucket for caching
- AWS credentials configured (see [AWS Setup](#aws-setup))

### Install from Source

```bash
cd python
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### AWS Setup

The SDK requires AWS credentials for S3 caching. Configure credentials using one of these methods:

1. **AWS Credentials File** (`~/.aws/credentials`):
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

2. **Environment Variables**:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=ap-southeast-1
```

3. **IAM Role** (when running on EC2/Lambda):
   - Attach IAM policy with S3 access to your role

---

## Quick Start

### Basic Usage

```python
from villa_ecommerce_sdk import VillaClient

# Initialize client (uses default bucket: villa-ecommerce-sdk-cache)
client = VillaClient()

# Or specify a custom bucket
client = VillaClient(s3_bucket="your-s3-bucket-name")

# Get products
products = client.get_product_list(branch=1000)
print(f"Found {len(products)} products")

# Get inventory
inventory = client.get_inventory(branch=1000)
print(f"Inventory items: {len(inventory)}")

# Create a payment
payment = client.create_payment(
    order_id="ORDER-123",
    amount=1500.00,
    currency="THB",
    payment_method="credit_card"
)
print(f"Payment created: {payment['paymentId']}")
```

---

## Architecture Overview

The SDK follows a service-oriented architecture:

```
VillaClient (Main Client)
├── ProductsService (extends BaseService)
├── InventoryService (extends BaseService)
└── PaymentService (extends BaseService)
```

### BaseService

All services extend `BaseService`, which provides:
- HTTP request handling (GET, POST, PUT, DELETE)
- Automatic caching integration
- Error handling
- Consistent API patterns

### Services

- **ProductsService**: Product catalog operations
- **InventoryService**: Inventory management
- **PaymentService**: Payment processing

---

## Base Class Usage

### Understanding BaseService

`BaseService` is the foundation for all SDK services. It provides common functionality for making API requests and handling caching.

### Creating a Custom Service

```python
from villa_ecommerce_sdk.base import BaseService
from typing import Dict, Any
import pandas as pd

class CustomService(BaseService):
    """Custom service example."""
    
    def get_service_name(self) -> str:
        return "CustomService"
    
    def get_custom_data(self, branch: int = 1000) -> pd.DataFrame:
        """Get custom data."""
        cache_key = f"custom/{branch}.json"
        data = self._get(
            endpoint=f"/api/custom/{branch}",
            cache_key=cache_key
        )
        
        # Process data
        if isinstance(data, dict) and 'data' in data:
            return pd.DataFrame(data['data'])
        return pd.DataFrame(data)
    
    def create_custom_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom item."""
        return self._post(
            endpoint="/api/custom/create",
            json_data=item_data
        )
```

### Using Custom Service

```python
from villa_ecommerce_sdk.cache import S3Cache
from custom_service import CustomService

# Initialize cache (using default bucket)
cache = S3Cache(bucket_name="villa-ecommerce-sdk-cache")

# Initialize custom service
custom_service = CustomService(
    base_url="https://shop.villamarket.com",
    cache=cache
)

# Use the service
data = custom_service.get_custom_data(branch=1000)
```

### BaseService Methods

#### `_get(endpoint, cache_key=None, params=None)`

Make a GET request with optional caching.

```python
data = self._get(
    endpoint="/api/products",
    cache_key="products.json",
    params={"branch": 1000}
)
```

#### `_post(endpoint, json_data=None, headers=None)`

Make a POST request.

```python
result = self._post(
    endpoint="/api/payment/create",
    json_data={"orderId": "123", "amount": 100}
)
```

#### `_put(endpoint, json_data=None, headers=None)`

Make a PUT request.

```python
result = self._put(
    endpoint="/api/product/update",
    json_data={"id": "123", "name": "New Name"}
)
```

#### `_delete(endpoint, headers=None)`

Make a DELETE request.

```python
result = self._delete(
    endpoint="/api/product/123"
)
```

---

## Products

### Get Product List

```python
# Get all products for a branch
products = client.get_product_list(branch=1000)

# Display product information
print(products.head())
print(f"Total products: {len(products)}")
print(f"Categories: {products['category'].unique()}")
```

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

### Get Products with Inventory

```python
# Get merged products and inventory
merged = client.get_products_with_inventory(branch=1000)

# With filters
filtered_merged = client.get_products_with_inventory(
    branch=1000,
    filters={
        "stock": {"gt": 0},
        "price": {"lt": 100}
    }
)
```

---

## Inventory

### Get Inventory Data

```python
# Get inventory for a branch
inventory = client.get_inventory(branch=1000)

# Check stock levels
low_stock = client.filter_dataframe(
    inventory,
    {"stock": {"lt": 10}}
)

print(f"Low stock items: {len(low_stock)}")
```

### Inventory Analysis

```python
import pandas as pd

inventory = client.get_inventory(branch=1000)

# Calculate total stock value
products = client.get_product_list(branch=1000)
merged = pd.merge(
    products,
    inventory,
    left_on='id',
    right_on='product_id',
    how='inner'
)
merged['total_value'] = merged['price'] * merged['stock']
total_value = merged['total_value'].sum()

print(f"Total inventory value: {total_value:,.2f} THB")
```

---

## Payments

### Create Payment

```python
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
print(f"Total payments: {len(all_payments)}")
print(f"Total revenue: {all_payments['amount'].sum()}")
print(f"Average payment: {all_payments['amount'].mean()}")
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
    print(f"  Fees: {method.get('fees', 'N/A')}")
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

## Advanced Usage

### Custom Headers

You can extend services to add custom headers:

```python
class CustomPaymentService(PaymentService):
    def create_payment(self, order_id, amount, **kwargs):
        headers = {
            "X-API-Key": "your-api-key",
            "X-Request-ID": str(uuid.uuid4())
        }
        return super().create_payment(
            order_id, amount,
            headers=headers,
            **kwargs
        )
```

### Batch Operations

```python
# Process multiple payments
orders = ["ORDER-1", "ORDER-2", "ORDER-3"]
payments = []

for order_id in orders:
    try:
        payment = client.create_payment(
            order_id=order_id,
            amount=1000.00
        )
        payments.append(payment)
    except Exception as e:
        print(f"Failed to create payment for {order_id}: {e}")

print(f"Successfully created {len(payments)} payments")
```

### Data Export

```python
# Export to CSV
products = client.get_product_list(branch=1000)
products.to_csv('products.csv', index=False)

# Export to Excel
inventory = client.get_inventory(branch=1000)
inventory.to_excel('inventory.xlsx', index=False)

# Export to JSON
import json
payment_history = client.get_payment_history()
payment_history.to_json('payments.json', orient='records', indent=2)
```

### Caching Strategy

```python
# Check if data is cached
is_cached = client.cache.is_cached("products/1000.json")

# Get cached data directly
cached_data = client.cache.get_cached("products/1000.json")

# Invalidate cache when needed
client.cache.invalidate("products/1000.json")

# Force fresh data fetch
client.cache.invalidate("products/1000.json")
products = client.get_product_list(branch=1000)
```

---

## Error Handling

### Common Exceptions

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient()  # Uses default bucket: villa-ecommerce-sdk-cache

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
```

---

## Best Practices

### 1. Reuse Client Instance

```python
# Good: Create once, reuse many times
client = VillaClient()  # Uses default bucket
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
# Cache is checked before making API calls
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
        # Return empty DataFrame or cached data
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

### 5. Batch Operations

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

---

## Extending the SDK

### Creating a New Service

1. **Create Service Class**:

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
```

2. **Add to Client**:

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

class CustomCache(S3Cache):
    """Custom cache with TTL support."""
    
    def get_cached(self, key: str) -> Optional[dict]:
        data = super().get_cached(key)
        if data and self._is_expired(data):
            self.invalidate(key)
            return None
        return data
    
    def _is_expired(self, data: dict) -> bool:
        # Implement TTL logic
        return False
```

---

## Complete Example: E-commerce Integration

```python
from villa_ecommerce_sdk import VillaClient
import pandas as pd

# Initialize client (uses default bucket: villa-ecommerce-sdk-cache)
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

## Troubleshooting

### Common Issues

1. **S3 Access Denied**
   - Check AWS credentials
   - Verify IAM permissions
   - Ensure bucket exists

2. **API Timeout**
   - Check network connection
   - Verify API endpoint is accessible
   - Increase timeout if needed

3. **Cache Not Working**
   - Verify S3 bucket permissions
   - Check cache key format
   - Ensure cache service is initialized

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# SDK will log all requests and responses
client = VillaClient()  # Uses default bucket
```

---

## Support and Resources

- **Documentation**: See `/docs` directory
- **API Reference**: See `/docs/api/python.md`
- **Examples**: See `/python/tests/` directory
- **Issues**: Report on GitHub

---

## License

MIT License

---

**Last Updated**: 2024

