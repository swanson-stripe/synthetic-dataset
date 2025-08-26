#!/usr/bin/env python3
"""
TechStyle Synthetic Stripe Payment Data Generator

Generates realistic payment data for an e-commerce fashion retailer over 24 months
across three lifecycle stages with proper Stripe API structure.

Usage:
    python generate_techstyle.py
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import os
import sys

# Third-party imports
try:
    from faker import Faker
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    sys.exit(1)

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

# Lifecycle stages configuration
LIFECYCLE_STAGES = {
    'early': {
        'months': (1, 8),
        'orders_per_month': (50, 200),
        'currencies': ['usd'],
        'failure_rate': 0.045,  # 4.5%
        'dispute_rate': 0.008,  # 0.8%
    },
    'growth': {
        'months': (9, 16),
        'orders_per_month': (500, 2000),
        'currencies': ['usd', 'eur', 'gbp'],
        'failure_rate': 0.025,  # 2.5%
        'dispute_rate': 0.005,  # 0.5%
    },
    'mature': {
        'months': (17, 24),
        'orders_per_month': (5000, 15000),
        'currencies': ['usd', 'eur', 'gbp', 'cad', 'aud', 'jpy', 'chf', 'sek', 'nok', 'dkk'],
        'failure_rate': 0.0175,  # 1.75%
        'dispute_rate': 0.003,   # 0.3%
    }
}

# Product categories and price ranges (in USD cents)
PRODUCT_CATEGORIES = {
    'womens_clothing': {'min': 2500, 'max': 15000, 'weight': 30},
    'mens_clothing': {'min': 3000, 'max': 12000, 'weight': 25},
    'shoes': {'min': 4000, 'max': 25000, 'weight': 20},
    'accessories': {'min': 1500, 'max': 8000, 'weight': 15},
    'outerwear': {'min': 8000, 'max': 35000, 'weight': 10},
}

# Currency exchange rates (approximate)
CURRENCY_RATES = {
    'usd': 1.0,
    'eur': 0.85,
    'gbp': 0.75,
    'cad': 1.25,
    'aud': 1.35,
    'jpy': 110.0,
    'chf': 0.92,
    'sek': 9.5,
    'nok': 8.8,
    'dkk': 6.3,
}

# Payment method distribution
PAYMENT_METHODS = {
    'card': 0.85,
    'apple_pay': 0.08,
    'google_pay': 0.05,
    'paypal': 0.02,
}

# Failure reasons
FAILURE_REASONS = [
    'card_declined',
    'insufficient_funds',
    'expired_card',
    'incorrect_cvc',
    'processing_error',
    'authentication_required',
]

# Initialize Faker
fake = Faker()
fake.seed_instance(42)  # For reproducible results
random.seed(42)
np.random.seed(42)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_stripe_ids() -> Dict[str, str]:
    """Generate properly formatted Stripe IDs."""
    return {
        'payment_intent': f"pi_{uuid.uuid4().hex[:24]}",
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'charge': f"ch_{uuid.uuid4().hex[:24]}",
        'payment_method': f"pm_{uuid.uuid4().hex[:24]}",
    }

def get_lifecycle_stage(month: int) -> str:
    """Determine lifecycle stage based on month."""
    for stage, config in LIFECYCLE_STAGES.items():
        if config['months'][0] <= month <= config['months'][1]:
            return stage
    return 'mature'

def convert_currency(amount_usd_cents: int, currency: str) -> int:
    """Convert USD cents to target currency."""
    usd_amount = amount_usd_cents / 100
    converted = usd_amount / CURRENCY_RATES[currency]
    
    # Handle JPY (no decimal places)
    if currency == 'jpy':
        return int(converted)
    else:
        return int(converted * 100)

def select_payment_method() -> str:
    """Select payment method based on distribution."""
    rand = random.random()
    cumulative = 0
    for method, probability in PAYMENT_METHODS.items():
        cumulative += probability
        if rand <= cumulative:
            return method
    return 'card'

# =============================================================================
# DATA GENERATION FUNCTIONS
# =============================================================================

def generate_customer(customer_number: int, created_date: datetime) -> Dict[str, Any]:
    """Generate a complete customer object."""
    ids = generate_stripe_ids()
    
    # Generate customer profile
    gender = random.choice(['male', 'female'])
    if gender == 'female':
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name_male()
    
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{fake.free_email_domain()}"
    
    return {
        'id': ids['customer'],
        'object': 'customer',
        'created': int(created_date.timestamp()),
        'email': email,
        'name': f"{first_name} {last_name}",
        'phone': fake.phone_number(),
        'address': {
            'line1': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'postal_code': fake.postcode(),
            'country': 'US',
        },
        'metadata': {
            'customer_number': str(customer_number),
            'acquisition_channel': random.choice(['organic', 'social', 'email', 'paid_search', 'referral']),
            'preferred_category': random.choices(
                list(PRODUCT_CATEGORIES.keys()),
                weights=[cat['weight'] for cat in PRODUCT_CATEGORIES.values()]
            )[0]
        }
    }

def generate_payment(customer: Dict[str, Any], order_date: datetime, lifecycle_stage: str) -> Dict[str, Any]:
    """Generate a complete payment intent object."""
    ids = generate_stripe_ids()
    stage_config = LIFECYCLE_STAGES[lifecycle_stage]
    
    # Select currency
    currency = random.choice(stage_config['currencies'])
    
    # Select product category and generate amount
    category = random.choices(
        list(PRODUCT_CATEGORIES.keys()),
        weights=[cat['weight'] for cat in PRODUCT_CATEGORIES.values()]
    )[0]
    
    # Generate base amount in USD cents
    cat_config = PRODUCT_CATEGORIES[category]
    base_amount = random.randint(cat_config['min'], cat_config['max'])
    
    # Convert to target currency
    amount = convert_currency(base_amount, currency)
    
    # Determine if payment fails
    is_failed = random.random() < stage_config['failure_rate']
    status = 'requires_payment_method' if is_failed else 'succeeded'
    
    # Generate order ID
    order_id = f"ORD-{random.randint(100000, 999999)}"
    
    # Payment method
    payment_method_type = select_payment_method()
    
    # Create charge data
    charge_data = {
        'id': ids['charge'],
        'object': 'charge',
        'amount': amount,
        'currency': currency,
        'created': int(order_date.timestamp()),
        'customer': customer['id'],
        'paid': not is_failed,
        'refunded': False,
        'disputed': False,
        'failure_code': random.choice(FAILURE_REASONS) if is_failed else None,
        'failure_message': 'Your card was declined.' if is_failed else None,
        'payment_method': ids['payment_method'],
        'payment_method_details': {
            'type': payment_method_type,
            'card': {
                'brand': random.choice(['visa', 'mastercard', 'amex', 'discover']),
                'last4': f"{random.randint(1000, 9999)}",
                'exp_month': random.randint(1, 12),
                'exp_year': random.randint(2024, 2030),
            } if payment_method_type == 'card' else None
        }
    }
    
    return {
        'id': ids['payment_intent'],
        'object': 'payment_intent',
        'amount': amount,
        'currency': currency,
        'status': status,
        'customer': customer['id'],
        'created': int(order_date.timestamp()),
        'description': f"Order #{order_id}",
        'payment_method': ids['payment_method'],
        'payment_method_types': [payment_method_type],
        'charges': {
            'object': 'list',
            'data': [charge_data],
            'has_more': False,
            'total_count': 1,
            'url': f"/v1/charges?payment_intent={ids['payment_intent']}"
        },
        'metadata': {
            'order_id': order_id,
            'product_category': category,
            'customer_email': customer['email'],
            'lifecycle_stage': lifecycle_stage,
        },
        'receipt_email': customer['email'],
        'setup_future_usage': None,
        'shipping': {
            'address': customer['address'],
            'name': customer['name'],
        }
    }

def generate_dispute(payment: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a dispute object for a payment."""
    dispute_id = f"dp_{uuid.uuid4().hex[:24]}"
    charge = payment['charges']['data'][0]
    
    return {
        'id': dispute_id,
        'object': 'dispute',
        'amount': payment['amount'],
        'currency': payment['currency'],
        'charge': charge['id'],
        'created': payment['created'] + random.randint(86400, 2592000),  # 1-30 days later
        'reason': random.choice(['duplicate', 'fraudulent', 'subscription_canceled', 'product_unacceptable']),
        'status': random.choice(['warning_needs_response', 'needs_response', 'under_review']),
        'metadata': {
            'original_payment_intent': payment['id'],
            'order_id': payment['metadata']['order_id'],
        }
    }

