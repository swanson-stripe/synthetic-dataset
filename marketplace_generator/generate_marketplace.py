#!/usr/bin/env python3
"""
LocalBites Synthetic Stripe Connect Marketplace Data Generator

Generates realistic food delivery marketplace data including connected accounts,
orders, payments, transfers, and issuing cards over a 24-month business lifecycle.

Usage:
    python generate_marketplace.py
"""

import json
import random
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import os
import sys
from collections import defaultdict

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
# MARKETPLACE CONFIGURATION
# =============================================================================

# Platform economics
PLATFORM_CONFIG = {
    'commission_rate': 0.15,      # 15% commission on food
    'delivery_base_fee': 299,     # $2.99 in cents
    'service_fee': 199,           # $1.99 in cents
    'average_order_value': 3500,  # $35.00 in cents
    'average_tip_rate': 0.15,     # 15% tip
    'instant_payout_fee': 150,    # $1.50 in cents
    'daily_card_limit': 50000,    # $500 in cents
}

# Lifecycle stages configuration (scaled down for performance)
LIFECYCLE_STAGES = {
    'early': {
        'months': range(0, 8),
        'total_restaurants': 50,
        'total_drivers': 100,
        'daily_orders': 500,
    },
    'growth': {
        'months': range(8, 16),
        'total_restaurants': 200,
        'total_drivers': 400,
        'daily_orders': 2000,
    },
    'mature': {
        'months': range(16, 24),
        'total_restaurants': 500,
        'total_drivers': 1000,
        'daily_orders': 5000,
    }
}

# Restaurant cuisines and average prep times
CUISINE_TYPES = {
    'italian': {'prep_time': 25, 'avg_order': 4200},
    'mexican': {'prep_time': 15, 'avg_order': 2800},
    'chinese': {'prep_time': 20, 'avg_order': 3200},
    'american': {'prep_time': 18, 'avg_order': 3800},
    'thai': {'prep_time': 22, 'avg_order': 3500},
    'indian': {'prep_time': 30, 'avg_order': 4000},
    'japanese': {'prep_time': 20, 'avg_order': 4500},
    'pizza': {'prep_time': 12, 'avg_order': 2500},
}

# Driver vehicle types
VEHICLE_TYPES = ['bicycle', 'scooter', 'car', 'motorcycle']

