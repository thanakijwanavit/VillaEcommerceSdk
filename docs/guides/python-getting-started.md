# Getting Started with Python SDK

A step-by-step guide to getting started with the Villa Ecommerce Python SDK.

## Prerequisites

- Python 3.8 or higher
- AWS account with S3 access
- AWS credentials configured

## Installation

### Using pip

```bash
pip install villa-ecommerce-sdk
```

### From Source

```bash
git clone https://github.com/your-org/VillaEcommerceSdk.git
cd VillaEcommerceSdk/python
pip install .
```

## AWS Setup

### 1. Deploy S3 Cache Bucket

The SDK requires an S3 bucket for caching. Deploy using the included SAM template:

```bash
cd python
sam build
sam deploy --guided
```

This will create:
- S3 bucket: `villa-ecommerce-sdk-cache`
- IAM policy: `VillaSDKCacheAccessPolicy`

### 2. Configure AWS Credentials

Choose one of these methods:

**Option A: AWS Credentials File**
```bash
aws configure
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=ap-southeast-1
```

**Option C: IAM Role** (for EC2/Lambda)
Attach the `VillaSDKCacheAccessPolicy` to your IAM role.

### 3. Attach IAM Policy

If using IAM users/roles, attach the policy:

```bash
# For IAM user
aws iam attach-user-policy \
  --user-name YOUR_USER \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/VillaSDKCacheAccessPolicy

# For IAM role
aws iam attach-role-policy \
  --role-name YOUR_ROLE \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/VillaSDKCacheAccessPolicy
```

## Basic Usage

### 1. Import the SDK

```python
from villa_ecommerce_sdk import VillaClient
```

### 2. Initialize Client

```python
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
```

### 3. Fetch Data

```python
# Get products
products = client.get_product_list(branch=1000)
print(products.head())

# Get inventory
inventory = client.get_inventory(branch=1000)
print(inventory.head())
```

## Common Use Cases

### Use Case 1: Get All Products

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products = client.get_product_list(branch=1000)

print(f"Total products: {len(products)}")
print(products.head())
```

### Use Case 2: Filter Products by Category

```python
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products = client.get_product_list(branch=1000)

# Filter electronics
electronics = client.filter_dataframe(
    products,
    {"category": "electronics"}
)

print(f"Electronics: {len(electronics)}")
```

### Use Case 3: Get Products with Inventory

```python
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")

# Get merged data
merged = client.get_products_with_inventory(branch=1000)

# Filter for in-stock items
in_stock = client.filter_dataframe(
    merged,
    {"stock": {"gt": 0}}
)

print(f"In-stock items: {len(in_stock)}")
```

### Use Case 4: Export to CSV

```python
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products = client.get_product_list(branch=1000)

# Export to CSV
products.to_csv('products.csv', index=False)
print("Exported to products.csv")
```

## Advanced Examples

### Example: Price Analysis

```python
import pandas as pd
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products = client.get_product_list(branch=1000)

# Calculate statistics
if 'price' in products.columns:
    print(f"Average price: {products['price'].mean():.2f}")
    print(f"Max price: {products['price'].max():.2f}")
    print(f"Min price: {products['price'].min():.2f}")
    
    # Price distribution
    print("\nPrice distribution:")
    print(products['price'].describe())
```

### Example: Category Analysis

```python
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products = client.get_product_list(branch=1000)

if 'category' in products.columns:
    # Count by category
    category_counts = products['category'].value_counts()
    print("Products by category:")
    print(category_counts)
```

### Example: Low Stock Alert

```python
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")

# Get products with inventory
merged = client.get_products_with_inventory(branch=1000)

# Find low stock items
low_stock = client.filter_dataframe(
    merged,
    {"stock": {"lt": 10}}
)

if len(low_stock) > 0:
    print(f"Alert: {len(low_stock)} items are low on stock")
    print(low_stock[['name', 'stock']])
```

## Troubleshooting

### Issue: "No module named 'villa_ecommerce_sdk'"

**Solution:** Install the package:
```bash
pip install villa-ecommerce-sdk
```

### Issue: "AccessDenied" when accessing S3

**Solution:** Ensure your AWS credentials have the `VillaSDKCacheAccessPolicy` attached.

### Issue: "Failed to fetch product list"

**Solution:** 
- Check your internet connection
- Verify the API endpoint is accessible
- Check if the branch ID is valid

### Issue: Cache not working

**Solution:**
- Verify S3 bucket exists and is accessible
- Check AWS credentials are configured
- Ensure IAM permissions are correct

## Next Steps

- Read the [API Reference](../api/python.md)
- Check out [Examples](../examples/python/)
- Review [Best Practices](../guides/python-best-practices.md)