def calculate_metrics(payments_df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive metrics from payments data."""
    # Convert timestamps to datetime
    payments_df['date'] = pd.to_datetime(payments_df['created'], unit='s').dt.date
    payments_df['month'] = pd.to_datetime(payments_df['created'], unit='s').dt.to_period('M')
    
    # Daily metrics - simplified structure
    daily_volume = payments_df.groupby('date')['amount'].sum().to_dict()
    daily_count = payments_df.groupby('date')['amount'].count().to_dict()
    daily_avg = payments_df.groupby('date')['amount'].mean().to_dict()
    daily_success = payments_df.groupby('date')['status'].apply(
        lambda x: (x == 'succeeded').sum() / len(x)
    ).to_dict()
    
    # Monthly metrics - simplified structure
    monthly_volume = payments_df.groupby('month')['amount'].sum().to_dict()
    monthly_count = payments_df.groupby('month')['amount'].count().to_dict()
    monthly_avg = payments_df.groupby('month')['amount'].mean().to_dict()
    monthly_success = payments_df.groupby('month')['status'].apply(
        lambda x: (x == 'succeeded').sum() / len(x)
    ).to_dict()
    
    # Success rates by lifecycle stage
    stage_success = payments_df.groupby('lifecycle_stage')['status'].apply(
        lambda x: (x == 'succeeded').sum() / len(x)
    ).to_dict()
    
    # Currency distribution
    currency_dist = payments_df['currency'].value_counts().to_dict()
    
    # Payment method breakdown
    payment_method_dist = payments_df['payment_method_type'].value_counts().to_dict()
    
    # Failure reasons
    failed_payments = payments_df[payments_df['status'] != 'succeeded']
    failure_reasons = failed_payments['failure_code'].value_counts().to_dict() if len(failed_payments) > 0 else {}
    
    # Convert date/period keys to strings for JSON serialization
    daily_metrics = {
        'volume': {str(k): v for k, v in daily_volume.items()},
        'count': {str(k): v for k, v in daily_count.items()},
        'average': {str(k): float(v) for k, v in daily_avg.items()},
        'success_rate': {str(k): float(v) for k, v in daily_success.items()}
    }
    
    monthly_metrics = {
        'volume': {str(k): v for k, v in monthly_volume.items()},
        'count': {str(k): v for k, v in monthly_count.items()},
        'average': {str(k): float(v) for k, v in monthly_avg.items()},
        'success_rate': {str(k): float(v) for k, v in monthly_success.items()}
    }
    
    return {
        'daily_metrics': daily_metrics,
        'monthly_metrics': monthly_metrics,
        'stage_success_rates': stage_success,
        'currency_distribution': currency_dist,
        'payment_method_distribution': payment_method_dist,
        'failure_reasons': failure_reasons,
        'summary': {
            'total_payments': len(payments_df),
            'total_volume': int(payments_df['amount'].sum()),
            'overall_success_rate': float((payments_df['status'] == 'succeeded').sum() / len(payments_df)),
            'average_order_value': float(payments_df['amount'].mean()),
            'date_range': {
                'start': str(payments_df['date'].min()),
                'end': str(payments_df['date'].max())
            }
        }
    }

# =============================================================================
# MAIN GENERATION LOGIC
# =============================================================================

def generate_techstyle_data() -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Generate complete TechStyle payment dataset."""
    print("🚀 Starting TechStyle synthetic data generation...")
    
    # Initialize data containers
    customers = []
    payments = []
    disputes = []
    
    # Start date: 24 months ago
    start_date = datetime.now() - timedelta(days=24*30)
    customer_counter = 1
    
    print("📊 Generating data across 24-month lifecycle...")
    
    # Generate data month by month
    for month in range(1, 25):
        current_date = start_date + timedelta(days=month*30)
        lifecycle_stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE_STAGES[lifecycle_stage]
        
        # Determine number of orders for this month
        orders_this_month = random.randint(
            stage_config['orders_per_month'][0],
            stage_config['orders_per_month'][1]
        )
        
        print(f"  Month {month:2d} ({lifecycle_stage:>6}): {orders_this_month:5d} orders")
        
        # Generate customers and payments for this month
        for _ in range(orders_this_month):
            # 70% chance of new customer, 30% chance of existing customer
            if len(customers) == 0 or random.random() < 0.7:
                # Create new customer
                customer = generate_customer(customer_counter, current_date)
                customers.append(customer)
                customer_counter += 1
            else:
                # Use existing customer
                customer = random.choice(customers)
            
            # Generate random order date within the month
            days_in_month = random.randint(0, 29)
            order_date = current_date + timedelta(days=days_in_month)
            
            # Generate payment
            payment = generate_payment(customer, order_date, lifecycle_stage)
            payments.append(payment)
            
            # Generate dispute (small chance)
            if (payment['status'] == 'succeeded' and 
                random.random() < stage_config['dispute_rate']):
                dispute = generate_dispute(payment)
                disputes.append(dispute)
    
    print(f"✅ Generated {len(payments):,} payments from {len(customers):,} customers")
    print(f"⚠️  Generated {len(disputes):,} disputes")
    
    return customers, payments, disputes

def prepare_dataframe(payments: List[Dict]) -> pd.DataFrame:
    """Convert payments to DataFrame for analysis."""
    # Flatten payment data for analysis
    flattened_payments = []
    
    for payment in payments:
        charge = payment['charges']['data'][0]
        flattened_payments.append({
            'id': payment['id'],
            'amount': payment['amount'],
            'currency': payment['currency'],
            'status': payment['status'],
            'created': payment['created'],
            'customer': payment['customer'],
            'product_category': payment['metadata']['product_category'],
            'lifecycle_stage': payment['metadata']['lifecycle_stage'],
            'payment_method_type': payment['payment_method_types'][0],
            'failure_code': charge.get('failure_code'),
        })
    
    return pd.DataFrame(flattened_payments)

def save_output_files(customers: List[Dict], payments: List[Dict], disputes: List[Dict], 
                     metrics: Dict[str, Any]) -> None:
    """Save all generated data to JSON files."""
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    print("💾 Saving output files...")
    
    # Save raw data
    with open(f'{output_dir}/payments_raw.json', 'w') as f:
        json.dump(payments, f, indent=2, default=str)
    
    with open(f'{output_dir}/customers.json', 'w') as f:
        json.dump(customers, f, indent=2, default=str)
    
    if disputes:
        with open(f'{output_dir}/disputes.json', 'w') as f:
            json.dump(disputes, f, indent=2, default=str)
    
    # Save metrics
    with open(f'{output_dir}/daily_metrics.json', 'w') as f:
        json.dump(metrics['daily_metrics'], f, indent=2, default=str)
    
    # Create chart-ready data
    chart_data = {
        'daily_volume': metrics['daily_metrics'],
        'currency_breakdown': metrics['currency_distribution'],
        'success_rates_by_stage': metrics['stage_success_rates'],
        'payment_methods': metrics['payment_method_distribution']
    }
    
    with open(f'{output_dir}/chart_data.json', 'w') as f:
        json.dump(chart_data, f, indent=2, default=str)
    
    # Save summary statistics
    with open(f'{output_dir}/summary_stats.json', 'w') as f:
        json.dump(metrics['summary'], f, indent=2, default=str)
    
    print(f"📁 Files saved to /{output_dir}/ directory")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    start_time = datetime.now()
    
    try:
        # Generate data
        customers, payments, disputes = generate_techstyle_data()
        
        # Prepare DataFrame for analysis
        payments_df = prepare_dataframe(payments)
        
        # Calculate metrics
        print("📈 Calculating metrics...")
        metrics = calculate_metrics(payments_df)
        
        # Save output files
        save_output_files(customers, payments, disputes, metrics)
        
        # Print summary validation
        print("\n" + "="*60)
        print("📊 TECHSTYLE DATA GENERATION SUMMARY")
        print("="*60)
        
        summary = metrics['summary']
        print(f"Generated {summary['total_payments']:,} payments")
        print(f"Success rate: {summary['overall_success_rate']:.2%}")
        print(f"Average order value: ${summary['average_order_value']/100:.2f}")
        print(f"Total volume: ${summary['total_volume']/100:,.2f}")
        print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"Unique customers: {len(customers):,}")
        print(f"Disputes generated: {len(disputes):,}")
        print("\nCurrency distribution:")
        for currency, count in metrics['currency_distribution'].items():
            print(f"  {currency.upper()}: {count:,} payments")
        
        print("\nFiles created in /output/ directory:")
        print("  - payments_raw.json")
        print("  - customers.json")
        print("  - daily_metrics.json") 
        print("  - chart_data.json")
        print("  - summary_stats.json")
        if disputes:
            print("  - disputes.json")
        
        execution_time = datetime.now() - start_time
        print(f"\n⏱️  Execution time: {execution_time.total_seconds():.1f} seconds")
        print("✅ TechStyle data generation complete!")
        
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()
