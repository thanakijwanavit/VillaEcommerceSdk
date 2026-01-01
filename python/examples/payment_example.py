"""
Example: Payment processing with Villa Ecommerce SDK.

This example demonstrates how to use the payment functionality
to create payments, process refunds, and manage payment history.
"""

from villa_ecommerce_sdk import VillaClient
import pandas as pd
from datetime import datetime, timedelta


def example_create_payment(client: VillaClient):
    """Example: Create a payment."""
    print("=== Creating Payment ===")
    
    payment = client.create_payment(
        order_id="ORDER-12345",
        amount=2500.00,
        currency="THB",
        payment_method="credit_card",
        customer_info={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+66123456789"
        },
        metadata={
            "source": "website",
            "campaign": "summer_sale"
        }
    )
    
    print(f"Payment ID: {payment['paymentId']}")
    print(f"Status: {payment['status']}")
    print(f"Amount: {payment['amount']} {payment['currency']}")
    return payment


def example_check_payment_status(client: VillaClient, payment_id: str):
    """Example: Check payment status."""
    print("\n=== Checking Payment Status ===")
    
    status = client.get_payment_status(payment_id=payment_id)
    print(f"Payment ID: {status['paymentId']}")
    print(f"Status: {status['status']}")
    print(f"Amount: {status['amount']} {status['currency']}")
    print(f"Created: {status.get('createdAt', 'N/A')}")
    return status


def example_payment_history(client: VillaClient):
    """Example: Get payment history."""
    print("\n=== Payment History ===")
    
    # Get all payments
    all_payments = client.get_payment_history(limit=100)
    print(f"Total payments: {len(all_payments)}")
    
    if len(all_payments) > 0:
        print(f"Total revenue: {all_payments['amount'].sum():,.2f} THB")
        print(f"Average payment: {all_payments['amount'].mean():,.2f} THB")
        print(f"Min payment: {all_payments['amount'].min():,.2f} THB")
        print(f"Max payment: {all_payments['amount'].max():,.2f} THB")
    
    # Get payments for specific order
    order_payments = client.get_payment_history(order_id="ORDER-12345")
    print(f"\nPayments for ORDER-12345: {len(order_payments)}")
    
    # Get payments for date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    recent_payments = client.get_payment_history(
        start_date=start_date,
        end_date=end_date,
        limit=100
    )
    print(f"Payments in last 30 days: {len(recent_payments)}")
    
    return all_payments


def example_refund(client: VillaClient, payment_id: str):
    """Example: Process a refund."""
    print("\n=== Processing Refund ===")
    
    # Full refund
    refund = client.process_refund(
        payment_id=payment_id,
        reason="Customer requested refund"
    )
    
    print(f"Refund ID: {refund['refundId']}")
    print(f"Status: {refund['status']}")
    print(f"Amount: {refund['amount']} {refund['currency']}")
    
    # Check refund status
    refund_status = client.get_refund_status(refund_id=refund['refundId'])
    print(f"\nRefund Status: {refund_status['status']}")
    
    return refund


def example_partial_refund(client: VillaClient, payment_id: str):
    """Example: Process a partial refund."""
    print("\n=== Processing Partial Refund ===")
    
    partial_refund = client.process_refund(
        payment_id=payment_id,
        amount=500.00,
        reason="Partial refund for damaged item"
    )
    
    print(f"Refund ID: {partial_refund['refundId']}")
    print(f"Status: {partial_refund['status']}")
    print(f"Amount: {partial_refund['amount']} {partial_refund['currency']}")
    
    return partial_refund


def example_payment_methods(client: VillaClient):
    """Example: Get available payment methods."""
    print("\n=== Available Payment Methods ===")
    
    methods = client.get_available_payment_methods(branch=1000)
    
    print(f"Available payment methods: {len(methods)}")
    for method in methods:
        print(f"\n{method['name']}")
        print(f"  Type: {method['type']}")
        print(f"  Enabled: {method.get('enabled', False)}")
        if 'fees' in method:
            print(f"  Fees: {method['fees']}")
        if 'description' in method:
            print(f"  Description: {method['description']}")


def example_verify_payment(client: VillaClient, payment_id: str, order_id: str):
    """Example: Verify payment."""
    print("\n=== Verifying Payment ===")
    
    verification = client.verify_payment(
        payment_id=payment_id,
        order_id=order_id
    )
    
    if verification['verified']:
        print("✓ Payment verified successfully")
        print(f"  Payment ID: {verification['paymentId']}")
        print(f"  Order ID: {verification['orderId']}")
        print(f"  Amount: {verification['amount']} {verification['currency']}")
    else:
        print("✗ Payment verification failed")
        print(f"  Reason: {verification.get('reason', 'Unknown')}")
    
    return verification


def example_complete_payment_flow(client: VillaClient):
    """Example: Complete payment flow."""
    print("\n=== Complete Payment Flow ===")
    
    # 1. Create payment
    payment = example_create_payment(client)
    payment_id = payment['paymentId']
    order_id = "ORDER-12345"
    
    # 2. Check status
    example_check_payment_status(client, payment_id)
    
    # 3. Verify payment
    example_verify_payment(client, payment_id, order_id)
    
    # 4. Get payment history
    example_payment_history(client)
    
    # 5. Get available payment methods
    example_payment_methods(client)
    
    # Note: Uncomment to test refunds
    # example_refund(client, payment_id)
    # example_partial_refund(client, payment_id)


def main():
    """Main function."""
    # Initialize client (uses default bucket: villa-ecommerce-sdk-cache)
    client = VillaClient()
    
    # Run examples
    try:
        example_complete_payment_flow(client)
    except Exception as e:
        print(f"\nError: {e}")
        print("Note: This example requires a valid API endpoint and credentials.")


if __name__ == "__main__":
    main()

