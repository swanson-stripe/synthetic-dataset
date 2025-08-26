#!/usr/bin/env python3
"""
CloudFlow Synthetic Stripe Subscription Data Generator

Generates realistic B2B SaaS subscription data including subscriptions, invoices,
usage events, and comprehensive SaaS metrics over a 24-month business lifecycle.

Usage:
    python generate_cloudflow.py
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
# CONFIGURATION & CONSTANTS
# =============================================================================

# SaaS Plans Configuration
PLANS = {
    'starter': {'price': 4900, 'name': 'Starter', 'interval': 'month', 'interval_count': 1},
    'professional': {'price': 19900, 'name': 'Professional', 'interval': 'month', 'interval_count': 1},
    'enterprise': {'price': 99900, 'name': 'Enterprise', 'interval': 'month', 'interval_count': 1},
    'starter_annual': {'price': 49000, 'name': 'Starter Annual', 'interval': 'year', 'interval_count': 1},
    'professional_annual': {'price': 199000, 'name': 'Professional Annual', 'interval': 'year', 'interval_count': 1},
    'enterprise_annual': {'price': 999000, 'name': 'Enterprise Annual', 'interval': 'year', 'interval_count': 1},
}

# Usage-based pricing
USAGE_BASED_PRICING = {
    'api_calls': 0.001,    # $0.001 per call
    'storage_gb': 0.10,    # $0.10 per GB
    'seats': 1500          # $15.00 per additional seat (cents)
}

# Business lifecycle stages
LIFECYCLE_STAGES = {
    'early': {
        'months': range(0, 8),
        'new_customers_per_month': (10, 30),
        'churn_rate': 0.10,
        'trial_conversion_rate': 0.15,
        'upgrade_rate': 0.05,
        'annual_percentage': 0.10
    },
    'growth': {
        'months': range(8, 16),
        'new_customers_per_month': (50, 100),
        'churn_rate': 0.05,
        'trial_conversion_rate': 0.25,
        'upgrade_rate': 0.08,
        'annual_percentage': 0.25
    },
    'mature': {
        'months': range(16, 24),
        'new_customers_per_month': (80, 150),
        'churn_rate': 0.02,
        'trial_conversion_rate': 0.35,
        'upgrade_rate': 0.12,
        'annual_percentage': 0.40
    }
}

# Trial periods in days
TRIAL_PERIODS = [14, 21, 30]

# Company size distribution for plan selection
COMPANY_SIZES = {
    'startup': {'weight': 40, 'plans': ['starter', 'starter_annual']},
    'smb': {'weight': 35, 'plans': ['starter', 'professional', 'starter_annual', 'professional_annual']},
    'mid_market': {'weight': 20, 'plans': ['professional', 'enterprise', 'professional_annual', 'enterprise_annual']},
    'enterprise': {'weight': 5, 'plans': ['enterprise', 'enterprise_annual']}
}

# Sales channels
SALES_CHANNELS = {
    'self_serve': 0.60,
    'inside_sales': 0.25,
    'field_sales': 0.10,
    'partner': 0.05
}

# Initialize Faker
fake = Faker()
fake.seed_instance(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_stripe_ids() -> Dict[str, str]:
    """Generate properly formatted Stripe IDs."""
    return {
        'subscription': f"sub_{uuid.uuid4().hex[:24]}",
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'invoice': f"in_{uuid.uuid4().hex[:24]}",
        'price': f"price_{uuid.uuid4().hex[:24]}",
        'subscription_item': f"si_{uuid.uuid4().hex[:24]}",
        'usage_record': f"mbur_{uuid.uuid4().hex[:24]}",
    }

def get_lifecycle_stage(month: int) -> str:
    """Determine lifecycle stage based on month."""
    for stage, config in LIFECYCLE_STAGES.items():
        if month in config['months']:
            return stage
    return 'mature'

def select_company_size() -> str:
    """Select company size based on distribution."""
    weights = [size['weight'] for size in COMPANY_SIZES.values()]
    return random.choices(list(COMPANY_SIZES.keys()), weights=weights)[0]

def select_plan_for_company(company_size: str, is_annual: bool = False) -> str:
    """Select appropriate plan based on company size."""
    available_plans = COMPANY_SIZES[company_size]['plans']
    if is_annual:
        annual_plans = [p for p in available_plans if 'annual' in p]
        if annual_plans:
            return random.choice(annual_plans)
    
    monthly_plans = [p for p in available_plans if 'annual' not in p]
    return random.choice(monthly_plans) if monthly_plans else random.choice(available_plans)

def select_sales_channel() -> str:
    """Select sales channel based on distribution."""
    channels = list(SALES_CHANNELS.keys())
    weights = list(SALES_CHANNELS.values())
    return random.choices(channels, weights=weights)[0]

def calculate_days_between(start_date: datetime, end_date: datetime) -> int:
    """Calculate days between two dates."""
    return (end_date - start_date).days

# =============================================================================
# CORE GENERATION FUNCTIONS
# =============================================================================

def generate_customer(customer_number: int, signup_date: datetime, company_size: str) -> Dict[str, Any]:
    """Generate a B2B customer object."""
    ids = generate_stripe_ids()
    
    # Generate company data
    company_name = fake.company()
    domain = company_name.lower().replace(' ', '').replace(',', '').replace('.', '') + '.com'
    
    # Generate contact person
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
    
    return {
        'id': ids['customer'],
        'object': 'customer',
        'created': int(signup_date.timestamp()),
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
            'company_name': company_name,
            'company_size': company_size,
            'domain': domain,
            'signup_date': signup_date.isoformat(),
            'sales_channel': select_sales_channel(),
            'initial_trial_days': random.choice(TRIAL_PERIODS)
        }
    }

def generate_subscription(customer: Dict[str, Any], start_date: datetime, plan_key: str, 
                         trial_end: datetime = None) -> Dict[str, Any]:
    """Generate a complete Stripe subscription object."""
    ids = generate_stripe_ids()
    plan = PLANS[plan_key]
    
    # Determine subscription status
    if trial_end and trial_end > start_date:
        status = 'trialing'
        current_period_start = int(trial_end.timestamp())
    else:
        status = 'active'
        current_period_start = int(start_date.timestamp())
    
    # Calculate current period end
    if plan['interval'] == 'month':
        # Handle month rollover correctly
        month = start_date.month + plan['interval_count']
        year = start_date.year
        while month > 12:
            month -= 12
            year += 1
        period_end = start_date.replace(year=year, month=month)
    else:  # year
        period_end = start_date.replace(year=start_date.year + plan['interval_count'])
    
    # Calculate quantity (number of seats)
    company_size = customer['metadata']['company_size']
    if company_size == 'startup':
        quantity = random.randint(1, 5)
    elif company_size == 'smb':
        quantity = random.randint(3, 20)
    elif company_size == 'mid_market':
        quantity = random.randint(15, 100)
    else:  # enterprise
        quantity = random.randint(50, 500)
    
    return {
        'id': ids['subscription'],
        'object': 'subscription',
        'customer': customer['id'],
        'status': status,
        'created': int(start_date.timestamp()),
        'current_period_start': current_period_start,
        'current_period_end': int(period_end.timestamp()),
        'trial_start': int(start_date.timestamp()) if trial_end else None,
        'trial_end': int(trial_end.timestamp()) if trial_end else None,
        'cancel_at_period_end': False,
        'canceled_at': None,
        'ended_at': None,
        'items': {
            'object': 'list',
            'data': [{
                'id': ids['subscription_item'],
                'object': 'subscription_item',
                'created': int(start_date.timestamp()),
                'price': {
                    'id': ids['price'],
                    'object': 'price',
                    'active': True,
                    'currency': 'usd',
                    'product': f"prod_{plan_key}",
                    'recurring': {
                        'interval': plan['interval'],
                        'interval_count': plan['interval_count']
                    },
                    'unit_amount': plan['price'],
                    'nickname': plan['name']
                },
                'quantity': quantity,
                'subscription': ids['subscription']
            }]
        },
        'metadata': {
            'initial_plan': plan_key,
            'company_name': customer['metadata']['company_name'],
            'company_size': customer['metadata']['company_size'],
            'sales_channel': customer['metadata']['sales_channel'],
            'seats': str(quantity)
        },
        'default_payment_method': f"pm_{uuid.uuid4().hex[:24]}",
        'collection_method': 'charge_automatically',
        'billing_cycle_anchor': current_period_start
    }

def generate_invoice(subscription: Dict[str, Any], billing_period_start: datetime, 
                    billing_period_end: datetime, usage_events: List[Dict] = None) -> Dict[str, Any]:
    """Generate invoice with line items including usage charges."""
    ids = generate_stripe_ids()
    
    # Base subscription line item
    sub_item = subscription['items']['data'][0]
    base_amount = sub_item['price']['unit_amount'] * sub_item['quantity']
    
    lines = [{
        'id': f"il_{uuid.uuid4().hex[:24]}",
        'object': 'line_item',
        'amount': base_amount,
        'currency': 'usd',
        'description': f"{sub_item['price']['nickname']} - {sub_item['quantity']} seats",
        'period': {
            'start': int(billing_period_start.timestamp()),
            'end': int(billing_period_end.timestamp())
        },
        'price': sub_item['price'],
        'quantity': sub_item['quantity'],
        'subscription': subscription['id'],
        'subscription_item': sub_item['id']
    }]
    
    # Add usage-based line items
    usage_total = 0
    if usage_events:
        usage_summary = defaultdict(int)
        for event in usage_events:
            usage_summary[event['dimension']] += event['quantity']
        
        for dimension, quantity in usage_summary.items():
            if dimension in USAGE_BASED_PRICING and quantity > 0:
                unit_price = int(USAGE_BASED_PRICING[dimension] * 100)  # Convert to cents
                line_amount = unit_price * quantity
                usage_total += line_amount
                
                lines.append({
                    'id': f"il_{uuid.uuid4().hex[:24]}",
                    'object': 'line_item',
                    'amount': line_amount,
                    'currency': 'usd',
                    'description': f"Usage: {dimension.replace('_', ' ').title()} ({quantity:,} units)",
                    'period': {
                        'start': int(billing_period_start.timestamp()),
                        'end': int(billing_period_end.timestamp())
                    },
                    'quantity': quantity,
                    'unit_amount': unit_price,
                    'metadata': {
                        'usage_dimension': dimension
                    }
                })
    
    total_amount = base_amount + usage_total
    
    # Determine invoice status
    if subscription['status'] == 'trialing':
        status = 'draft'
        paid = False
    else:
        # 95% success rate for payments
        payment_success = random.random() > 0.05
        status = 'paid' if payment_success else 'open'
        paid = payment_success
    
    return {
        'id': ids['invoice'],
        'object': 'invoice',
        'customer': subscription['customer'],
        'subscription': subscription['id'],
        'status': status,
        'paid': paid,
        'created': int(billing_period_start.timestamp()),
        'due_date': int((billing_period_start + timedelta(days=30)).timestamp()),
        'period_start': int(billing_period_start.timestamp()),
        'period_end': int(billing_period_end.timestamp()),
        'amount_due': total_amount if not paid else 0,
        'amount_paid': total_amount if paid else 0,
        'amount_remaining': 0 if paid else total_amount,
        'subtotal': total_amount,
        'total': total_amount,
        'currency': 'usd',
        'lines': {
            'object': 'list',
            'data': lines,
            'has_more': False,
            'total_count': len(lines)
        },
        'metadata': {
            'billing_reason': 'subscription_cycle',
            'usage_charges': str(usage_total)
        }
    }

def generate_usage_events(subscription_id: str, period_start: datetime, 
                         period_end: datetime, company_size: str) -> List[Dict[str, Any]]:
    """Generate metered usage events for the billing period."""
    events = []
    days_in_period = (period_end - period_start).days
    
    # Generate usage based on company size
    if company_size == 'startup':
        daily_api_calls = random.randint(100, 1000)
        daily_storage_gb = random.randint(1, 10)
        additional_seats = random.randint(0, 2)
    elif company_size == 'smb':
        daily_api_calls = random.randint(1000, 10000)
        daily_storage_gb = random.randint(10, 100)
        additional_seats = random.randint(1, 10)
    elif company_size == 'mid_market':
        daily_api_calls = random.randint(10000, 100000)
        daily_storage_gb = random.randint(100, 1000)
        additional_seats = random.randint(5, 50)
    else:  # enterprise
        daily_api_calls = random.randint(100000, 1000000)
        daily_storage_gb = random.randint(1000, 10000)
        additional_seats = random.randint(20, 200)
    
    # Generate daily usage events
    for day in range(days_in_period):
        event_date = period_start + timedelta(days=day)
        
        # API calls (varies by day of week)
        weekday_multiplier = 0.7 if event_date.weekday() >= 5 else 1.0  # Weekend reduction
        api_calls = int(daily_api_calls * weekday_multiplier * random.uniform(0.8, 1.2))
        
        if api_calls > 0:
            events.append({
                'id': f"mbur_{uuid.uuid4().hex[:24]}",
                'object': 'usage_record',
                'subscription_item': subscription_id,
                'quantity': api_calls,
                'timestamp': int(event_date.timestamp()),
                'dimension': 'api_calls',
                'metadata': {
                    'date': event_date.strftime('%Y-%m-%d'),
                    'day_of_week': event_date.strftime('%A')
                }
            })
    
    # Storage (monthly aggregate)
    storage_variation = random.uniform(0.9, 1.1)
    total_storage = int(daily_storage_gb * days_in_period * storage_variation)
    
    if total_storage > 0:
        events.append({
            'id': f"mbur_{uuid.uuid4().hex[:24]}",
            'object': 'usage_record',
            'subscription_item': subscription_id,
            'quantity': total_storage,
            'timestamp': int(period_end.timestamp()),
            'dimension': 'storage_gb',
            'metadata': {
                'billing_period': f"{period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}"
            }
        })
    
    # Additional seats (if any)
    if additional_seats > 0 and random.random() < 0.3:  # 30% chance of additional seats
        events.append({
            'id': f"mbur_{uuid.uuid4().hex[:24]}",
            'object': 'usage_record',
            'subscription_item': subscription_id,
            'quantity': additional_seats,
            'timestamp': int(period_end.timestamp()),
            'dimension': 'seats',
            'metadata': {
                'billing_period': f"{period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}"
            }
        })
    
    return events

def simulate_subscription_changes(subscription: Dict[str, Any], month: int, 
                                lifecycle_stage: str) -> Tuple[Dict[str, Any], str]:
    """Simulate subscription changes (upgrades, downgrades, cancellations)."""
    stage_config = LIFECYCLE_STAGES[lifecycle_stage]
    
    # Check for cancellation
    if random.random() < stage_config['churn_rate'] / 12:  # Monthly churn probability
        subscription['status'] = 'canceled'
        subscription['canceled_at'] = int(datetime.now().timestamp())
        subscription['cancel_at_period_end'] = True
        return subscription, 'canceled'
    
    # Check for plan upgrades/downgrades
    if random.random() < stage_config['upgrade_rate'] / 12:  # Monthly upgrade probability
        current_plan = subscription['metadata']['initial_plan']
        company_size = subscription['metadata']['company_size']
        
        # Determine upgrade/downgrade direction
        if 'starter' in current_plan:
            new_plan = select_plan_for_company(company_size)
            if new_plan != current_plan:
                # Update subscription
                new_plan_config = PLANS[new_plan]
                subscription['items']['data'][0]['price'].update({
                    'unit_amount': new_plan_config['price'],
                    'nickname': new_plan_config['name'],
                    'recurring': {
                        'interval': new_plan_config['interval'],
                        'interval_count': new_plan_config['interval_count']
                    }
                })
                subscription['metadata']['current_plan'] = new_plan
                return subscription, 'upgraded' if new_plan_config['price'] > PLANS[current_plan]['price'] else 'downgraded'
    
    return subscription, 'active'

# =============================================================================
# METRICS CALCULATION FUNCTIONS
# =============================================================================

def calculate_mrr(subscriptions: List[Dict], target_date: datetime) -> float:
    """Calculate Monthly Recurring Revenue for a specific date."""
    mrr = 0
    target_timestamp = target_date.timestamp()
    
    for sub in subscriptions:
        # Check if subscription was active on target date
        if (sub['created'] <= target_timestamp and 
            (sub['canceled_at'] is None or sub['canceled_at'] > target_timestamp)):
            
            # Get plan details
            price_info = sub['items']['data'][0]['price']
            unit_amount = price_info['unit_amount']
            quantity = sub['items']['data'][0]['quantity']
            interval = price_info['recurring']['interval']
            
            # Convert to monthly
            if interval == 'month':
                monthly_amount = unit_amount * quantity
            elif interval == 'year':
                monthly_amount = (unit_amount * quantity) / 12
            else:
                monthly_amount = 0
            
            mrr += monthly_amount / 100  # Convert cents to dollars
    
    return mrr

def calculate_churn_rate(subscriptions: List[Dict], period_start: datetime, period_end: datetime) -> float:
    """Calculate churn rate for a specific period."""
    active_at_start = 0
    churned_in_period = 0
    
    start_ts = period_start.timestamp()
    end_ts = period_end.timestamp()
    
    for sub in subscriptions:
        # Was active at start of period
        if (sub['created'] <= start_ts and 
            (sub['canceled_at'] is None or sub['canceled_at'] > start_ts)):
            active_at_start += 1
            
            # Churned during period
            if (sub['canceled_at'] is not None and 
                start_ts < sub['canceled_at'] <= end_ts):
                churned_in_period += 1
    
    return churned_in_period / active_at_start if active_at_start > 0 else 0

def calculate_ltv_by_cohort(subscriptions: List[Dict], invoices: List[Dict]) -> Dict[str, float]:
    """Calculate Lifetime Value by customer cohort."""
    cohorts = defaultdict(list)
    customer_revenue = defaultdict(float)
    
    # Group customers by signup month
    for sub in subscriptions:
        signup_date = datetime.fromtimestamp(sub['created'])
        cohort_month = signup_date.strftime('%Y-%m')
        cohorts[cohort_month].append(sub['customer'])
    
    # Calculate total revenue per customer
    for invoice in invoices:
        if invoice['paid']:
            customer_revenue[invoice['customer']] += invoice['amount_paid'] / 100
    
    # Calculate average LTV per cohort
    cohort_ltv = {}
    for cohort_month, customers in cohorts.items():
        total_revenue = sum(customer_revenue[customer] for customer in customers)
        avg_ltv = total_revenue / len(customers) if customers else 0
        cohort_ltv[cohort_month] = avg_ltv
    
    return cohort_ltv

def calculate_saas_metrics(subscriptions: List[Dict], invoices: List[Dict]) -> Dict[str, Any]:
    """Calculate comprehensive SaaS metrics."""
    current_date = datetime.now()
    current_mrr = calculate_mrr(subscriptions, current_date)
    
    # Calculate churn rate (last 30 days)
    period_start = current_date - timedelta(days=30)
    churn_rate = calculate_churn_rate(subscriptions, period_start, current_date)
    
    # Calculate ARPU (Average Revenue Per User)
    active_subs = [s for s in subscriptions if s['status'] in ['active', 'trialing']]
    arpu = current_mrr / len(active_subs) if active_subs else 0
    
    # Calculate LTV
    cohort_ltv = calculate_ltv_by_cohort(subscriptions, invoices)
    avg_ltv = np.mean(list(cohort_ltv.values())) if cohort_ltv else 0
    
    # Revenue calculations
    total_revenue = sum(inv['amount_paid'] / 100 for inv in invoices if inv['paid'])
    
    return {
        'mrr': current_mrr,
        'arr': current_mrr * 12,
        'churn_rate': churn_rate,
        'arpu': arpu,
        'ltv': avg_ltv,
        'total_revenue': total_revenue,
        'active_subscriptions': len(active_subs),
        'total_customers': len(set(sub['customer'] for sub in subscriptions)),
        'cohort_ltv': cohort_ltv
    }

# =============================================================================
# MAIN GENERATION LOGIC
# =============================================================================

def generate_cloudflow_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete CloudFlow SaaS subscription dataset."""
    print("🚀 Starting CloudFlow SaaS data generation...")
    
    customers = []
    subscriptions = []
    invoices = []
    usage_events = []
    
    start_date = datetime.now() - timedelta(days=24*30)  # 24 months ago
    customer_counter = 1
    
    print("📊 Generating subscription data across 24-month lifecycle...")
    
    # Generate data month by month
    for month in range(24):
        current_date = start_date + timedelta(days=month*30)
        lifecycle_stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE_STAGES[lifecycle_stage]
        
        # Determine number of new customers for this month
        new_customers = random.randint(*stage_config['new_customers_per_month'])
        
        print(f"  Month {month+1:2d} ({lifecycle_stage:>6}): {new_customers:3d} new customers")
        
        # Generate new customers and subscriptions
        for _ in range(new_customers):
            company_size = select_company_size()
            customer = generate_customer(customer_counter, current_date, company_size)
            customers.append(customer)
            
            # Determine if customer gets annual plan
            is_annual = random.random() < stage_config['annual_percentage']
            plan_key = select_plan_for_company(company_size, is_annual)
            
            # Determine trial period and conversion
            trial_days = int(customer['metadata']['initial_trial_days'])
            trial_end = current_date + timedelta(days=trial_days)
            
            # Check if trial converts (simulate trial conversion)
            converts_trial = random.random() < stage_config['trial_conversion_rate']
            trial_end_date = trial_end if converts_trial else None
            
            # Create subscription
            subscription = generate_subscription(customer, current_date, plan_key, trial_end_date)
            subscriptions.append(subscription)
            
            customer_counter += 1
        
        # Process existing subscriptions (check for changes, generate invoices)
        for subscription in subscriptions:
            if subscription['status'] in ['active', 'trialing']:
                # Check for subscription changes
                subscription, change_type = simulate_subscription_changes(
                    subscription, month, lifecycle_stage
                )
                
                # Generate invoice for billing cycle (every month for monthly, every 12 months for annual)
                sub_start = datetime.fromtimestamp(subscription['created'])
                plan_interval = subscription['items']['data'][0]['price']['recurring']['interval']
                
                # Check if it's time to bill
                should_bill = False
                trial_completed = (subscription['trial_end'] is None or 
                                 datetime.fromtimestamp(subscription['trial_end']) <= current_date)
                
                # Convert from trial to active if trial period ended
                if subscription['status'] == 'trialing' and trial_completed:
                    subscription['status'] = 'active'
                
                if subscription['status'] == 'active' and trial_completed:
                    months_since_sub = (current_date.year - sub_start.year) * 12 + (current_date.month - sub_start.month)
                    
                    if plan_interval == 'month':
                        # Bill monthly subscriptions every month
                        should_bill = months_since_sub >= 0
                    elif plan_interval == 'year':
                        # Bill annual subscriptions every 12 months
                        should_bill = months_since_sub > 0 and months_since_sub % 12 == 0
                
                if should_bill and subscription['status'] == 'active':
                    billing_start = current_date.replace(day=1)
                    if plan_interval == 'month':
                        billing_end = billing_start + timedelta(days=30)
                    else:  # annual
                        billing_end = billing_start.replace(year=billing_start.year + 1)
                    
                    # Generate usage events
                    company_size = subscription['metadata']['company_size']
                    usage = generate_usage_events(
                        subscription['id'], billing_start, billing_end, company_size
                    )
                    usage_events.extend(usage)
                    
                    # Generate invoice
                    invoice = generate_invoice(subscription, billing_start, billing_end, usage)
                    invoices.append(invoice)
    
    print(f"✅ Generated {len(subscriptions):,} subscriptions from {len(customers):,} customers")
    print(f"📄 Generated {len(invoices):,} invoices")
    print(f"📊 Generated {len(usage_events):,} usage events")
    
    return customers, subscriptions, invoices, usage_events

