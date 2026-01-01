"""
Data analysis examples using Villa Ecommerce Python SDK with pandas.
"""

import pandas as pd
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")

# Get data
products = client.get_product_list(branch=1000)
merged = client.get_products_with_inventory(branch=1000)

# Example 1: Basic statistics
print("=== Example 1: Basic Statistics ===")
if 'price' in products.columns:
    print(f"Average price: {products['price'].mean():.2f}")
    print(f"Max price: {products['price'].max():.2f}")
    print(f"Min price: {products['price'].min():.2f}")
    print(f"Total value: {products['price'].sum():.2f}")
print()

# Example 2: Category analysis
print("=== Example 2: Category Analysis ===")
if 'category' in products.columns:
    category_stats = products.groupby('category').agg({
        'price': ['count', 'mean', 'sum']
    }).round(2)
    print(category_stats)
print()

# Example 3: Stock analysis
print("=== Example 3: Stock Analysis ===")
if 'stock' in merged.columns:
    stock_stats = merged['stock'].describe()
    print(stock_stats)
    
    # Low stock items
    low_stock = merged[merged['stock'] < 10]
    print(f"\nLow stock items (< 10): {len(low_stock)}")
print()

# Example 4: Export to CSV
print("=== Example 4: Export Data ===")
products.to_csv('products_export.csv', index=False)
print("Exported products to products_export.csv")

if len(merged) > 0:
    merged.to_csv('merged_export.csv', index=False)
    print("Exported merged data to merged_export.csv")
print()

# Example 5: Data visualization (requires matplotlib)
try:
    import matplotlib.pyplot as plt
    
    if 'price' in products.columns:
        print("=== Example 5: Price Distribution ===")
        products['price'].hist(bins=20)
        plt.title('Price Distribution')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.savefig('price_distribution.png')
        print("Saved price_distribution.png")
except ImportError:
    print("Matplotlib not installed, skipping visualization")
print()

