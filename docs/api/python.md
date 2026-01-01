# Python SDK API Reference

Complete API reference for the Villa Ecommerce Python SDK.

## VillaClient

Main client class for interacting with Villa Market APIs.

### Constructor

```python
VillaClient(s3_bucket: str, base_url: str = "https://shop.villamarket.com")
```

**Parameters:**
- `s3_bucket` (str): Name of the S3 bucket to use for caching. Required.
- `base_url` (str): Base URL for Villa API. Defaults to `"https://shop.villamarket.com"`.

**Example:**
```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="my-cache-bucket")
client = VillaClient(s3_bucket="my-cache-bucket", base_url="https://custom.api.com")
```

### Methods

#### `get_product_list(branch: int = 1000) -> pd.DataFrame`

Retrieves the product list for a specific branch.

**Parameters:**
- `branch` (int): Branch ID. Defaults to `1000`.

**Returns:**
- `pd.DataFrame`: DataFrame containing product data with columns from the API response.

**Raises:**
- `Exception`: If the API request fails or data processing fails.

**Example:**
```python
products = client.get_product_list(branch=1000)
print(products.head())
print(f"Total products: {len(products)}")
```

**Behavior:**
- Checks S3 cache first
- If cached, returns cached data
- If not cached, fetches from API and caches the response
- Returns data as pandas DataFrame

#### `get_inventory(branch: int = 1000) -> pd.DataFrame`

Retrieves inventory data for a specific branch.

**Parameters:**
- `branch` (int): Branch ID. Defaults to `1000`.

**Returns:**
- `pd.DataFrame`: DataFrame containing inventory data.

**Raises:**
- `Exception`: If the API request fails or data processing fails.

**Example:**
```python
inventory = client.get_inventory(branch=1000)
print(inventory.head())
```

**Behavior:**
- Checks S3 cache first
- If cached, returns cached data
- If not cached, fetches from API and caches the response
- Returns data as pandas DataFrame

#### `get_products_with_inventory(branch: int = 1000, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame`

Gets merged products and inventory data with optional filtering.

**Parameters:**
- `branch` (int): Branch ID. Defaults to `1000`.
- `filters` (dict, optional): Dictionary of filters to apply. See [Filtering](#filtering) section.

**Returns:**
- `pd.DataFrame`: Merged DataFrame containing both product and inventory data, optionally filtered.

**Example:**
```python
# Without filters
merged = client.get_products_with_inventory(branch=1000)

# With filters
filtered = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "electronics", "stock": {"gt": 0}}
)
```

**Behavior:**
1. Fetches product list
2. Fetches inventory data
3. Merges dataframes on common keys (product_id, id, sku, etc.)
4. Applies filters if provided
5. Returns merged and filtered DataFrame

#### `filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame`

Filters a DataFrame based on provided criteria.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to filter.
- `filters` (dict): Dictionary of filter criteria. See [Filtering](#filtering) section.

**Returns:**
- `pd.DataFrame`: Filtered DataFrame.

**Example:**
```python
filtered = client.filter_dataframe(
    products,
    {"category": "electronics", "price": {"gt": 100}}
)
```

## Filtering

The SDK supports various filtering options:

### Filter Types

#### Exact Match
```python
filters = {"category": "electronics"}
```

#### Comparison Operators
```python
# Greater than
{"price": {"gt": 100}}

# Less than
{"price": {"lt": 50}}

# Greater than or equal
{"price": {"gte": 100}}

# Less than or equal
{"price": {"lte": 200}}

# Equal
{"price": {"eq": 150}}
```

#### Multiple Values (OR)
```python
filters = {"category": ["electronics", "food", "clothing"]}
```

#### Multiple Filters (AND)
```python
filters = {
    "category": "electronics",
    "price": {"gt": 100},
    "in_stock": True
}
```

### Filter Behavior

- Filters are applied sequentially (AND logic)
- Non-existent columns are ignored
- Comparison operators work with numeric and date columns
- List filters use `isin()` for OR logic

## S3Cache

Low-level cache interface (accessed via `client.cache`).

### Methods

#### `get_cached(key: str) -> Optional[dict]`

Retrieves cached data from S3.

**Parameters:**
- `key` (str): Cache key (e.g., `"products/1000.json"`).

**Returns:**
- `dict` or `None`: Cached data as dictionary, or `None` if not found.

**Example:**
```python
cached = client.cache.get_cached("products/1000.json")
```

#### `set_cached(key: str, data: dict) -> None`

Stores data in S3 cache.

**Parameters:**
- `key` (str): Cache key.
- `data` (dict): Data to cache (will be JSON serialized).

**Example:**
```python
client.cache.set_cached("products/1000.json", {"products": [...]})
```

#### `is_cached(key: str) -> bool`

Checks if a key exists in cache.

**Parameters:**
- `key` (str): Cache key to check.

**Returns:**
- `bool`: `True` if key exists, `False` otherwise.

**Example:**
```python
if client.cache.is_cached("products/1000.json"):
    print("Data is cached")
```

#### `invalidate(key: str) -> None`

Removes cached data from S3.

**Parameters:**
- `key` (str): Cache key to invalidate.

**Example:**
```python
client.cache.invalidate("products/1000.json")
```

## Error Handling

### Common Exceptions

#### API Request Failures
```python
try:
    products = client.get_product_list(branch=1000)
except Exception as e:
    # Handle API errors
    print(f"API Error: {e}")
```

#### Cache Errors
Cache operations fail silently and fall back to API calls. No exceptions are raised for cache failures.

#### Network Errors
```python
try:
    products = client.get_product_list(branch=1000)
except Exception as e:
    if "Failed to fetch" in str(e):
        # Network error
        print("Network error occurred")
```

## Data Formats

### Product List Response

The product list API returns data that is converted to a DataFrame. The exact columns depend on the API response structure.

**Common columns:**
- `id` or `product_id`: Product identifier
- `name`: Product name
- `price`: Product price
- `category`: Product category
- Additional fields from API response

### Inventory Response

The inventory API returns data that is converted to a DataFrame.

**Common columns:**
- `id` or `product_id`: Product identifier
- `stock` or `quantity`: Stock quantity
- `branch`: Branch ID
- Additional fields from API response

### Merged Data

When using `get_products_with_inventory()`, the DataFrames are merged on common keys. If multiple merge keys exist, the first matching key is used.

**Merge keys tried (in order):**
1. `product_id`
2. `id`
3. `sku`
4. `productId`
5. Index-based merge (if same length)
6. Fallback: products DataFrame copy

## Best Practices

1. **Reuse Client**: Create one `VillaClient` instance and reuse it
2. **Use Caching**: Let the SDK handle caching automatically
3. **Handle Errors**: Always wrap API calls in try-except blocks
4. **Filter Early**: Use filters to reduce data processing
5. **Pandas Operations**: Leverage pandas for data manipulation

## Examples

See the [README](../README.md) for more examples.