def save_output_files(customers: List[Dict], subscriptions: List[Dict], 
                     invoices: List[Dict], usage_events: List[Dict]) -> None:
    """Save all generated data to JSON files."""
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    print("💾 Saving output files...")
    
    # Save raw data
    with open(f'{output_dir}/subscriptions.json', 'w') as f:
        json.dump(subscriptions, f, indent=2, default=str)
    
    with open(f'{output_dir}/customers.json', 'w') as f:
        json.dump(customers, f, indent=2, default=str)
    
    with open(f'{output_dir}/invoices.json', 'w') as f:
        json.dump(invoices, f, indent=2, default=str)
    
    with open(f'{output_dir}/usage_events.json', 'w') as f:
        json.dump(usage_events, f, indent=2, default=str)
    
    # Calculate and save metrics
    print("📈 Calculating SaaS metrics...")
    metrics = calculate_saas_metrics(subscriptions, invoices)
    
    with open(f'{output_dir}/saas_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    
    # Generate MRR timeline
    mrr_timeline = {}
    start_date = datetime.now() - timedelta(days=24*30)
    for month in range(24):
        month_date = start_date + timedelta(days=month*30)
        mrr = calculate_mrr(subscriptions, month_date)
        mrr_timeline[month_date.strftime('%Y-%m')] = mrr
    
    with open(f'{output_dir}/mrr_timeline.json', 'w') as f:
        json.dump(mrr_timeline, f, indent=2, default=str)
    
    # Generate cohort analysis
    cohort_analysis = {
        'ltv_by_cohort': metrics['cohort_ltv'],
        'retention_analysis': 'Generated with subscription data'
    }
    
    with open(f'{output_dir}/cohort_analysis.json', 'w') as f:
        json.dump(cohort_analysis, f, indent=2, default=str)
    
    print(f"📁 Files saved to /{output_dir}/ directory")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    start_time = time.time()
    
    try:
        # Generate data
        customers, subscriptions, invoices, usage_events = generate_cloudflow_data()
        
        # Save output files
        save_output_files(customers, subscriptions, invoices, usage_events)
        
        # Calculate final metrics
        metrics = calculate_saas_metrics(subscriptions, invoices)
        
        # Print validation output
        print("\n" + "="*60)
        print("📊 CLOUDFLOW SAAS DATA GENERATION COMPLETE")
        print("="*60)
        
        active_subs = [s for s in subscriptions if s['status'] in ['active', 'trialing']]
        
        print(f"Total customers: {metrics['total_customers']:,}")
        print(f"Active subscriptions: {len(active_subs):,}")
        print(f"Current MRR: ${metrics['mrr']:,.2f}")
        print(f"Current ARR: ${metrics['arr']:,.2f}")
        print(f"Churn rate: {metrics['churn_rate']:.1%}")
        print(f"ARPU: ${metrics['arpu']:,.2f}")
        print(f"Average LTV: ${metrics['ltv']:,.2f}")
        print(f"Total revenue: ${metrics['total_revenue']:,.2f}")
        
        print("\nPlan distribution:")
        plan_counts = defaultdict(int)
        for sub in active_subs:
            plan_name = sub['items']['data'][0]['price']['nickname']
            plan_counts[plan_name] += 1
        
        for plan, count in sorted(plan_counts.items()):
            print(f"  {plan}: {count:,} subscriptions")
        
        print(f"\nFiles saved to /data/ directory")
        
        execution_time = time.time() - start_time
        print(f"\n⏱️  Execution time: {execution_time:.1f} seconds")
        print("✅ CloudFlow SaaS data generation complete!")
        
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()