# Initialize Faker
fake = Faker()
fake.seed_instance(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_id(prefix: str) -> str:
    """Generate Stripe-style ID with prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:24]}"

def calculate_distance() -> float:
    """Calculate delivery distance in miles."""
    return round(random.uniform(0.5, 8.0), 1)

def calculate_delivery_fee(distance: float) -> int:
    """Calculate delivery fee based on distance."""
    base_fee = PLATFORM_CONFIG['delivery_base_fee']
    if distance > 2.0:
        extra_fee = int((distance - 2.0) * 50)  # $0.50 per mile over 2 miles
        return base_fee + extra_fee
    return base_fee

# =============================================================================
# CONNECTED ACCOUNT GENERATION
# =============================================================================

def create_restaurant_account(restaurant_id: int, onboarded_date: datetime) -> Dict[str, Any]:
    """Create a restaurant connected account."""
    cuisine = random.choice(list(CUISINE_TYPES.keys()))
    business_name = f"{fake.company()} {cuisine.title()}"
    
    return {
        'id': generate_id('acct'),
        'object': 'account',
        'type': 'custom',
        'created': int(onboarded_date.timestamp()),
        'country': 'US',
        'charges_enabled': True,
        'payouts_enabled': True,
        'business_profile': {
            'mcc': 5812,  # Eating places
            'name': business_name,
            'product_description': f"{cuisine.title()} restaurant",
        },
        'capabilities': {
            'card_payments': {'status': 'active'},
            'transfers': {'status': 'active'}
        },
        'metadata': {
            'restaurant_id': str(restaurant_id),
            'cuisine_type': cuisine,
            'average_prep_time': str(CUISINE_TYPES[cuisine]['prep_time']),
            'platform_type': 'restaurant'
        }
    }

def create_driver_account(driver_id: int, onboarded_date: datetime) -> Dict[str, Any]:
    """Create a driver connected account."""
    vehicle = random.choice(VEHICLE_TYPES)
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    return {
        'id': generate_id('acct'),
        'object': 'account',
        'type': 'express',
        'created': int(onboarded_date.timestamp()),
        'country': 'US',
        'charges_enabled': False,
        'payouts_enabled': True,
        'individual': {
            'first_name': first_name,
            'last_name': last_name,
            'email': f"{first_name.lower()}.{last_name.lower()}@email.com",
        },
        'capabilities': {
            'transfers': {'status': 'active'},
            'card_issuing': {'status': 'active'}
        },
        'metadata': {
            'driver_id': str(driver_id),
            'vehicle_type': vehicle,
            'rating': str(round(random.uniform(4.2, 5.0), 1)),
            'platform_type': 'driver'
        }
    }

def create_driver_card(driver_account: Dict[str, Any]) -> Dict[str, Any]:
    """Create a virtual card for driver expenses."""
    return {
        'id': generate_id('ic'),
        'object': 'issuing.card',
        'brand': 'visa',
        'cardholder': {
            'name': f"{driver_account['individual']['first_name']} {driver_account['individual']['last_name']}",
            'email': driver_account['individual']['email'],
        },
        'created': driver_account['created'],
        'currency': 'usd',
        'last4': f"{random.randint(1000, 9999)}",
        'status': 'active',
        'type': 'virtual',
        'spending_controls': {
            'allowed_categories': ['gas_stations', 'parking', 'tolls_bridge_fees'],
            'spending_limits': [{'amount': PLATFORM_CONFIG['daily_card_limit'], 'interval': 'daily'}]
        },
        'metadata': {
            'driver_account': driver_account['id'],
            'driver_id': driver_account['metadata']['driver_id'],
        }
    }

# =============================================================================
# ORDER AND PAYMENT PROCESSING
# =============================================================================

def process_order(order_id: int, customer_id: str, restaurant: Dict[str, Any], 
                 driver: Dict[str, Any], order_date: datetime) -> Tuple[Dict, Dict, Dict, Dict]:
    """Process a complete order with payment and transfers."""
    
    # Calculate order amounts
    cuisine = restaurant['metadata']['cuisine_type']
    base_food_amount = CUISINE_TYPES[cuisine]['avg_order']
    food_amount = int(base_food_amount * random.uniform(0.7, 1.8))
    
    distance = calculate_distance()
    delivery_fee = calculate_delivery_fee(distance)
    service_fee = PLATFORM_CONFIG['service_fee']
    tip_amount = int(food_amount * PLATFORM_CONFIG['average_tip_rate'])
    total_amount = food_amount + delivery_fee + service_fee + tip_amount
    
    # Calculate platform fees
    restaurant_commission = int(food_amount * PLATFORM_CONFIG['commission_rate'])
    restaurant_net = food_amount - restaurant_commission
    driver_earnings = delivery_fee + tip_amount
    platform_earnings = restaurant_commission + service_fee
    
    # Payment success (98% success rate)
    payment_success = random.random() > 0.02
    
    # Create payment intent
    payment_intent = {
        'id': generate_id('pi'),
        'object': 'payment_intent',
        'amount': total_amount,
        'currency': 'usd',
        'customer': customer_id,
        'created': int(order_date.timestamp()),
        'status': 'succeeded' if payment_success else 'requires_payment_method',
        'description': f"LocalBites Order #{order_id}",
        'metadata': {
            'order_id': str(order_id),
            'restaurant_id': restaurant['metadata']['restaurant_id'],
            'driver_id': driver['metadata']['driver_id'],
            'distance_miles': str(distance)
        },
        'application_fee_amount': platform_earnings
    }
    
    # Create transfers (only if payment succeeded)
    restaurant_transfer = None
    driver_transfer = None
    
    if payment_success:
        restaurant_transfer = {
            'id': generate_id('tr'),
            'object': 'transfer',
            'amount': restaurant_net,
            'currency': 'usd',
            'created': int(order_date.timestamp()),
            'destination': restaurant['id'],
            'description': f"Order #{order_id} payout",
            'metadata': {
                'order_id': str(order_id),
                'transfer_type': 'restaurant_payout'
            }
        }
        
        driver_transfer = {
            'id': generate_id('tr'),
            'object': 'transfer',
            'amount': driver_earnings,
            'currency': 'usd',
            'created': int((order_date + timedelta(minutes=45)).timestamp()),
            'destination': driver['id'],
            'description': f"Delivery #{order_id} payout",
            'metadata': {
                'order_id': str(order_id),
                'transfer_type': 'driver_payout'
            }
        }
    
    # Create order record
    order = {
        'id': f"order_{order_id}",
        'order_number': order_id,
        'customer_id': customer_id,
        'restaurant_id': restaurant['id'],
        'driver_id': driver['id'],
        'payment_intent_id': payment_intent['id'],
        'created': int(order_date.timestamp()),
        'status': 'delivered' if payment_success else 'failed',
        'amounts': {
            'food_amount': food_amount,
            'delivery_fee': delivery_fee,
            'service_fee': service_fee,
            'tip_amount': tip_amount,
            'total_amount': total_amount
        },
        'restaurant_payout': restaurant_net if payment_success else 0,
        'driver_payout': driver_earnings if payment_success else 0,
        'platform_earnings': platform_earnings if payment_success else 0,
        'delivery_distance': distance,
        'cuisine_type': cuisine,
        'vehicle_type': driver['metadata']['vehicle_type']
    }
    
    return payment_intent, restaurant_transfer, driver_transfer, order

def generate_card_authorization(driver_card: Dict[str, Any], auth_date: datetime) -> Dict[str, Any]:
    """Generate a card authorization for driver expenses."""
    expense_types = {
        'gas_stations': {'min': 2000, 'max': 8000},
        'parking': {'min': 200, 'max': 1500},
        'tolls_bridge_fees': {'min': 150, 'max': 800}
    }
    
    category = random.choice(list(expense_types.keys()))
    amount = random.randint(expense_types[category]['min'], expense_types[category]['max'])
    
    return {
        'id': generate_id('iauth'),
        'object': 'issuing.authorization',
        'amount': amount,
        'currency': 'usd',
        'card': driver_card['id'],
        'created': int(auth_date.timestamp()),
        'approved': True,
        'merchant_data': {'category': category},
        'metadata': {
            'driver_account': driver_card['metadata']['driver_account'],
            'expense_type': category
        }
    }

# =============================================================================
# METRICS CALCULATION
# =============================================================================

def calculate_marketplace_metrics(orders: List[Dict], payments: List[Dict]) -> Dict[str, Any]:
    """Calculate comprehensive marketplace metrics."""
    successful_orders = [o for o in orders if o['status'] == 'delivered']
    
    # Basic counts
    total_orders = len(successful_orders)
    total_restaurants = len(set(o['restaurant_id'] for o in orders))
    total_drivers = len(set(o['driver_id'] for o in orders))
    
    # Financial metrics
    gmv = sum(o['amounts']['total_amount'] for o in successful_orders) / 100
    platform_revenue = sum(o['platform_earnings'] for o in successful_orders) / 100
    take_rate = (platform_revenue / gmv * 100) if gmv > 0 else 0
    
    # Operational metrics
    avg_order_value = gmv / total_orders if total_orders > 0 else 0
    
    # Payment metrics
    payment_failure_rate = len([p for p in payments if p['status'] != 'succeeded']) / len(payments) if payments else 0
    
    return {
        'gmv': gmv,
        'platform_revenue': platform_revenue,
        'take_rate_percentage': take_rate,
        'average_order_value': avg_order_value,
        'total_orders': total_orders,
        'total_restaurants': total_restaurants,
        'total_drivers': total_drivers,
        'orders_per_restaurant': total_orders / total_restaurants if total_restaurants > 0 else 0,
        'orders_per_driver': total_orders / total_drivers if total_drivers > 0 else 0,
        'payment_failure_rate': payment_failure_rate,
        'refund_rate': 0.04,  # 4% estimated refund rate
        'driver_utilization_rate': min(total_orders / (total_drivers * 50), 1.0) if total_drivers > 0 else 0,
    }

# =============================================================================
# MAIN GENERATION LOGIC
# =============================================================================

def generate_marketplace_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete LocalBites marketplace dataset."""
    print("🚀 Starting LocalBites marketplace data generation...")
    
    # Data containers
    connected_accounts = []
    orders = []
    payments = []
    transfers = []
    issuing_cards = []
    issuing_authorizations = []
    
    # Create initial data structures
    restaurants = []
    drivers = []
    customers = []
    
    # Generate customer base
    for i in range(1000):  # 1000 customers
        customers.append(generate_id('cus'))
    
    start_date = datetime.now() - timedelta(days=24*30)
    order_counter = 1
    
    print("📊 Generating marketplace data across 24-month lifecycle...")
    
    # Generate by lifecycle stage
    for stage_name, stage_config in LIFECYCLE_STAGES.items():
        print(f"  Processing {stage_name} stage...")
        
        # Onboard restaurants for this stage
        restaurants_needed = stage_config['total_restaurants'] - len(restaurants)
        for i in range(restaurants_needed):
            restaurant = create_restaurant_account(len(restaurants) + 1, start_date)
            restaurants.append(restaurant)
            connected_accounts.append(restaurant)
        
        # Onboard drivers for this stage
        drivers_needed = stage_config['total_drivers'] - len(drivers)
        for i in range(drivers_needed):
            driver = create_driver_account(len(drivers) + 1, start_date)
            drivers.append(driver)
            connected_accounts.append(driver)
            
            # Create issuing card
            card = create_driver_card(driver)
            issuing_cards.append(card)
        
        # Generate orders for this stage (sample across the stage period)
        stage_months = len(stage_config['months'])
        orders_per_month = stage_config['daily_orders'] * 10  # 10 sample days per month
        
        for month_offset in range(stage_months):
            current_date = start_date + timedelta(days=(stage_config['months'][0] + month_offset) * 30)
            
            for _ in range(orders_per_month):
                if not restaurants or not drivers:
                    continue
                
                # Select random entities
                customer_id = random.choice(customers)
                restaurant = random.choice(restaurants)
                driver = random.choice(drivers)
                
                # Process order
                payment, restaurant_transfer, driver_transfer, order = process_order(
                    order_counter, customer_id, restaurant, driver, current_date
                )
                
                orders.append(order)
                payments.append(payment)
                
                # Add transfers if they exist
                if restaurant_transfer:
                    transfers.append(restaurant_transfer)
                if driver_transfer:
                    transfers.append(driver_transfer)
                
                order_counter += 1
                
                # Progress indicator
                if order_counter % 1000 == 0:
                    print(f"    Generated {order_counter:,} orders...")
    
    # Generate some card authorizations
    for _ in range(min(500, len(issuing_cards))):  # Cap at 500 authorizations
        card = random.choice(issuing_cards)
        auth_date = start_date + timedelta(days=random.randint(30, 720))
        authorization = generate_card_authorization(card, auth_date)
        issuing_authorizations.append(authorization)
    
    print(f"✅ Generated {len(orders):,} orders from {len(restaurants)} restaurants and {len(drivers)} drivers")
    print(f"💳 Generated {len(issuing_cards):,} driver cards with {len(issuing_authorizations):,} authorizations")
    
    return connected_accounts, orders, payments, transfers, issuing_cards, issuing_authorizations

def save_marketplace_files(connected_accounts: List[Dict], orders: List[Dict], 
                          payments: List[Dict], transfers: List[Dict],
                          issuing_cards: List[Dict], issuing_authorizations: List[Dict]) -> Dict:
    """Save all generated marketplace data to JSON files."""
    output_dir = 'marketplace_data'
    os.makedirs(output_dir, exist_ok=True)
    
    print("💾 Saving marketplace files...")
    
    # Save data files
    files_to_save = {
        'connected_accounts.json': connected_accounts,
        'orders.json': orders,
        'payments.json': payments,
        'transfers.json': transfers,
        'issuing_cards.json': issuing_cards,
        'issuing_authorizations.json': issuing_authorizations,
    }
    
    for filename, data in files_to_save.items():
        with open(f'{output_dir}/{filename}', 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # Calculate and save metrics
    metrics = calculate_marketplace_metrics(orders, payments)
    with open(f'{output_dir}/marketplace_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    
    print(f"📁 Files saved to /{output_dir}/ directory")
    return metrics

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    start_time = time.time()
    
    try:
        # Generate marketplace data
        data = generate_marketplace_data()
        connected_accounts, orders, payments, transfers, issuing_cards, issuing_authorizations = data
        
        # Save files and get metrics
        metrics = save_marketplace_files(connected_accounts, orders, payments, transfers, issuing_cards, issuing_authorizations)
        
        # Print validation output
        print("\n" + "="*60)
        print("📊 LOCALBITES MARKETPLACE DATA GENERATION COMPLETE")
        print("="*60)
        
        restaurants = [acc for acc in connected_accounts if acc['metadata']['platform_type'] == 'restaurant']
        drivers = [acc for acc in connected_accounts if acc['metadata']['platform_type'] == 'driver']
        
        print(f"Total restaurants onboarded: {len(restaurants):,}")
        print(f"Total drivers onboarded: {len(drivers):,}")
        print(f"Total orders processed: {metrics['total_orders']:,}")
        print(f"GMV in dollars: ${metrics['gmv']:,.2f}")
        print(f"Platform revenue in dollars: ${metrics['platform_revenue']:,.2f}")
        print(f"Average take rate percentage: {metrics['take_rate_percentage']:.1f}%")
        print(f"Average order value: ${metrics['average_order_value']:.2f}")
        print(f"Orders per restaurant: {metrics['orders_per_restaurant']:.1f}")
        print(f"Orders per driver: {metrics['orders_per_driver']:.1f}")
        print(f"Payment failure rate: {metrics['payment_failure_rate']:.1%}")
        print(f"Driver utilization rate: {metrics['driver_utilization_rate']:.1%}")
        
        # Cuisine and vehicle distribution
        cuisine_counts = defaultdict(int)
        vehicle_counts = defaultdict(int)
        
        for restaurant in restaurants:
            cuisine_counts[restaurant['metadata']['cuisine_type']] += 1
        for driver in drivers:
            vehicle_counts[driver['metadata']['vehicle_type']] += 1
        
        print(f"\nTop cuisines: {dict(sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)[:3])}")
        print(f"Vehicle types: {dict(vehicle_counts)}")
        
        execution_time = time.time() - start_time
        print(f"\n⏱️  Execution time: {execution_time:.1f} seconds")
        print("✅ LocalBites marketplace data generation complete!")
        
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()