# Villa Ecommerce SDK - Quick Start Guide

## Installation

```bash
pip install -e .
```

## Basic Setup

```python
from villa_ecommerce_sdk import VillaClient

# Initialize (uses default bucket: villa-ecommerce-sdk-cache)
client = VillaClient()

# Or specify a custom bucket
client = VillaClient(s3_bucket="your-s3-bucket-name")
```

## Common Use Cases

### 1. Get Products

```python
# Get all products for a branch
products = client.get_product_list(branch=1000)
print(products.head())
```

### 2. Get Inventory

```python
# Get inventory data
inventory = client.get_inventory(branch=1000)
print(inventory.head())
```

### 3. Get Products with Inventory

```python
# Get merged products and inventory
merged = client.get_products_with_inventory(branch=1000)

# With filters
filtered = client.get_products_with_inventory(
    branch=1000,
    filters={"stock": {"gt": 0}, "price": {"lt": 100}}
)
```

### 4. Create Payment

```python
# Create a payment
payment = client.create_payment(
    order_id="ORDER-123",
    amount=1500.00,
    currency="THB",
    payment_method="credit_card"
)
print(f"Payment ID: {payment['paymentId']}")
```

### 5. Check Payment Status

```python
status = client.get_payment_status(payment_id="PAY-123")
print(f"Status: {status['status']}")
```

### 6. Get Payment History

```python
# Get all payments
payments = client.get_payment_history()

# Filter by date
recent = client.get_payment_history(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### 7. Process Refund

```python
# Full refund
refund = client.process_refund(
    payment_id="PAY-123",
    reason="Customer requested"
)

# Partial refund
partial = client.process_refund(
    payment_id="PAY-123",
    amount=500.00,
    reason="Damaged item"
)
```

## Filtering Examples

```python
# Exact match
filtered = client.filter_dataframe(
    products,
    {"category": "electronics"}
)

# Comparison operators
filtered = client.filter_dataframe(
    products,
    {"price": {"gt": 100}}
)

# Multiple filters (AND)
filtered = client.filter_dataframe(
    products,
    {
        "category": "electronics",
        "price": {"gt": 50},
        "available": True
    }
)

# Multiple values (OR)
filtered = client.filter_dataframe(
    products,
    {"category": ["electronics", "food", "clothing"]}
)
```

## Complete E-commerce Flow

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="your-bucket")

# 1. Show available products
products = client.get_products_with_inventory(
    branch=1000,
    filters={"stock": {"gt": 0}}
)

# 2. Customer selects items (example)
order_total = 2500.00
order_id = "ORDER-12345"

# 3. Create payment
payment = client.create_payment(
    order_id=order_id,
    amount=order_total,
    currency="THB",
    payment_method="credit_card",
    customer_info={
        "name": "John Doe",
        "email": "john@example.com"
    }
)

# 4. Verify payment
verification = client.verify_payment(
    payment_id=payment['paymentId'],
    order_id=order_id
)

if verification['verified']:
    print("Order confirmed!")
```

## Extending with Base Class

```python
from villa_ecommerce_sdk.base import BaseService
import pandas as pd

class CustomService(BaseService):
    def get_service_name(self) -> str:
        return "CustomService"
    
    def get_data(self, branch: int = 1000) -> pd.DataFrame:
        cache_key = f"custom/{branch}.json"
        data = self._get(
            endpoint=f"/api/custom/{branch}",
            cache_key=cache_key
        )
        return pd.DataFrame(data.get('data', []))
```

## Error Handling

```python
try:
    products = client.get_product_list(branch=1000)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

## Cache Management

```python
# Check if cached
is_cached = client.cache.is_cached("products/1000.json")

# Invalidate cache
client.cache.invalidate("products/1000.json")

# Get cached data directly
cached = client.cache.get_cached("products/1000.json")
```

## Next Steps

- Read the [Complete Manual](MANUAL.md) for detailed documentation
- Check [API Reference](docs/api/python.md) for all available methods
- See [Examples](tests/) for more use cases

