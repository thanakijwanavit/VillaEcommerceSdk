# Villa Ecommerce SDK for Python

A Python SDK for fetching product lists and inventory data from Villa Market APIs with S3-based caching.

## Installation

```bash
pip install villa-ecommerce-sdk
```

## Quick Start

```python
from villa_ecommerce_sdk import VillaClient

# Initialize client with S3 bucket for caching
client = VillaClient(s3_bucket="your-s3-bucket-name")

# Get product list for branch 1000 (default)
products = client.get_product_list(branch=1000)
print(products.head())

# Get inventory for branch 1000
inventory = client.get_inventory(branch=1000)
print(inventory.head())

# Get merged products and inventory with filtering
filtered_data = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "electronics", "price": {"gt": 100}}
)
print(filtered_data.head())
```

## Features

- **Product List Fetching**: Retrieve product data from Villa Market API
- **Inventory Management**: Get inventory data for specific branches
- **Data Merging**: Automatically merge product and inventory data
- **Advanced Filtering**: Filter data using various criteria (exact match, comparison operators, lists)
- **S3 Caching**: Automatic caching of API responses in S3 for improved performance
- **Pandas Integration**: All data returned as pandas DataFrames for easy manipulation

## Requirements

- Python 3.8+
- pandas >= 1.5.0
- requests >= 2.28.0
- boto3 >= 1.26.0

## Configuration

### AWS Credentials

The SDK uses boto3 for S3 access. Configure your AWS credentials using one of these methods:

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
   - Attach the `VillaSDKCacheAccessPolicy` IAM policy to your role

### S3 Bucket Setup

The SDK requires an S3 bucket for caching. You can deploy the infrastructure using the included SAM template:

```bash
cd python
sam build
sam deploy --guided
```

Or use the deployed bucket: `villa-ecommerce-sdk-cache`

## API Reference

### VillaClient

Main client class for interacting with Villa Market APIs.

#### `__init__(s3_bucket: str, base_url: str = "https://shop.villamarket.com")`

Initialize the Villa API client.

**Parameters:**
- `s3_bucket` (str): Name of the S3 bucket to use for caching
- `base_url` (str, optional): Base URL for Villa API. Defaults to `https://shop.villamarket.com`

**Example:**
```python
client = VillaClient(s3_bucket="my-cache-bucket")
```

#### `get_product_list(branch: int = 1000) -> pd.DataFrame`

Get product list for a specific branch.

**Parameters:**
- `branch` (int, optional): Branch ID. Defaults to 1000

**Returns:**
- `pd.DataFrame`: DataFrame containing product data

**Example:**
```python
products = client.get_product_list(branch=1000)
```

#### `get_inventory(branch: int = 1000) -> pd.DataFrame`

Get inventory data for a specific branch.

**Parameters:**
- `branch` (int, optional): Branch ID. Defaults to 1000

**Returns:**
- `pd.DataFrame`: DataFrame containing inventory data

**Example:**
```python
inventory = client.get_inventory(branch=1000)
```

#### `get_products_with_inventory(branch: int = 1000, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame`

Get merged products and inventory data with optional filtering.

**Parameters:**
- `branch` (int, optional): Branch ID. Defaults to 1000
- `filters` (dict, optional): Dictionary of filters to apply. See Filtering section below.

**Returns:**
- `pd.DataFrame`: Merged and filtered DataFrame

**Example:**
```python
# Without filters
data = client.get_products_with_inventory(branch=1000)

# With filters
filtered = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "electronics", "price": {"gt": 100}}
)
```

#### `filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame`

Filter a DataFrame based on provided criteria.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to filter
- `filters` (dict): Dictionary of filter criteria. See Filtering section below.

**Returns:**
- `pd.DataFrame`: Filtered DataFrame

**Example:**
```python
filtered = client.filter_dataframe(df, {"category": "electronics"})
```

## Filtering

The SDK supports various filtering options:

### Exact Match
```python
filters = {"category": "electronics"}
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
```

### Multiple Values (OR condition)
```python
filters = {"category": ["electronics", "food", "clothing"]}
```

### Multiple Filters (AND condition)
```python
filters = {
    "category": "electronics",
    "price": {"gt": 100},
    "in_stock": True
}
```

## Caching

The SDK automatically caches API responses in S3 to improve performance and reduce API calls.

### Cache Keys

- Products: `villa-sdk/products/{branch}.json`
- Inventory: `villa-sdk/inventory/{branch}.json`

### Cache Behavior

- Cache is checked first before making API calls
- Successful API responses are automatically cached
- Cache is stored in JSON format in S3
- Cache keys use the prefix `villa-sdk/` by default

### Manual Cache Management

```python
# Check if data is cached
is_cached = client.cache.is_cached("products/1000.json")

# Get cached data directly
cached_data = client.cache.get_cached("products/1000.json")

# Invalidate cache
client.cache.invalidate("products/1000.json")
```

## Examples

### Basic Usage

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")

# Get products
products = client.get_product_list(branch=1000)
print(f"Found {len(products)} products")

# Get inventory
inventory = client.get_inventory(branch=1000)
print(f"Found {len(inventory)} inventory items")
```

### Filtering Products

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

# Multiple filters
filtered = client.filter_dataframe(
    products,
    {
        "category": "electronics",
        "price": {"gt": 50},
        "available": True
    }
)
```

### Merging Products and Inventory

```python
# Get merged data
merged = client.get_products_with_inventory(branch=1000)

# Get merged data with filters
filtered_merged = client.get_products_with_inventory(
    branch=1000,
    filters={
        "stock": {"gt": 0},
        "price": {"lt": 100}
    }
)
```

### Working with DataFrames

```python
import pandas as pd

# Get data
products = client.get_product_list(branch=1000)

# Use pandas operations
total_value = products['price'].sum()
average_price = products['price'].mean()
category_counts = products['category'].value_counts()

# Export to CSV
products.to_csv('products.csv', index=False)

# Export to Excel
products.to_excel('products.xlsx', index=False)
```

## Error Handling

The SDK handles errors gracefully:

- **API Errors**: Raises exceptions with descriptive messages
- **Cache Errors**: Falls back to API calls if cache operations fail
- **Network Errors**: Provides clear error messages

```python
try:
    products = client.get_product_list(branch=1000)
except Exception as e:
    print(f"Error fetching products: {e}")
```

## Testing

Run the test suite:

```bash
cd python
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=villa_ecommerce_sdk --cov-report=html
```

## Infrastructure Deployment

The SDK includes a SAM template for deploying the S3 cache bucket:

```bash
cd python
sam build
sam deploy --guided
```

This creates:
- S3 bucket for caching
- IAM managed policy for bucket access
- Lifecycle rules for cache cleanup

See `template.yaml` for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
