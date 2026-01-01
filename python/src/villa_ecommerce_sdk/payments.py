"""Payment functionality for Villa Ecommerce SDK."""

from typing import Optional, Dict, Any, List
import pandas as pd
from villa_ecommerce_sdk.base import BaseService


class PaymentService(BaseService):
    """Service for handling payment operations."""
    
    def get_service_name(self) -> str:
        """Get service name."""
        return "PaymentService"
    
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
        payload = {
            "orderId": order_id,
            "amount": amount,
            "currency": currency,
            "paymentMethod": payment_method
        }
        
        if customer_info:
            payload["customerInfo"] = customer_info
        
        if metadata:
            payload["metadata"] = metadata
        
        return self._post(
            endpoint="/api/payment/create",
            json_data=payload,
            headers={"Content-Type": "application/json"}
        )
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status by payment ID.
        
        Args:
            payment_id: Payment identifier
            
        Returns:
            Payment status data
        """
        cache_key = f"payments/{payment_id}.json"
        return self._get(
            endpoint=f"/api/payment/status/{payment_id}",
            cache_key=cache_key
        )
    
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
        params = {"limit": limit}
        
        if order_id:
            params["orderId"] = order_id
        if customer_id:
            params["customerId"] = customer_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        cache_key = f"payments/history/{order_id or 'all'}.json"
        data = self._get(
            endpoint="/api/payment/history",
            cache_key=cache_key,
            params=params
        )
        
        # Convert to DataFrame
        if isinstance(data, dict):
            if 'payments' in data:
                payments_list = data['payments']
            elif 'data' in data:
                payments_list = data['data']
            elif 'items' in data:
                payments_list = data['items']
            else:
                payments_list = [data] if not isinstance(data, list) else data
        elif isinstance(data, list):
            payments_list = data
        else:
            payments_list = [data]
        
        return pd.DataFrame(payments_list)
    
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
        payload = {
            "paymentId": payment_id
        }
        
        if amount is not None:
            payload["amount"] = amount
        
        if reason:
            payload["reason"] = reason
        
        return self._post(
            endpoint="/api/payment/refund",
            json_data=payload,
            headers={"Content-Type": "application/json"}
        )
    
    def get_refund_status(self, refund_id: str) -> Dict[str, Any]:
        """
        Get refund status by refund ID.
        
        Args:
            refund_id: Refund identifier
            
        Returns:
            Refund status data
        """
        cache_key = f"refunds/{refund_id}.json"
        return self._get(
            endpoint=f"/api/payment/refund/status/{refund_id}",
            cache_key=cache_key
        )
    
    def get_available_payment_methods(self, branch: int = 1000) -> List[Dict[str, Any]]:
        """
        Get available payment methods for a branch.
        
        Args:
            branch: Branch ID (default: 1000)
            
        Returns:
            List of available payment methods
        """
        cache_key = f"payment-methods/{branch}.json"
        data = self._get(
            endpoint=f"/api/payment/methods/{branch}",
            cache_key=cache_key
        )
        
        if isinstance(data, dict):
            if 'methods' in data:
                return data['methods']
            elif 'data' in data:
                return data['data'] if isinstance(data['data'], list) else [data['data']]
            else:
                return [data] if not isinstance(data, list) else data
        elif isinstance(data, list):
            return data
        else:
            return [data]
    
    def verify_payment(self, payment_id: str, order_id: str) -> Dict[str, Any]:
        """
        Verify a payment matches an order.
        
        Args:
            payment_id: Payment identifier
            order_id: Order identifier
            
        Returns:
            Verification result
        """
        return self._post(
            endpoint="/api/payment/verify",
            json_data={
                "paymentId": payment_id,
                "orderId": order_id
            },
            headers={"Content-Type": "application/json"}
        )

