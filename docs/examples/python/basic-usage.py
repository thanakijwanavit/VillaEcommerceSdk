"""
Basic usage examples for Villa Ecommerce Python SDK.
"""

from villa_ecommerce_sdk import VillaClient

# Initialize client
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")

# Example 1: Get product list
print("=== Example 1: Get Product List ===")
products = client.get_product_list(branch=1000)
print(f"Total products: {len(products)}")
print(products.head())
print()

# Example 2: Get inventory
print("=== Example 2: Get Inventory ===")
inventory = client.get_inventory(branch=1000)
print(f"Total inventory items: {len(inventory)}")
print(inventory.head())
print()

# Example 3: Filter products
print("=== Example 3: Filter Products ===")
if 'category' in products.columns:
    electronics = client.filter_dataframe(
        products,
        {"category": "electronics"}
    )
    print(f"Electronics: {len(electronics)}")
print()

# Example 4: Get merged data
print("=== Example 4: Get Products with Inventory ===")
merged = client.get_products_with_inventory(branch=1000)
print(f"Merged data: {len(merged)} rows")
print(merged.head())
print()

# Example 5: Filter merged data
print("=== Example 5: Filter Merged Data ===")
if 'stock' in merged.columns:
    in_stock = client.get_products_with_inventory(
        branch=1000,
        filters={"stock": {"gt": 0}}
    )
    print(f"In-stock items: {len(in_stock)}")
print()

