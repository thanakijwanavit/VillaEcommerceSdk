"""Base API client for Villa Ecommerce SDK."""

from typing import Optional, Dict, Any
import pandas as pd


class VillaClient:
    """Main client for interacting with Villa Ecommerce API."""
    
    def __init__(self, s3_bucket: Optional[str] = None, base_url: str = "https://shop.villamarket.com"):
        """
        Initialize Villa API client.
        
        Args:
            s3_bucket: S3 bucket name for caching (default: villa-ecommerce-sdk-cache)
            base_url: Base URL for Villa API (default: https://shop.villamarket.com)
        """
        # Use default bucket name from template.yaml if not provided
        if s3_bucket is None:
            s3_bucket = "villa-ecommerce-sdk-cache"
        self.base_url = base_url.rstrip('/')
        self.s3_bucket = s3_bucket
        
        # Import here to avoid circular dependency
        from villa_ecommerce_sdk.cache import S3Cache
        from villa_ecommerce_sdk.products import ProductsService
        from villa_ecommerce_sdk.inventory import InventoryService
        from villa_ecommerce_sdk.payments import PaymentService
        
        self.cache = S3Cache(bucket_name=s3_bucket)
        self.products_service = ProductsService(base_url=base_url, cache=self.cache)
        self.inventory_service = InventoryService(base_url=base_url, cache=self.cache)
        self.payment_service = PaymentService(base_url=base_url, cache=self.cache)
    
    def get_product_list(self, branch: int = 1000) -> pd.DataFrame:
        """
        Get product list for a specific branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            DataFrame containing product data
        """
        return self.products_service.get_product_list(branch=branch)
    
    def get_inventory(self, branch: int = 1000) -> pd.DataFrame:
        """
        Get inventory data for a specific branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            DataFrame containing inventory data
        """
        return self.inventory_service.get_inventory(branch=branch)
    
    def get_products_with_inventory(
        self, 
        branch: int = 1000, 
        filters: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Get merged products and inventory data with optional filtering.
        
        This method fetches both product and inventory data, merges them,
        and applies filters if provided.
        
        Args:
            branch: Branch ID (default: 1000)
            filters: Optional dictionary of filters to apply to the merged DataFrame
                    Keys should be column names, values are filter criteria
                    Example: {"category": "electronics", "in_stock": True}
            
        Returns:
            Merged and filtered DataFrame
        """
        # Fetch both datasets
        products_df = self.get_product_list(branch=branch)
        inventory_df = self.get_inventory(branch=branch)
        
        # Merge dataframes
        # Try common merge keys (product_id, id, sku, etc.)
        merged_df = self._merge_dataframes(products_df, inventory_df)
        
        # Apply filters if provided
        if filters:
            merged_df = self.filter_dataframe(merged_df, filters)
        
        return merged_df
    
    def _merge_dataframes(
        self, 
        products_df: pd.DataFrame, 
        inventory_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge product and inventory dataframes.
        
        Attempts to find common columns for merging (product_id, id, sku, etc.)
        
        Args:
            products_df: Products DataFrame
            inventory_df: Inventory DataFrame
            
        Returns:
            Merged DataFrame
        """
        # Try common merge keys in order of preference
        merge_keys = ['product_id', 'id', 'sku', 'productId', 'product_id']
        
        for key in merge_keys:
            if key in products_df.columns and key in inventory_df.columns:
                return pd.merge(
                    products_df, 
                    inventory_df, 
                    on=key, 
                    how='outer',
                    suffixes=('_product', '_inventory')
                )
        
        # If no common key found, try to merge on index
        # This is a fallback - may need adjustment based on actual API response structure
        if len(products_df) == len(inventory_df):
            return pd.concat([products_df, inventory_df], axis=1)
        
        # Last resort: return products with inventory columns appended
        # This will need to be adjusted based on actual API response structure
        return products_df.copy()
    
    def filter_dataframe(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter DataFrame based on provided criteria.
        
        Args:
            df: DataFrame to filter
            filters: Dictionary where keys are column names and values are filter criteria
                    Supports:
                    - Exact match: {"column": "value"}
                    - Boolean: {"column": True}
                    - Numeric comparison: {"column": {"gt": 100}} or {"column": {"lt": 50}}
                    - Multiple conditions: {"column": ["value1", "value2"]}
        
        Returns:
            Filtered DataFrame
        """
        filtered_df = df.copy()
        
        for column, criteria in filters.items():
            if column not in filtered_df.columns:
                continue
            
            if isinstance(criteria, dict):
                # Handle comparison operators
                if 'gt' in criteria:
                    filtered_df = filtered_df[filtered_df[column] > criteria['gt']]
                elif 'lt' in criteria:
                    filtered_df = filtered_df[filtered_df[column] < criteria['lt']]
                elif 'gte' in criteria:
                    filtered_df = filtered_df[filtered_df[column] >= criteria['gte']]
                elif 'lte' in criteria:
                    filtered_df = filtered_df[filtered_df[column] <= criteria['lte']]
                elif 'eq' in criteria:
                    filtered_df = filtered_df[filtered_df[column] == criteria['eq']]
            elif isinstance(criteria, list):
                # Handle multiple values (OR condition)
                filtered_df = filtered_df[filtered_df[column].isin(criteria)]
            else:
                # Exact match
                filtered_df = filtered_df[filtered_df[column] == criteria]
        
        return filtered_df
    
    # Payment methods
    def create_payment(
        self,
        order_id: str,
        amount: float,
        currency: str = "THB",
        payment_method: str = "credit_card",
        customer_info: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new payment for an order.
        
        Args:
            order_id: Order identifier
            amount: Payment amount
            currency: Currency code (default: THB)
            payment_method: Payment method (credit_card, bank_transfer, etc.)
            customer_info: Optional customer information
            metadata: Optional additional metadata
            
        Returns:
            Payment response data
        """
        return self.payment_service.create_payment(
            order_id=order_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            customer_info=customer_info,
            metadata=metadata
        )
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status by payment ID.
        
        Args:
            payment_id: Payment identifier
            
        Returns:
            Payment status data
        """
        return self.payment_service.get_payment_status(payment_id=payment_id)
    
    def get_payment_history(
        self,
        order_id: Optional[str] = None,
        customer_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Get payment history with optional filters.
        
        Args:
            order_id: Optional order ID filter
            customer_id: Optional customer ID filter
            start_date: Optional start date (YYYY-MM-DD format)
            end_date: Optional end date (YYYY-MM-DD format)
            limit: Maximum number of records to return
            
        Returns:
            DataFrame containing payment history
        """
        return self.payment_service.get_payment_history(
            order_id=order_id,
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
    
    def process_refund(
        self,
        payment_id: str,
        amount: Optional[float] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a refund for a payment.
        
        Args:
            payment_id: Payment identifier to refund
            amount: Optional partial refund amount (if None, full refund)
            reason: Optional refund reason
            
        Returns:
            Refund response data
        """
        return self.payment_service.process_refund(
            payment_id=payment_id,
            amount=amount,
            reason=reason
        )
    
    def get_refund_status(self, refund_id: str) -> Dict[str, Any]:
        """
        Get refund status by refund ID.
        
        Args:
            refund_id: Refund identifier
            
        Returns:
            Refund status data
        """
        return self.payment_service.get_refund_status(refund_id=refund_id)
    
    def get_available_payment_methods(self, branch: int = 1000) -> list:
        """
        Get available payment methods for a branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            List of available payment methods
        """
        return self.payment_service.get_available_payment_methods(branch=branch)
    
    def verify_payment(self, payment_id: str, order_id: str) -> Dict[str, Any]:
        """
        Verify a payment matches an order.
        
        Args:
            payment_id: Payment identifier
            order_id: Order identifier
            
        Returns:
            Verification result
        """
        return self.payment_service.verify_payment(
            payment_id=payment_id,
            order_id=order_id
        )

