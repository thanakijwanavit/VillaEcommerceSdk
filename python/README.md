# Villa Ecommerce SDK for Python

A Python SDK for fetching product lists and inventory data from Villa Market APIs with S3-based caching and pandas DataFrame support.

## Installation

```bash
pip install villa-ecommerce-sdk
```

## Requirements

- Python 3.8 or higher
- AWS credentials configured (for S3 caching)
- An S3 bucket for caching API responses

## Quick Start

```python
from villa_ecommerce_sdk import VillaClient

# Initialize the client with your S3 bucket name
client = VillaClient(s3_bucket="my-bucket")

# Get product list for branch 1000 (default)
products_df = client.get_product_list(branch=1000)

# Get inventory for branch 1000
inventory_df = client.get_inventory(branch=1000)

# Get merged products and inventory
merged_df = client.get_products_with_inventory(branch=1000)

# With filters
filtered_df = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "electronics", "in_stock": True}
)
```

## Features

- **Product List Fetching**: Get product data for any Villa branch
- **Inventory Management**: Retrieve inventory data for branches
- **S3 Caching**: Automatic caching of API responses to reduce API calls
- **DataFrame Support**: All data returned as pandas DataFrames for easy manipulation
- **Data Merging**: Automatically merge product and inventory data
- **Filtering**: Built-in filtering capabilities for DataFrames

## API Reference

### VillaClient

Main client class for interacting with Villa Ecommerce API.

#### `__init__(s3_bucket: str, base_url: str = "https://shop.villamarket.com")`

Initialize the Villa API client.

**Parameters:**
- `s3_bucket` (str): Name of the S3 bucket to use for caching
- `base_url` (str): Base URL for Villa API (default: "https://shop.villamarket.com")

#### `get_product_list(branch: int = 1000) -> pd.DataFrame`

Get product list for a specific branch.

**Parameters:**
- `branch` (int): Branch ID (default: 1000)

**Returns:**
- `pd.DataFrame`: DataFrame containing product data

**Example:**
```python
products_df = client.get_product_list(branch=1000)
print(products_df.head())
```

#### `get_inventory(branch: int = 1000) -> pd.DataFrame`

Get inventory data for a specific branch.

**Parameters:**
- `branch` (int): Branch ID (default: 1000)

**Returns:**
- `pd.DataFrame`: DataFrame containing inventory data

**Example:**
```python
inventory_df = client.get_inventory(branch=1000)
print(inventory_df.head())
```

#### `get_products_with_inventory(branch: int = 1000, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame`

Get merged products and inventory data with optional filtering.

This method fetches both product and inventory data, merges them, and applies filters if provided.

**Parameters:**
- `branch` (int): Branch ID (default: 1000)
- `filters` (Optional[Dict[str, Any]]): Optional dictionary of filters to apply

**Returns:**
- `pd.DataFrame`: Merged and filtered DataFrame

**Example:**
```python
# Without filters
merged_df = client.get_products_with_inventory(branch=1000)

# With exact match filter
filtered_df = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "electronics"}
)

# With numeric comparison
filtered_df = client.get_products_with_inventory(
    branch=1000,
    filters={"price": {"gt": 100}}
)

# With multiple values (OR condition)
filtered_df = client.get_products_with_inventory(
    branch=1000,
    filters={"category": ["electronics", "food"]}
)
```

#### `filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame`

Filter a DataFrame based on provided criteria.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to filter
- `filters` (Dict[str, Any]): Dictionary where keys are column names and values are filter criteria

**Supported filter types:**
- Exact match: `{"column": "value"}`
- Boolean: `{"column": True}`
- Numeric comparison: `{"column": {"gt": 100}}`, `{"column": {"lt": 50}}`, `{"column": {"gte": 10}}`, `{"column": {"lte": 200}}`
- Multiple values: `{"column": ["value1", "value2"]}`

**Returns:**
- `pd.DataFrame`: Filtered DataFrame

**Example:**
```python
df = client.get_product_list(branch=1000)
filtered = client.filter_dataframe(df, {
    "category": "electronics",
    "price": {"gt": 100},
    "in_stock": True
})
```

## Caching

The SDK uses S3 for caching API responses. Cache keys are automatically generated based on the endpoint and branch ID:

- Products: `villa-sdk/products/{branch}.json`
- Inventory: `villa-sdk/inventory/{branch}.json`

The cache is checked before making API calls. If cached data exists, it's returned immediately. Otherwise, the API is called and the response is cached for future use.

### Cache Configuration

The cache uses the S3 bucket specified when initializing `VillaClient`. Make sure your AWS credentials are configured (via environment variables, IAM role, or AWS credentials file).

## Error Handling

The SDK handles errors gracefully:

- If caching fails, the SDK falls back to API calls
- API errors raise exceptions with descriptive messages
- Invalid filters are silently ignored (column doesn't exist)

## Examples

### Basic Usage

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="my-villa-cache-bucket")

# Get products
products = client.get_product_list(branch=1000)

# Get inventory
inventory = client.get_inventory(branch=1000)

# Merge and filter
merged = client.get_products_with_inventory(
    branch=1000,
    filters={"in_stock": True}
)
```

### Working with DataFrames

```python
import pandas as pd
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="my-bucket")
df = client.get_products_with_inventory(branch=1000)

# Use pandas operations
df_sorted = df.sort_values('price', ascending=False)
df_grouped = df.groupby('category').agg({'price': 'mean'})

# Export to CSV
df.to_csv('products.csv', index=False)
```

### Multiple Branches

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="my-bucket")

branches = [1000, 1001, 1002]
all_products = []

for branch in branches:
    products = client.get_product_list(branch=branch)
    products['branch'] = branch
    all_products.append(products)

combined = pd.concat(all_products, ignore_index=True)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

