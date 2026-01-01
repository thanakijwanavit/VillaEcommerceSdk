"""
Advanced filtering examples for Villa Ecommerce Python SDK.
"""

from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products = client.get_product_list(branch=1000)

# Example 1: Multiple comparison operators
print("=== Example 1: Price Range Filter ===")
if 'price' in products.columns:
    affordable = client.filter_dataframe(
        products,
        {"price": {"gte": 10, "lte": 100}}
    )
    print(f"Affordable products (10-100): {len(affordable)}")
print()

# Example 2: Multiple filters (AND logic)
print("=== Example 2: Multiple Filters ===")
filters = {}
if 'category' in products.columns:
    filters["category"] = "electronics"
if 'price' in products.columns:
    filters["price"] = {"gt": 50}

if filters:
    filtered = client.filter_dataframe(products, filters)
    print(f"Filtered products: {len(filtered)}")
print()

# Example 3: List filter (OR logic)
print("=== Example 3: Multiple Categories ===")
if 'category' in products.columns:
    multi_category = client.filter_dataframe(
        products,
        {"category": ["electronics", "food", "clothing"]}
    )
    print(f"Multi-category products: {len(multi_category)}")
print()

# Example 4: Complex filtering
print("=== Example 4: Complex Filter ===")
complex_filters = {}
if 'price' in products.columns:
    complex_filters["price"] = {"gte": 20, "lte": 200}
if 'category' in products.columns:
    complex_filters["category"] = ["electronics", "food"]

if complex_filters:
    complex_filtered = client.filter_dataframe(products, complex_filters)
    print(f"Complex filtered: {len(complex_filtered)}")
print()

